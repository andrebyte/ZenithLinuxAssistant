# 🌌 Zenith Linux Assistent

![Zenith Linux Banner](https://img.shields.io/badge/Zenith-Linux_Assistant-3b82f6?style=for-the-badge&logo=linux)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

> **Sprachen:** [English](README.md) | [Türkçe](README_TR.md) | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

**Zenith Linux Assistent** ist Ihr ultimativer Begleiter, der den Übergang von Windows zu Linux reibungslos gestaltet. Er überwacht Ihre Hardware-Metriken, bietet 1-Klick-Installationen für beliebte Anwendungen in verschiedenen Distributionen (Debian, Arch, Fedora), übersetzt Terminalfehler sofort und behebt häufige Linux-Fehler.

---

## ✨ Funktionen
* **Hardware-Dashboard:** Überwachen Sie Ihr Betriebssystem, Kernel, CPU und RAM in Echtzeit.
* **1-Klick-Installationen:** Kopieren Sie die genauen Installationsbefehle für Apps wie VS Code, Chrome, Spotify und VLC abhängig von Ihrer Linux-Familie.
* **Fehlerübersetzer:** Fügen Sie jeden englischen Terminalfehler ein und erhalten Sie sofort eine Übersetzung in Ihre bevorzugte Sprache (via `deep-translator`).
* **Problemlöser:** 1-Klick-Fixes für häufige Fehler (kein Ton, WLAN-Abbrüche, Bildschirmflackern, Paketsperren).
* **Dynamische Themen & Sprachen:** Wechseln Sie sofort zwischen Hell/Dunkel-Modus und 5 Oberflächensprachen (EN, TR, ES, DE, RU) ohne Neustart.

---

## 🚀 Schnellstart (Vorkompilierte Datei)
Wenn Sie Python nicht installieren oder sich nicht mit Quellcode beschäftigen möchten, können Sie die ausführbare Datei direkt aus dem **Releases** Tab herunterladen.

**Für Linux-Benutzer:**
1. Laden Sie `ZenithLinuxAssistant` unter Releases herunter.
2. Rechtsklick auf die Datei -> **Eigenschaften** -> **Berechtigungen** -> Aktivieren Sie **"Datei als Programm ausführen zulassen"**.
3. Doppelklicken Sie zum Ausführen!

---

## 💻 Manuelle Installation (Aus Quellcode ausführen)
Wenn die kompilierte Datei für Ihre Distribution nicht funktioniert oder Sie sie aus dem Quellcode ausführen möchten:

### 1. Voraussetzungen installieren
Sie benötigen Python 3 und pip.
Für Ubuntu/Debian-basierte Systeme:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Repository klonen
```bash
git clone https://github.com/IHR_BENUTZERNAME/ZenithLinuxAssistant.git
cd ZenithLinuxAssistant
```

### 3. Erforderliche Bibliotheken installieren
```bash
pip install -r requirements.txt
```

### 4. Anwendung starten
```bash
python3 main.py
```

---

## 🛠️ Eigene Binärdatei erstellen (Für Entwickler)
So erstellen Sie eine eigenständige ausführbare Datei für Ihr aktuelles Betriebssystem:

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --windowed --name "ZenithLinuxAssistant" --add-data "$(python3 -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" main.py
```
Die kompilierte Anwendung wird im Ordner `dist/` generiert.

---

## 📝 Lizenz
Dieses Projekt ist Open Source und kostenlos nutzbar. Beiträge sind willkommen!
