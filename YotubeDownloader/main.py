import os
import sys

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QLabel, QLineEdit, QPushButton, \
    QComboBox, QListWidget, QListWidgetItem, QProgressBar, QWidget, QWidgetItem, QVBoxLayout, QListView
from PyQt5.QtCore import pyqtSignal, Qt

import downloader
import downloader as YD

FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname(__file__), "UIs", "YV.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)  # Ensure UI is set up before accessing UI elements
        self.setWindowTitle("Youtube Video Downloader")
        # Find UI elements
        self.file_name_label = self.findChild(QLabel, 'FileType_2')
        self.file_duration_label = self.findChild(QLabel, 'FileType_3')
        self.url_entre_box = self.findChild(QLineEdit, 'lineEdit2')
        self.file_path = self.findChild(QLineEdit, 'SaveLocationYV')
        self.cancel_button = self.findChild(QPushButton, 'pushButton_3')
        self.BrowseButton = self.findChild(QPushButton, 'BrowseButtonYV')
        self.DownloadButton = self.findChild(QPushButton, 'DownloadYoutubeVideo')
        self.QualityBox = self.findChild(QComboBox, 'QualityBox')
        self.SingleProgressBar = self.findChild(QProgressBar, 'SingleProgressBar')
        self.SingleProgressBar.setValue(0)
        # self.TotalProgressBar = self.findChild(QProgressBar, 'TotalProgressBar')
        self.CurrentDownload = self.findChild(QLabel, 'label_2')
        # self.number_of_videos = self.findChild(QLabel, 'label_4')
        self.list_widget = self.findChild(QListWidget, 'listWidget')

        # Handle button connections
        self.Handle_Buttons()

        # Initialize variables
        self.full_save_path = ""
        self.Video_Title = ""

        print("DownloadingPage initialized successfully.")

    def Handle_Buttons(self):
        self.BrowseButton.clicked.connect(self.Browse)
        self.cancel_button.clicked.connect(self.Cancel)
        self.DownloadButton.clicked.connect(self.start_download_single_video)
        self.url_entre_box.textChanged.connect(lambda: YD.get_info(self))

    def Cancel(self):
        self.close()

    def Browse(self):
        initial_filename = self.file_name_label.text() if self.file_name_label.text() else "untitled"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", initial_filename, "All Files (*)")
        if file_path:
            self.full_save_path = file_path
            self.file_path.setText(os.path.basename(file_path))

    def start_download_single_video(self):
        # Get the size of the video for the selected quality
        size_str = downloader.extract_size(self.QualityBox.currentText())

        # Create a new video item with initial progress
        video_item = {
            'title': self.file_name_label.text() if self.file_name_label.text() else 'untitled',
            'size': size_str,
            'progress': 0  # Initial progress, will be updated by progress hook
        }
        # Add the video item to the list widget
        self.list_widget.addItem(
            f"Title: {video_item['title']}, Size: {video_item['size']}")

        # Scroll to the bottom to show the new item
        self.list_widget.scrollToBottom()
        # Prepare download options
        outtmpl = os.path.join(f'{self.full_save_path} .%(ext)s')
        quality = self.QualityBox.currentData() if self.QualityBox.currentData() else 'best'
        url = self.url_entre_box.text()

        # Initialize download thread with empty options
        self.download_thread = YD.DownloadThread({}, url)  # Initialize download_thread with empty ydl_opts

        ydl_opts = {
            'outtmpl': outtmpl,
            'format': quality,
            'nocheckcertificate': True,
            'noplaylist': True,
            # 'progress_hooks': [self.update_progress],
        }

        self.download_thread.ydl_opts = ydl_opts  # Update ydl_opts in download_thread

        # Connect the signal to update progress
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.download_finished.connect(self.handle_download_finish)

        # Start the download thread
        self.download_thread.start()

    def update_progress(self, progress):
        try:
            self.SingleProgressBar.setValue(int(progress))  # Update the progress bar
        except ValueError:
            print(f"Error: Can't convert '{progress}' to integer at update_progress()")

    def handle_download_finish(self, success, message):
        if success:
            QMessageBox.information(self, "Download Finished", message)
        else:
            QMessageBox.critical(self, "Download Error", message)



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
