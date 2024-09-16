# main.py is the main file that contains the main application logic.
import os
import sys

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QLabel, QLineEdit, QPushButton, \
    QComboBox, QListWidget, QListWidgetItem, QProgressBar, QWidget, QWidgetItem, QVBoxLayout, QListView, \
    QStyledItemDelegate, QStyleOptionProgressBar, QStyle

import downloader
import downloader as YD

FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname(__file__), "UIs", "YV.ui"))

class VideoDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Get the video item
        video_item = index.data(Qt.DisplayRole)
        print(f"Video item: {video_item}")  # Print the video item

        # Check if video_item is a dictionary
        if isinstance(video_item, dict):
            # Draw the title and size on the first line
            title = video_item.get('title', '')
            size = video_item.get('size', '')
            painter.drawText(option.rect, Qt.AlignLeft, f"{title} - {size}")

            print("Before creating QStyleOptionProgressBar")
            self.download_progress_hook = QStyleOptionProgressBar()
            print("After creating QStyleOptionProgressBar")

            print("Before setting rect property")
            self.download_progress_hook.rect = QRect(option.rect.left(), option.rect.top() + 20, option.rect.width(), 20)
            print("After setting rect property")

            progress = video_item.get('progress', 0)
            print(f"Progress: {progress}")  # Print the progress value

            print("Before setting progress property")
            self.download_progress_hook.progress = progress
            print("After setting progress property")

            print("Before setting textVisible property")
            self.download_progress_hook.textVisible = True
            print("After setting textVisible property")

            print("Before setting text property")
            self.download_progress_hook.text = f"{progress}%"
            print("After setting text property")

            print("Before drawing progress bar")
            QApplication.style().drawControl(QStyle.CE_ProgressBar, self.download_progress_hook, painter)
            print("After drawing progress bar")
        else:
            print(f"Error: Expected a dictionary, but got {type(video_item)}")

    def sizeHint(self, option, index):
        return QSize(200, 60)  # Customize size for each item

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)  # Ensure UI is set up before accessing UI elements

        # Find UI elements
        self.file_name_label = self.findChild(QLabel, 'FileType_2')
        self.file_duration_label = self.findChild(QLabel, 'FileType_3')
        self.url_entre_box = self.findChild(QLineEdit, 'lineEdit2')
        self.file_path = self.findChild(QLineEdit, 'SaveLocationYV')
        self.cancel_button = self.findChild(QPushButton, 'pushButton_3')
        self.BrowseButton = self.findChild(QPushButton, 'BrowseButtonYV')
        self.DownloadButton = self.findChild(QPushButton, 'DownloadYoutubeVideo')
        self.QualityBox = self.findChild(QComboBox, 'QualityBox')

        # Initialize QListView and Model
        self.list_view = self.findChild(QListView, 'listView')
        self.model = downloader.VideoListModel()
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(downloader.VideoDelegate())  # Ensure delegate is set

        # Handle button connections
        self.Handle_Buttons()

        # Initialize variables
        self.full_save_path = ""
        self.Video_Title = ""

        print("DownloadingPage initialized successfully.")

    def Handle_Buttons(self):
        self.BrowseButton.clicked.connect(self.Browse)
        self.cancel_button.clicked.connect(self.Cancel)
        self.DownloadButton.clicked.connect(self.start_download)
        self.url_entre_box.textChanged.connect(lambda: YD.get_info(self))

    def Cancel(self):
        self.close()

    def Browse(self):
        initial_filename = self.file_name_label.text() if self.file_name_label.text() else "untitled"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", initial_filename, "All Files (*)")
        if file_path:
            self.full_save_path = file_path
            self.file_path.setText(os.path.basename(file_path))

    def start_download(self):


        # Get the size of the video for the selected quality
        size_str = downloader.extract_size(self.QualityBox.currentText())

        # Create a new video item and add it to the model
        video_item = {
            'title': self.file_name_label.text() if self.file_name_label.text() else 'untitled',
            'size': size_str,
            'progress': 0  # Initial progress, will be updated by progress hook
        }

        # Initialize QListView and Model
        self.list_view = self.findChild(QListView, 'listView')
        self.model = downloader.VideoListModel()
        self.list_view.setModel(self.model)
        # Add the video item to the model
        self.model.addVideo(video_item)

        self.list_view.setItemDelegate(VideoDelegate())  # Ensure delegate is set
        # Optionally update the list view to reflect the new item
        self.list_view.scrollToBottom()  # Ensure the view scrolls to the latest item

        outtmpl = self.full_save_path
        quality = self.QualityBox.currentData() if self.QualityBox.currentData() else 'best'
        ydl_opts = {
            'outtmpl': outtmpl,
            'format': quality,
            'nocheckcertificate': True,
            'noplaylist': True,
            'progress_hooks': [self.download_progress_hook],
        }
        url = self.url_entre_box.text()
        self.download_thread = YD.DownloadThread(ydl_opts, url)

        # Connect signals to slots
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.download_finished.connect(self.handle_download_finish)
        # Start the thread
        self.download_thread.start()

    # def update_progress_bar(self, d):
    #     if d['status'] == 'downloading':
    #         p = d['_percent_str']
    #         p = p.replace('%','')
    #         self.download_progress_hook.setValue(int(float(p)))

    def update_progress(self, progress):
        # Directly update the progress bar using the received progress value
        if isinstance(progress, int):
            self.download_progress_hook.setValue(progress)

    def handle_download_finish(self, success, message):
        if success:
            QMessageBox.information(self, "Download Finished", message)
        else:
            QMessageBox.critical(self, "Download Error", message)

class VideoDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Get the video item
        video_item = index.data(Qt.DisplayRole)
        print(f"Video item: {video_item}")  # Print the video item

        # Check if video_item is a dictionary
        if isinstance(video_item, dict):
            # Draw the title and size on the first line
            title = video_item.get('title', '')
            size = video_item.get('size', '')
            painter.drawText(option.rect, Qt.AlignLeft, f"{title} - {size}")

            print("Before creating QStyleOptionProgressBar")
            self.download_progress_hook = QStyleOptionProgressBar()
            print("After creating QStyleOptionProgressBar")

            print("Before setting rect property")
            self.download_progress_hook.rect = QRect(option.rect.left(), option.rect.top() + 20, option.rect.width(), 20)
            print("After setting rect property")

            progress = video_item.get('progress', 0)
            print(f"Progress: {progress}")  # Print the progress value

            print("Before setting progress property")
            self.download_progress_hook.progress = progress
            print("After setting progress property")

            print("Before setting textVisible property")
            self.download_progress_hook.textVisible = True
            print("After setting textVisible property")

            print("Before setting text property")
            self.download_progress_hook.text = f"{progress}%"
            print("After setting text property")

            print("Before drawing progress bar")
            QApplication.style().drawControl(QStyle.CE_ProgressBar, self.download_progress_hook, painter)
            print("After drawing progress bar")
        else:
            print(f"Error: Expected a dictionary, but got {type(video_item)}")

    def sizeHint(self, option, index):
        return QSize(200, 60)  # Customize size for each item

class VideoItemWidget(QWidget):
    def __init__(self, title, size, progress, parent=None):
        super(VideoItemWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Create and add widgets for title, size, and progress
        self.title_label = QLabel(title, self)
        self.size_label = QLabel(size, self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(progress)

        layout.addWidget(self.title_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
