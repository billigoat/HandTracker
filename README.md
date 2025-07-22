# Package Installation Instructions for macOS

## To set up the environment for this project on macOS, make sure you have Python installed (preferably via Homebrew or the official installer). Then:

- Open Terminal.
- ### Create and activate a virtual environment to keep dependencies isolated:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- ### Upgrade pip to the latest version:
  ```bash
  pip install --upgrade pip
  ```
- ### Then install packages
  ```bash
  pip install numpy==1.26.4 opencv-python mediapipe==0.10.21
  ```
