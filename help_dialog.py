from PySide6.QtWidgets import QMessageBox

def showHelp(parent):
    # 显示帮助信息对话框
    about_text = """
    <h2>关于 Image Saver 应用程序</h2>
    <p>这是一个用于保存和预览图片的应用程序。</p>
    <p>功能包括：</p>
    <ul>
        <li>上传和绑定图片到特定按钮</li>
        <li>预览已保存的图片</li>
        <li>支持多种图片格式（PNG, JPG, BMP）</li>
    </ul>
    <p>开发者：Gnay</p>
    <p>版本：0.0.1</p>
    <p>感谢使用我们的应用程序！</p>
    """
    QMessageBox.information(parent, '关于', about_text)
