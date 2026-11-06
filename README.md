# CJ Launcher

CJ Launcher is a small Python launcher for Minecraft Java Edition, with an HTML landing page that keeps the original CJ look.

## Features

- Select from recent Minecraft release versions.
- Install or repair the selected game version.
- Let `minecraft-launcher-lib` install the Java runtime required by that version.
- Launch the game from the command line.
- Responsive landing page with keyboard focus styles and reduced-motion support.

## Requirements

- Python 3.9 or newer.
- Internet access for downloading Minecraft files and the required Java runtime.
- A supported Windows, macOS, or Linux installation.

## Install and run

```bash
python -m venv .venv
```

Activate it, then install the dependency:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python launcher.py
```

The launcher uses the default Minecraft directory for your operating system. The first install may take a while and use several gigabytes of disk space. Keep the terminal open while the game is running.

## Offline mode limitations

This launcher currently accepts an offline username and does not sign in to a Microsoft account. Offline mode is for local/single-player use; it does not authenticate you for online-mode multiplayer servers or Realms. Do not enter or store Microsoft passwords or access tokens in this project. Use the official Minecraft Launcher for authenticated play.

## Landing page

Open `index.html` in a browser to view the landing page. It links to the Python script; users still need Python and the listed dependency to run it. This repository does not package a standalone executable.

## Troubleshooting

- If downloads fail, check your internet connection and try again.
- If Minecraft fails to start, check the printed error, available memory, OS compatibility, and the selected version's requirements.
- The launcher has not been tested on every OS or Minecraft release. The library's install routine handles version-specific Java runtime metadata, but an actual launch should be verified on your device.
