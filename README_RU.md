# 🌌 Zenith Linux Ассистент

![Zenith Linux Banner](https://img.shields.io/badge/Zenith-Linux_Assistant-3b82f6?style=for-the-badge&logo=linux)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

> **Языки:** [English](README.md) | [Türkçe](README_TR.md) | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

**Zenith Linux Ассистент** — это ваш идеальный помощник, созданный для плавного перехода с Windows на Linux. Он отслеживает метрики вашего оборудования, обеспечивает установку популярных приложений (Debian, Arch, Fedora) в один клик, мгновенно переводит ошибки терминала и решает частые проблемы Linux.

---

## ✨ Возможности
* **Панель Оборудования:** Отслеживайте использование ОС, Ядра, Процессора и ОЗУ в реальном времени.
* **Установка в Один Клик:** Копируйте точные команды установки для VS Code, Chrome, Spotify и VLC в зависимости от вашего семейства Linux.
* **Переводчик Ошибок:** Вставьте любую ошибку терминала на английском и мгновенно получите перевод на ваш язык с помощью `deep-translator`.
* **Устранение Неполадок:** Решения в один клик для частых проблем (нет звука, отключение Wi-Fi, блокировка менеджера пакетов).
* **Динамические Темы и Языки:** Мгновенное переключение между Светлой/Темной темой и 5 языками (EN, TR, ES, DE, RU) без перезапуска.

---

## 🚀 Быстрый Старт (Готовый файл)
Если вы не хотите устанавливать Python или работать с исходным кодом, скачайте готовый исполняемый файл со вкладки **Releases**.

**Для пользователей Linux:**
1. Скачайте `ZenithLinuxAssistant` из Releases.
2. Кликните правой кнопкой мыши по файлу -> **Свойства** -> **Права** -> Отметьте **"Разрешить выполнение файла как программы"**.
3. Дважды кликните, чтобы запустить!

---

## 💻 Ручная Установка (Запуск из исходников)
Если готовый файл не работает в вашей системе или вы хотите запустить приложение из исходного кода, выполните эти шаги:

### 1. Установите необходимые пакеты
У вас должен быть установлен Python 3 и pip.
Для систем на базе Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Клонируйте Репозиторий
```bash
git clone https://github.com/ВАШ_ПОЛЬЗОВАТЕЛЬ/ZenithLinuxAssistant.git
cd ZenithLinuxAssistant
```

### 3. Установите Библиотеки
```bash
pip install -r requirements.txt
```

### 4. Запустите Приложение
```bash
python3 main.py
```

---

## 🛠️ Сборка собственного файла (Для Разработчиков)
Чтобы создать независимый исполняемый файл для вашей текущей операционной системы:

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --windowed --name "ZenithLinuxAssistant" --add-data "$(python3 -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" main.py
```
Скомпилированное приложение появится в папке `dist/`.

---

## 📝 Лицензия
Этот проект с открытым исходным кодом и абсолютно бесплатен. Будем рады вашему участию!
