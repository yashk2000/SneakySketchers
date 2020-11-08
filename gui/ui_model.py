from gui.ui_window import Ui_Form
from gui.ui_draw import *
from PIL import Image, ImageQt

class ui_model(QtWidgets.QWidget, Ui_Form):
    shape = 'line'
    CurrentWidth = 1

    def __init__(self):
        super(ui_model, self).__init__()
        self.setupUi(self)
        self.show_result_flag = False
        self.model_name = ['celeba_center', 'paris_center', 'imagenet_center', 'place2_center',
                           'celeba_random', 'paris_random','imagenet_random', 'place2_random']
        self.graphicsView_2.setMaximumSize(286, 286)

        # original mask
        self.new_painter()


        # load image
        self.pushButton.clicked.connect(self.load_image)

        # draw/erasure the mask
        self.radioButton.toggled.connect(lambda: self.draw_mask('line'))
        self.spinBox.valueChanged.connect(self.change_thickness)
        # erase
        self.pushButton_5.clicked.connect(self.clear_mask)

        # fill image, image process
        self.pushButton_3.clicked.connect(self.fill_mask)


    def showImage(self, fname):
        """Show the masked images"""
        value = self.comboBox.currentIndex()
        img = Image.open(fname).convert('RGB')
        self.img_original = img.resize([266, 266])
        self.img = self.img_original
        self.show_image = ImageQt.ImageQt(self.img)
        self.new_painter(self.show_image)

    def load_image(self):
        """Load the image"""
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'select the image', 'Image files(*.jpg *.png)')
        self.showImage(self.fname)

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
        value = self.comboBox.currentIndex()
        if value > 4:
            mask = torch.autograd.Variable(self.transform(pil_im)).unsqueeze(0)
            # mask from the random mask
            # mask = Image.open(self.mname)
            # mask = torch.autograd.Variable(self.transform(mask)).unsqueeze(0)
            mask = (mask < 1).float()
        else:
            mask = task.center_mask(img).unsqueeze(0)
        if 1 > 0:
            img = img.unsqueeze(0)
            mask = mask

        # get I_m and I_c for image with mask and complement regions for training
        mask = mask
        self.img_truth = img * 2 - 1
        self.img_m = mask * self.img_truth
        self.img_c = (1 - mask) * self.img_truth

        return self.img_m, self.img_c, self.img_truth, mask

    def fill_mask(self):
        """Forward to get the generation results"""
        img_m, img_c, img_truth, mask = self.set_input()
        if self.PaintPanel.iteration < 100:
            with torch.no_grad():
                # encoder process
                distributions, f = self.model.net_E(img_m)
                q_distribution = torch.distributions.Normal(distributions[-1][0], distributions[-1][1])
                #q_distribution = torch.distributions.Normal( torch.zeros_like(distributions[-1][0]), torch.ones_like(distributions[-1][1]))
                z = q_distribution.sample()

                # decoder process
                scale_mask = task.scale_pyramid(mask, 4)
                self.img_g, self.atten = self.model.net_G(z, f_m=f[-1], f_e=f[2], mask=scale_mask[0].chunk(3, dim=1)[0])
                self.img_out = (1 - mask) * self.img_g[-1].detach() + mask * img_m

                # get score
                score =self.model.net_D(self.img_out).mean()
                self.label_6.setText(str(round(score.item(),3)))
                self.PaintPanel.iteration += 1

        self.show_result_flag = True
        self.show_result()
