# Import modules
import re
import os
import sys
import yt_dlp
import ffmpeg
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Regex to validate YouTube URL 
youtube_regex = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$"

# Regex to validate time format
time_regex = r"^[0-9]{1,2}\:[0-9]{2}$"

# Validate YouTube URL
def validate_url(url):
  """Check if the url is a valid YouTube video url."""
  if re.match(youtube_regex, url):
    return True
  return False 

# Validate time format  
def validate_time(time):
  """Check if the time is in mm:ss format."""
  if re.match(time_regex, time):
     return True
  return False

# Get video and audio streams  
def get_streams(url):
  """Get the video and audio stream urls from a YouTube video url."""
  if not validate_url(url):
    return None
  
  ydl_opts = {
    'format': 'bestvideo[height<=?{0}]+bestaudio/best[height<=?{0}]'.format(resolution.get()), # Set the resolution limit according to the user's choice
    'quiet': True
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False) 
    video = ydl.get_best_video_url(info)
    audio = ydl.get_best_audio_url(info)
  
  return video, audio

# Download segment
def download_segment(v_url, a_url, start, end, filename):
  """Download and trim a video segment from the stream urls, start time, end time, and output file name."""
  if not validate_time(start) or not validate_time(end):
    return False

  start_sec = convert_to_sec(start)
  end_sec = convert_to_sec(end)

  try:
    # Create a progress bar widget to show the download status
    progress = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
    progress.grid(row=6, column=1)
    progress['maximum'] = end_sec - start_sec # Set the maximum value of the progress bar to the duration of the segment
    
    # Define a callback function to update the progress bar value and text
    def progress_callback(in_filename, frame_number, frame_time, total_size):
      progress['value'] = frame_time - start_sec # Set the current value of the progress bar to the current frame time minus the start time
      progress.update() # Update the progress bar widget
      status_label['text'] = 'Downloading: {0:.2f}%'.format(progress['value'] / progress['maximum'] * 100) # Display the percentage of completion on the status label
    
    ffmpeg.input(v_url, ss=start_sec)\
          .input(a_url, ss=start_sec)\
          .output(filename, ss=5, t=(end_sec-start_sec), vcodec=codec.get())\ # Set the video codec according to the user's choice
          .run(callback=progress_callback) # Run the ffmpeg command with the callback function
    
    return True 
  except:
    return False

# Convert time to seconds
def convert_to_sec(time):
  """Convert time from mm:ss format to seconds."""
  m, s = time.split(':')
  return int(m) * 60 + int(s)

# Validate filename
def validate_filename(filename):
  """Check if the filename is valid and has .mp4 extension."""
  invalid = "\\/:*<>|"
  return not any(char in invalid for char in filename) and filename.endswith('.mp4')

# Download button clicked
def download():
  """Handle the download button click event."""

  url = url_entry.get()
  start = start_entry.get()
  end = end_entry.get()
  filename = filename_entry.get()

  if not validate_url(url):
    status_label['text'] = 'Invalid URL'
    return

  if not validate_time(start) or not validate_time(end):
    status_label['text'] = 'Invalid start/end time format'
    return

  if not validate_filename(filename):
    status_label['text'] = 'Invalid filename' 
    return

  v_url, a_url = get_streams(url)

  if not v_url or not a_url:
    status_label['text'] = 'Error getting video streams'
    return

  if os.path.exists(filename):
    status_label['text'] = 'File already exists'
    return

  downloaded = download_segment(v_url, a_url, start, end, filename)

  if downloaded:
    status_label['text'] = 'Download complete'
  else:
    status_label['text'] = 'Error downloading segment'
  

# Tkinter GUI
window = tk.Tk()
window.title('YouTube Video Segment Downloader')

# Labels
tk.Label(window, text="YouTube URL:").grid(row=0, column=0)
tk.Label(window, text="Start Time (mm:ss):").grid(row=1, column=0)
tk.Label(window, text="End Time (mm:ss):").grid(row=2, column=0)
tk.Label(window, text="File Name:").grid(row=3, column=0)
tk.Label(window, text="Resolution:").grid(row=4, column=0)
tk.Label(window, text="Codec:").grid(row=5, column=0)

# Entry widgets
url_entry = tk.Entry(window)
start_entry = tk.Entry(window)
end_entry = tk.Entry(window)
filename_entry = tk.Entry(window)

url_entry.grid(row=0, column=1)
start_entry.grid(row=1, column=1)
end_entry.grid(row=2, column=1)  
filename_entry.grid(row=3, column=1)

# Download button
download_btn = tk.Button(window, text="Download", command=download)
download_btn.grid(row=7, column=1)

# Status label 
status_label = tk.Label(window, text="")
status_label.grid(row=8, column=1)

# Resolution option menu
resolution = tk.StringVar(window) # Create a string variable to store the resolution choice
resolution.set('1080') # Set the default value to 1080
resolution_options = ['2160', '1440', '1080', '720', '480', '360', '240', '144'] # Create a list of resolution options
resolution_menu = tk.OptionMenu(window, resolution, *resolution_options) # Create an option menu widget with the resolution variable and options
resolution_menu.grid(row=4, column=1) # Place the option menu widget on the grid

# Codec option menu
codec = tk.StringVar(window) # Create a string variable to store the codec choice
codec.set('libx264') # Set the default value to libx264
codec_options = ['libx264', 'libx265', 'libvpx', 'libvpx-vp9', 'copy'] # Create a list of codec options
codec_menu = tk.OptionMenu(window, codec, *codec_options) # Create an option menu widget with the codec variable and options
codec_menu.grid(row=5, column=1) # Place the option menu widget on the grid

window.mainloop()
