# 🎥 YouTube Downloader

Welcome to **YouTube Downloader** – your ultimate tool for downloading YouTube videos with style! This project offers a sleek, user-friendly interface for fetching your favorite videos and playlists directly to your device.

## 📸 Screenshots

Check out how YouTube Downloader looks in action:

- **Main Page**: ![Main Page](YouTube%20Downloader/assets/screenshots/MainPage.png)
- **Download Progress**: ![Progressbar](YouTube%20Downloader/assets/screenshots/Progressbar.png)
- **Video Qualities**: ![Qualities](YouTube%20Downloader/assets/screenshots/Qualities.png)
- **Fast Info Collection**: ![Fast Info Collect](YouTube%20Downloader/assets/screenshots/FastInfoCollect.png)
- **Finish Reminder**: ![Finish Reminder](YouTube%20Downloader/assets/screenshots/FinishReminder.png)
- **Responsive Design**: ![Responsive](YouTube%20Downloader/assets/screenshots/Responsive.png)

## 🚀 Features

- **Download Videos**: Easily download your favorite YouTube videos.
- **Progress Tracking**: Visual progress bar to keep track of your download status.
- **Quality Selection**: Choose the video quality you prefer.
- **Responsive Design**: Optimized for all screen sizes.
- **Stylish Interface**: Modern design with creative gradients and UI elements.

## 💻 Installation

Get started with YouTube Downloader by following these simple steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ahmed-hazem-1/Youtube-Downloader.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd Youtube-Downloader
   ```
3. **Install Required Dependencies**:
   Install the necessary packages with:
   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes:
   ```
   PyQt5
   yt-dlp
   tqdm
   ```

4. **Run the Application**:
   Start the application with:
   ```bash
   python main.py
   ```

## 🎨 Customizing the UI

The UI is designed with QDesigner. Find the UI files in the `YouTube Downloader/UIs` directory:

- `Downloading_page.ui`
- `YP.ui`
- `YV.ui`

Open these files with QDesigner to customize the look and feel as you like.

## 🛠️ Project Structure

Here’s a quick overview of the project:

- `YouTube Downloader/assets/screenshots/`: Screenshots of the application.
- `YouTube Downloader/downloader.py`: Logic for handling video downloads.
- `YouTube Downloader/main.py`: Entry point of the application.
- `YouTube Downloader/UIs/`: UI files created with QDesigner.
- `YouTube Downloader/Utils/`: Utility functions and modules.

## 🤝 Contributing

We welcome contributions! To contribute, fork the repository and submit a pull request. Your help in improving the tool is greatly appreciated.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
