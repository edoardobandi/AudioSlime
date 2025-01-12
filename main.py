import os
import subprocess
import threading
import time
from tkinter import Button, Label, filedialog, ttk, Text, Entry

from pydub import AudioSegment
from ttkthemes import ThemedTk


def log_message_spotdl(message):
    spotdl_log_text.insert('end', message + "\n")
    spotdl_log_text.yview('end')


spotdl_process = None


def download_with_spotdl(link, output_folder):
    global spotdl_process
    if not link or not output_folder:
        log_message_spotdl("Error: Provide both link and output folder.")
        return

    try:
        output_folder = os.path.join(output_folder, '')
        command = f'spotdl "{link}" --output "{output_folder}"'

        command = command.replace('"', '')

        spotdl_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True)

        for line in spotdl_process.stdout:
            log_message_spotdl(line.strip())
        stderr_output = spotdl_process.stderr.read()
        if stderr_output:
            log_message_spotdl(stderr_output.strip())

        spotdl_process.wait()
        log_message_spotdl("Download complete!")

    except subprocess.CalledProcessError:
        log_message_spotdl("Error during download. Check the link and try again.")


def on_close():
    global spotdl_process
    if spotdl_process:
        spotdl_process.terminate()
        spotdl_process.wait()
        log_message_spotdl("SpotDL process terminated.")
    root.destroy()


def select_spotdl_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        spotdl_output_folder_label.config(text=f"Output Folder: {folder}")
    return folder


def start_spotdl_download():
    link = link_entry.get()
    output_folder = spotdl_output_folder_label.cget("text").replace("Output Folder: ", "")
    threading.Thread(target=download_with_spotdl, args=(link, output_folder), daemon=True).start()


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
root.geometry("600x600")
root.set_theme("xpnative")
root.iconbitmap("favicon.ico")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
style.configure("TLabel", background="#2e2e2e", foreground="#e1e1e1", font=("Arial", 12))
style.configure("TNotebook", background="#2e2e2e", foreground="#e1e1e1")
style.configure("TNotebook.Tab", font=("Arial", 12, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")
notebook.pack(expand=True, fill="both")

audio_tab = ttk.Frame(notebook, style="TFrame")
notebook.add(audio_tab, text="Concatenate Audio")

Label(audio_tab, text="Select Tracks Folder").pack(pady=15)
select_tracks_button = Button(audio_tab, text="Select Folder", command=select_tracks_folder, bg="#4CAF50", fg="white",
                              relief="flat")
select_tracks_button.pack()
tracks_folder_label = Label(audio_tab, text="Tracks Folder: ")
tracks_folder_label.pack(pady=10)

Label(audio_tab, text="Select Output Folder").pack(pady=15)
select_output_button = Button(audio_tab, text="Select Output Folder", command=select_output_folder, bg="#4CAF50",
                              fg="white", relief="flat")
select_output_button.pack()
output_folder_label = Label(audio_tab, text="Output Folder: ")
output_folder_label.pack(pady=10)

concatenate_button = Button(audio_tab, text="Concatenate Tracks", command=start_concatenation, bg="#FF5733", fg="white",
                            relief="flat")
concatenate_button.pack(pady=15)

log_text = Text(audio_tab, height=10, width=60, bg="#1e1e1e", fg="#e1e1e1", wrap="word")
log_text.pack(pady=20)
spotdl_tab = ttk.Frame(notebook, style="TFrame")
notebook.add(spotdl_tab, text="Download with SpotDL")

Label(spotdl_tab, text="Enter Spotify Link:").pack(pady=10)
link_entry = Entry(spotdl_tab, width=50, bg="#1e1e1e", fg="#e1e1e1", insertbackground="white")
link_entry.pack(pady=5)

Button(spotdl_tab, text="Select Output Folder", command=select_spotdl_output_folder, bg="#4CAF50", fg="white",
       relief="flat").pack(pady=10)
spotdl_output_folder_label = Label(spotdl_tab, text="Output Folder: ")
spotdl_output_folder_label.pack(pady=5)

Button(spotdl_tab, text="Download", command=start_spotdl_download, bg="#FF5733", fg="white", relief="flat").pack(
    pady=15)
download_log_label = Label(spotdl_tab, text="")
download_log_label.pack(pady=10)

spotdl_log_text = Text(spotdl_tab, height=10, width=60, bg="#1e1e1e", fg="#e1e1e1", wrap="word")
spotdl_log_text.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_close)
setup_ffmpeg()
root.mainloop()
