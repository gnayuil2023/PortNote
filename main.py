import sys
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget, QVBoxLayout, QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QDialogButtonBox
import os

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(400, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 添加用户名标签和输入框
        self.username_label = QLabel("用户名:")
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # 添加按钮框
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # 从配置文件读取用户名
        self.load_username()

    def load_username(self):
        try:
            with open("config/user.txt", "r", encoding="utf-8") as file:
                username = file.read().strip()
                self.username_input.setText(username)
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", "未找到用户配置文件。")

    def get_username(self):
        return self.username_input.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口标题和默认大小
        self.setWindowTitle("Test")
        self.setFixedSize(1024, 768)  # 设置固定大小为 1024x768

        # 设置背景图片
        self.set_background_image("config/BackImage.jpeg")  # 确保图片路径和扩展名正确

        # 创建主内容区域
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 从config文件夹中读取按钮是否可移动的配置
        self.button_movable = self.read_button_movable("config/ButtonMove.txt")

        # 创建按钮
        self.create_buttons_from_file("config/ButtonName.txt")

    def set_background_image(self, image_file):
        # 使用样式表设置背景图片
        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({image_file});
                background-repeat: no-repeat;
                background-position: center;
            }}
            QWidget#centralwidget {{
                background: transparent;  # 确保内容区域背景透明
            }}
        """)

    def read_button_movable(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                value = file.read().strip()
                return value == '1'
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", f"未找到文件 {file_path}，默认设置为不可移动。")
            return False

    def create_buttons_from_file(self, file_path):
        # 从文件中读取按钮名称并创建按钮
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    button_name = line.strip()
                    if button_name:
                        button = DraggableButton(button_name, self)
                        button.set_movable(self.button_movable)
                        button.move(50 + (i % 4) * 200, 100 + (i // 4) * 60)  # 设置按钮位置
                        self.layout.addWidget(button)
                        button.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", f"未找到文件 {file_path}。")

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 50)  # 设置按钮大小
        self._startPos = None
        self.movable = True  # 按钮是否可移动的标志
        self.text = text

    def set_movable(self, movable):
        self.movable = movable

    def mousePressEvent(self, event):
        if self.movable and event.button() == Qt.LeftButton:
            self._startPos = event.position()  # 使用 position() 代替 pos()
        elif not self.movable:
            super().mousePressEvent(event)  # 调用父类方法实现点击功能

    def mouseMoveEvent(self, event):
        if self.movable and event.buttons() == Qt.LeftButton and self._startPos is not None:
            # 计算移动的偏移量并更新按钮位置
            offset = event.position() - self._startPos
            new_pos = self.mapToParent(QPointF(offset))
            self.move(new_pos.toPoint())  # 将 QPointF 转换为 QPoint 进行移动

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.movable:
                self._startPos = None
            else:
                # 打开新窗口
                new_window = SecondaryWindow(self.text)
                new_window.exec()  # 显示窗口为模态对话框

class SecondaryWindow(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)  # 使用按钮的名称作为窗口标题
        self.setFixedSize(1024, 768)  # 设置固定大小为 1024x768

if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 显示登录对话框
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted:
        # 创建主窗口对象
        main_window = MainWindow()
        main_window.show()

        # 进入应用程序主循环
        sys.exit(app.exec())
