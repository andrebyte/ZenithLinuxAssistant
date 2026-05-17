# 🌌 Zenith Linux Assistant

![Zenith Linux Banner](https://img.shields.io/badge/Zenith-Linux_Assistant-3b82f6?style=for-the-badge&logo=linux)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

> **Idiomas:** [English](README.md) | [Türkçe](README_TR.md) | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Русский](README_RU.md)

**Zenith Linux Assistant** es tu compañero definitivo diseñado para hacer que la transición de Windows a Linux sea perfecta. Monitorea las métricas de tu hardware, proporciona instalaciones con un solo clic para aplicaciones populares en varias distribuciones (Debian, Arch, Fedora), traduce errores de terminal al instante y soluciona errores comunes de Linux.

---

## ✨ Características
* **Panel de Hardware:** Monitorea tu sistema operativo, Kernel, CPU y RAM en tiempo real.
* **Instaladores de un Clic:** Copia los comandos exactos de instalación para aplicaciones como VS Code, Chrome, Spotify y VLC dependiendo de tu familia de Linux.
* **Traductor de Errores:** Pega cualquier error de terminal en inglés y obtén una traducción instantánea a tu idioma preferido usando `deep-translator`.
* **Solucionador de Problemas:** Soluciones de un clic para errores comunes (sin sonido, desconexiones de Wi-Fi, parpadeo de pantalla, bloqueos de paquetes).
* **Temas y Localización Dinámicos:** Cambia instantáneamente entre temas Claro/Oscuro y 5 idiomas de interfaz (EN, TR, ES, DE, RU) sin reiniciar.

---

## 🚀 Inicio Rápido (Binario Precompilado)
Si no deseas instalar Python o lidiar con el código fuente, puedes descargar el ejecutable directamente desde la pestaña **Releases**.

**Para usuarios de Linux:**
1. Descarga `ZenithLinuxAssistant` desde Releases.
2. Haz clic derecho en el archivo -> **Propiedades** -> **Permisos** -> Marca **"Permitir ejecutar el archivo como un programa"**.
3. ¡Haz doble clic para ejecutar!

---

## 💻 Instalación Manual (Ejecutar desde el Código Fuente)
Si el binario no funciona para tu distribución específica o si deseas ejecutarlo desde el código fuente, sigue estos pasos:

### 1. Instalar Requisitos Previos
Necesitas tener Python 3 y pip instalados en tu sistema.
Para sistemas basados en Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### 2. Clonar el Repositorio
```bash
git clone https://github.com/TU_USUARIO/ZenithLinuxAssistant.git
cd ZenithLinuxAssistant
```

### 3. Instalar Bibliotecas Requeridas
Instala los paquetes de python requeridos usando pip:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
```bash
python3 main.py
```

---

## 🛠️ Compilar el Binario tú mismo (Para Desarrolladores)
Para crear un ejecutable independiente para tu sistema operativo actual:

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --onefile --windowed --name "ZenithLinuxAssistant" --add-data "$(python3 -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))'):customtkinter/" main.py
```
La aplicación compilada se generará en la carpeta `dist/`.

---

## 📝 Licencia
Este proyecto es de código abierto y de uso gratuito. ¡Las contribuciones son bienvenidas!
