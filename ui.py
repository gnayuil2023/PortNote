from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog
from PySide6.QtGui import QAction
from functools import partial
from help_dialog import showHelp
from image_processor import ImageProcessor

class ImageSaverApp(QMainWindow):
    MAX_SIZE = (800, 600)  # 定义窗口最大尺寸

    def __init__(self):
        super().__init__()
        self.initUI()  # 初始化UI

    def initUI(self):
        self.setWindowTitle('Image Saver')  # 设置窗口标题
        self.setGeometry(100, 100, 400, 300)  # 设置窗口初始位置和大小
        self.setMaximumSize(*self.MAX_SIZE)  # 设置窗口最大尺寸

        # 创建菜单栏和帮助菜单
        menubar = self.menuBar()
        helpMenu = menubar.addMenu('帮助')
        helpAction = QAction('关于', self)
        helpAction.triggered.connect(self.showHelp)  # 绑定帮助菜单的动作
        helpMenu.addAction(helpAction)

        # 设置中央窗口部件和布局
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QGridLayout(centralWidget)  # 使用网格布局

        self.idCardButtons = []  # 存储按钮的列表
        buttonNames = [f'按钮{str(i).zfill(2)}' for i in range(1, 10)]  # 创建按钮名称列表
        positions = [(i, j) for i in range(3) for j in range(3)]  # 九宫格布局位置

        # 创建按钮并绑定事件
        for position, name in zip(positions, buttonNames):
            button = QPushButton(name)
            # 绑定按钮点击事件，使用 partial 传递参数
            button.clicked.connect(partial(self.loadOrUploadIdCardImage, name))
            layout.addWidget(button, *position)
            self.idCardButtons.append(button)

        self.imageProcessor = ImageProcessor()  # 创建 ImageProcessor 对象
        self.checkIdCardImages()  # 检查图片是否存在

    def get_image_path(self, image_name):
        # 获取图片路径
        return self.imageProcessor.get_image_path(image_name)

    def checkIdCardImages(self):
        # 检查并更新按钮状态
        for button in self.idCardButtons:
            imagePath = self.get_image_path(button.text())
            button.setEnabled(True)  # 默认启用按钮
            # 根据图片是否存在更新按钮状态
            if not self.imageProcessor.image_exists(imagePath):
                button.setEnabled(True)  # 即使图片不存在，也允许用户点击按钮进行上传

    def loadOrUploadIdCardImage(self, buttonName):
        # 加载或上传身份证图片
        idCardImagePath = self.get_image_path(buttonName)
        if self.imageProcessor.image_exists(idCardImagePath):
            self.showImageInNewWindow(idCardImagePath)  # 显示已存在的图片
        else:
            # 弹出文件对话框上传图片
            fileName, _ = QFileDialog.getOpenFileName(self, '选择图片', '', '图片文件 (*.png *.jpg *.bmp)')
            if fileName:
                # 将上传的图片保存到指定路径
                self.imageProcessor.save_uploaded_image(idCardImagePath, fileName)
                self.showImageInNewWindow(idCardImagePath)  # 显示新保存的图片

    def showImageInNewWindow(self, imagePath):
        # 在新窗口中显示图片
        self.imageWindow = QMainWindow()
        self.imageWindow.setWindowTitle('Image Preview')
        label = QLabel(self.imageWindow)
        pixmap = self.imageProcessor.load_pixmap(imagePath)  # 加载图片
        label.setPixmap(pixmap)
        self.imageWindow.setCentralWidget(label)
        self.imageWindow.resize(pixmap.width(), pixmap.height())  # 根据图片大小调整窗口尺寸
        self.imageWindow.show()

    def showHelp(self):
        # 显示帮助信息
        showHelp(self)
