# SMGNet

Official Pytorch Code base for "Integrating historical map information for remote sensing image semantic change detection"

[Project](https://github.com/long123524/SMGNet)

## Introduction

We propose a novel multitask network (i.e., SMGNet) that fully integrates available semantic information derived from historical maps, with the aim of improving the under-detection of changed areas and misclassiffcation of
changed classes derived from high-resolution satellite images. 

<p align="center">
  <img src="imgs/SMGNet.png" width="800"/>
</p>

<p align="center">
  <img src="imgs/results.png" width="800"/>
</p>


## Using the code:

The code is stable while using Python 3.9.0, CUDA >=11.0

- Clone this repository:
```bash
git clone https://github.com/long123524/SMGNet
cd SMGNet
```

To install all the dependencies using conda or pip:

```
PyTorch
TensorboardX
OpenCV
numpy
tqdm
```

## Data Format

Make sure to put the files as the following structure:

```
inputs
└── <train>
    ├── image1
    |   ├── 001.tif
    │   ├── 002.tif
    │   ├── 003.tif
    │   ├── ...
    |
    └── image2
    |   ├── 001.tif
    |   ├── 002.tif
    |   ├── 003.tif
    |   ├── ...
    └── label1
    |   ├── 001.tif
    |   ├── 002.tif
    |   ├── 003.tif
    |   ├── ...
    └── label2
    |   ├── 001.tif
    |   ├── 002.tif
    |   ├── 003.tif
    |   ├── ...
    └── prior_t1
    |   ├── 001.tif
    |   ├── 002.tif
    |   ├── 003.tif
    |   ├── ...
    └── ...
    
```

For testing and validation datasets, the same structure as the above.

## Datasets

A preprocessed dataset is available at https://drive.google.com/file/d/1nvtgmqFSm99CWDvmyOnS-IRqpstBGTXc/view?usp=sharing.

## Training and testing

1. Train the model.
```
The code and data will be available.
```
2. Test the model.
```
The code and data will be available.
```
3. Accuracy evaluation.

```
The code and data will be available.
```

## A pretrained weight
A pretrained weight of PVT-V2 on the ImageNet dataset is provided: https://drive.google.com/file/d/1uzeVfA4gEQ772vzLntnkqvWePSw84F6y/view?usp=sharing

### Acknowledgements:

This code-base uses certain code-blocks and helper functions from [HGINet](https://github.com/long123524/HGINet-torch) and [BiSRNet](https://github.com/DingLei14/Bi-SRNet).

### Citation:
