# 🎨 Image Inpainting

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yashk2000/SneakySketchers/blob/main/InPainting%20Notebook/Inpainting.ipynb)

We have used the technique for **partial convolutions** for performing image inpainting. 

## Partial Convolutions for Image Inpainting using PyTorch 🔦

This is a PyTorch implementation of "Image Inpainting for Irregular Holes Using Partial Convolutions", [https://arxiv.org/abs/1804.07723](https://arxiv.org/abs/1804.07723)
by Guilin Liu, Fitsum A. Reda, Kevin J. Shih, Ting-Chun Wang, Andrew Tao and Bryan Catanzaro from NVIDIA.

## What makes this technique work 🛠️

### Partial Convolution Layer
The key element here is ofcourse the partial convolutional layer. Basically, given the convolutional filter **W** and the corresponding bias *b*, the following partial convolution is applied instead of a normal convolution:

<img src='https://raw.githubusercontent.com/MathiasGruber/PConv-Keras/master/data/images/eq1.PNG' />

where ⊙ is element-wise multiplication and **M** is a binary mask of 0s and 1s. Importantly, after each partial convolution, the mask is also updated, so that if the convolution was able to condition its output on at least one valid input, then the mask is removed at that location, i.e.

<img src='https://raw.githubusercontent.com/MathiasGruber/PConv-Keras/master/data/images/eq2.PNG' />

The result of this is that with a sufficiently deep network, the mask will eventually be all ones (i.e. disappear)

### UNet Architecture
The architechture essentially it's based on a UNet-like structure, where all normal convolutional layers are replace with partial convolutional layers, such that in all cases the image is passed through the network alongside the mask.

<img src='https://raw.githubusercontent.com/MathiasGruber/PConv-Keras/master/data/images/architecture.png' />

### The loss function

This technique uses quite an intense loss function. The highlights of it are:

* Per-pixel losses both for maskes and un-masked regions
* Perceptual loss based on ImageNet pre-trained VGG-16 (*pool1, pool2 and pool3 layers*)
* Style loss on VGG-16 features both for predicted image and for computed image (non-hole pixel set to ground truth)
* Total variation loss for a 1-pixel dilation of the hole region

The weighting of all these loss terms are as follows:
<img src='https://raw.githubusercontent.com/MathiasGruber/PConv-Keras/master/data/images/eq7.PNG' />

### VGG16 model for feature extraction

The authors of the paper used PyTorch to implement the model. The VGG16 model was chosen for feature extraction. The [VGG16 model in PyTorch](https://pytorch.org/docs/stable/torchvision/models.html) was trained with the following image pre-processing:
1. Divide the image by 255,
2. Subtract [0.485, 0.456, 0.406] from the RGB channels, respectively,
3. Divide the RGB channels by [0.229, 0.224, 0.225], respectively.

## Resources 📚

- https://github.com/MathiasGruber/PConv-Keras
- "Image Inpainting for Irregular Holes Using Partial Convolutions", https://arxiv.org/abs/1804.07723
