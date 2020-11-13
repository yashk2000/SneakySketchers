import torch
from torchvision import transforms

from initDS import InitDataset
from model import PConvUNet
from loss import InpaintingLoss, VGG16FeatureExtractor
from trainer import Trainer
from utilities import Config, load_ckpt, create_ckpt_dir

config = Config("config.yml")
config.ckpt = create_ckpt_dir()
print("Check Point is '{}'".format(config.ckpt))


device = torch.device("cuda:{}".format(config.cuda_id)
                      if torch.cuda.is_available() else "cpu")


print("Loading the Model...")
model = PConvUNet(finetune=config.finetune,
                  layer_size=config.layer_size)

if config.finetune:
    model.load_state_dict(torch.load(config.finetune)['model'])
model.to(device)

# Data Transformation
img_tf = transforms.Compose([
            transforms.ToTensor()
            ])

mask_tf = transforms.Compose([
            transforms.RandomResizedCrop(256),
            transforms.ToTensor()
            ])


print("Loading the Validation Dataset...")
dataset_val = InitDataset(config.data_root,
                      img_tf,
                      mask_tf,
                      data="val")


print("Loading the Training Dataset...")
dataset_train = InitDataset(config.data_root,
                        img_tf,
                        mask_tf,
                        data="train")

# Loss fucntion
criterion = InpaintingLoss(VGG16FeatureExtractor(),
                            tv_loss=config.tv_loss).to(device)
# Optimizer
lr = config.finetune_lr if config.finetune else config.initial_lr
if config.optim == "Adam":
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad,
                                        model.parameters()),
                                    lr=lr,
                                    weight_decay=config.weight_decay)
elif config.optim == "SGD":
    optimizer = torch.optim.SGD(filter(lambda p: p.requires_grad,
                                        model.parameters()),
                                lr=lr,
                                momentum=config.momentum,
                                weight_decay=config.weight_decay)

start_iter = 0
trainer = Trainer(start_iter, config, device, model, dataset_train,
                    dataset_val, criterion, optimizer)
trainer.iterate()