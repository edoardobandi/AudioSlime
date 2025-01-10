import os
import threading
from pydub import AudioSegment
from tkinter import Tk, Button, Label, filedialog, ttk, Text
from ttkthemes import ThemedTk
import time

def select_tracks_folder():
    folder_path = filedialog.askdirectory(title="Select Tracks Folder")
    tracks_folder_label.config(text=f"Tracks Folder: {folder_path}")
    return folder_path

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    output_folder_label.config(text=f"Output Folder: {folder_path}")
    return folder_path

def log_message(message):
    log_text.insert('end', message + "\n")
    log_text.yview('end')

def concatenate_audio():
    tracks_folder = tracks_folder_label.cget("text").replace("Tracks Folder: ", "")
    output_folder = output_folder_label.cget("text").replace("Output Folder: ", "")

    if not tracks_folder or not output_folder:
        log_message("Error: Please select all options!")
        return

    output_file = os.path.join(output_folder, "concatenated_output.mp3")
    timestamps_file = os.path.join(output_folder, "timestamps.txt")

    if os.path.exists(output_file):
        log_message(f"Deleting existing file: {output_file}")
        os.remove(output_file)

    if os.path.exists(timestamps_file):
        log_message(f"Deleting existing file: {timestamps_file}")
        os.remove(timestamps_file)

    files = [f for f in os.listdir(tracks_folder) if f.endswith(".mp3")]
    files.sort()
    concatenated_audio = AudioSegment.empty()
    timestamps = []
    current_time = 0

    log_message("Concatenating tracks...")

    progress_bar.pack(pady=20)
    progress_bar['maximum'] = len(files)
    progress_bar['value'] = 0
    root.update_idletasks()

    for idx, file in enumerate(files):
        track_path = os.path.join(tracks_folder, file)
        log_message(f"Processing: {file}")

        track = AudioSegment.from_mp3(track_path)
        concatenated_audio += track
        minutes = current_time // 60000
        seconds = (current_time % 60000) // 1000
        timestamps.append(f"{minutes:02}:{seconds:02} - {os.path.splitext(file)[0]}")
        current_time += len(track)

        progress_bar['value'] = idx + 1
        root.update_idletasks()
        time.sleep(0.1)

    concatenated_audio.export(output_file, format="mp3")
    log_message(f"Output saved to: {output_file}")

    with open(timestamps_file, "w") as f:
        f.write("YouTube Timestamps:\n\n")
        f.writelines("\n".join(timestamps))
    log_message(f"Timestamps saved to: {timestamps_file}")

    log_message("Concatenation completed!")

def setup_ffmpeg():
    ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")
    AudioSegment.ffmpeg = ffmpeg_path

def start_concatenation():
    threading.Thread(target=concatenate_audio, daemon=True).start()

root = ThemedTk()
root.title("Audio Slime")

root.geometry("500x700")
root.set_theme("arc")

root.iconbitmap("favicon.ico")
root.config(bg="#2e2e2e")

Label(root, text="Select Tracks Folder", bg="#2e2e2e", fg="#e1e1e1", font=("Arial", 14)).pack(pady=15)
select_tracks_button = Button(root, text="Select Folder", command=select_tracks_folder, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=15, pady=10)
select_tracks_button.pack()

tracks_folder_label = Label(root, text="Tracks Folder: ", bg="#2e2e2e", fg="#e1e1e1", font=("Arial", 12))
tracks_folder_label.pack(pady=10)

Label(root, text="Select Output Folder", bg="#2e2e2e", fg="#e1e1e1", font=("Arial", 14)).pack(pady=15)
select_output_button = Button(root, text="Select Output Folder", command=select_output_folder, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=15, pady=10)
select_output_button.pack()

output_folder_label = Label(root, text="Output Folder: ", bg="#2e2e2e", fg="#e1e1e1", font=("Arial", 12))
output_folder_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=350, mode='determinate')
progress_bar.pack_forget()

concatenate_button = Button(root, text="Concatenate Tracks", command=start_concatenation, bg="#FF5733", fg="white", font=("Arial", 14, "bold"), relief="flat", padx=30, pady=15)
concatenate_button.pack(pady=20)

result_label = Label(root, text="", bg="#2e2e2e", fg="#e1e1e1", font=("Arial", 12))
result_label.pack(pady=10)

log_text = Text(root, height=10, width=60, bg="#2e2e2e", fg="#e1e1e1", font=("Courier", 10), wrap="word")
log_text.pack(pady=20)

setup_ffmpeg()
root.mainloop()

