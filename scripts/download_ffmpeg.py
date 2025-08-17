#!/usr/bin/env python3
import os
import platform
import urllib.request
import zipfile
import tarfile
import shutil

FFMPEG_DIR = os.path.join("drivebox", "resources", "ffmpeg")

def download_ffmpeg():
    system = platform.system().lower()
    url = None

    if system == "windows":
        # Windows build (zip)
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    elif system == "linux":
        # Linux static build (tar.xz)
        url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    elif system == "darwin":  # macOS
        # macOS build (zip)
        url = "https://evermeet.cx/ffmpeg/ffmpeg-6.1.zip"

    if not url:
        raise RuntimeError(f"Unsupported OS: {system}")

    os.makedirs(FFMPEG_DIR, exist_ok=True)
    filename = os.path.join(FFMPEG_DIR, os.path.basename(url))

    print(f"Downloading ffmpeg from {url}...")
    urllib.request.urlretrieve(url, filename)

    print("Extracting ffmpeg...")
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
    elif filename.endswith(".tar.xz"):
        with tarfile.open(filename, "r:xz") as tar_ref:
            tar_ref.extractall(FFMPEG_DIR)

    # Try to locate ffmpeg binary inside extracted folder
    ffmpeg_bin = None
    for root, dirs, files in os.walk(FFMPEG_DIR):
        for f in files:
            if f.startswith("ffmpeg"):
                ffmpeg_bin = os.path.join(root, f)
                break

    if ffmpeg_bin:
        # Move binary to FFMPEG_DIR root
        target = os.path.join(FFMPEG_DIR, os.path.basename(ffmpeg_bin))
        shutil.move(ffmpeg_bin, target)
        print(f"ffmpeg ready at: {target}")
    else:
        print("⚠️ Could not find ffmpeg binary after extraction.")

    # Clean up archive
    os.remove(filename)

if __name__ == "__main__":
    download_ffmpeg()