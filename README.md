![SneakySketchers](https://socialify.git.ci/yashk2000/SneakySketchers/image?description=1&descriptionEditable=Make%20your%20almost%20perfect%20photos%2C%20perfect!&font=Source%20Code%20Pro&forks=1&issues=1&language=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark)

# 🖼️ Sneaky Sketchers

## 🙋 What is Sneaky Sketchers?

Have you ever taken a photo in which there is some unneeded object in the background, ever taken a photo and someone just walked behind you, and now you feel the photo is not as good as it could have been? 📷 

If so, worry not! This desktop application allows you to select the areas in a photo you want to remove by drawing on them. Once you're done, the app will erase the objects you drew on, and generate a new photo which would look as if those obejcts were never present! 🔥

You can also use this application for having some fun. Ever wondered how you would look without a moustache, or with spectacles? Or wondered how your face would like with different features? Well draw over your face, and let the app do the magic! 👦 👧

## 👨‍🏭 Who are we?
This project was built by [Shambhavi Aggarwal](https://github.com/agg-shambhavi), [Farhan Kiyani](https://github.com/farhan2742), [Yash Khare](https://github.com/yashk2000) and [Ridham Bhat](https://github.com/ridhambhat).

## 💻 What did we use?
Sneaky Sketchers is built completely in [Python](https://www.python.org/). We have created [Jupyter Notebooks](https://jupyter.org/) on [Google Colab](https://colab.research.google.com/) to train our models and the desktop app is built using [PyQt5](https://pypi.org/project/PyQt5/) 🐍

## :hammer: Installation 

For setting up the desktop app, head over [here](https://github.com/yashk2000/SneakySketchers/tree/main/application).

## :man_technologist: How do I contribute?
- To get more detailed documentation, please check out our project's wiki. :book:
- Before contributing do go through the [Code of Conduct](https://github.com/yashk2000/SneakySketchers/blob/main/CODE_OF_CONDUCT.md) :wrench:
- Please go through the [Contributing Guidelines](https://github.com/yashk2000/SneakySketchers/blob/main/CONTRIBUTING.md) as well. 📚
- If you find any bugs in the application, or a feature you think would be nice to have, please open an issue.❗

## 🪜 Folder Struture 

Each folder has it's own dedicated readme on what it's contents do, how to set them up and use them. 

- [`InPainting Notebook`](https://github.com/yashk2000/SneakySketchers/tree/main/InPainting%20Notebook): This folder contains the jupyter notebook we trained on Google Colab. 
- [`application`](https://github.com/yashk2000/SneakySketchers/tree/main/application): This folder contains the main PyQt5 desktop application.  
- [`inpainting`](https://github.com/yashk2000/SneakySketchers/tree/main/inpainting): This folder contains python scripts that can be used for training a model, or making predictions. They can directly be imported into your own project. 

## 💭 What we learned 

- This was the first time Yash worked with PyQt and leanred a lot about making desktop apps with it. He also worked with PyTorch to this extent for the first time.  
- Shambhavi had never worked with PyTorch before, and helped implement an entire research paper by NVIDIA in completely in PyTorch. 
- Farhan did not have much experince with machine leanring, but he contributed to the project and learned a lot as well. 

This project ended up being a kind of a research project for us since we spent quite a lot of our time reading the paper on Partial Convolutions by NVIDIA, understanding how it works, and implementing it. We found a Keras implementation which gave pretty good results. We understood the paper with the Keras code, and created a PyTorch implementation. Since this model is a bit large in size, we decided to go ahead with building a desktop application which can be used offline.

## 🕒 Training Time

The paper which we referred to has trained the model on 3 different datasets, for a period of 14 days. Where as with the resources we had(thanks to Google Colab), we just trained our model on a subset of the Places2 dataset for one night. Based on this limited amount of training, the model does not match the performance given by the original implementation, but it does a pretty good job. In future, should we get the time and resources to train the model completely, we would be able to improve our model a lot.  

## 📷 How the desktop app looks 

| ![Screenshot_20201114_023136](https://user-images.githubusercontent.com/41234408/99120923-b6591600-2621-11eb-8995-4ba92802416c.png) | ![Screenshot_20201114_023152](https://user-images.githubusercontent.com/41234408/99120920-b48f5280-2621-11eb-8f48-c6a9b5c6df5b.png)  |
|---|---|
| PyQt App | Loading an image |
| ![gg](https://user-images.githubusercontent.com/41234408/99121621-ba396800-2622-11eb-9526-f57f67ebd687.png) | ![gg1](https://user-images.githubusercontent.com/41234408/99121620-b9083b00-2622-11eb-829e-499da1a7a449.png) |
| Original | Inpainted |
| ![ff](https://user-images.githubusercontent.com/41234408/99121719-ea810680-2622-11eb-9316-f8ab7fef7888.png) | ![ff2](https://user-images.githubusercontent.com/41234408/99121713-e8b74300-2622-11eb-87b8-823935ecf182.png) |
| Original | Inpainted |
| ![ee](https://user-images.githubusercontent.com/41234408/99121752-fc62a980-2622-11eb-92eb-e806539e4492.png) | ![ee1](https://user-images.githubusercontent.com/41234408/99121748-fa98e600-2622-11eb-942c-b3a5978a69c6.png) |
| Original | Inpainted |

## :soon: What's next? 

- A web version of the application with a lighter model. 
- A better UI for the desktop app
- Training the model further to improve it's performance. 

## 📜 License
This project is released under a free and open-source software license, Apache License 2.0 or later ([LICENSE](LICENSE) or https://www.apache.org/licenses/LICENSE-2.0). The documentation is also released under a free documentation license, namely the [GFDL v1.3](https://www.gnu.org/licenses/fdl-1.3.en.html) license or later.

### 🖊️ Contributions
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be licensed as above, without any additional terms or conditions.

## :books: Resources 

- [https://github.com/MathiasGruber/PConv-Keras](https://github.com/MathiasGruber/PConv-Keras)
"Image Inpainting for Irregular Holes Using Partial Convolutions", [https://arxiv.org/abs/1804.07723](https://arxiv.org/abs/1804.07723)

### Citation

```
@inproceedings{liu2018partialpadding,
   author    = {Guilin Liu and Kevin J. Shih and Ting-Chun Wang and Fitsum A. Reda and Karan Sapra and Zhiding Yu and Andrew Tao and Bryan Catanzaro},
   title     = {Partial Convolution based Padding},
   booktitle = {arXiv preprint arXiv:1811.11718},   
   year      = {2018},
}
```

```
@inproceedings{liu2018partialinpainting,
   author    = {Guilin Liu and Fitsum A. Reda and Kevin J. Shih and Ting-Chun Wang and Andrew Tao and Bryan Catanzaro},
   title     = {Image Inpainting for Irregular Holes Using Partial Convolutions},
   booktitle = {The European Conference on Computer Vision (ECCV)},   
   year      = {2018},
}
```
