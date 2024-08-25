import sys
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget, QVBoxLayout, QDialog
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口标题和默认大小
        self.setWindowTitle("PySide6 示例")
        self.setFixedSize(1024, 768)  # 设置固定大小为 1024x768

        # 设置背景图片
        self.set_background_image("beijing")  # 确保图片路径和扩展名正确

        # 创建菜单栏
        menubar = self.menuBar()
        self.set_menu_bar_style(menubar)

        # 创建"帮助"菜单并添加"关于"选项
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        # 创建"设置"菜单
        settings_menu = menubar.addMenu("设置")
        self.toggle_move_action = QAction("启用按钮移动", self)
        self.toggle_move_action.setCheckable(True)
        self.toggle_move_action.setChecked(True)  # 默认启用按钮移动
        self.toggle_move_action.triggered.connect(self.toggle_button_movement)
        settings_menu.addAction(self.toggle_move_action)

        # 创建主内容区域
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建按钮
        self.create_buttons_from_file("anniu.txt")

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

    def set_menu_bar_style(self, menubar):
        # 使用样式表为菜单栏设置背景和边框
        menubar.setStyleSheet("""
            QMenuBar {
                background: rgba(0, 0, 0, 150);  # 半透明黑色背景
                color: white;  # 设置菜单栏文字颜色为白色
                border: 1px solid rgba(255, 255, 255, 100);  # 边框颜色和透明度
            }
            QMenuBar::item {
                background: rgba(100, 100, 100, 150);  # 半透明菜单项背景色
                padding: 5px;
                border-radius: 3px;
            }
            QMenuBar::item:selected {
                background: rgba(150, 150, 150, 200);  # 选中时的背景色
            }
            QMenu {
                background: rgba(0, 0, 0, 150);  # 半透明黑色背景
                color: white;  # 设置菜单文字颜色为白色
            }
            QMenu::item:selected {
                background: rgba(150, 150, 150, 200);  # 选中时的菜单项背景色
            }
        """)

    def create_buttons_from_file(self, file_path):
        # 从文件中读取按钮名称并创建按钮
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    button_name = line.strip()
                    if button_name:
                        button = DraggableButton(button_name, self)
                        button.move(50 + (i % 4) * 200, 100 + (i // 4) * 60)  # 设置按钮位置
                        self.layout.addWidget(button)
                        button.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", f"未找到文件 {file_path}。")

    def show_about_dialog(self):
        # 显示"关于"对话框
        QMessageBox.about(self, "关于", "这是一个使用 PySide6 创建的示例程序。")

    def toggle_button_movement(self):
        # 切换按钮移动开关
        enable_movement = self.toggle_move_action.isChecked()
        for button in self.findChildren(DraggableButton):
            button.set_movable(enable_movement)

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 50)  # 设置按钮大小
        self._startPos = None
        self.movable = True  # 按钮是否可移动的标志

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
        if self.movable and event.button() == Qt.LeftButton:
            self._startPos = None
        elif not self.movable:
            super().mouseReleaseEvent(event)  # 调用父类方法实现点击功能

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 打开新窗口
            new_window = SecondaryWindow()
            new_window.exec()  # 显示窗口为模态对话框

class SecondaryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("新窗口")
        self.setFixedSize(1024, 768)  # 设置固定大小为 1024x768

if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口对象
    main_window = MainWindow()
    main_window.show()

    # 进入应用程序主循环
    sys.exit(app.exec())
