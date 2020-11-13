from gui.window import Form
from gui.draw import *
from PIL import Image, ImageQt
import random, io, os
import numpy as np
import torch
import cv2
import torchvision.transforms as transforms
from util import util
import os
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF

from pconv.model import PConvUNet


class model(QtWidgets.QWidget, Form):
    shape = 'line'
    CurrentWidth = 1

    def __init__(self, opt):
        super(model, self).__init__()
        self.setupUi(self)
        self.opt = opt
        # self.show_image = None
        self.show_result_flag = False
        self.opt.loadSize = [256, 256]
        self.img_root = './results/'
        self.graphicsView_2.setMaximumSize(self.opt.loadSize[0]+30, self.opt.loadSize[1]+30)

        self.device = torch.device("cpu")

        # Define the model
        print("Loading the Model...")
        self.model = PConvUNet(finetune=False, layer_size=7)
        self.model.load_state_dict(torch.load("model.pth", map_location=self.device)['model'])
        self.model.to(self.device)
        self.model.eval()

        # show logo
        self.show_logo()

        # original mask
        self.new_painter()

        # selcet model
        #self.comboBox.activated.connect(self.load_model)

        # load image
        self.pushButton.clicked.connect(self.load_image)

        # save result
        self.pushButton_4.clicked.connect(self.save_result)

        # draw/erasure the mask
        self.radioButton.toggled.connect(lambda: self.draw_mask('line'))
        self.radioButton_2.toggled.connect(lambda: self.draw_mask('rectangle'))
        self.spinBox.valueChanged.connect(self.change_thickness)
        # erase
        self.pushButton_5.clicked.connect(self.clear_mask)

        # fill image, image process
        self.transform = transforms.Compose([transforms.ToTensor()])
        self.pushButton_3.clicked.connect(self.predict)

        # show the result
        self.pushButton_6.clicked.connect(self.show_result)

    def showImage(self, fname):
        """Show the masked images"""
        #value = self.comboBox.currentIndex()
        img = Image.open(fname).convert('RGB')
        self.img_original = img.resize(self.opt.loadSize)
        self.img = self.img_original
        self.show_image = ImageQt.ImageQt(self.img)
        self.new_painter(self.show_image)

    def show_result(self):
        """Show the results and original image"""
        if self.show_result_flag:
            self.show_result_flag = False
            out = TF.to_pil_image(self.img_out)
            new_pil_image = out
            new_qt_image = ImageQt.ImageQt(new_pil_image)
        else:
            self.show_result_flag = True
            new_qt_image = ImageQt.ImageQt(self.img_original)
        self.graphicsView_2.scene = QtWidgets.QGraphicsScene()
        item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(new_qt_image))
        self.graphicsView_2.scene.addItem(item)
        self.graphicsView_2.setScene(self.graphicsView_2.scene)

    def show_logo(self):
        img = QtWidgets.QLabel(self)
        img.setGeometry(750, 20, 140, 50)
        # read images
        pixmap = QtGui.QPixmap("./gui/icon.png")
        pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        img.setPixmap(pixmap)
        img.show()

    def load_model(self):
        """Load different kind models for different datasets and mask types"""
        #value = self.comboBox.currentIndex()
        if value == 0:
            raise NotImplementedError("Please choose a model")
        else:
            # define the model type and dataset type
            index = value-1
            self.opt.name = self.model_name[index]
        self.model = create_model(self.opt)

    def load_image(self):
        """Load the image"""
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'select the image', os.path.expanduser("~"), 'Image files(*.jpg *.png)')
        self.showImage(self.fname)

    def save_result(self):
        self.opt.results_dir = "./results"
        """Save the results to the disk"""
        util.mkdir(self.opt.results_dir)
        img_name = self.fname.split('/')[-1]

        # save the original image
        original_name = '%s_%s' % ('original', img_name)
        original_path = os.path.join(self.opt.results_dir, original_name)
        img_original = util.tensor2im(self.img_truth)
        util.save_image(img_original, original_path)

        # save the mask
        mask_name = '%s_%d_%s' % ('mask', self.PaintPanel.iteration, img_name)
        mask_path = os.path.join(self.opt.results_dir, mask_name)
        img_mask = util.tensor2im(self.img_c)
        ret, img_mask = cv2.threshold(img_mask, 150, 255, cv2.THRESH_BINARY)
        util.save_image(img_mask, mask_path)

        # save the results
        result_name = '%s_%d_%s' % ('result', self.PaintPanel.iteration, img_name)
        result_path = os.path.join(self.opt.results_dir, result_name)
        img_result = TF.to_pil_image(self.img_out)
        img_result = np.array(img_result)
        util.save_image(img_result, result_path)

    def new_painter(self, image=None):
        """Build a painter to load and process the image"""
        # painter
        self.PaintPanel = painter(self, image)
        self.PaintPanel.close()
        self.stackedWidget.insertWidget(0, self.PaintPanel)
        self.stackedWidget.setCurrentWidget(self.PaintPanel)

    def change_thickness(self, num):
        """Change the width of the painter"""
        self.CurrentWidth = num
        self.PaintPanel.CurrentWidth = num

    def draw_mask(self, maskStype):
        """Draw the mask"""
        self.shape = maskStype
        self.PaintPanel.shape = maskStype

    def clear_mask(self):
        """Clear the mask"""
        self.showImage(self.fname)
        if self.PaintPanel.Brush:
            self.PaintPanel.Brush = False
        else:
            self.PaintPanel.Brush = True

    def set_input(self):
        """Set the input for the network"""
        # get the test mask from painter
        self.PaintPanel.saveDraw()
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.ReadWrite)
        self.PaintPanel.map.save(buffer, 'PNG')
        pil_im = Image.open(io.BytesIO(buffer.data()))

        # transform the image to the tensor
        img = self.transform(self.img)
        #value = self.comboBox.currentIndex()
        mask = torch.autograd.Variable(self.transform(pil_im)).unsqueeze(0)
        # mask from the random mask
        # mask = Image.open(self.mname)
        # mask = torch.autograd.Variable(self.transform(mask)).unsqueeze(0)
        mask = (mask < 1).float()

        # get I_m and I_c for image with mask and complement regions for training
        mask = mask
        self.img_truth = img * 2 - 1
        self.img_m = mask * self.img_truth
        self.img_c = mask

        return self.img_m, self.img_c, self.img_truth, mask

    def predict(self):

        # Loading Input and Mask
        print("Loading the inputs...")
        img_m, img_c, img_truth, mask = self.set_input()
        img_original = util.tensor2im(img_truth)
        org = Image.fromarray(img_original)
        org = TF.to_tensor(org.convert('RGB')) 
        img_mask = util.tensor2im(img_c)
        ret, img_mask = cv2.threshold(img_mask, 150, 255, cv2.THRESH_BINARY)
        mask = Image.fromarray(img_mask)
        mask = mask.convert('L')
        mask = mask.point(lambda x: 0 if x<128 else 255, '1')
        mask = TF.to_tensor(mask.convert('RGB'))
        inp = org * mask

        # Model prediction
        print("Model Prediction...")
        with torch.no_grad():
            inp_ = inp.unsqueeze(0).to(self.device)
            mask_ = mask.unsqueeze(0).to(self.device)
            raw_out, _ = self.model(inp_, mask_)

        # Post process
        raw_out = raw_out.to(torch.device('cpu')).squeeze()
        raw_out = raw_out.clamp(0.0, 1.0)
        out = mask * inp + (1 - mask) * raw_out
        self.img_out = out
        self.show_result_flag = True
        self.show_result()
