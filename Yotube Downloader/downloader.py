from datetime import timedelta
import re

from PyQt5.QtCore import QThread, pyqtSignal, QAbstractListModel, Qt, QVariant, QModelIndex

import Utils.utils as utils
import yt_dlp


def format_quality_info(fmt, size):
    """
    Formats quality and size information for a given format.

    Args:
        fmt (dict): Format dictionary containing format details.
        size (int or None): Size of the format in bytes.

    Returns:
        str or None: Formatted quality information or None if no size is provided.
    """
    # Retrieve the resolution from the 'height' key for video formats
    resolution = fmt.get('height')
    if resolution is not None:
        quality = f"Video: {resolution}p"
    else:
        # Retrieve the audio bitrate from the 'abr' key for audio formats
        audio_bitrate = fmt.get('abr')
        if audio_bitrate is not None:
            quality = f"Audio: {audio_bitrate}kbps"
        else:
            quality = 'Unknown Quality'

    ext_type = fmt.get('ext', 'Unknown Extension')

    if size is not None:
        size_str = utils.size_convertor(size)
        return f"{quality} ({size_str}) ({ext_type})"
    # return f"{quality} (Size unknown) ({ext_type})"

def extract_size(quality_string):
    # Split the string by '(' and ')'
    parts = quality_string.split('(')

    # Check if parts has at least two elements
    if len(parts) < 2:
        raise ValueError(f"Invalid format for quality_string: {quality_string}")

    # The size is the second part, remove the trailing ')'
    size_str = parts[1].rstrip(')')

    return size_str
def extract_qualities(formats):
    """
    Extracts video and audio qualities from the list of formats.

    Args:
        formats (list): List of format dictionaries.

    Returns:
        tuple: Two lists containing video/audio qualities and their format IDs.
    """
    video_audio_qualities = []
    audio_qualities = []

    for fmt in formats:
        ext_type = fmt.get('ext')
        size = fmt.get('filesize')
        quality_size = format_quality_info(fmt, size)

        # Format with both video and audio
        if quality_size and ext_type == 'mp4':
            quality_format_id = (quality_size, f'{fmt.get("format_id")} + bestaudio/best')
            if quality_format_id not in video_audio_qualities:
                video_audio_qualities.append(quality_format_id)

        # Format with audio only
        if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
            if quality_size:  # Check if quality_size is not None before appending
                quality_format_id = (quality_size, fmt.get('format_id'))
                if quality_format_id not in audio_qualities:
                    audio_qualities.append(quality_format_id)

    return video_audio_qualities, audio_qualities


def get_info(ui):
    """Fetch video info from URL and update UI elements."""
    if hasattr(ui, 'url_entre_box'):
        url = ui.url_entre_box.text().strip()

        if not url:
            print("Error: URL is empty.")
            return

        try:
            ydl_opts = {
                'noplaylist': True,  # Ensure that only a single video is processed
            }
            video_info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)

            # Check if the extracted info is a dictionary
            # Debugging: Ensure video_info is correctly retrieved
            # print("Video Info:", video_info)

            ui.Video_Title = video_info.get('title', 'Video Title')
            # if hasattr(self, 'SaveLocationYV'):
            #     self.SaveLocationYV.setText(self.Video_Title)
            if hasattr(ui, 'file_name_label'):
                ui.file_name_label.setText(ui.Video_Title)

            video_duration = video_info.get('duration', 0)
            video_duration_str = str(timedelta(seconds=video_duration))
            if hasattr(ui, 'file_duration_label'):
                ui.file_duration_label.setText(video_duration_str)

            formats = video_info.get('formats', [])
            # print("Formats:", formats)  # Debugging print

            # Check if formats list is not empty
            if not formats:
                print("No formats found.")
                return

            video_audio_qualities, audio_qualities = extract_qualities(formats)

            # Debugging: Print the extracted qualities
            # print("Extracted video and audio qualities:", video_audio_qualities)
            # print("Extracted audio qualities:", audio_qualities)

            video_audio_qualities.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))
            audio_qualities.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))

            if hasattr(ui, 'QualityBox'):
                ui.QualityBox.clear()
                for quality_size, format_id in video_audio_qualities:
                    if 'Unknown Quality' not in quality_size:
                        ui.QualityBox.addItem(quality_size, format_id)
                for quality_size, format_id in audio_qualities:
                    if 'Unknown Quality' not in quality_size:
                        ui.QualityBox.addItem(quality_size, format_id)
            else:
                print("Error: QualityBox not found in the UI.")

        except Exception as e:
            print(f"Error while fetching video info: {e}")


    else:
        print("Error: URL input box not found in the UI.")


# def download_video(url, save_path, format_id):
#     ydl_opts = {
#         'format': format_id,
#         'outtmpl': save_path
#     }
#
#     download_thread = DownloadThread(ydl_opts, url)
#     download_thread.start()
#
#
class DownloadThread(QThread):
    download_progress = pyqtSignal(int)
    download_finished = pyqtSignal(bool, str)

    def __init__(self, ydl_opts, url):
        super(DownloadThread, self).__init__()
        self.ydl_opts = ydl_opts
        self.url = url

    def run(self):
        try:
            # Use yt-dlp for downloading
            import yt_dlp
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url])
            self.download_finished.emit(True, "Download complete!")
        except Exception as e:
            self.download_finished.emit(False, str(e))

# class DownloadThread(QThread):
#     # Define signals
#     download_progress = pyqtSignal(int)  # Signal to report progress (percentage)
#     download_finished = pyqtSignal(bool, str)  # Signal to report completion (success/failure and message)
#
#     def __init__(self, ydl_opts, url):
#         super(DownloadThread, self).__init__()
#         self.ydl_opts = ydl_opts
#         self.url = url
#
#     def run(self):
#         try:
#             print(yt_dlp.YoutubeDL)  # Print yt_dlp.YoutubeDL to check if it's None
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 # Optionally connect to progress hooks if needed
#
#                 ydl.download([self.url])
#                 self.download_finished.emit(True, "Download completed successfully.")
#         except Exception as e:
#             self.download_finished.emit(False, f"Error during download: {str(e)}")


from PyQt5.QtWidgets import QStyledItemDelegate, QApplication

from PyQt5.QtCore import QSize

# Custom Delegate to render widgets (title, progress bar, size)
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionProgressBar
from PyQt5.QtCore import Qt, QRect

# class VideoDelegate(QStyledItemDelegate):
#     def paint(self, painter, option, index):
#         # Get the video item
#         video_item = index.data(Qt.DisplayRole)
#         print(f"Video item: {video_item}")  # Print the video item
#
#         # Check if video_item is a dictionary
#         if isinstance(video_item, dict):
#             # Draw the title and size on the first line
#             title = video_item.get('title', '')
#             size = video_item.get('size', '')
#             painter.drawText(option.rect, Qt.AlignLeft, f"{title} - {size}")
#
#             print("Before creating QStyleOptionProgressBar")
#             progress_bar_option = QStyleOptionProgressBar()
#             print("After creating QStyleOptionProgressBar")
#
#             print("Before setting rect property")
#             progress_bar_option.rect = QRect(option.rect.left(), option.rect.top() + 20, option.rect.width(), 20)
#             print("After setting rect property")
#
#             progress = video_item.get('progress', 0)
#             print(f"Progress: {progress}")  # Print the progress value
#
#             print("Before setting progress property")
#             progress_bar_option.progress = progress
#             print("After setting progress property")
#
#             print("Before setting textVisible property")
#             progress_bar_option.textVisible = True
#             print("After setting textVisible property")
#
#             print("Before setting text property")
#             progress_bar_option.text = f"{progress}%"
#             print("After setting text property")
#
#             print("Before drawing progress bar")
#             QApplication.style().drawControl(QStyle.CE_ProgressBar, progress_bar_option, painter)
#             print("After drawing progress bar")
#         else:
#             print(f"Error: Expected a dictionary, but got {type(video_item)}")
#
#     def sizeHint(self, option, index):
#         return QSize(200, 60)  # Customize size for each item


# Custom Model to hold the download items
class VideoListModel(QAbstractListModel):
    def __init__(self, videos=None):
        super(VideoListModel, self).__init__()
        self.videos = videos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Return the entire video dictionary for the DisplayRole
            return self.videos[index.row()]
        if role == Qt.UserRole + 1:
            return self.videos[index.row()]['progress']
        if role == Qt.UserRole + 2:
            return self.videos[index.row()]['size']
        return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.videos)

    def addVideo(self, video):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.videos.append(video)
        self.endInsertRows()