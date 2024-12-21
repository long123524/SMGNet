import os
import numpy as np
import torch
from skimage import io
from torch.utils import data
import utils.transform as transform
import matplotlib.pyplot as plt
from skimage.transform import rescale
from torchvision.transforms import functional as F
import cv2

###HRSCD数据集
num_classes = 6
ST_COLORMAP = [[128,128,128], [255,0,0], [250,250,150], [150,250,150], [0,255,0], [0,0,255]]
ST_CLASSES = ['unchanged', 'ground', 'agricutural areas', 'tree', 'wetlands','water']

MEAN_A = np.array([113.40, 114.08, 116.45])
STD_A  = np.array([48.30,  46.27,  48.14])
MEAN_B = np.array([111.07, 114.04, 118.18])
STD_B  = np.array([49.41,  47.01,  47.94])

root = '/HOME/scw6865/run/hr/code/data_HRSCD'

colormap2label = np.zeros(256 ** 3)
for i, cm in enumerate(ST_COLORMAP):
    colormap2label[(cm[0] * 256 + cm[1]) * 256 + cm[2]] = i

def Colorls2Index(ColorLabels):
    IndexLabels = []
    for i, data in enumerate(ColorLabels):
        IndexMap = Color2Index(data)
        IndexLabels.append(IndexMap)
    return IndexLabels

def Color2Index(ColorLabel):
    data = ColorLabel.astype(np.int32)
    idx = (data[:, :, 0] * 256 + data[:, :, 1]) * 256 + data[:, :, 2]
    IndexMap = colormap2label[idx]
    #IndexMap = 2*(IndexMap > 1) + 1 * (IndexMap <= 1)
    IndexMap = IndexMap * (IndexMap < num_classes)
    return IndexMap

def Index2Color(pred):
    colormap = np.asarray(ST_COLORMAP, dtype='uint8')
    x = np.asarray(pred, dtype='int32')
    return colormap[x, :]

def showIMG(img):
    plt.imshow(img)
    plt.show()
    return 0

def normalize_image(im, time='A'):
    assert time in ['A', 'B']
    if time=='A':
        im = (im - MEAN_A) / STD_A
    else:
        im = (im - MEAN_B) / STD_B
    return im

def normalize_images(imgs, time='A'):
    for i, im in enumerate(imgs):
        imgs[i] = normalize_image(im, time)
    return imgs

def read_RSimages(mode, rescale=False):
    #assert mode in ['train', 'val', 'test']
    img_A_dir = os.path.join(root, mode, 'im1')
    img_B_dir = os.path.join(root, mode, 'im2')
    label_A_dir = os.path.join(root, mode, 'label1')
    label_B_dir = os.path.join(root, mode, 'label2')
    semantic_label = os.path.join(root, mode, 'prior_t1')

    data_list = os.listdir(img_A_dir)
    imgs_list_A, imgs_list_B, labels_A, labels_B, semnatics_cla = [], [], [], [], []
    count = 0
    for it in data_list:
        # print(it)
        if (it[-4:]=='.png') or (it[-4:]=='.tif'):
            img_A_path = os.path.join(img_A_dir, it)
            img_B_path = os.path.join(img_B_dir, it)
            label_A_path = os.path.join(label_A_dir, it)
            label_B_path = os.path.join(label_B_dir, it)
            semantic_path = os.path.join(semantic_label, it)

            imgs_list_A.append(img_A_path)
            imgs_list_B.append(img_B_path)

            label_A = io.imread(label_A_path)
            label_B = io.imread(label_B_path)
            semantic_class = io.imread(semantic_path)
            label_A = np.uint8(label_A)
            label_B = np.uint8(label_B)
            semantic_class = np.uint8(semantic_class)
            labels_A.append(label_A)
            labels_B.append(label_B)
            semnatics_cla.append(semantic_class)

        count+=1
        if not count%500: print('%d/%d images loaded.'%(count, len(data_list)))

    print(labels_A[0].shape)
    print(str(len(imgs_list_A)) + ' ' + mode + ' images' + ' loaded.')

    return imgs_list_A, imgs_list_B, labels_A, labels_B, semnatics_cla

class Data(data.Dataset):
    def __init__(self, mode, random_flip = False):
        self.random_flip = random_flip
        self.imgs_list_A, self.imgs_list_B, self.labels_A, self.labels_B, self.semnatics_cla = read_RSimages(mode)

    def get_mask_name(self, idx):
        mask_name = os.path.split(self.imgs_list_A[idx])[-1]
        return mask_name

    def __getitem__(self, idx):
        img_A = io.imread(self.imgs_list_A[idx])
        img_A = normalize_image(img_A, 'A')
        img_B = io.imread(self.imgs_list_B[idx])
        img_B = normalize_image(img_B, 'B')
        label_A = self.labels_A[idx]

        label_B = self.labels_B[idx]
        class_label = self.semnatics_cla[idx]

        if self.random_flip:
            img_A, img_B, label_A, label_B, class_label = transform.rand_rot90_flip_MCD(img_A, img_B, label_A, label_B, class_label)
            s = 12
        return F.to_tensor(img_A), F.to_tensor(img_B), torch.from_numpy(label_A), torch.from_numpy(label_B), torch.from_numpy(class_label)

    def __len__(self):
        return len(self.imgs_list_A)

class Data_test(data.Dataset):
    def __init__(self, test_dir):
        self.imgs_A = []
        self.imgs_B = []
        self.class_prior = []
        self.mask_name_list = []
        imgA_dir = os.path.join(test_dir, 'im1')
        imgB_dir = os.path.join(test_dir, 'im2')
        class_label = os.path.join(test_dir, 'prior_t1')
        data_list = os.listdir(imgA_dir)
        for it in data_list:
            if (it[-4:]=='.tif') or (it[-4:]=='.png'):
                img_A_path = os.path.join(imgA_dir, it)
                img_B_path = os.path.join(imgB_dir, it)
                class_label_path = os.path.join(class_label, it)
                self.imgs_A.append(io.imread(img_A_path))
                self.imgs_B.append(io.imread(img_B_path))
                self.class_prior.append(np.uint8(io.imread(class_label_path)))
                self.mask_name_list.append(it)
        self.len = len(self.imgs_A)

    def get_mask_name(self, idx):
        return self.mask_name_list[idx]

    def __getitem__(self, idx):
        img_A = self.imgs_A[idx]
        img_B = self.imgs_B[idx]
        class_priors = self.class_prior[idx]
        img_A = normalize_image(img_A, 'A')
        img_B = normalize_image(img_B, 'B')
        return F.to_tensor(img_A), F.to_tensor(img_B), torch.from_numpy(class_priors)

    def __len__(self):
        return self.len

