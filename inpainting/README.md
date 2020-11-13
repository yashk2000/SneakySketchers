# 🐍 The Python Module for training the inpainting module 

## 🛠️ How to run it

Once you have cloned the repo and downloaded the model from [here](https://drive.google.com/file/d/1_J-NgecLjU9PDvkmnJAo7-ghcQuqia2N/view?usp=sharing), you can use the 
requirements.txt to install the needed dependencies and run the entire training process on your machine. We have provided a Jupyter Notebook [here](https://github.com/yashk2000/SneakySketchers/tree/main/InPainting%20Notebook) as well which 
you can directly run on Google Colab. 

```bash 
pip install -r requirements.txt
```

## 🏋️ Training a model 

Any image dataset can be used to train an inpainting model. We trained our model on a subset of the [Places2](http://places2.csail.mit.edu/download.html) dataset.

In order to generate masks to train the model, run the [`masks.py`](https://github.com/yashk2000/SneakySketchers/blob/main/inpainting/masks.py) script. You can change
the amount of masks to be generated and the directory for training as well as validation masks as well. 

Simple execute the following line to generate the masks: 

```
python masks.py
```

Most of the configuration settings are present in the [`config.yml`](https://github.com/yashk2000/SneakySketchers/blob/main/inpainting/config.yml) file. You can change
the number of interations, the optimizer to be used the other constants directly over here instead of searching for them in the code. 

Once you're satisfied with your setting and have the dataset ready, to train the model simply run:

```
python main.py
```

## 🔮 Making predictions using the model

If you are just interested in making predictions with the model, or you have trained it and now want to use it for predictions, you can follow the following steps. 
The best way would be to use the desktop app we have provided over [here](https://github.com/yashk2000/SneakySketchers/tree/main/application) along with instructions
on how to use it. 

### Using the model directly from the command line

If you're interested in running the model directly from the command line, you will need to use the [`predict.py`](https://github.com/yashk2000/SneakySketchers/blob/main/inpainting/predict.py)
script. The model takes in an image, and a mask as it's input. To do this, run the following command:

```
python predict.py --image <path to input image> --mask <path to mask> --model <path to stored model>
```

## 🏗️ The model

We have used the technique for **partial convolutions** for performing image inpainting and training the model. This is a PyTorch implementation of "Image Inpainting for Irregular Holes Using Partial Convolutions", [https://arxiv.org/abs/1804.07723](https://arxiv.org/abs/1804.07723)
by Guilin Liu, Fitsum A. Reda, Kevin J. Shih, Ting-Chun Wang, Andrew Tao and Bryan Catanzaro from NVIDIA. 

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
