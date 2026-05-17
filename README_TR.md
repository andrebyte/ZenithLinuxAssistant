# 🌌 Zenith Linux Asistanı

![Zenith Linux Banner](https://img.shields.io/badge/Zenith-Linux_Assistant-3b82f6?style=for-the-badge&logo=linux)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

> **Diller:** [English](README.md) | [Türkçe](README_TR.md) | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

**Zenith Linux Asistanı**, Windows'tan Linux'a geçişi kusursuz hale getirmek için tasarlanmış nihai yardımcı aracınızdır. Donanım değerlerinizi izler, çeşitli Linux dağıtımlarına (Debian, Arch, Fedora) popüler uygulamaları tek tıkla kurmanızı sağlar, terminal hatalarını anında çevirir ve sık karşılaşılan sistem hatalarını (ses, wifi vb.) tek tıkla onarır.

---

## ✨ Özellikler
* **Donanım Paneli:** İşletim sisteminizi, Kernel sürümünüzü, CPU ve RAM kullanımınızı gerçek zamanlı izleyin.
* **Tek Tıkla Kurulum:** VS Code, Chrome, Spotify, VLC gibi uygulamaların dağıtımınıza (APT, DNF, Pacman) özel kurulum komutlarını anında kopyalayın.
* **Hata Çevirmeni:** Anlaşılmayan İngilizce terminal hatalarını yapıştırın ve `deep-translator` sayesinde anında kendi dilinize çevirin.
* **Hata Çözücü:** Sesi gelmeyen kulaklıklar, kopan Wi-Fi ağları, ekran yırtılmaları ve kilitlenen paket yöneticileri için tek tıkla çözüm komutları.
* **Dinamik Tema & Dil:** Uygulamayı yeniden başlatmaya gerek kalmadan Açık/Koyu tema ve 5 farklı dil (EN, TR, ES, DE, RU) arasında anında geçiş yapın.

---

## 🚀 Hızlı Başlangıç (Hazır Dosya)
Eğer Python kurmakla veya kodlarla uğraşmak istemiyorsanız, doğrudan **Releases (Sürümler)** sekmesinden çalıştırılabilir hazır dosyayı indirebilirsiniz.

**Linux Kullanıcıları İçin:**
1. `ZenithLinuxAssistant` dosyasını indirin.
2. Dosyaya sağ tıklayın -> **Özellikler** -> **İzinler** -> **"Dosyayı bir program gibi çalıştırmaya izin ver"** seçeneğini işaretleyin.
3. Çalıştırmak için çift tıklayın!

---

## 💻 Manuel Kurulum (Kaynak Koddan Çalıştırma)
Eğer hazır dosya (binary) sizin dağıtımınızda hata verirse veya uygulamayı kodlardan başlatmak isterseniz şu adımları izleyin:

### 1. Ön Gereksinimleri Kurun
Sisteminizde Python 3 ve pip kurulu olmalıdır.
Ubuntu/Debian tabanlı sistemler için:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Projeyi Bilgisayarınıza İndirin
```bash
git clone https://github.com/KULLANICI_ADINIZ/ZenithLinuxAssistant.git
cd ZenithLinuxAssistant
```

### 3. Gerekli Kütüphaneleri Kurun
```bash
pip install -r requirements.txt
```
*(Eğer sistem "externally managed environment" hatası verirse komutun sonuna `--break-system-packages` ekleyebilir veya bir sanal ortam (venv) oluşturabilirsiniz).*

### 4. Uygulamayı Başlatın
```bash
python3 main.py
```

---

## 🛠️ Kendiniz Paketlemek İsterseniz (Geliştiriciler İçin)
Uygulamayı mevcut işletim sisteminiz için tek parça `.exe` veya Linux executable dosyasına dönüştürmek için:

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --windowed --name "ZenithLinuxAssistant" --add-data "$(python3 -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" main.py
```
Oluşturulan uygulama dosyası `dist/` klasörü içerisinde yer alacaktır.

---

## 📝 Lisans
Bu proje tamamen açık kaynaklı ve ücretsizdir. Geliştirmelere ve katkılara açıktır!
