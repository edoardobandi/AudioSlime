
# Audio Slime

Audio Slime is a Python application that allows you to concatenate MP3 audio tracks into a single file and generate timestamp metadata for YouTube. The application features a modern, dark-themed graphical interface built with **Tkinter** and **TtkThemes**.

## Features

- **Concatenate MP3 Tracks**: Combine multiple audio files into one seamless track.
- **Timestamp File**: Automatically generate a `timestamps.txt` file for YouTube chapters.
- **Real-time Logs**: View process logs directly in the interface.

## Installation

### Requirements
- **Python 3.x**
- **FFmpeg**
- Python libraries:
  - `pydub`
  - `ttkthemes`
  - `tkinter`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/edoardobandi/audioslime.git
   cd audioslime
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install FFmpeg:
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org) and add it to the PATH.
   - **Linux**: 
     ```bash
     sudo apt install ffmpeg
     ```
   - **macOS** (via Homebrew):
     ```bash
     brew install ffmpeg
     ```

6. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the app and select the folder containing MP3 files.
2. Choose an output folder.
3. Click **Concatenate Tracks** to process the files.
4. View logs in the terminal or app interface.
5. The concatenated MP3 file and `timestamps.txt` will be saved in the output folder.
