from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PIL import Image, ImageQt
import design
import helper 
import matplotlib.pyplot as plt

# TODO:
#
# At rotation image is cropped
# and when it's rotated to default position
# image sizes don't persist
#
# ==========================
#
# Deal with scaling at fit_to_window mode
#
# ==========================
#
# Add reset button for transform/rotating/scaling operations?


# original_image and edited_image are instances of class ImageQt/ Image
class EditorApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._original_image = None
        self._edited_image = None
        self._pixmap = None
        self._without_rotation_image = None
        self._anlge = 0
        self._scale_factor = 1.0
        self._scale_factor_step = 0.25
        self._scale_factor_upper_bound = 3.0
        self._scale_factor_lower_bound = 0.25
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionReset.triggered.connect(self.reset)
        #Filters
        self.actionFilterSmooth.triggered.connect(self.smooth)
        self.actionFilterSmoothMore.triggered.connect(self.smooth_more)
        self.actionFilterSharpen.triggered.connect(self.sharpen)
        self.actionFilterGaussianBlur.triggered.connect(self.gaussian_blur)
        self.actionFilterBlur.triggered.connect(self.blur)
        self.actionFilterGreyscale.triggered.connect(self.greyscale)
        self.actionFilterInvert.triggered.connect(self.invert)
        self.actionFilterNoise.triggered.connect(self.noise)
        self.actionFilterEmboss.triggered.connect(self.emboss)
        self.actionFilterFindEdges.triggered.connect(self.find_edges)
        # Resize width and height listeners
        self.lineEditHeight.textEdited.connect(self.on_change_height_size)
        self.lineEditWidth.textEdited.connect(self.on_change_width_size)
        #Transform
        self.btnResize.clicked.connect(self.resize_image)
        self.btnRotateLeft.clicked.connect(self.rotate_to_the_left)
        self.btnRotateRight.clicked.connect(self.rotate_to_the_right)
        self.btnHistogram.clicked.connect(self.plot_histogram)
        self.checkBoxFitToWindowSize.stateChanged.connect(self.fit_to_window_size)
        self.btnZoomIn.clicked.connect(self.zoom_in)
        self.btnZoomOut.clicked.connect(self.zoom_out)
        
    def open_file(self):       
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл с изображением' , filter="Images (*.png *.jpg *.jpeg *.bmp *.gif *.gif *.cur *.ico)")[0]       
        if file_path:
            self._pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(file_path))
            self._original_image = ImageQt.fromqpixmap(self._pixmap)
            self._edited_image = self._original_image.copy()
            self.photo.setPixmap(self._pixmap)
            self.photo.resize(self._pixmap.width() , self._pixmap.height())
            self.enable_elements()
            self.reset_values()
              
    def save_file(self):
        if self._original_image is None:
            return
        file_path = QtWidgets.QFileDialog.getSaveFileName(self,'Сохранить файл с изображением' , filter="Images (*.png *.jpg *.jpeg *.bmp *.gif *.gif *.cur *.ico)")[0]
        if file_path:    
            #self._original_image.save(file_path)
            self._edited_image.save(file_path)

    def fit_to_window_size(self):
        if(self.checkBoxFitToWindowSize.isChecked()):
            self.scrollArea.setWidgetResizable(True)
            self.reset_values(fit = True)
        else:
            self.scrollArea.setWidgetResizable(False)
            self.photo.resize(self._pixmap.width() , self._pixmap.height())
            self.reset_values()
            pass
        #update_pixmap()

    def reset(self):
        self._edited_image = self._original_image.copy()
        self.update_pixmap()
        self._scale_factor = 1.0
        self.change_percentage(self._scale_factor)

    def plot_histogram(self):
        value = helper.histogram(self._edited_image)
        if(value == -1):
            self.error_dialog(message = "") # handle it
    
    def noise(self):
        self._edited_image = helper.noise(self._edited_image)
        self.update_pixmap()

    def blur(self):
        # if image is not null
        self._edited_image = helper.blur(self._edited_image)
        self.update_pixmap()
    
    def invert(self):
        self._edited_image = helper.invert(self._edited_image)
        self.update_pixmap()

    def greyscale(self):
        self._edited_image = helper.greyscale(self._edited_image)
        self.update_pixmap()

    def smooth(self):
        self._edited_image = helper.smooth(self._edited_image)
        self.update_pixmap()

    def smooth_more(self):
        self._edited_image = helper.smooth_more(self._edited_image)
        self.update_pixmap()

    def sharpen(self):
        self._edited_image = helper.sharpen(self._edited_image)
        self.update_pixmap()

    def gaussian_blur(self):
        self._edited_image = helper.gaussian_blur(self._edited_image)
        self.update_pixmap()

    def emboss(self):
        self._edited_image = helper.emboss(self._edited_image)
        self.update_pixmap()

    def find_edges(self):
        self._edited_image = helper.find_edges(self._edited_image)
        self.update_pixmap()

    def box_blur(self):
        print("inside box blur")
        self._edited_image = helper.box_blur(self._edited_image)
        self.update_pixmap()

    def resize_image(self):
        width = self.lineEditWidth.text()
        height = self.lineEditHeight.text()
        if(width =='' or height == ''):
            return
        try:
            width = int(width)
            height = int(height)
        except TypeError as e:
            return
        if( width > 0 and height > 0):
            self._edited_image = helper.resize(self._edited_image, width, height)
            self.update_pixmap()
            #qdialog?

    def scale(self, factor):
        self.photo.resize(factor * self._pixmap.width() , factor *self._pixmap.height())
        self.change_percentage(factor)

    def zoom_in(self):
        if(self._scale_factor == self._scale_factor_lower_bound):
            self.btnZoomOut.setEnabled(True)
        self._scale_factor += self._scale_factor_step
        if(self._scale_factor == self._scale_factor_upper_bound):
            self.btnZoomIn.setDisabled(True)
        self.scale(self._scale_factor)
        
    def zoom_out(self):
        if(self._scale_factor == self._scale_factor_upper_bound):
            self.btnZoomIn.setEnabled(True)
        self._scale_factor -= self._scale_factor_step
        if(self._scale_factor == self._scale_factor_lower_bound):
            self.btnZoomOut.setDisabled(True)
        self.scale(self._scale_factor)

    def rotate_to_the_left(self):
        angle = 90
        self._edited_image = helper.rotate(self._edited_image , angle)
        self.update_pixmap()
    
    def rotate_to_the_right(self):
        angle = -90
        self._edited_image = helper.rotate(self._edited_image , angle)
        self.update_pixmap()

    def on_change_height_size(self):
        if(self.lineEditHeight.text() == ''):
            return
        if(self.checkBoxAutoRatio.isChecked()):
            r_width = helper.get_ratio_width(self._edited_image.width , self._edited_image.height , int(self.lineEditHeight.text()))
            self.lineEditWidth.setText(str(r_width))

    def on_change_width_size(self):
        if(self.lineEditWidth.text() == ''):
            return
        if(self.checkBoxAutoRatio.isChecked()):
            r_height = helper.get_ratio_height(self._edited_image.width , self._edited_image.height , int(self.lineEditWidth.text()))
            self.lineEditHeight.setText(str(r_height))

    def change_percentage(self , factor):
        self.percentage.setText(str(int(factor * 100)) + "%")

    def update_pixmap(self):
        self._pixmap = ImageQt.toqpixmap(self._edited_image)
        self.photo.setPixmap(self._pixmap)
        self.photo.resize(self._pixmap.width() , self._pixmap.height())

    def disable_elements(self):
        pass
    
    def enable_elements(self):
        #self.photo.setScaledContents(True)
        self.actionSave.setEnabled(True) 
        self.actionFilterBlur.setEnabled(True)
        self.btnRotateLeft.setEnabled(True)
        self.btnRotateRight.setEnabled(True)
        self.btnHistogram.setEnabled(True)
        self.menuFilters.setEnabled(True)
        self.menuOther.setEnabled(True)
        self.actionSave.setEnabled(True)
        self.btnResize.setEnabled(True)
        self.checkBoxAutoRatio.setEnabled(True)
        self.btnZoomIn.setEnabled(True)
        self.btnZoomOut.setEnabled(True)
        self.checkBoxFitToWindowSize.setEnabled(True)

    def reset_values(self, fit = False):
        self._scale_factor = 1.0
        self.percentage.setText("100%")
        self.btnZoomIn.setEnabled(not fit)
        self.btnZoomOut.setEnabled(not fit)

    def error_dialog(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Исключение")
        if(message):
            msg.setText(message)
        else:
            msg.setText("Произошла ошибка при использовании гистограммы. Попробуйте использовать её с другим фильтром или без них.")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
