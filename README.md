# 🌌 Zenith Linux Assistant

![Zenith Linux Banner](https://img.shields.io/badge/Zenith-Linux_Assistant-3b82f6?style=for-the-badge&logo=linux)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

> **Languages:** [English](README.md) | [Türkçe](README_TR.md) | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

**Zenith Linux Assistant** is your ultimate companion designed to make the transition to Linux seamless. It monitors your hardware metrics, provides one-click installations for popular applications across various distributions (Debian, Arch, Fedora), translates terminal errors instantly, and fixes common post-transition Linux bugs.

---

## ✨ Features
* **Hardware Dashboard:** Monitor your active OS, Kernel, CPU, and RAM metrics in real-time.
* **One-Click Installers:** Copy the exact installation commands for apps like VS Code, Chrome, Spotify, and VLC depending on your specific Linux family.
* **Error Translator:** Paste any English terminal error and get an instant translation into your preferred language using `deep-translator`.
* **Troubleshooter:** One-click fixes for common bugs (no sound, Wi-Fi dropping, screen flickering, package locks).
* **Dynamic Theming & Localization:** Instantly switch between Light/Dark themes and 5 interface languages (EN, TR, ES, DE, RU) without restarting.

---

## 🚀 Quick Start (Pre-Compiled Binary)
If you don't want to install Python or mess with source code, you can download the standalone executable from the **Releases** tab.

**For Linux Users:**
1. Download `ZenithLinuxAssistant` from Releases.
2. Right-click the file -> **Properties** -> **Permissions** -> Check **"Allow executing file as program"**.
3. Double-click to run!

---

## 💻 Manual Installation (Run from Source)
If the binary doesn't work for your specific distribution or if you want to run it from the source code, follow these steps:

### 1. Install Prerequisites
You need Python 3 and pip installed on your system. 
For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ZenithLinuxAssistant.git
cd ZenithLinuxAssistant
```

### 3. Install Required Libraries
Install the required python packages using pip:
```bash
pip install -r requirements.txt
```
*(If your system complains about externally managed environments, use `pip install -r requirements.txt --break-system-packages` or create a virtual environment).*

### 4. Run the Application
```bash
python3 main.py
```

---

## 🛠️ Building the Binary Yourself (For Developers)
To create a standalone executable for your current OS:

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --windowed --name "ZenithLinuxAssistant" --add-data "$(python3 -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" main.py
```
The compiled application will be generated in the `dist/` folder.

---

## 📝 License
This project is open-source and free to use. Contributions are welcome!
