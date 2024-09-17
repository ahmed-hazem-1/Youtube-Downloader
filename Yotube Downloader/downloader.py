from datetime import timedelta
import re
from tqdm import tqdm

from PyQt5.QtCore import QThread, pyqtSignal, QAbstractListModel, Qt, QVariant, QModelIndex

import Utils.utils as utils
import yt_dlp
from PyQt5.QtCore import Qt
import main


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
            # ui.number_of_videos.setText(video_info.get('n_entries', 0))
            # Check if the extracted info is a dictionary
            # Debugging: Ensure video_info is correctly retrieved
            # print("Video Info:", video_info)


            ui.Video_Title = video_info.get('title', 'Video Title')
            # if hasattr(self, 'SaveLocationYV'):
            #     self.SaveLocationYV.setText(self.Video_Title)
            if hasattr(ui, 'file_name_label'):
                ui.file_name_label.setText(ui.Video_Title)
                ui.CurrentDownload.setText(ui.Video_Title)
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
# class PlaylistDownloadThread(QThread):
#     download_progress = pyqtSignal(int)
#     download_finished = pyqtSignal(bool, str)
#     video_downloading = pyqtSignal(str)  # New signal
#     total_number_of_videos = pyqtSignal(int)  # New signal
#     current_video_number = pyqtSignal(int)  # New signal
#
#     def __init__(self, ydl_opts, url):
#         super(PlaylistDownloadThread, self).__init__()
#         self.ydl_opts = ydl_opts
#         self.url = url
#
#     def run(self):
#         try:
#             self.ydl_opts['noplaylist'] = False  # Treat the URL as a playlist
#             self.ydl_opts['progress_hooks'] = [main.MainApp.update_progress]
#
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 video_info = ydl.extract_info(self.url, download=False)
#                 total_video_number = video_info.get('n_entries', 0)
#                 self.total_number_of_videos.emit(total_video_number)  # Emit the total number of videos signal
#
#                 for i, entry in enumerate(video_info['entries'], start=1):
#                     video_title = entry.get('title', 'Unknown Title')
#                     self.current_video_number.emit(i)  # Emit the current video number signal
#                     self.video_downloading.emit(video_title)  # Emit the video downloading signal
#
#                     ydl.process_ie_result(entry, download=True)
#
#             self.download_finished.emit(True, "Download complete!")
#         except Exception as e:
#             self.download_finished.emit(False, str(e))


class DownloadThread(QThread):
    download_progress = pyqtSignal(int)  # Signal to emit progress
    download_finished = pyqtSignal(bool, str)  # This signal should be properly defined
    video_downloading = pyqtSignal(str)
    total_number_of_videos = pyqtSignal(int)
    current_video_number = pyqtSignal(int)

    def __init__(self, ydl_opts, url):
        super(DownloadThread, self).__init__()
        self.ydl_opts = ydl_opts
        self.url = url

    def run(self):
        try:
            # Fetch video info
            video_info = yt_dlp.YoutubeDL().extract_info(self.url, download=False)
            total_size = video_info.get('filesize', 0)  # Get total file size

            # Emit the title of the video being downloaded
            video_title = video_info.get('title', 'Unknown Title')
            self.video_downloading.emit(video_title)

            # Initialize the progress bar using tqdm
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as self.progress_bar:
                self.ydl_opts['progress_hooks'] = [self.emit_progress]  # Hook to track progress
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([self.url])

            self.download_progress.emit(100)  # Emit 100% completion signal after download
            self.download_finished.emit(True, "Download complete!")  # Emit finished signal on success

        except Exception as e:
            self.download_finished.emit(False, str(e))  # Emit finished signal on error

    def emit_progress(self, progress_info):
        if progress_info['status'] == 'downloading':
            downloaded = progress_info.get('downloaded_bytes', 0)
            total = progress_info.get('total_bytes', 1)

            if self.progress_bar:
                self.progress_bar.update(downloaded - self.progress_bar.n)  # Update tqdm bar

            percentage = int((downloaded / total) * 100)
            self.download_progress.emit(percentage)




