import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pytube import YouTube

def download_video():
    link = link_entry.get()

    if not link:
        messagebox.showerror("Error", "Please enter a valid YouTube video URL.")
        return

    try:
        youtube = YouTube(link, on_progress_callback=on_progress)
        video_stream = youtube.streams.get_highest_resolution()

        save_path = filedialog.askdirectory(initialdir=os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "Videos"),
                                             title="Select Download Location")
        if not save_path:
            return

        video_stream.download(output_path=save_path)
        messagebox.showinfo("Success", "Video downloaded successfully!")

        # Clear input field
        link_entry.delete(0, tk.END)
        
        # Reset progress bar and countdown label
        progress_bar['value'] = 0
        countdown_label.config(text="")
        
        # Stop tracking download progress
        is_downloading = False

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_progress(stream, chunk, bytes_remaining):
    progress_value = (stream.filesize - bytes_remaining) / stream.filesize * 100
    progress_bar["value"] = progress_value
    countdown_label.config(text=f"Remaining: {int(progress_value)}%")
    root.update_idletasks()

root = tk.Tk()
root.title("YouTube Video Downloader")

link_label = tk.Label(root, text="Enter YouTube Video URL:")
link_label.pack(pady=5)

link_entry = tk.Entry(root, width=50)
link_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=5)

is_downloading = False
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=5)

# Label for displaying the countdown
countdown_label = tk.Label(root, text="", fg="blue")
countdown_label.pack(pady=5)


root.mainloop()