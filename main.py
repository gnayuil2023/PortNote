import sys
import os
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PySide6.QtGui import QPixmap

class ImageUploaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ensure_images_directory()

    def initUI(self):
        self.setWindowTitle("Upload Image Example")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Click a button to upload an image", self)
        layout.addWidget(self.label)

        # Button 1
        button1 = QPushButton("Upload Button1 Image", self)
        button1.clicked.connect(self.upload_image)
        layout.addWidget(button1)

        # Button 2
        button2 = QPushButton("Upload Button2 Image", self)
        button2.clicked.connect(self.upload_image)
        layout.addWidget(button2)

        self.image_label = QLabel(self)  # Label to display the uploaded image
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def ensure_images_directory(self):
        # Create 'images' directory in the program's root if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")

    def upload_image(self):
        button = self.sender()
        button_name = button.text().replace("Upload ", "").replace(" Image", "")

        # Open a file dialog to select an image
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg)")

        if file_path:
            # Set the new file name and path based on button name
            new_file_name = f"{button_name}.png"
            new_file_path = os.path.join("images", new_file_name)

            # Copy the selected image to the 'images' directory with the new name
            shutil.copy(file_path, new_file_path)

            # Display the uploaded image in the label
            self.image_label.setPixmap(QPixmap(new_file_path).scaled(200, 200))
            self.label.setText(f"Image uploaded and saved as {new_file_name}")
            print(f"Image uploaded and saved as {new_file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageUploaderApp()
    ex.show()
    sys.exit(app.exec())
