import os
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor
from PySide6.QtWidgets import QFileDialog
from datetime import datetime

class ImageProcessor:
    IMAGES_DIR = 'images'  # 定义图片存储目录

    def get_image_path(self, image_name):
        # 获取图片路径
        program_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(program_dir, self.IMAGES_DIR)
        return os.path.join(images_dir, f'{image_name}.png')

    def image_exists(self, image_path):
        # 检查图片是否存在
        return os.path.exists(image_path)

    def load_pixmap(self, image_path):
        # 加载图片为 QPixmap 对象
        return QPixmap(image_path)

    def save_uploaded_image(self, image_path, fileName):
        # 保存上传的图片到指定路径
        pixmap = QPixmap(fileName)  # 加载选择的图片
        self.addWatermark(pixmap)  # 添加水印
        self.save_pixmap(image_path, pixmap)  # 保存图片

    def save_pixmap(self, image_path, pixmap):
        # 保存图片到指定路径
        images_dir = os.path.dirname(image_path)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)  # 创建目录
        if not pixmap.save(image_path):
            print(f"图片保存失败：{image_path}")

    def addWatermark(self, pixmap):
        # 添加水印
        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 20))
        inverted_color = self.calculateInvertedColor(pixmap)  # 计算反色
        painter.setPen(inverted_color)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        painter.drawText(10, 30, timestamp)  # 在图片上绘制时间戳
        painter.end()

    def calculateInvertedColor(self, pixmap):
        # 计算图片左上角像素的反色
        background_color = pixmap.toImage().pixelColor(0, 0)
        return QColor(255 - background_color.red(), 255 - background_color.green(), 255 - background_color.blue())
