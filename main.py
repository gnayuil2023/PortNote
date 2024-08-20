import sys
from PySide6.QtWidgets import QApplication
from ui import ImageSaverApp

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    imageSaverApp = ImageSaverApp()  # 创建 ImageSaverApp 对象
    imageSaverApp.show()  # 显示主窗口
    sys.exit(app.exec())  # 进入应用程序主循环
