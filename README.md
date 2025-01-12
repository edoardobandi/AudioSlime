```markdown
# Audio Slime

Audio Slime is a Python application that allows you to concatenate MP3 audio tracks into a single file, generate timestamp metadata for YouTube, and download audio tracks directly from Spotify using **spotdl**. The application features a modern, dark-themed graphical interface built with **Tkinter** and **TtkThemes**.

## Features

- **Concatenate MP3 Tracks**: Combine multiple audio files into one seamless track.
- **Timestamp File**: Automatically generate a `timestamps.txt` file for YouTube chapters.
- **Spotify Integration**: Download Spotify tracks using **spotdl**.
- **Real-time Logs**: View process logs directly in the interface.

## Installation

### Requirements
- **Python 3.x**
- **FFmpeg**
- **spotdl**
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

6. Install **spotdl** for Spotify integration:
   ```bash
   pip install spotdl
   ```

7. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the app and select the folder containing MP3 files.
2. To download a track from Spotify, paste the Spotify URL in the "Spotify Track URL" input field.
3. Select an output folder for both MP3 files and the downloaded Spotify track.
4. Click **Concatenate Tracks** to process the files.
5. View logs in the terminal or app interface.
6. The concatenated MP3 file, the downloaded Spotify track, and `timestamps.txt` will be saved in the output folder.
```
