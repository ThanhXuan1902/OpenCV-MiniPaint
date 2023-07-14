from pickle import FALSE
import sys
from xml.etree.ElementTree import QName
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QLabel, QPushButton, \
    QFileDialog, QMessageBox, QMenu, QDesktopWidget, QGroupBox, QFormLayout, QLineEdit, QComboBox, \
    QDialogButtonBox, QVBoxLayout, QDialog
from PyQt5.QtGui import QImage, QBrush, QIcon, QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import QSize, Qt
import tkinter as tk

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.title = 'XỬ LÝ ẢNH'
        self.win_x = 350    # .
        self.win_y = 80     # .
        self.width = 1200   # width window
        self.height = 820   # heigt window
        self.zoom = 1       # mức độ zoom của ảnh đầu vào
        self.x_pos = 0      # .
        self.y_pos = 0      # .
        self.x0 = 0         # .
        self.y0 = 0         # .
        self.x1 = 0         # .
        self.y1 = 0         # .
        self.pixel = 1      # .
        self.font_scale = 1 # .
        self.select_color_x = 675 # .
        self.select_color_y = 32  # .
        self.color = (0, 0, 0)   # .
        self.font_style = cv2.FONT_HERSHEY_COMPLEX # .
        # Set ảnh đầu ra là False
        self.converted = False # .
        self.draw_rect = False # .
        self.draw_elli = False #
        self.draw_tri = False  # .
        self.draw_l = False    # .
        self.put_t = False     # .
        self.flag = False      # .
        self.crop = False      # .

        self.label = QLabel(self)   
        self.label_origin = QLabel(self)
        self.about_window = AboutWindow()

        self.ui_components()

    def ui_components(self): ## toàn bộ hàm của giao diện
        # Xử lý về cửa sổ window và các thứ tự của hàm trong giao diện
        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))
        self.menu_bar()
        self.tools_bar()
        self.background_image_backup()
        self.background_image_origin()
        self.disable_action()
        self.backup_image()
    def center(self): # Hàm xử lý cửa sổ window nằm ở giữa
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def menu_bar(self): # Hàm xử lý thanh menu bar ở phía trên cùng
        self.menu_file = self.menuBar().addMenu('Tập Tin') # Thêm vào thanh menu bar tập tin
        self.menu_image = self.menuBar().addMenu('Ảnh') # Thêm vào thanh menu bar ảnh
        self.menu_help = self.menuBar().addMenu('Giúp Đỡ') # Thêm vào thanh menu bar giúp đỡ
        self.menu_smoothing = self.menuBar().addMenu('Làm Mịn') # Thêm vào thanh menu bar Làm Mịn
        self.menu_filter = self.menuBar().addMenu('Bộ Lọc') # Thêm vào thanh menu bar Lọc
        self.menu_diffrent = self.menuBar().addMenu('Biến Đổi Khác') # Thêm vào thanh menu bar Lọc
        
        # Xử lý mục Tập tin
        self.action_open = QAction('Mở tập tin', self)    # Khi có sự kiện vào Mở tập tin
        self.action_open.setShortcut('Ctrl+O')            # Hoặc ctro + O
        self.action_open.triggered.connect(self.browse_image) # Kết nối thực thi hàm browse_image
        self.menu_file.addAction(self.action_open)  # Thêm hành động action_open vào mục Tập Tin
        self.menu_file.addSeparator() # Thêm chữ Mở tập tin  khi click vào Tập tin

        self.action_save = QAction('Lưu', self) # Khi có sự kiện Lưu file
        self.action_save.setShortcut('Ctrl+S')  # Hoặc có sự kiện ctrl + S
        self.action_save.triggered.connect(self.save_image) # Kết nối tới hàm save_image
        self.menu_file.addAction(self.action_save) # Thêm hành động action_save vào mục Tập Tin
        self.menu_file.addSeparator()   # Thêm chữ Lưu khi click vào Tập tin

        self.action_exit = QAction('Thoát', self) # Khi có sự kiện thoát
        self.action_exit.triggered.connect(app.quit) # Kết nối tớ hàm app. quit tức là sẽ tắt ứng dụng
        self.menu_file.addAction(self.action_exit) # Thêm sự kiện thoát vào mục Tập Tin

        # Xử lý mục ảnh
        self.action_zoom_in = QAction('Phóng to', self) # Khi có sự kiện vào Phóng to
        self.action_zoom_in.setShortcut('Ctrl++')       # Hoặc ctrl +
        self.action_zoom_in.triggered.connect(self.zoom_in) # Kết nối tới hàm zoom_in
        self.menu_image.addAction(self.action_zoom_in) # Thêm mục xử lý sự kiện phóng to vào ảnh
        self.menu_image.addSeparator() # Thêm chữ Phóng to khi click vào ảnh

        self.action_zoom_out = QAction('Thu nhỏ', self) # Khi có sự kiện vào Thu nhỏ
        self.action_zoom_out.setShortcut('Ctrl+-')      # Hoặc Ctrl -
        self.action_zoom_out.triggered.connect(self.zoom_out) # Kết nối tới hàm hàm zoom_out
        self.menu_image.addAction(self.action_zoom_out) # # Thêm mục xử lý sự kiện thu nhỏ vào ảnh
        self.menu_image.addSeparator()# Thêm chữ Thu nhỏ khi click vào ảnh

        self.action_convert_to = self.menu_image.addMenu('Chuyển đổi sang') # Thêm tiêu đề chuyển đổi sang khi click vào ảnh
        self.menu_image.addSeparator() # Thêm chữ chuyển đổi sang khi click vào ảnh

        self.action_original = QAction('Original', self) # Khi có sự kiện vào Original
        self.action_convert_to.addAction(self.action_original) # # Thêm mục xử lý sự kiện Original vào ảnh
        self.action_original.triggered.connect(self.convert_to_original) # Kết nối tới hàm convert_to_original

        self.action_gray = QAction('Gray', self) # # Khi có sự kiện vào Gray
        self.action_convert_to.addAction(self.action_gray) #  Thêm mục xử lý sự kiện Gray vào ảnh
        self.action_gray.triggered.connect(self.convert_to_gray) # Kết nối tới hàm convert_to_gray

        self.action_HSV = QAction('HSV', self) # # Khi có sự kiện vào HSV
        self.action_convert_to.addAction(self.action_HSV) #  Thêm mục xử lý sự kiện HSV vào ảnh
        self.action_HSV.triggered.connect(self.convert_to_hsv) # Kết nối tới hàm convert_to_hsv

        self.action_HLS = QAction('HLS', self)  # # Khi có sự kiện vào HLS
        self.action_convert_to.addAction(self.action_HLS) # Thêm mục xử lý sự kiện HLS vào ảnh
        self.action_HLS.triggered.connect(self.convert_to_hls) # Kết nối tới hàm convert_to_hls

        self.action_LAB = QAction('LAB', self) # Khi có sự kiện vào LAB
        self.action_convert_to.addAction(self.action_LAB)   # Thêm mục xử lý sự kiện LAB vào ảnh
        self.action_LAB.triggered.connect(self.convert_to_lab) # Kết nối tới hàm convert_to_lab

        self.action_LUV = QAction('LUV', self) # Khi có sự kiện vào LUV
        self.action_convert_to.addAction(self.action_LUV) #  # Thêm mục xử lý sự kiện LUV vào ảnh
        self.action_LUV.triggered.connect(self.convert_to_luv)# Kết nối tới hàm convert_to_luv

        self.action_YUV = QAction('YUV', self)# Khi có sự kiện vào YUV
        self.action_convert_to.addAction(self.action_YUV)  #  # Thêm mục xử lý sự kiện YUV vào ảnh
        self.action_YUV.triggered.connect(self.convert_to_yuv)# Kết nối tới hàm convert_to_YUV

        #  mục làm mịn
        self.action_BLUR = QAction('Làm mở (Blur)', self) # 
        self.menu_smoothing.addAction(self.action_BLUR) #  Thêm mục xử lý sự kiện Làm mở vào làm mịn khi click
        self.action_BLUR.triggered.connect(self.action_blur) # kết nối tới hàm action_blur

        self.action_BOX = QAction('Lọc ảnh (Box Filter)', self)
        self.menu_smoothing.addAction(self.action_BOX) #  Thêm mục xử lý sự kiện Lọc ảnh vào làm mịn khi click
        self.action_BOX.triggered.connect(self.action_box) # kết nối tới hàm action_box
        
        self.action_MEDIAN = QAction('Lọc trung vị (Median Filter)', self)
        self.menu_smoothing.addAction(self.action_MEDIAN) #  Thêm mục xử lý sự kiện Lọc trung vị vào làm mịn khi click
        self.action_MEDIAN.triggered.connect(self.action_median) # kết nối tới hàm action_median

        self.action_BILATERAL = QAction('Lọc hai chiều (Bilateral Filter)', self)
        self.menu_smoothing.addAction(self.action_BILATERAL) #  Thêm mục xử lý sự kiện Lọc hai chiều vào làm mịn khi click
        self.action_BILATERAL.triggered.connect(self.action_bilateral) # kết nối tới hàm action_bilateral

        self.action_GAUSS = QAction('Lọc Gauss (Gaussian Filter)', self)
        self.menu_smoothing.addAction(self.action_GAUSS) #  Thêm mục xử lý sự kiện Lọc hai chiều vào làm mịn khi click
        self.action_GAUSS.triggered.connect(self.action_gauss) # kết nối tới hàm action_gauss
        
        # Mục lọc ảnh
        self.action_THRESHOLD = QAction('Lọc ngưỡng trung bình(Median Threshold)', self)
        self.menu_filter.addAction(self.action_THRESHOLD) #  Thêm mục xử lý sự kiện Lọc ngưỡng trung bình vào lọc ảnh khi click
        self.action_THRESHOLD.triggered.connect(self.action_threshold) # kết nối tới hàm action_threshold

        self.action_DIRECTIONAL = QAction('Lọc định hướng(Directional Filtering)', self)
        self.menu_filter.addAction(self.action_DIRECTIONAL) #  Thêm mục xử lý sự kiện Lọc lọc định hướng  vào lọc ảnh khi click
        self.action_DIRECTIONAL.triggered.connect(self.action_directional) # kết nối tới hàm action_directional

        self.action_DIRECTIONAL_2 = QAction('Lọc định hướng 2(Directional Filtering 2)', self)
        self.menu_filter.addAction(self.action_DIRECTIONAL_2) #  Thêm mục xử lý sự kiện Lọc lọc định hướng  vào lọc ảnh khi click
        self.action_DIRECTIONAL_2.triggered.connect(self.action_directional_2) # kết nối tới hàm action_directional

        self.action_DIRECTIONAL_3 = QAction('Lọc định hướng 3(Directional Filtering 3)', self)
        self.menu_filter.addAction(self.action_DIRECTIONAL_3) #  Thêm mục xử lý sự kiện Lọc lọc định hướng  vào lọc ảnh khi click
        self.action_DIRECTIONAL_3.triggered.connect(self.action_directional_3) # kết nối tới hàm action_directional

        # Mục biến đổi khác
        self.action_GRAY = QAction('Ảnh Xám(Grayscale)', self)
        self.menu_diffrent.addAction(self.action_GRAY) #  Thêm mục xử lý sự kiện Ảnh Xám  vào lọc ảnh khi click
        self.action_GRAY.triggered.connect(self.action_grays) # kết nối tới hàm action_gray

        self.action_NEGATIVE = QAction('Ảnh Âm Bản(Negative)', self)
        self.menu_diffrent.addAction(self.action_NEGATIVE) #  Thêm mục xử lý sự kiện Ảnh Âm Bản vào lọc ảnh khi click
        self.action_NEGATIVE.triggered.connect(self.action_negative) # kết nối tới hàm action_gray

        self.action_LOG = QAction('Ảnh Log', self)
        self.menu_diffrent.addAction(self.action_LOG) #  Thêm mục xử lý sự kiện Ảnh Log vào lọc ảnh khi click
        self.action_LOG.triggered.connect(self.action_log) # kết nối tới hàm action_log
        
        self.action_HISTOGRAM = QAction('Ảnh Histogram Equal', self)
        self.menu_diffrent.addAction(self.action_HISTOGRAM) #  Thêm mục xử lý sự kiện ẢnhH histogram vào lọc ảnh khi click
        self.action_HISTOGRAM.triggered.connect(self.action_histogram) # kết nối tới hàm action_histogram

        self.action_GAMMA = QAction('Ảnh Gamma', self)
        self.menu_diffrent.addAction(self.action_GAMMA) #  Thêm mục xử lý sự kiện ẢnhH histogram vào lọc ảnh khi click
        self.action_GAMMA.triggered.connect(self.action_gamma) # kết nối tới hàm action_histogram

        # Mục giúp đỡ
        self.action_about = QAction('Về Chúng Tôi', self) # Khi có sự kiện vào Về Chúng Tôi
        self.action_about.triggered.connect(self.open_about_window) # kết nối tới hàm open_about_window
        self.menu_help.addAction(self.action_about) #  Thêm mục xử lý sự kiện Về Chúng Tôi vào Giúp đỡ 

    def tools_bar(self):  # Hàm xử lý tool bar nằm dưới menu bar 
        
        # Triển khai từng button trong tool_bar
        # Vị trí đầu tiên là button ảnh icon_image_details.png
        self.button_image_details = QPushButton('', self) # Khi nhấn vào button ảnh icon_image_details.png
        self.button_image_details.move(10, 33)  # Vị trí của hộp ảnh button icon_image_details.png
        self.button_image_details.resize(55, 55) # Kích thước hộp ảnh button icon_image_details.png
        self.button_image_details.setIcon(QIcon(r'pic\icon\icon_image_details.png')) # Đường dẫn của ảnh icon_image_details.png
        self.button_image_details.setIconSize(QSize(45, 45)) ## Kích thước icon ảnh icon_image_details.png
        self.button_image_details.setToolTip('Ảnh mắc định') #  Title của hộp dialog window icon_image_details
        self.button_image_details.clicked.connect(self.show_image_details) # Kết nối tới hàm show_image_details

        # Vị trí thứ 2 là button icon_rotate.png
        self.button_rotate = QPushButton('', self) # Khi nhấn vào button ảnh icon_rotate.png
        self.button_rotate.move(75, 33)  # Vị trí của hộp ảnh button image rotate
        self.button_rotate.resize(55, 55) # Kích thước hộp ảnh button icon_rotate.png
        self.button_rotate.setIcon(QIcon(r'pic\icon\icon_rotate.png')) # # Đường dẫn của ảnh icon_rotate.png
        self.button_rotate.setIconSize(QSize(45, 45)) ##ích thước icon ảnh  icon_rotate.png
        self.rotate = QMenu(self)   # Tạo một modal khi nhấn vào ảnh  icon_rotate.png

        self.rtt_right = QAction('Quay Phải 90°', self) # Khi có sự kiện nhấn vào Quay Phải 90°
        self.rtt_right.triggered.connect(self.rotate_right) # Kết nối tới rotate_right
        self.rtt_right.setShortcut('R') # Hoặc nhấn chữ R để quay sang phải
        self.rotate.addAction(self.rtt_right) # Thêm sự kiện quay sang phải vào ảnh icon_rotate.png
        self.rotate.addSeparator() # Thêm chữ Quay sang phải 90 độ vào ảnh icon_rotate.png

        self.rtt_left = QAction('Quay Trái 90°', self) # Khi có sự kiện nhấn vào Quay Trái 90°
        self.rtt_left.triggered.connect(self.rotate_left) #  # Kết nối tới rotate_left
        self.rtt_left.setShortcut('shift+R') # Hoặc nhấn vào shift+R
        self.rotate.addAction(self.rtt_left) # Thêm sự kiện Quay sang trái vài ảnh icon_rotate.png
        self.button_rotate.setMenu(self.rotate) # Tạo một modal khi click vào button ảnh icon_rotate.png

        # Vị trí thứ 3 là button icon_flip.png
        self.button_flip = QPushButton('', self) # Khi nhấn vào button ảnh icon_flip.png
        self.button_flip.move(140, 33) # Vị trí của hộp ảnh button icon_flip.png
        self.button_flip.resize(55, 55) # Kích thước của hộp button icon_flip.png
        self.button_flip.setIcon(QIcon(r'pic\icon\icon_flip.png')) # Đường dẫn ảnh icon_flip.png
        self.button_flip.setIconSize(QSize(45, 45)) # Kích thước ảnh icon_flip.png
        self.flip = QMenu(self) # Tạo một modal khi nhấn vào ảnh icon_flip.png

        self.flip_v = QAction('Lật dọc', self) # Khi có sự kiện vào chữ Lật dọc
        self.flip_v.triggered.connect(self.flip_image_vertical) # Kết nối tớ hàm flip_image_vertical
        self.flip_v.setShortcut('F') # Hoặc khi nhấn F
        self.flip.addAction(self.flip_v) #Thêm sự kiện lật dọc vào ảnh icon_flip.png
        self.flip.addSeparator() # Thêm chữ Lật dọc vào ảnh khi nhấn vào ảnh icon_flip.png khi 

        self.flip_h = QAction('Lật ngang', self) # Khi có sự kiện vào chữ Lật ngang
        self.flip_h.triggered.connect(self.flip_image_horizontal)  # Kết nối tớ hàm flip_image_horizontal
        self.flip.addAction(self.flip_h) # Thêm sự kiện lật ngang và ảnh icon_flip.png
        self.flip_h.setShortcut('shift+F') # Hoặc khi nhấn shift+F
        self.button_flip.setMenu(self.flip) # Tạo một hộp modal khi nhấn button ảnh  icon_flip.png

        # Vị trí thứ 4 là button icon_draw.png
        self.button_draw = QPushButton('', self) #  # Khi nhấn vào button ảnh icon_draw.png
        self.button_draw.move(205, 33) # Vị trí của hộp ảnh button icon_draw.png
        self.button_draw.resize(55, 55) # Kích thước hộp ảnh button icon_draw.png
        self.button_draw.setIcon(QIcon(r'pic\icon\icon_draw.png')) # đường đẫn ảnh icon_draw.png
        self.button_draw.setIconSize(QSize(45, 45))# Kích thước ảnh icon_draw.png

        self.shape = QMenu(self) # Tạo một modal khi nhấn vào button ảnh icon_draw.png
        self.rectangle_shape = QAction('Hình chữ nhật', self) # Khi nhấn vào Hình chữ nhật
        self.rectangle_shape.triggered.connect(self.draw_rectangle) # Kết nối tới draw_rectangle
        self.shape.addAction(self.rectangle_shape) #  # Thêm sự kiện vẽ Hình chữ nhật vào ảnh icon_draw.png

        self.ellipse_shape = QAction('Ellipse', self)  # Khi nhấn  Hình Ellipse
        self.ellipse_shape.triggered.connect(self.draw_ellipse) # Kết nối tới hàm draw_ellipse
        self.shape.addAction(self.ellipse_shape)  # Thêm sự kiện vẽ Ellipse vào ảnh icon_draw.png

        self.triangle_shape = QAction('Tam giác', self) # Khi nhấn  Hình tam giác
        self.triangle_shape.triggered.connect(self.draw_triangle) # # Kết nối tới hàm draw_triangle
        self.shape.addAction(self.triangle_shape)  # Thêm sự kiện vẽ tam giác vào ảnh icon_draw.png

        self.line_shape = QAction('Đường thẳng', self) # Khi nhấn vào đường thẳng
        self.line_shape.triggered.connect(self.draw_line)# # Kết nối tới hàm draw_line
        self.shape.addAction(self.line_shape) # Thêm sự kiện vẽ  đường thẳng vào ảnh icon_draw.png
        self.button_draw.setMenu(self.shape) # Tạo một hộp modal khi nhấn button ảnh   icon_draw.png

        self.button_text = QPushButton('', self) # Khi nhấn vào BUTTON ảnh icon_text.png
        self.button_text.move(270, 33) # Vị trí của hộp ảnh button icon_text.png
        self.button_text.resize(55, 55) # Kích thước hộp ảnh button icon_text.png
        self.button_text.setIcon(QIcon(r'pic\icon\icon_text.png')) #Đường dẫn icon_text.png
        self.button_text.setIconSize(QSize(45, 45)) # # Kích thước ảnh icon_text.png
        self.button_text.clicked.connect(self.putting_text) ## Kết nối tới hàm putting_text

        #  mục độ dày
        self.text_pixel = QLabel(self)
        self.text_pixel.setText('Độ dày:')
        self.text_pixel.move(402, 30)
        self.combo_box_pixel = QComboBox(self)
        self.combo_box_pixel.move(468, 33)
        self.combo_box_pixel.resize(55, 25)
        self.combo_box_pixel.addItem('1 px')
        self.combo_box_pixel.addItem('2 px')
        self.combo_box_pixel.addItem('3 px')
        self.combo_box_pixel.addItem('4 px')
        self.combo_box_pixel.addItem('5 px')
        self.combo_box_pixel.currentIndexChanged.connect(self.pixel_selection) # Kêt nối tới pixel_selection
        
        # Mục kiểu phông
        self.text_font_style = QLabel(self)
        self.text_font_style.setText('Kiểu phông: ')
        self.text_font_style.move(402, 59)
        self.combo_box_font = QComboBox(self)
        self.combo_box_font.move(468, 62)
        self.combo_box_font.resize(195, 25)
        self.combo_box_font.addItem('HERSHEY COMPLEX')
        self.combo_box_font.addItem('HERSHEY COMPLEX SMALL')
        self.combo_box_font.addItem('HERSHEY DUPLEX')
        self.combo_box_font.addItem('HERSHEY PLAIN')
        self.combo_box_font.addItem('HERSHEY SCRIPT COMPLEX')
        self.combo_box_font.addItem('HERSHEY SCRIPT SIMPLEX')
        self.combo_box_font.addItem('HERSHEY SIMPLEX')
        self.combo_box_font.addItem('HERSHEY TRIPLEX')
        self.combo_box_font.addItem('ITALIC')
        self.combo_box_font.currentIndexChanged.connect(self.font_style_selection) # Kêt nối tới font_style_selection
        
        # Mục cỡ chữ
        self.text_font_scale = QLabel(self)
        self.text_font_scale.setText('Cỡ chữ')
        self.text_font_scale.move(533, 30)
        self.combo_box_font_size = QComboBox(self)
        self.combo_box_font_size.move(603, 33)
        self.combo_box_font_size.resize(60, 25)
        self.combo_box_font_size.addItem('1')
        self.combo_box_font_size.addItem('2')
        self.combo_box_font_size.addItem('3')
        self.combo_box_font_size.currentIndexChanged.connect(self.font_scale_selection) #Kêt nối tới Hàm font_scale_selection

        self.button_reset = QPushButton('', self) 
        self.button_reset.move(1135, 33)
        self.button_reset.resize(55, 55)
        self.button_reset.setIcon(QIcon(r'pic\icon\icon_reset.png'))
        self.button_reset.setIconSize(QSize(45, 45))
        self.button_reset.setToolTip('Reset')
        self.button_reset.clicked.connect(self.load_original_image) ##Kêt nối tới Hàm load_original_image

    def background_image_backup(self): # Hàm về background cho ảnh backup
        self.label.setGeometry(10,110,550,550)
        self.label.setStyleSheet("background: #5e6e7f;border-radius:8px;opacity:0;")

        self.word_backup = QLabel(self)
        self.word_backup.setText("Vùng Ảnh Chỉnh Sửa")
        self.word_backup.resize(250,100)
        self.word_backup.move(200, 650)
        self.word_backup.setStyleSheet("font-weight: 700; font-size:20px;")

    def background_image_origin(self): # # Hàm về background cho ảnh orgin
        self.word_origin = QLabel(self)
        self.label_origin.setGeometry(640,110,550,550)
        self.label_origin.setStyleSheet("background: #5e6e7f;border-radius:8px;opacity:0;")
        self.word_origin.setText("Vùng Ảnh Gốc")
        self.word_origin.resize(250,100)
        self.word_origin.move(850, 650)
        self.word_origin.setStyleSheet("font-weight: 700; font-size:20px;")
        
    # ********************   menu bar operations   ********************************************************************
    def browse_image(self): # Hàm xử lý mở tập tin
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Image Files (*.png *.jpg *.jpeg)')
        if self.filename:
            self.load_original_image()
        self.converted = False

    def save_image(self): # Hàm xử lý lưu ảnh đầu ra
        self.image = self.backup_img
        self.filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if self.filePath:
            cv2.imwrite(self.filePath, self.image)

    def zoom_in(self): # Hàm xử lý phóng to ảnh
        self.zoom += 0.2
        self.print_image(self.image)

    def zoom_out(self): # Hàm xử lý thu nhỏ ảnh
        self.zoom -= 0.2
        self.print_image(self.image)

    def convert_to_original(self): # Hàm xử lý khi nhấn vào original
        self.print_image(self.image)
        cv2.imwrite('backup_img.jpg', self.image)
        self.converted = False

    def convert_to_gray(self): # Hàm xử lý khi nhấn vào gray
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_hsv(self): ##Hàm xử lý khi nhấn vào hsv
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.print_image(self.hsv)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.hsv)

    def convert_to_hls(self): # Hàm xử lý khi nhấn vào hls
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_lab(self): # Hàm xử lý khi nhấn vào Lab
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_luv(self): # Hàm xử lý khi nhấ vào luv
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LUV)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_yuv(self):# Hàm xử lý khi nhấ vào yuv
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_blur(self): # Hàm xử lý khi nhấn vào mục làm mờ
        self.backup_img = cv2.blur(self.image, (5, 5))
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_box(self): ## Hàm xử lý khi nhấn vào mục lọc ảnh
        self.backup_img = cv2.boxFilter(self.image, -1,(20,20))
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_median(self): # Hàm xử lý lọc trung vị
        self.backup_img = cv2.medianBlur(self.image,5)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_bilateral(self): # Hàm xử lý lọc 2 chiều
        self.backup_img = cv2.bilateralFilter(self.image,9,75,75)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_gauss(self): #Hàm xử lý lọc gauss
        self.backup_img = cv2.GaussianBlur(self.image,(5,5),0)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_threshold(self): #Hàm xử lý lọc ngưỡng trung bình
        grayscaled = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.backup_img = cv2.medianBlur(self.image,5)
        retval, threshold = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.backup_img = threshold
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_directional(self): # Hàm xử lý lọc định hướng
        kernel = np.ones((3, 3), np.float32) / 9
        self.backup_img = cv2.filter2D(self.image, -1, kernel)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_directional_2(self): # Hàm xử lý lọc định hướng 2
        kernel = np.ones((5, 5), np.float32) / 9
        self.backup_img = cv2.filter2D(self.image, -1, kernel)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_directional_3(self): # Hàm xử lý lọc định hướng 3
        kernel = np.ones((7, 7), np.float32) / 9
        self.backup_img = cv2.filter2D(self.image, -1, kernel)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_grays(self): # Hàm xử lý ảnh xám
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_negative(self): # Hàm xử lý ảnh âm bản
        self.backup_img = ~self.image #(self.image, cv2.COLOR_BGR2GRAY)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def action_log(self): # Hàm xử lý ảnh log
        img_2 = np.uint8(np.log(self.image))
        c = 2
        self.backup_img = cv2.threshold(img_2, c, 225, cv2.THRESH_BINARY)[1]
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)    

    def action_histogram(self): # Hàm xử lý ảnh histogram
        img_yuv = cv2.cvtColor(self.image, cv2.COLOR_RGB2YUV)
        #cân bằng biểu đồ trên kênh  U
        img_yuv[:, 2:, 0] = cv2.equalizeHist(img_yuv[:, 2 :, 0])
        #chuyển đổi hình ảnh YUV trở lại định dạng RGB
        self.backup_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img) 
    
    def action_gamma(self): # Hàm xử lý ảnh gamma
        gamma = 1.5
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

        self.backup_img = cv2.LUT(self.image, table)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img) 
    def open_about_window(self): # Hàm xử lý khi nhấn vào về chúng tôi
        self.about_window.show()

    # ********************   tool bar operations   ********************************************************************
    def show_image_details(self): # Hàm xử lý của xuất hiện hộp thoại khi nhấn vào ảnh icon_image_details.png
        QMessageBox.information(self, 'Thông tin ảnh', "Width : {} px".format(self.image.shape[1]) +
                                "\nHeight : {} px".format(self.image.shape[0]), QMessageBox.Ok)

    def rotate_right(self): # Hàm xử lý quay sang phải 90 độ
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.backup_img = cv2.rotate(self.backup_img, cv2.ROTATE_90_CLOCKWISE)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def rotate_left(self): # Hàm xử lý quay sang trái 90 độ
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.backup_img = cv2.rotate(self.backup_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def flip_image_vertical(self): # Hàm xử lý ảnh lật dọc
        self.image = cv2.flip(self.image, 0)
        self.backup_img = cv2.flip(self.backup_img, 0)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def flip_image_horizontal(self): # Hàm xử lý ảnh ngang
        self.image = cv2.flip(self.image, 1)
        self.backup_img = cv2.flip(self.backup_img, 1)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def draw_rectangle(self): # Hàm xử lý vẽ hình chữ nhật 
        self.draw_rect = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_ellipse(self): # Hàm xử lý hàm elip
        self.draw_elli = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_triangle(self): # Hàm xử lý vẽ hình tam giác
        self.draw_tri = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_line(self): # Hàm xử lý vẽ đường thẳng
        self.draw_l = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def putting_text(self): #Hàm xử lý viết chữ
        self.put_t = True
        QLabel.setCursor(self, Qt.IBeamCursor)

    def font_scale_selection(self, index): # Hàm xử lý cỡ chữ
        if index == 0:
            self.font_scale = 1
        if index == 1:
            self.font_scale = 2
        if index == 2:
            self.font_scale = 3

    def pixel_selection(self, index): # Hàm xử lý khi chọn độ dày
        if index == 0:
            self.pixel = 1
        if index == 1:
            self.pixel = 2
        if index == 2:
            self.pixel = 3
        if index == 3:
            self.pixel = 4
        if index == 4:
            self.pixel = 5

    def font_style_selection(self, index): # Hàm xử lý khi chọn font chữ
        if index == 0:
            self.font_style = cv2.FONT_HERSHEY_COMPLEX
        if index == 1:
            self.font_style = cv2.FONT_HERSHEY_COMPLEX_SMALL
        if index == 2:
            self.font_style = cv2.FONT_HERSHEY_DUPLEX
        if index == 3:
            self.font_style = cv2.FONT_HERSHEY_PLAIN
        if index == 4:
            self.font_style = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        if index == 5:
            self.font_style = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        if index == 6:
            self.font_style = cv2.FONT_HERSHEY_SIMPLEX
        if index == 7:
            self.font_style = cv2.FONT_HERSHEY_TRIPLEX
        if index == 7:
            self.font_style = cv2.FONT_ITALIC

    def load_original_image(self): # Hàm xử lý trả lại ảnh gốc
        self.image = cv2.imread(self.filename, 1)
        self.image = cv2.resize(self.image, (550, 550))  # Hàm xử lý kích thước ảnh gốc
        self.print_image(self.image)
        self.print_image_origin(self.image)
        cv2.imwrite('backup_img.jpg', self.image)
        self.backup_image()

    # ********************   print image   ****************************************************************************
    def print_image(self, image): # Hàm xử lý hiển thị ra ảnh chỉnh sửa khi open
        self.enable_action()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        self.qformat = QImage.Format_ARGB32
        self.img = QImage(image.data, int(image.shape[1]), int(image.shape[0]), int(self.qformat))
        self.label.setPixmap((QPixmap.scaled(QPixmap.fromImage(self.img), int(image.shape[1] * self.zoom),
                                             int(image.shape[0] * self.zoom), Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)))
        self.label.setGeometry(10, 110,550, 550) # set anh setGeometry x y width height
        self.label.setStyleSheet("background:#000;border-radius:8px;padding:50px 0")  

    def print_image_origin(self,image):
        self.label_origin.setPixmap((QPixmap.scaled(QPixmap.fromImage(self.img), int(image.shape[1] * self.zoom),
                                             int(image.shape[0] * self.zoom), Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)))
        self.label_origin.setGeometry(640, 110,550, 550) # set anh setGeometry x y width height
        self.label_origin.setStyleSheet("background:#000;border-radius:8px;padding:50px 0")  

    # ********************   mouse control   *************************************************************************
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.crop or self.draw_rect or self.draw_elli or self.draw_tri or self.draw_l:
                self.flag = True
                self.x0 = event.x()
                self.y0 = event.y()
            elif self.put_t:
                self.x0 = event.x()
                self.y0 = event.y()
                self.open_text_box()
                QLabel.setCursor(self, Qt.CustomCursor)
            elif 679 < event.x() < 699 and 36 < event.y() < 56:
                self.color = (0, 0, 0)
                self.select_color_x = 675
                self.select_color_y = 32
                self.update()
            elif 708 < event.x() < 728 and 36 < event.y() < 56:
                self.color = (128, 128, 128)
                self.select_color_x = 704
                self.select_color_y = 32
                self.update()
            elif 737 < event.x() < 757 and 36 < event.y() < 56:
                self.color = (0, 0, 128)
                self.select_color_x = 733
                self.select_color_y = 32
                self.update()
            elif 766 < event.x() < 786 and 36 < event.y() < 56:
                self.color = (0, 128, 128)
                self.select_color_x = 762
                self.select_color_y = 32
                self.update()
            elif 795 < event.x() < 815 and 36 < event.y() < 56:
                self.color = (0, 128, 0)
                self.select_color_x = 791
                self.select_color_y = 32
                self.update()
            elif 824 < event.x() < 844 and 36 < event.y() < 56:
                self.color = (128, 128, 0)
                self.select_color_x = 820
                self.select_color_y = 32
                self.update()
            elif 853 < event.x() < 873 and 36 < event.y() < 56:
                self.color = (128, 0, 0)
                self.select_color_x = 849
                self.select_color_y = 32
                self.update()
            elif 882 < event.x() < 902 and 36 < event.y() < 56:
                self.color = (128, 0, 128)
                self.select_color_x = 878
                self.select_color_y = 32
                self.update()

            elif 679 < event.x() < 699 and 64 < event.y() < 84:
                self.color = (255, 255, 255)
                self.select_color_x = 675
                self.select_color_y = 60
                self.update()
            elif 708 < event.x() < 728 and 64 < event.y() < 84:
                self.color = (192, 192, 192)
                self.select_color_x = 704
                self.select_color_y = 60
                self.update()
            elif 737 < event.x() < 757 and 64 < event.y() < 84:
                self.color = (0, 0, 255)
                self.select_color_x = 733
                self.select_color_y = 60
                self.update()
            elif 766 < event.x() < 786 and 64 < event.y() < 84:
                self.color = (0, 255, 255)
                self.select_color_x = 762
                self.select_color_y = 60
                self.update()
            elif 795 < event.x() < 815 and 64 < event.y() < 84:
                self.color = (0, 255, 0)
                self.select_color_x = 791
                self.select_color_y = 60
                self.update()
            elif 824 < event.x() < 844 and 64 < event.y() < 84:
                self.color = (255, 255, 0)
                self.select_color_x = 820
                self.select_color_y = 60
                self.update()
            elif 853 < event.x() < 873 and 64 < event.y() < 84:
                self.color = (255, 0, 0)
                self.select_color_x = 849
                self.select_color_y = 60
                self.update()
            elif 882 < event.x() < 902 and 64 < event.y() < 84:
                self.color = (255, 0, 255)
                self.select_color_x = 878
                self.select_color_y = 60
                self.update()

        elif event.buttons() == Qt.RightButton:
            if self.crop or self.draw_rect or self.draw_elli or self.draw_tri or self.draw_l or self.put_t:
                self.crop = False
                self.draw_rect = False
                self.draw_elli = False
                self.draw_tri = False
                self.draw_l = False
                self.put_t = False
                QLabel.setCursor(self, Qt.CustomCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.flag:
                self.x1 = event.x()
                self.y1 = event.y()
                self.update()
                instant_img = cv2.imread('backup_img.jpg')
                if self.crop:
                    cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110),
                                  (self.x1 - 11, self.y1 - 110), (0, 0, 255), 2)
                elif self.draw_rect:
                    cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110),
                                  (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
                elif self.draw_elli:
                    cv2.ellipse(instant_img, (int(((self.x0-11)+(self.x1-11))/2), int(((self.y0-110)+(self.y1-110)/2))),
                                (int(((self.x1-11) - (self.x0-11))/2), int(((self.y1-110) - (self.y0-110))/2)),
                                1, 0, 360, self.color, self.pixel)
                elif self.draw_tri:
                    cv2.line(instant_img, ((int(((self.x0-11)+(self.x1-11))/2)), self.y0-110),
                             (self.x0-11, self.y1-110), self.color, self.pixel)
                    cv2.line(instant_img, (self.x0-11, self.y1-110), (self.x1-11, self.y1-110), self.color, self.pixel)
                    cv2.line(instant_img, (self.x1-11, self.y1-110),
                             ((int(((self.x0-11)+(self.x1-11))/2)), self.y0-110), self.color, self.pixel)
                elif self.draw_l:
                    cv2.line(instant_img, (self.x0-11, self.y0-110), (self.x1-11, self.y1-110), self.color, self.pixel)
                self.print_image(instant_img)

    def mouseReleaseEvent(self, event):
        if self.crop:
            self.flag = False
            instant_img = cv2.imread('backup_img.jpg')
            cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          (0, 0, 255), 2)
            self.print_image(instant_img)
        elif self.draw_rect:
            self.flag = False
            cv2.rectangle(self.backup_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          self.color, self.pixel)
            cv2.rectangle(self.image, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_rect = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_elli:
            self.flag = False
            cv2.ellipse(self.backup_img,
                        (int(((self.x0 - 11) + (self.x1 - 11)) / 2), int(((self.y0 - 110) + (self.y1 - 110) / 2))),
                        (int(((self.x1 - 11) - (self.x0 - 11)) / 2), int(((self.y1 - 110) - (self.y0 - 110)) / 2)),
                        1, 0, 360, self.color, self.pixel)
            cv2.ellipse(self.image,
                        (int(((self.x0 - 11) + (self.x1 - 11)) / 2), int(((self.y0 - 110) + (self.y1 - 110) / 2))),
                        (int(((self.x1 - 11) - (self.x0 - 11)) / 2), int(((self.y1 - 110) - (self.y0 - 110)) / 2)),
                        1, 0, 360, self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_elli = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_tri:
            self.flag = False
            cv2.line(self.backup_img, ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110),
                     (self.x0 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.backup_img, (self.x0 - 11, self.y1 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.backup_img, (self.x1 - 11, self.y1 - 110),
                     ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110), self.color, self.pixel)
            cv2.line(self.image, ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110),
                     (self.x0 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.image, (self.x0 - 11, self.y1 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.image, (self.x1 - 11, self.y1 - 110),
                     ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110), self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_tri = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_l:
            self.flag = False
            cv2.line(self.backup_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                     self.color, self.pixel)
            cv2.line(self.image, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_l = False
            QLabel.setCursor(self, Qt.CustomCursor)

    # ********************   text box dialog   ************************************************************************
    def open_text_box(self):
        self.dialog = QDialog(self)
        self.form_group_box = QGroupBox('Insert Text')
        self.text_box = QLineEdit(self)

        layout = QFormLayout()
        layout.addRow(QLabel("Text:"), self.text_box)
        self.form_group_box.setLayout(layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.close_text_box1)
        button_box.rejected.connect(self.close_text_box2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)

        self.dialog.setLayout(main_layout)
        self.dialog.setWindowTitle('Text Box')
        self.dialog.show()

    def close_text_box1(self):
        self.put_t = False
        self.dialog.close()
        cv2.putText(self.image, self.text_box.text(), (self.x0 - 11, self.y0 - 100), self.font_style,
                    self.font_scale, self.color, self.pixel)
        cv2.putText(self.backup_img, self.text_box.text(), (self.x0 - 11, self.y0 - 100), self.font_style,
                    self.font_scale, self.color, self.pixel)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def close_text_box2(self):
        self.put_t = False
        self.dialog.close()

    # ********************   set cursor   *****************************************************************************
    def cursor_shape(self):
        if self.crop:
            QLabel.setCursor(self, Qt.CrossCursor)
        else:
            QLabel.setCursor(self, Qt.CustomCursor)

    # *****************************************************************************************************************
    def backup_image(self): # hàm xử lý khi đã lưu ảnh
        self.backup_img = cv2.imread('backup_img.jpg', 1)

    def paintEvent(self, event): # Hàm xử lý body
        tool_bar_rect = QPainter(self)
        tool_bar_rect.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        tool_bar_rect.drawRect(-1, 0, 1201, 97)

        black_rect = QPainter(self)
        black_rect.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        black_rect.drawRect(679, 36, 20, 20)
        dark_gray_rect = QPainter(self)
        dark_gray_rect.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        dark_gray_rect.drawRect(708, 36, 20, 20)
        dark_red_rect = QPainter(self)
        dark_red_rect.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))
        dark_red_rect.drawRect(737, 35, 21, 21)
        dark_yellow_rect = QPainter(self)
        dark_yellow_rect.setBrush(QBrush(Qt.darkYellow, Qt.SolidPattern))
        dark_yellow_rect.drawRect(766, 35, 21, 21)
        dark_green_rect = QPainter(self)
        dark_green_rect.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
        dark_green_rect.drawRect(795, 35, 21, 21)
        dark_cyan_rect = QPainter(self)
        dark_cyan_rect.setBrush(QBrush(Qt.darkCyan, Qt.SolidPattern))
        dark_cyan_rect.drawRect(824, 35, 21, 21)
        dark_blue_rect = QPainter(self)
        dark_blue_rect.setBrush(QBrush(Qt.darkBlue, Qt.SolidPattern))
        dark_blue_rect.drawRect(853, 35, 21, 21)
        dark_magenta_rect = QPainter(self)
        dark_magenta_rect.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
        dark_magenta_rect.drawRect(882, 35, 21, 21)

        white_rect = QPainter(self)
        white_rect.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        white_rect.drawRect(679, 64, 20, 20)
        light_gray_rect = QPainter(self)
        light_gray_rect.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))
        light_gray_rect.drawRect(708, 64, 20, 20)
        red_rect = QPainter(self)
        red_rect.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        red_rect.drawRect(737, 64, 21, 21)
        yellow_rect = QPainter(self)
        yellow_rect.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        yellow_rect.drawRect(766, 64, 21, 21)
        green_rect = QPainter(self)
        green_rect.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        green_rect.drawRect(795, 64, 21, 21)
        cyan_rect = QPainter(self)
        cyan_rect.setBrush(QBrush(Qt.cyan, Qt.SolidPattern))
        cyan_rect.drawRect(824, 64, 21, 21)
        blue_rect = QPainter(self)
        blue_rect.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        blue_rect.drawRect(853, 64, 21, 21)
        magenta_rect = QPainter(self)
        magenta_rect.setBrush(QBrush(Qt.magenta, Qt.SolidPattern))
        magenta_rect.drawRect(882, 64, 21, 21)

        select_rect = QPainter(self)
        select_rect.drawRect(self.select_color_x, self.select_color_y, 28, 28)

    def reset_crop_label(self): 
        self.x0 = 0
        self.x1 = 0
        self.y0 = 0
        self.y1 = 0

    def disable_action(self): # Xử lý vô hiệu hóa các sự kiện khi chưa có ảnh
        self.disabled_list = [self.action_save,
                              self.action_zoom_in, self.action_zoom_out,
                              self.action_convert_to,
                              self.action_BLUR,self.action_BOX,self.action_MEDIAN,self.action_BILATERAL,self.action_GAUSS,
                              self.action_THRESHOLD,self.action_DIRECTIONAL,self.action_DIRECTIONAL_2,self.action_DIRECTIONAL_3,
                              self.action_GRAY,self.action_NEGATIVE,self.action_LOG,self.action_HISTOGRAM,self.action_GAMMA,
                              self.action_original, self.button_image_details,
                              self.button_rotate, self.button_flip, self.button_draw,
                              self.button_text, self.button_reset]
        for i in range(len(self.disabled_list)):
            self.disabled_list[i].setDisabled(True)

    def enable_action(self): # Hàm xử lý kích hoạt sự kiện khi có ảnh
        for i in range(len(self.disabled_list)):
            self.disabled_list[i].setDisabled(False)


class AboutWindow(QWidget): ## Lớp "VỀ Chúng Tôi"
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.title = 'Thông tin về chúng tôi'
        self.x_pos = 650    # Vị trí theo trục x của modal về chúng tôi
        self.y_pos = 300     # Vị trí theo trục y của modal về chúng tôi
        self.width = 600 # Width bảng modal về chúng tôi
        self.height = 200    # Height bảng modal về chúng tôi
        self.ui_components()

    def ui_components(self):
        self.setGeometry(self.x_pos, self.y_pos, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        ## Thông tin bảng khi click vào modal về chúng tôi
        self.label_message01 = QLabel("Người hướng dẫn:", self)
        self.label_message01.move(20, 20)
        self.label_message01.setFont(QFont('Arial', 13))
        self.label_message02 = QLabel("Sinh viên thực hiện:", self)
        self.label_message02.move(20, 50)
        self.label_message02.setFont(QFont('Arial', 13))
        self.label_message03 = QLabel("Lớp:", self)
        self.label_message03.move(20, 110)
        self.label_message03.setFont(QFont('Arial', 13))
        self.label_message04 = QLabel("TS. Phạm Nguyễn Minh Nhựt", self)
        self.label_message04.move(220, 20)
        self.label_message04.setFont(QFont('Arial', 13))
        self.label_message05 = QLabel("Nguyễn Đức Huy", self)
        self.label_message05.move(220, 50)
        self.label_message05.setFont(QFont('Arial', 13))
        self.label_message06 = QLabel("Trần Thị Thu Phương", self)
        self.label_message06.move(220, 80)
        self.label_message06.setFont(QFont('Arial', 13))
        self.label_message07 = QLabel("19IT6", self)
        self.label_message07.move(220, 110)
        self.label_message07.setFont(QFont('Arial', 13))

        self.button = QPushButton('OK', self) 
        self.button.move(485, 405)
        self.button.clicked.connect(self.close_win) # Kết nối tới hàm đóng cửa sổ window

    def close_win(self): # Hàm đóng của sổ window
        self.close()

    @staticmethod
    def draw_line(qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(42, 180, 558, 180)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
