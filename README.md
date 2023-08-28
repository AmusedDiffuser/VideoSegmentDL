# Video Segment Downloader

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [GUI](#gui)
  - [Command Line](#command-line)
- [Customization](#customization)
  - [Resolution](#resolution)
  - [Codec](#codec)  
- [Issues](#issues)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application allows downloading a specific segment from a YouTube video by specifying the start and end times. It provides both a graphical user interface (GUI) as well as a command line interface. 

Key features:

- Downloads video in best available quality 
- Trims video segment based on start and end times
- Saves trimmed video segment to MP4 file
- Shows download progress
- Allows setting resolution and codec

[Back to Top](#video-segment-downloader)

## Installation

First, clone this repository:

```
git clone https://github.com/user/video-segment-downloader.git
```

### Dependencies

This project requires the following dependencies:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [Python 3](https://www.python.org/) 
  - tkinter
  - re
  - os

Install dependencies using pip:

```
pip install yt-dlp ffmpeg-python tkinter regex os
```

[Back to Top](#video-segment-downloader)

## Usage

The application can be run in two modes - GUI mode and command line mode.

### GUI

To launch the GUI, run:

```
python downloader_gui.py
```

This will open up the application window. Enter the required download details like YouTube URL, start and end times, resolution (optional), and output file name. Finally click the 'Download' button to begin.

The progress will be shown in the bar at the bottom.

### Command Line

To use the command line interface, run:

```
python downloader_cli.py [args]
```

The following arguments can be passed:

- -u : YouTube URL of the video
- -s : Start time in mm:ss format 
- -e : End time in mm:ss format
- -o : Output file name
- -r : Resolution (optional)
- -c : Codec (optional)

Example usage:
```
python downloader_cli.py -u https://www.youtube.com/watch?v=xyz -s 00:30 -e 02:00 -o output.mp4
```

This will download the video segment from 00:30 to 02:00 and save it to output.mp4.

[Back to Top](#video-segment-downloader)

## Customization

The application provides options to customize the resolution and codec of the downloaded video.

### Resolution

Use the -r argument in CLI or select from the drop down in GUI to set the desired resolution. The available options are:

- 2160p
- 1440p 
- 1080p
- 720p
- 480p
- 360p
- 240p

### Codec

Use the -c argument in CLI or select from the drop down in GUI to set the desired codec. The available options are: 

- libx264
- libx265
- libvpx
- libvpx-vp9

[Back to Top](#video-segment-downloader)

## Issues

For any bugs or issues, please open a GitHub issue [here](https://github.com/user/video-segment-downloader/issues).

[Back to Top](#video-segment-downloader)

## Contributing 

Contributions to add features or fix bugs are welcome! Follow these steps:

1. Fork this repository 
2. Create a new branch 
3. Make your changes and commit
4. Push changes to your fork
5. Create a pull request

[Back to Top](#video-segment-downloader)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

[Back to Top](#video-segment-downloader)
