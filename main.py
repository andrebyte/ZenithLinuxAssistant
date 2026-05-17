#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zenith Linux Assistant - System Management & Translation Companion for Linux Beginners
Author: Antigravity AI
Description: A modern CustomTkinter GUI application that displays system info, installs
             popular applications with one click across different distribution families
             (Debian, Arch, Fedora), translates terminal errors in real-time, and
             supports live dynamic English/Turkish localization and theme configuration.
"""

import os
import sys
import platform
import subprocess
import threading
import random
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from deep_translator import GoogleTranslator

# CustomTkinter Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ZenithLinuxAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Active Language Settings ("tr" on startup as requested)
        self.active_lang = "tr"

        # Global Translation Dictionary
        self.translations = {
            "tr": {
                "app_title": "Zenith Linux Asistanı - Nihai Linux Yardımcınız",
                "sidebar_title": "🌌 ZENITH LINUX",
                "sidebar_subtitle": "Sistem ve Çeviri Kılavuzu",
                "menu_dashboard": "🖥️  Sistemim",
                "menu_debian": "🌀  Debian Dünyası",
                "menu_arch": "🦅  Arch Dünyası",
                "menu_fedora": "🎩  Fedora / RedHat",
                "menu_translator": "🌐  Hata Çevirmeni",
                "menu_commands": "⌨️  Temel Komutlar",
                "menu_fixes": "🔧  Ortak Çözümler",
                "menu_settings": "⚙️  Ayarlar",
                "status_title": "Algılanan Aile",
                
                # Tab 1: Dashboard
                "dashboard_welcome": "🚀 Zenith Linux Asistanına Hoş Geldiniz!",
                "dashboard_desc": "Linux sisteminizi ve donanımınızı izlemek, temel araçlara hızlıca erişmek için kontrol paneliniz.",
                "card_os": "🖥️ İşletim Sistemi",
                "card_kernel": "⚙️ Linux Çekirdeği (Kernel)",
                "card_cpu": "🧠 İşlemci (CPU)",
                "card_ram": "💾 Sistem Belleği (RAM)",
                "cpu_sub": "Tüm çekirdekler aktif ve stabil çalışıyor",
                "ram_sub": "Aktif bellek kullanım durumu",
                "fact_title": "💡 Linux Gerçeği:",
                "refresh_btn": "Yenile 🔄",
                "os_sub_family": "Aile: {family} Linux",
                "cpu_unknown": "Bilinmeyen İşlemci",
                "ram_unknown": "Bilgi Yok",
                
                # Distro Tabs Details
                "debian_title": "🌀 Debian & Ubuntu Dünyası",
                "debian_quote": "\"Ubuntu, Debian'ın en popüler ve uslu çocuğudur.\"",
                "debian_desc": "Debian ailesi; sağlamlığı, kararlılığı ve devasa paket havuzuyla bilinir. Masaüstü Linux dağıtımlarının yarısından fazlası bu sağlam temel üzerine kuruludur. Yeni başlayanlar için en güvenli limandır.",
                
                "arch_title": "🦅 Arch Linux Dünyası",
                "arch_quote": "\"'I use Arch by the way' sözünün doğduğu efsanevi topraklar!\"",
                "arch_desc": "Arch Linux, 'KISS' (Keep It Simple, Stupid) felsefesini benimser. Kullanıcıya tam kontrol verir; sisteminizi temelden parça parça kendiniz inşa edersiniz. Rolling release ile her zaman en güncel paketleri sunar.",
                
                "fedora_title": "🎩 Fedora & RedHat Dünyası",
                "fedora_quote": "\"Yeniliğin ve kurumsal gücün masaüstündeki yansıması.\"",
                "fedora_desc": "Fedora, Linus Torvalds'ın kişisel dağıtım tercihidir; en yeni teknolojileri (Wayland, PipeWire vb.) ilk getiren vizyoner bir platformdur. RedHat'in kurumsal gücüyle desteklenir.",
                
                "compatible_yes": "✓ Uyumlu Sistem: Bilgisayarınız {family} tabanlı. Butonlar doğrudan çalışacaktır!",
                "compatible_no": "⚠ Uyumsuz Sistem: Sisteminiz {family} tabanlı değil. Bu komutlar bilgisayarınızda çalışmayabilir!",
                
                "terminal_log_header": " Zenith Terminal Günlüğü\n---------------------------------------\nKomut kopyalama kayıtları ve talimatlar burada görünecektir.\n",
                "copy_btn_text": "Komutu Kopyala 📋",
                "app_copied_title": "Komut Kopyalandı",
                "app_copied_info": "'{command_str}' komutu başarıyla panoya kopyalandı!\n\nKurulumu çalıştırmak için terminalinizi açın (Ctrl+Alt+T) ve komutu yapıştırın.",
                "app_copied_log_header": "📋 Komut Kopyalandı: {app_name} Kurulumu\n",
                "app_copied_log_help": "💡 Hızlı Yardım & Talimatlar:\n",
                "app_copied_log_step1": " 1. Kısayolu kullanarak terminalinizi açın: Ctrl + Alt + T\n",
                "app_copied_log_step2": " 2. Kopyalanan komutu yapıştırın (Sağ Tık -> Yapıştır, veya Ctrl + Shift + V)\n",
                "app_copied_log_step3": " 3. Enter'a basın, sistem şifrenizi girin ve kurulumun bitmesini bekleyin!\n",
                
                # Popular Applications translation
                "app_chrome_name": "Chromium Tarayıcı",
                "app_chrome_desc": "Google Chrome'un açık kaynaklı temeli, hızlı ve güvenli.",
                "app_discord_name": "Discord",
                "app_discord_desc": "Oyuncular ve topluluklar için sesli ve yazılı sohbet uygulaması.",
                "app_steam_name": "Steam",
                "app_steam_desc": "Linux'ta binlerce oyuna açılan mükemmel kapı.",
                "app_vlc_name": "VLC Medya Oynatıcı",
                "app_vlc_desc": "Her şeyi oynatan evrensel medya oynatıcısı.",
                "app_vscode_name": "Visual Studio Code",
                "app_vscode_desc": "Geliştiriciler için en popüler kod düzenleyici.",
                "app_spotify_name": "Spotify Müzik",
                "app_spotify_desc": "Sisteminizde milyonlarca şarkı ve podcast çalın.",
                "app_libreoffice_name": "LibreOffice Paketi",
                "app_libreoffice_desc": "Microsoft Office'in yerini alan güçlü ve ücretsiz ofis paketi.",

                # Tab 5: Translator
                "ceviri_title": "🌐 Evrensel Hata & Belge Çevirmeni",
                "ceviri_desc": "İngilizce hata loglarını veya yabancı belgeleri buraya yapıştırın. GoogleTranslator motorunu kullanarak anında, tamamen ücretsiz ve sınırsız bir şekilde çevirin.",
                "ceviri_source": "🌐 Kaynak Metin / Hata Kodu (Otomatik Algıla):",
                "ceviri_source_placeholder": "İngilizce hata günlüğünüzü veya komut çıktınızı buraya yapıştırın...\n\nÖrnek:\ndpkg: error processing package python3 (--configure):\n dependency problems - leaving unconfigured",
                "ceviri_result_placeholder": "Çeviri sonucu burada görünecek...",
                "ceviri_target_lang": "🎯 Hedef Dil:",
                "ceviri_btn_translate": "Hızlı Çevir 🚀",
                "ceviri_btn_clear": "Temizle 🧹",
                "ceviri_btn_copy": "Çeviriyi Kopyala 📋",
                "ceviri_connecting": "Bağlanıyor...",
                "ceviri_translating": "Çevriliyor... ⏳",
                "ceviri_success": "✓ Çeviri Başarılı!",
                "ceviri_copied": "📋 Panoya Kopyalandı!",
                "ceviri_warning_title": "Uyarı",
                "ceviri_warning_empty": "Çeviri Hatası: Lütfen çevrilecek metni girin!",
                "ceviri_warning_no_translation": "Kopyalanacak çeviri bulunamadı!",
                "ceviri_conn_error": "✗ Bağlantı Hatası!",
                "ceviri_error_desc": "Çeviri motoruna bağlanılamadı. Lütfen internet bağlantınızı kontrol edin.\nHata: {e}",

                # Tab 6: Basic Commands
                "commands_title": " Lifesaver Temel Linux Komutları",
                "commands_desc": "Linux terminalinden korkmayın! En çok ihtiyaç duyacağınız temel komutları kategorize ettik. Kopyalama butonlarını kullanarak anında kopyalayabilirsiniz.",
                "cat_files": "📁 Dosya ve Dizin İşlemleri",
                "cat_resources": "⚙️ Sistem Bilgisi ve Kaynaklar",
                "cat_packages": "📦 Paket ve Güncelleme Yönetimi (Sisteminizle uyumlu)",
                "cat_network": "🌐 Ağ ve İnternet Kontrolü",
                "cat_shortcuts": "⚡ Hayat Kurtaran Kısayollar ve Sıcak Tuşlar",
                
                # Command Details
                "cmd_ls_desc": "Dosyaları ve klasörleri listeler.",
                "cmd_cd_desc": "Mevcut dizini değiştirir.",
                "cmd_mkdir_desc": "Yeni bir klasör oluşturur.",
                "cmd_rm_desc": "Dosyaları/klasörleri güvenli bir şekilde siler.",
                "cmd_df_desc": "Sürücü alanı kullanımını gösterir.",
                "cmd_free_desc": "Aktif RAM kullanımını gösterir.",
                "cmd_uname_desc": "Çalışan işletim sistemi çekirdeğini gösterir.",
                "cmd_update_desc": "Tüm paketleri yükseltir.",
                "cmd_install_desc": "Yeni yazılım yükler.",
                "cmd_vscode_desc": "Visual Studio Code düzenleyicisini kurar.",
                "cmd_ping_desc": "Ağ gecikmesini test eder.",
                "cmd_ipa_desc": "Aktif IP adreslerini listeler.",
                "cmd_altf2_desc": "Uygulamaları anında çalıştırmak için hızlı komut kutusunu açar.",
                "cmd_ctrlaltt_desc": "Anında yeni bir terminal penceresi açar.",
                "cmd_ctrlshiftc_desc": "Terminalden seçilen metni kopyalar.",
                "cmd_ctrlshiftv_desc": "Kopyalanan metni terminale yapıştırır.",
                "cmd_super_desc": "Uygulama arama menüsünü açar.",
                "cmd_ctrlaltl_desc": "Masaüstü ekranınızı anında kilitler.",
                "cmd_ctrlaltd_desc": "Masaüstünü göstermek için tüm pencereleri simge durumuna küçültür.",
                "cmd_alttab_desc": "Açık uygulamalar arasında geçiş yapar.",
                "cmd_ctrlesc_desc": "Sistem işlem/görev yöneticisini açar.",
                "cmd_ctrlaltarrows_desc": "Aktif çalışma alanları arasında geçiş yapar.",

                # Tab 7: Troubleshooter
                "fixes_title": "🔧 Hata Çözücü ve Geçiş Düzeltmeleri",
                "fixes_desc": "Windows'tan geçenlerin en çok karşılaştığı yaygın Linux sorunlarına tek tıkla kopyalanabilir terminal çözümleri.",
                "cat_fixes_audio": "🔊 Ses ve Hoparlör Sorunları",
                "cat_fixes_network": "🌐 Kablosuz Ağ ve İnternet Sorunları",
                "cat_fixes_graphics": "🖥️ Grafik ve Ekran Sorunları",
                "cat_fixes_maintenance": "📦 Sistem Bakımı ve Kilitlenme Hataları",
                
                # Troubleshooter details
                "fix_pavucontrol_desc": "Ses profillerini yapılandırın, stereoyu dengeleyin ve dijital çıkışları seçin.",
                "fix_alsamixer_desc": "Sessize alınmış donanım kanallarını açmak için terminal mikserini açın.",
                "fix_restart_audio_desc": "Donan kartları düzeltmek için Pipewire/PulseAudio servislerini yeniden başlatın.",
                "fix_restart_nm_desc": "Donan Wi-Fi veya ağ bağlantılarını düzeltmek için ağ servisini yeniden başlatın.",
                "fix_flush_dns_desc": "Geçersiz web adres çözümlerini düzeltmek için yerel DNS önbelleğini temizleyin.",
                "fix_auto_sync_desc": "Ekran titremesini çözmek için aktif ekran yapılandırmasını eşitlemeye zorlayın.",
                "fix_list_gpu_desc": "Kullanımdaki aktif GPU modelini ve mevcut çekirdek modüllerini kontrol edin.",
                "fix_unlock_pkg_desc": "Paket yönetimi işlemlerini engelleyen eski veritabanı kilitlerini kaldırın.",
                "fix_clean_cache_desc": "Disk alanı kazanmak için indirilen paket arşivlerini temizleyin.",

                # Tab 8: Settings
                "settings_title": "⚙️ Uygulama Ayarları",
                "settings_desc": "Zenith Linux Asistanı uygulamasının görünüm, tema ve dil tercihlerini buradan özelleştirin.",
                "setting_theme": "Uygulama Teması (App Theme):",
                "setting_lang": "Arayüz Dili (App Language):",
                "theme_dark": "Koyu (Dark)",
                "theme_light": "Açık (Light)",
                "theme_system": "Sistem (System)",
                "dialog_copied_title": "Kopyalandı",
                "dialog_copied_body": "'{command_str}' komutu başarıyla panoya kopyalandı!"
            },

            "es": {
                "app_title": "Zenith Linux Assistant - Tu Compañero Definitivo de Linux",
                "sidebar_title": "🌌 ZENITH LINUX",
                "sidebar_subtitle": "Guía de Sistema y Traducción",
                "menu_dashboard": "🖥️  Panel Principal",
                "menu_debian": "🌀  Mundo Debian",
                "menu_arch": "🦅  Mundo Arch",
                "menu_fedora": "🎩  Mundo Fedora",
                "menu_translator": "🌐  Traductor de Errores",
                "menu_commands": "⌨️  Comandos Básicos",
                "menu_fixes": "🔧  Soluciones Comunes",
                "menu_settings": "⚙️  Ajustes",
                "status_title": "Familia Detectada",
                "dashboard_welcome": "🚀 ¡Bienvenido a Zenith Linux Assistant! 🌌",
                "dashboard_desc": "Tu panel central para monitorear métricas de hardware y acceder a herramientas.",
                "card_os": "🖥️ Sistema Operativo",
                "card_kernel": "⚙️ Kernel Linux",
                "card_cpu": "🧠 Procesador (CPU)",
                "card_ram": "💾 Memoria del Sistema (RAM)",
                "cpu_sub": "Todos los núcleos están activos y estables",
                "ram_sub": "Estado de uso activo de memoria",
                "fact_title": "💡 Dato de Linux:",
                "refresh_btn": "Actualizar 🔄",
                "os_sub_family": "Familia: {family} Linux",
                "cpu_unknown": "Procesador Desconocido",
                "ram_unknown": "Sin Información Disponible",
                "debian_title": "🌀 Mundo Debian & Ubuntu",
                "debian_quote": "\"Ubuntu es el hijo más popular y educado de Debian.\"",
                "debian_desc": "La familia Debian es conocida por su robustez, estabilidad y depósito masivo de paquetes. Es el puerto más seguro para principiantes.",
                "arch_title": "🦅 Mundo Arch Linux",
                "arch_quote": "\"¡Las tierras legendarias donde nació la frase 'I use Arch by the way'!\"",
                "arch_desc": "Arch Linux abraza la filosofía 'KISS'. Te da control total; construyes tu sistema bloque a bloque desde cero.",
                "fedora_title": "🎩 Mundo Fedora & RedHat",
                "fedora_quote": "\"El reflejo de la innovación y el poder empresarial en el escritorio.\"",
                "fedora_desc": "Fedora es la elección de Linus Torvalds, una plataforma visionaria que ofrece tecnologías de vanguardia (Wayland, PipeWire).",
                "compatible_yes": "✓ Sistema Compatible: ¡Tu sistema se basa en {family}!",
                "compatible_no": "⚠ Sistema Incompatible: Estos comandos pueden fallar en tu sistema.",
                "terminal_log_header": " Registro de Terminal Zenith\n---------------------------------------\nAquí aparecerán los comandos.\n",
                "copy_btn_text": "Copiar Comando 📋",
                "app_copied_title": "Comando Copiado",
                "app_copied_info": "¡El comando '{command_str}' se ha copiado con éxito!",
                "app_copied_log_header": "📋 Comando Copiado: Instalar {app_name}\n",
                "app_copied_log_help": "💡 Ayuda rápida:\n",
                "app_copied_log_step1": " 1. Abre tu terminal (Ctrl + Alt + T)\n",
                "app_copied_log_step2": " 2. Pega el comando copiado (Ctrl + Shift + V)\n",
                "app_copied_log_step3": " 3. ¡Presiona Enter, escribe tu contraseña y listo!\n",
                "app_chrome_name": "Navegador Chromium",
                "app_chrome_desc": "El núcleo de código abierto de Google Chrome, rápido y seguro.",
                "app_discord_name": "Discord",
                "app_discord_desc": "Aplicación de chat para jugadores y comunidades.",
                "app_steam_name": "Steam",
                "app_steam_desc": "La puerta de entrada a miles de juegos en Linux.",
                "app_vlc_name": "Reproductor VLC",
                "app_vlc_desc": "El reproductor multimedia que reproduce absolutamente todo.",
                "app_vscode_name": "Visual Studio Code",
                "app_vscode_desc": "El editor de código más popular para desarrolladores.",
                "app_spotify_name": "Spotify Music",
                "app_spotify_desc": "Reproduce millones de canciones en tu sistema.",
                "app_libreoffice_name": "LibreOffice Suite",
                "app_libreoffice_desc": "Poderosa suite ofimática gratuita (reemplazo de MS Office).",
                "ceviri_title": "🌐 Traductor Universal de Errores",
                "ceviri_desc": "Pega registros de errores en inglés aquí. Tradúcelos al instante gratis usando GoogleTranslator.",
                "ceviri_source": "🌐 Texto de origen (Auto-Detectado):",
                "ceviri_source_placeholder": "Pega tu error en inglés aquí...",
                "ceviri_result_placeholder": "El resultado de la traducción aparecerá aquí...",
                "ceviri_target_lang": "🎯 Idioma de Destino:",
                "ceviri_btn_translate": "Traducir 🚀",
                "ceviri_btn_clear": "Limpiar 🧹",
                "ceviri_btn_copy": "Copiar 📋",
                "ceviri_connecting": "Conectando...",
                "ceviri_translating": "Traduciendo... ⏳",
                "ceviri_success": "✓ ¡Traducción Exitosa!",
                "ceviri_copied": "📋 ¡Copiado al Portapapeles!",
                "ceviri_warning_title": "Advertencia",
                "ceviri_warning_empty": "¡Ingresa texto para traducir!",
                "ceviri_warning_no_translation": "¡No se encontró traducción para copiar!",
                "ceviri_conn_error": "✗ ¡Error de Conexión!",
                "ceviri_error_desc": "No se pudo conectar al motor de traducción.\nError: {e}",
                "commands_title": "⌨️ Comandos Básicos de Linux",
                "commands_desc": "¡No dejes que la terminal te intimide! Clasificamos los comandos que más necesitarás.",
                "cat_files": "📁 Operaciones de Archivos",
                "cat_resources": "⚙️ Recursos del Sistema",
                "cat_packages": "📦 Gestión de Paquetes",
                "cat_network": "🌐 Control de Redes",
                "cat_shortcuts": "⚡ Atajos Salvavidas",
                "cmd_ls_desc": "Lista archivos y carpetas.",
                "cmd_cd_desc": "Cambia la carpeta actual.",
                "cmd_mkdir_desc": "Crea una nueva carpeta.",
                "cmd_rm_desc": "Elimina archivos de forma segura.",
                "cmd_df_desc": "Muestra el uso del disco.",
                "cmd_free_desc": "Muestra el uso de RAM activo.",
                "cmd_uname_desc": "Muestra el kernel operativo.",
                "cmd_update_desc": "Actualiza todos los paquetes.",
                "cmd_install_desc": "Instala un nuevo software.",
                "cmd_vscode_desc": "Instala el editor de código VS Code.",
                "cmd_ping_desc": "Prueba la latencia de la red.",
                "cmd_ipa_desc": "Lista de direcciones IP activas.",
                "cmd_altf2_desc": "Abre un cuadro rápido de comandos.",
                "cmd_ctrlaltt_desc": "Abre una nueva terminal al instante.",
                "cmd_ctrlshiftc_desc": "Copia el texto seleccionado de la terminal.",
                "cmd_ctrlshiftv_desc": "Pega el texto copiado en la terminal.",
                "cmd_super_desc": "Abre el menú de búsqueda de aplicaciones.",
                "cmd_ctrlaltl_desc": "Bloquea la pantalla al instante.",
                "cmd_ctrlaltd_desc": "Minimiza las ventanas.",
                "cmd_alttab_desc": "Cambia entre aplicaciones abiertas.",
                "cmd_ctrlesc_desc": "Abre el monitor de procesos.",
                "cmd_ctrlaltarrows_desc": "Cambia las pantallas activas.",
                "fixes_title": "🔧 Soluciones a Problemas Comunes",
                "fixes_desc": "Soluciones con un clic a los errores más comunes.",
                "cat_fixes_audio": "🔊 Problemas de Audio",
                "cat_fixes_network": "🌐 Problemas de Red WiFi",
                "cat_fixes_graphics": "🖥️ Errores de Pantalla",
                "cat_fixes_maintenance": "📦 Mantenimiento y Bloqueos",
                "fix_pavucontrol_desc": "Configura perfiles de audio y equilibra estéreos.",
                "fix_alsamixer_desc": "Abre el mezclador para desmutear canales.",
                "fix_restart_audio_desc": "Reinicia los demonios de audio para arreglar tarjetas congeladas.",
                "fix_restart_nm_desc": "Reinicia los servicios de red para arreglar Wi-Fi.",
                "fix_flush_dns_desc": "Limpia la caché del resolvedor de DNS.",
                "fix_auto_sync_desc": "Sincroniza la pantalla para resolver parpadeos.",
                "fix_list_gpu_desc": "Verifica el modelo de GPU activo.",
                "fix_unlock_pkg_desc": "Elimina bloqueos de bases de datos obsoletos.",
                "fix_clean_cache_desc": "Elimina archivos descargados para liberar espacio.",
                "settings_title": "⚙️ Ajustes de la Aplicación",
                "settings_desc": "Personaliza la apariencia, el tema y los idiomas de Zenith Linux Assistant.",
                "setting_theme": "Tema de la aplicación:",
                "setting_lang": "Idioma de la interfaz:",
                "theme_dark": "Oscuro (Dark)",
                "theme_light": "Claro (Light)",
                "theme_system": "Sistema (System)",
                "dialog_copied_title": "Copiado",
                "dialog_copied_body": "¡El comando '{command_str}' se copió al portapapeles!"
            },
            "de": {
                "app_title": "Zenith Linux Assistent - Ihr Ultimativer Linux Begleiter",
                "sidebar_title": "🌌 ZENITH LINUX",
                "sidebar_subtitle": "System & Übersetzungsguide",
                "menu_dashboard": "🖥️  Dashboard",
                "menu_debian": "🌀  Debian Welt",
                "menu_arch": "🦅  Arch Welt",
                "menu_fedora": "🎩  Fedora Welt",
                "menu_translator": "🌐  Fehlerübersetzer",
                "menu_commands": "⌨️  Grundbefehle",
                "menu_fixes": "🔧  Gemeinsame Lösungen",
                "menu_settings": "⚙️  Einstellungen",
                "status_title": "Erkannte Familie",
                "dashboard_welcome": "🚀 Willkommen beim Zenith Linux Assistenten! 🌌",
                "dashboard_desc": "Ihr zentrales Dashboard zur Überwachung von Hardware-Metriken.",
                "card_os": "🖥️ Betriebssystem",
                "card_kernel": "⚙️ Linux Kernel",
                "card_cpu": "🧠 Prozessor (CPU)",
                "card_ram": "💾 Arbeitsspeicher (RAM)",
                "cpu_sub": "Alle Kerne sind aktiv und stabil",
                "ram_sub": "Aktive Speichernutzung",
                "fact_title": "💡 Linux-Fakt:",
                "refresh_btn": "Aktualisieren 🔄",
                "os_sub_family": "Familie: {family} Linux",
                "cpu_unknown": "Unbekannter Prozessor",
                "ram_unknown": "Keine Informationen",
                "debian_title": "🌀 Debian & Ubuntu Welt",
                "debian_quote": "\"Ubuntu ist das beliebteste und artigste Kind von Debian.\"",
                "debian_desc": "Die Debian-Familie ist bekannt für ihre Robustheit und Stabilität. Der sicherste Hafen für Anfänger.",
                "arch_title": "🦅 Arch Linux Welt",
                "arch_quote": "\"Das legendäre Land der Phrase 'I use Arch by the way'!\"",
                "arch_desc": "Arch Linux umfasst die 'KISS'-Philosophie. Sie haben die volle Kontrolle über das System.",
                "fedora_title": "🎩 Fedora & RedHat Welt",
                "fedora_quote": "\"Spiegelbild der Innovation auf dem Desktop.\"",
                "fedora_desc": "Fedora ist die Wahl von Linus Torvalds, eine visionäre Plattform für neueste Technologien.",
                "compatible_yes": "✓ Kompatibles System: Ihr Computer ist {family}-basiert!",
                "compatible_no": "⚠ Inkompatibles System: Diese Befehle könnten fehlschlagen!",
                "terminal_log_header": " Zenith Terminal Protokoll\n---------------------------------------\nBefehle werden hier angezeigt.\n",
                "copy_btn_text": "Befehl Kopieren 📋",
                "app_copied_title": "Befehl kopiert",
                "app_copied_info": "Der Befehl '{command_str}' wurde erfolgreich kopiert!",
                "app_copied_log_header": "📋 Kopierter Befehl: {app_name} installieren\n",
                "app_copied_log_help": "💡 Schnelle Hilfe:\n",
                "app_copied_log_step1": " 1. Öffnen Sie Ihr Terminal (Strg + Alt + T)\n",
                "app_copied_log_step2": " 2. Fügen Sie den Befehl ein (Strg + Umschalt + V)\n",
                "app_copied_log_step3": " 3. Drücken Sie Enter, geben Sie Ihr Passwort ein!\n",
                "app_chrome_name": "Chromium Browser",
                "app_chrome_desc": "Der Open-Source-Kern von Google Chrome, schnell und sicher.",
                "app_discord_name": "Discord",
                "app_discord_desc": "Chat-Anwendung für Gamer und Communities.",
                "app_steam_name": "Steam",
                "app_steam_desc": "Das ultimative Tor zu Tausenden von Spielen unter Linux.",
                "app_vlc_name": "VLC Media Player",
                "app_vlc_desc": "Der universelle Mediaplayer, der absolut alles abspielt.",
                "app_vscode_name": "Visual Studio Code",
                "app_vscode_desc": "Der beliebteste Code-Editor für Entwickler.",
                "app_spotify_name": "Spotify Music",
                "app_spotify_desc": "Spielen Sie Millionen von Songs und Podcasts ab.",
                "app_libreoffice_name": "LibreOffice Suite",
                "app_libreoffice_desc": "Leistungsstarkes kostenloses Office-Paket (MS Office Ersatz).",
                "ceviri_title": "🌐 Universeller Fehlerübersetzer",
                "ceviri_desc": "Fügen Sie englische Fehlerprotokolle hier ein. Übersetzen Sie diese sofort und kostenlos mit GoogleTranslator.",
                "ceviri_source": "🌐 Quelltext / Fehlercode:",
                "ceviri_source_placeholder": "Fügen Sie Ihr englisches Fehlerprotokoll hier ein...",
                "ceviri_result_placeholder": "Das Übersetzungsergebnis wird hier angezeigt...",
                "ceviri_target_lang": "🎯 Zielsprache:",
                "ceviri_btn_translate": "Übersetzen 🚀",
                "ceviri_btn_clear": "Löschen 🧹",
                "ceviri_btn_copy": "Kopieren 📋",
                "ceviri_connecting": "Verbinden...",
                "ceviri_translating": "Übersetzen... ⏳",
                "ceviri_success": "✓ Übersetzung erfolgreich!",
                "ceviri_copied": "📋 In die Zwischenablage kopiert!",
                "ceviri_warning_title": "Warnung",
                "ceviri_warning_empty": "Bitte Text eingeben!",
                "ceviri_warning_no_translation": "Keine Übersetzung zum Kopieren gefunden!",
                "ceviri_conn_error": "✗ Verbindungsfehler!",
                "ceviri_error_desc": "Fehler beim Verbinden mit der Übersetzungs-Engine.\nFehler: {e}",
                "commands_title": "⌨️ Linux Basisbefehle",
                "commands_desc": "Lassen Sie sich nicht einschüchtern! Die wichtigsten Befehle zum sofortigen Kopieren.",
                "cat_files": "📁 Datei- und Ordneroperationen",
                "cat_resources": "⚙️ Systeminformationen",
                "cat_packages": "📦 Paketverwaltung",
                "cat_network": "🌐 Netzwerkkontrolle",
                "cat_shortcuts": "⚡ Wichtige Tastenkombinationen",
                "cmd_ls_desc": "Listet Dateien und Ordner auf.",
                "cmd_cd_desc": "Ordner wechseln.",
                "cmd_mkdir_desc": "Neuen Ordner erstellen.",
                "cmd_rm_desc": "Dateien sicher löschen.",
                "cmd_df_desc": "Laufwerksspeicherplatz anzeigen.",
                "cmd_free_desc": "Aktive RAM-Auslastung anzeigen.",
                "cmd_uname_desc": "Betriebssystem-Kernel anzeigen.",
                "cmd_update_desc": "Alle Pakete aktualisieren.",
                "cmd_install_desc": "Neue Software installieren.",
                "cmd_vscode_desc": "VS Code Editor installieren.",
                "cmd_ping_desc": "Netzwerklatenz testen.",
                "cmd_ipa_desc": "Aktive IP-Adressen auflisten.",
                "cmd_altf2_desc": "Schnelles Befehlsfeld öffnen.",
                "cmd_ctrlaltt_desc": "Terminal sofort öffnen.",
                "cmd_ctrlshiftc_desc": "Markierten Text kopieren.",
                "cmd_ctrlshiftv_desc": "Kopierten Text einfügen.",
                "cmd_super_desc": "Anwendungssuchmenü öffnen.",
                "cmd_ctrlaltl_desc": "Bildschirm sofort sperren.",
                "cmd_ctrlaltd_desc": "Alle Fenster minimieren.",
                "cmd_alttab_desc": "Zwischen Apps wechseln.",
                "cmd_ctrlesc_desc": "Systemmonitor öffnen.",
                "cmd_ctrlaltarrows_desc": "Arbeitsbereiche wechseln.",
                "fixes_title": "🔧 Problembehandlung & Fixes",
                "fixes_desc": "Ein-Klick-Lösungen für häufige Linux-Probleme.",
                "cat_fixes_audio": "🔊 Audio- & Soundprobleme",
                "cat_fixes_network": "🌐 WLAN- & Netzwerkprobleme",
                "cat_fixes_graphics": "🖥️ Anzeige- & Grafikfehler",
                "cat_fixes_maintenance": "📦 Systemwartung & Sperren",
                "fix_pavucontrol_desc": "Audioprofile konfigurieren und digitale Ausgänge wählen.",
                "fix_alsamixer_desc": "Terminal-Mixer öffnen, um stummgeschaltete Kanäle zu aktivieren.",
                "fix_restart_audio_desc": "Audio-Dienste neu starten, um Soundprobleme zu beheben.",
                "fix_restart_nm_desc": "Netzwerkdienste neu starten, um WLAN zu reparieren.",
                "fix_flush_dns_desc": "Lokalen DNS-Cache leeren.",
                "fix_auto_sync_desc": "Bildschirmsynchronisation erzwingen gegen Flackern.",
                "fix_list_gpu_desc": "Aktives GPU-Modell überprüfen.",
                "fix_unlock_pkg_desc": "Veraltete Datenbank-Sperren der Paketverwaltung entfernen.",
                "fix_clean_cache_desc": "Heruntergeladene Paketarchive löschen, um Platz zu sparen.",
                "settings_title": "⚙️ App Einstellungen",
                "settings_desc": "Passen Sie Design, Thema und Sprachen von Zenith Linux an.",
                "setting_theme": "App-Thema:",
                "setting_lang": "App-Sprache:",
                "theme_dark": "Dunkel (Dark)",
                "theme_light": "Hell (Light)",
                "theme_system": "System",
                "dialog_copied_title": "Kopiert",
                "dialog_copied_body": "Der Befehl '{command_str}' wurde in die Zwischenablage kopiert!"
            },
            "ru": {
                "app_title": "Zenith Linux Ассистент - Ваш лучший компаньон Linux",
                "sidebar_title": "🌌 ZENITH LINUX",
                "sidebar_subtitle": "Система и Переводчик",
                "menu_dashboard": "🖥️  Панель управления",
                "menu_debian": "🌀  Мир Debian",
                "menu_arch": "🦅  Мир Arch",
                "menu_fedora": "🎩  Мир Fedora",
                "menu_translator": "🌐  Переводчик ошибок",
                "menu_commands": "⌨️  Базовые команды",
                "menu_fixes": "🔧  Решения проблем",
                "menu_settings": "⚙️  Настройки",
                "status_title": "Обнаруженная система",
                "dashboard_welcome": "🚀 Добро пожаловать в Zenith Linux! 🌌",
                "dashboard_desc": "Ваша центральная панель для мониторинга системы.",
                "card_os": "🖥️ Операционная система",
                "card_kernel": "⚙️ Ядро Linux",
                "card_cpu": "🧠 Процессор (CPU)",
                "card_ram": "💾 Оперативная память (RAM)",
                "cpu_sub": "Все ядра активны и работают стабильно",
                "ram_sub": "Активное использование памяти",
                "fact_title": "💡 Факт о Linux:",
                "refresh_btn": "Обновить 🔄",
                "os_sub_family": "Семейство: {family} Linux",
                "cpu_unknown": "Неизвестный процессор",
                "ram_unknown": "Нет информации",
                "debian_title": "🌀 Мир Debian и Ubuntu",
                "debian_quote": "\"Ubuntu - самый популярный и послушный ребенок Debian.\"",
                "debian_desc": "Семейство Debian известно своей стабильностью и огромным репозиторием. Это самая безопасная гавань для новичков.",
                "arch_title": "🦅 Мир Arch Linux",
                "arch_quote": "\"Легендарные земли, где родилась фраза 'I use Arch by the way'!\"",
                "arch_desc": "Arch Linux дает вам полный контроль; вы строите свою систему блок за блоком с нуля.",
                "fedora_title": "🎩 Мир Fedora и RedHat",
                "fedora_quote": "\"Отражение инноваций и корпоративной мощи на рабочем столе.\"",
                "fedora_desc": "Fedora - это личный выбор Линуса Торвальдса, платформа для передовых технологий.",
                "compatible_yes": "✓ Совместимая система: Ваш компьютер основан на {family}!",
                "compatible_no": "⚠ Несовместимая система: Эти команды могут не работать!",
                "terminal_log_header": " Журнал Терминала Zenith\n---------------------------------------\nЗдесь будут появляться команды.\n",
                "copy_btn_text": "Копировать 📋",
                "app_copied_title": "Команда скопирована",
                "app_copied_info": "Команда '{command_str}' успешно скопирована!",
                "app_copied_log_header": "📋 Команда скопирована: Установить {app_name}\n",
                "app_copied_log_help": "💡 Быстрая помощь:\n",
                "app_copied_log_step1": " 1. Откройте ваш терминал (Ctrl + Alt + T)\n",
                "app_copied_log_step2": " 2. Вставьте скопированную команду (Ctrl + Shift + V)\n",
                "app_copied_log_step3": " 3. Нажмите Enter и введите пароль!\n",
                "app_chrome_name": "Chromium Browser",
                "app_chrome_desc": "Свободное ядро Google Chrome, быстрое и безопасное.",
                "app_discord_name": "Discord",
                "app_discord_desc": "Голосовой и текстовый чат для геймеров и сообществ.",
                "app_steam_name": "Steam",
                "app_steam_desc": "Лучший портал к тысячам игр на Linux.",
                "app_vlc_name": "VLC Media Player",
                "app_vlc_desc": "Универсальный медиаплеер, который воспроизводит абсолютно все.",
                "app_vscode_name": "Visual Studio Code",
                "app_vscode_desc": "Самый популярный редактор кода для разработчиков.",
                "app_spotify_name": "Spotify Music",
                "app_spotify_desc": "Слушайте миллионы песен и подкастов в вашей системе.",
                "app_libreoffice_name": "LibreOffice Suite",
                "app_libreoffice_desc": "Мощный бесплатный офисный пакет (замена MS Office).",
                "ceviri_title": "🌐 Универсальный переводчик ошибок",
                "ceviri_desc": "Вставьте логи ошибок на английском здесь. Переводите их мгновенно с помощью GoogleTranslator.",
                "ceviri_source": "🌐 Исходный текст (Автоопределение):",
                "ceviri_source_placeholder": "Вставьте ошибку на английском языке здесь...",
                "ceviri_result_placeholder": "Результат перевода появится здесь...",
                "ceviri_target_lang": "🎯 Язык перевода:",
                "ceviri_btn_translate": "Перевести 🚀",
                "ceviri_btn_clear": "Очистить 🧹",
                "ceviri_btn_copy": "Копировать 📋",
                "ceviri_connecting": "Подключение...",
                "ceviri_translating": "Перевод... ⏳",
                "ceviri_success": "✓ Перевод успешен!",
                "ceviri_copied": "📋 Скопировано в буфер!",
                "ceviri_warning_title": "Предупреждение",
                "ceviri_warning_empty": "Пожалуйста, введите текст!",
                "ceviri_warning_no_translation": "Нет перевода для копирования!",
                "ceviri_conn_error": "✗ Ошибка соединения!",
                "ceviri_error_desc": "Не удалось подключиться к движку перевода.\nОшибка: {e}",
                "commands_title": "⌨️ Базовые команды Linux",
                "commands_desc": "Не бойтесь терминала! Команды, которые вам пригодятся больше всего.",
                "cat_files": "📁 Работа с файлами и папками",
                "cat_resources": "⚙️ Системная информация",
                "cat_packages": "📦 Управление пакетами",
                "cat_network": "🌐 Сеть и Интернет",
                "cat_shortcuts": "⚡ Полезные горячие клавиши",
                "cmd_ls_desc": "Список файлов и папок.",
                "cmd_cd_desc": "Сменить папку.",
                "cmd_mkdir_desc": "Создать новую папку.",
                "cmd_rm_desc": "Удалить файлы безопасно.",
                "cmd_df_desc": "Показать использование диска.",
                "cmd_free_desc": "Показать использование ОЗУ.",
                "cmd_uname_desc": "Показать ядро ОС.",
                "cmd_update_desc": "Обновить все пакеты.",
                "cmd_install_desc": "Установить новую программу.",
                "cmd_vscode_desc": "Установить VS Code.",
                "cmd_ping_desc": "Проверить сетевую задержку.",
                "cmd_ipa_desc": "Список активных IP-адресов.",
                "cmd_altf2_desc": "Открыть панель быстрого запуска.",
                "cmd_ctrlaltt_desc": "Мгновенно открыть терминал.",
                "cmd_ctrlshiftc_desc": "Скопировать выделенный текст.",
                "cmd_ctrlshiftv_desc": "Вставить скопированный текст.",
                "cmd_super_desc": "Открыть меню поиска приложений.",
                "cmd_ctrlaltl_desc": "Мгновенно заблокировать экран.",
                "cmd_ctrlaltd_desc": "Свернуть все окна.",
                "cmd_alttab_desc": "Переключение между окнами.",
                "cmd_ctrlesc_desc": "Открыть монитор процессов.",
                "cmd_ctrlaltarrows_desc": "Переключение рабочих мест.",
                "fixes_title": "🔧 Устранение неполадок",
                "fixes_desc": "Решения частых проблем одним кликом.",
                "cat_fixes_audio": "🔊 Проблемы со звуком",
                "cat_fixes_network": "🌐 Проблемы с Wi-Fi и сетью",
                "cat_fixes_graphics": "🖥️ Ошибки экрана и графики",
                "cat_fixes_maintenance": "📦 Обслуживание и блокировки",
                "fix_pavucontrol_desc": "Настроить аудио профили и цифровые выходы.",
                "fix_alsamixer_desc": "Открыть терминальный микшер.",
                "fix_restart_audio_desc": "Перезапустить аудио службы.",
                "fix_restart_nm_desc": "Перезапустить службы сети для починки Wi-Fi.",
                "fix_flush_dns_desc": "Очистить локальный кэш DNS.",
                "fix_auto_sync_desc": "Принудительно синхронизировать экран против мерцания.",
                "fix_list_gpu_desc": "Проверить активную модель GPU.",
                "fix_unlock_pkg_desc": "Удалить старые блокировки базы пакетов.",
                "fix_clean_cache_desc": "Очистить кэш загруженных пакетов.",
                "settings_title": "⚙️ Настройки приложения",
                "settings_desc": "Настройте тему и языки Zenith Linux Assistant.",
                "setting_theme": "Тема приложения:",
                "setting_lang": "Язык интерфейса:",
                "theme_dark": "Темная (Dark)",
                "theme_light": "Светлая (Light)",
                "theme_system": "Системная (System)",
                "dialog_copied_title": "Скопировано",
                "dialog_copied_body": "Команда '{command_str}' скопирована в буфер!"
            },
            "en": {
                "app_title": "Zenith Linux Assistant - Your Ultimate Linux Companion",
                "sidebar_title": "🌌 ZENITH LINUX",
                "sidebar_subtitle": "System & Translation Guide",
                "menu_dashboard": "🖥️  Dashboard",
                "menu_debian": "🌀  Debian World",
                "menu_arch": "🦅  Arch World",
                "menu_fedora": "🎩  Fedora / RedHat",
                "menu_translator": "🌐  Error Translator",
                "menu_commands": "⌨️  Basic Commands",
                "menu_fixes": "🔧  Common Fixes",
                "menu_settings": "⚙️  Settings",
                "status_title": "Detected Family",
                
                # Tab 1: Dashboard
                "dashboard_welcome": "🚀 Welcome to Zenith Linux Assistant! 🌌",
                "dashboard_desc": "Your central dashboard to monitor hardware metrics and access distribution-specific tools.",
                "card_os": "🖥️ Operating System",
                "card_kernel": "⚙️ Linux Kernel",
                "card_cpu": "🧠 Processor (CPU)",
                "card_ram": "💾 System Memory (RAM)",
                "cpu_sub": "All cores are active and running stably",
                "ram_sub": "Active memory usage status",
                "fact_title": "💡 Linux Fact:",
                "refresh_btn": "Refresh 🔄",
                "os_sub_family": "Family: {family} Linux",
                "cpu_unknown": "Unknown Processor",
                "ram_unknown": "No Information Available",
                
                # Distro Tabs Details
                "debian_title": "🌀 Debian & Ubuntu World",
                "debian_quote": "\"Ubuntu is Debian's most popular and well-behaved child.\"",
                "debian_desc": "The Debian family is known for its robustness, stability, and massive package repository. More than half of the desktop Linux distributions are built on this solid foundation. It is the safest harbor for beginners.",
                
                "arch_title": "🦅 Arch Linux World",
                "arch_quote": "\"The legendary lands where the phrase 'I use Arch by the way' was born!\"",
                "arch_desc": "Arch Linux embraces the 'KISS' (Keep It Simple, Stupid) philosophy. It gives the user full control; you build your system block by block from the ground up. It always provides the latest packages directly via rolling release.",
                
                "fedora_title": "🎩 Fedora & RedHat World",
                "fedora_quote": "\"The reflection of innovation and enterprise power on the desktop.\"",
                "fedora_desc": "Fedora is Linus Torvalds' personal choice of distribution, a visionary platform that brings cutting-edge technologies (Wayland, PipeWire, etc.) first. It is backed by the community power of RedHat.",
                
                "compatible_yes": "✓ Compatible System: Your computer is {family} based. Buttons will work directly!",
                "compatible_no": "⚠ Incompatible System: Your system is not {family} based. These commands might fail on your system!",
                
                "terminal_log_header": " Zenith Terminal Log\n---------------------------------------\nCommand copying logs and instructions will appear here.\n",
                "copy_btn_text": "Copy Command 📋",
                "app_copied_title": "Command Copied",
                "app_copied_info": "'{command_str}' command successfully copied to clipboard!\n\nOpen your terminal (Ctrl+Alt+T) and paste it to run the installation.",
                "app_copied_log_header": "📋 Command Copied: Install {app_name}\n",
                "app_copied_log_help": "💡 Quick Help & Instructions:\n",
                "app_copied_log_step1": " 1. Open your terminal using the shortcut: Ctrl + Alt + T\n",
                "app_copied_log_step2": " 2. Paste the copied command (Right-click -> Paste, or Ctrl + Shift + V)\n",
                "app_copied_log_step3": " 3. Press Enter, type your system password, and let the installer finish!\n",
                
                # Popular Applications translation
                "app_chrome_name": "Chromium Browser",
                "app_chrome_desc": "The open-source core of Google Chrome, fast and secure.",
                "app_discord_name": "Discord",
                "app_discord_desc": "Voice and text chat app for gamers and communities.",
                "app_steam_name": "Steam",
                "app_steam_desc": "The ultimate gateway to thousands of games on Linux.",
                "app_vlc_name": "VLC Media Player",
                "app_vlc_desc": "The universal media player that plays absolutely everything.",
                "app_vscode_name": "Visual Studio Code",
                "app_vscode_desc": "The most popular code editor for developers.",
                "app_spotify_name": "Spotify Music",
                "app_spotify_desc": "Play millions of songs and podcasts on your system.",
                "app_libreoffice_name": "LibreOffice Suite",
                "app_libreoffice_desc": "The powerful free office suite replacing Microsoft Office.",

                # Tab 5: Translator
                "ceviri_title": "🌐 Universal Error & Document Translator",
                "ceviri_desc": "Paste English error logs or foreign documentation here. Translate them instantly, completely free, and limitlessly using the GoogleTranslator engine.",
                "ceviri_source": "🌐 Source Text / Error Code (Auto-Detect):",
                "ceviri_source_placeholder": "Paste your English error log or command output here...\n\nExample:\ndpkg: error processing package python3 (--configure):\n dependency problems - leaving unconfigured",
                "ceviri_result_placeholder": "Translation result will appear here...",
                "ceviri_target_lang": "🎯 Target Language:",
                "ceviri_btn_translate": "Quick Translate 🚀",
                "ceviri_btn_clear": "Clear 🧹",
                "ceviri_btn_copy": "Copy Translation 📋",
                "ceviri_connecting": "Connecting...",
                "ceviri_translating": "Translating... ⏳",
                "ceviri_success": "✓ Translation Successful!",
                "ceviri_copied": "📋 Copied to Clipboard!",
                "ceviri_warning_title": "Warning",
                "ceviri_warning_empty": "Translation Warning: Please enter some text to translate!",
                "ceviri_warning_no_translation": "No translation found to copy!",
                "ceviri_conn_error": "✗ Connection Error!",
                "ceviri_error_desc": "Could not connect to the translation engine. Please check your internet connection.\nError: {e}",

                # Tab 6: Basic Commands
                "commands_title": "⌨️ Lifesaver Basic Linux Commands",
                "commands_desc": "Don't let the Linux terminal intimidate you! We categorized the basic commands you will need the most. You can instantly copy them using the copy buttons.",
                "cat_files": "📁 File & Directory Operations",
                "cat_resources": "⚙️ System Info & Resources",
                "cat_packages": "📦 Package & Update Management (Compatible with your system)",
                "cat_network": "🌐 Network & Internet Control",
                "cat_shortcuts": "⚡ Lifesaver Linux Shortcuts & Hotkeys",
                
                # Command Details
                "cmd_ls_desc": "Lists files and folders.",
                "cmd_cd_desc": "Switch current folder.",
                "cmd_mkdir_desc": "Create a new folder.",
                "cmd_rm_desc": "Delete files/folders safely.",
                "cmd_df_desc": "Show drive space usage.",
                "cmd_free_desc": "Show active RAM usage.",
                "cmd_uname_desc": "Show running OS kernel.",
                "cmd_update_desc": "Upgrade all packages.",
                "cmd_install_desc": "Install new software.",
                "cmd_vscode_desc": "Install Visual Studio Code editor.",
                "cmd_ping_desc": "Test network latency.",
                "cmd_ipa_desc": "List active IP addresses.",
                "cmd_altf2_desc": "Open quick command box to run apps instantly.",
                "cmd_ctrlaltt_desc": "Open a new terminal window instantly.",
                "cmd_ctrlshiftc_desc": "Copy selected text from terminal.",
                "cmd_ctrlshiftv_desc": "Paste copied text to terminal.",
                "cmd_super_desc": "Open application search menu.",
                "cmd_ctrlaltl_desc": "Lock your desktop screen instantly.",
                "cmd_ctrlaltd_desc": "Minimize all windows to show desktop.",
                "cmd_alttab_desc": "Switch between open applications.",
                "cmd_ctrlesc_desc": "Open system process/task monitor.",
                "cmd_ctrlaltarrows_desc": "Switch active workspace screens.",

                # Tab 7: Troubleshooter
                "fixes_title": "🔧 Troubleshooter & Post-Transition Fixes",
                "fixes_desc": "One-click solutions to the most common post-transition bugs faced by Windows switchers.",
                "cat_fixes_audio": "🔊 Audio & Sound Fixes",
                "cat_fixes_network": "🌐 Wi-Fi & Network Fixes",
                "cat_fixes_graphics": "🖥️ Graphics & Display Fixes",
                "cat_fixes_maintenance": "📦 System Maintenance & Locks",
                
                # Troubleshooter details
                "fix_pavucontrol_desc": "Configure audio profiles, balance stereos & select digital outputs.",
                "fix_alsamixer_desc": "Open terminal mixer to unmute muted hardware channels.",
                "fix_restart_audio_desc": "Gracefully restart Pipewire/PulseAudio daemons to fix frozen cards.",
                "fix_restart_nm_desc": "Restart network services to fix frozen Wi-Fi or connections.",
                "fix_flush_dns_desc": "Flush local DNS resolver cache to fix invalid web resolutions.",
                "fix_auto_sync_desc": "Force sync active screen configuration to solve display flickering.",
                "fix_list_gpu_desc": "Check active GPU model and current kernel modules in use.",
                "fix_unlock_pkg_desc": "Remove stale database locks holding package management transactions.",
                "fix_clean_cache_desc": "Flush downloaded package archives to reclaim disk space.",

                # Tab 8: Settings
                "settings_title": "⚙️ Application Settings",
                "settings_desc": "Customize Zenith Linux Assistant appearance, theme accents, and global interface languages.",
                "setting_theme": "App Theme:",
                "setting_lang": "App Language:",
                "theme_dark": "Dark",
                "theme_light": "Light",
                "theme_system": "System",
                "dialog_copied_title": "Copied",
                "dialog_copied_body": "'{command_str}' command successfully copied to clipboard!"
            }
        }

        # Window Configuration
        self.title(self.get_text("app_title"))
        self.geometry("950x650")
        self.resizable(False, False)

        # Detect System Information (Backend)
        self.os_info = self.detect_system_info()
        self.package_manager = self.os_info["package_manager"]
        self.system_family = self.os_info["family"]

        # Main Layout Grid (Sidebar & Content Container)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------ Left Navigation Sidebar ------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("#f9fafb", "#13131a"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)  # Stretchable bottom spacer at row 10

        # Logo and Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=self.get_text("sidebar_title"), 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 2))

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=self.get_text("sidebar_subtitle"), 
            font=ctk.CTkFont(family="Inter", size=11, slant="italic"),
            text_color=("#4b5563", "#9ca3af")
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 25))

        # Menu Buttons
        self.menu_buttons = {}
        menu_items = [
            ("Sistemim", self.get_text("menu_dashboard"), self.show_sistemim),
            ("Debian", self.get_text("menu_debian"), self.show_debian),
            ("Arch", self.get_text("menu_arch"), self.show_arch),
            ("Fedora", self.get_text("menu_fedora"), self.show_fedora),
            ("Ceviri", self.get_text("menu_translator"), self.show_ceviri),
            ("Komutlar", self.get_text("menu_commands"), self.show_komutlar),
            ("Troubleshoot", self.get_text("menu_fixes"), self.show_troubleshoot),
            ("Settings", self.get_text("menu_settings"), self.show_settings),
        ]

        for i, (key, text, command) in enumerate(menu_items, start=2):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                font=ctk.CTkFont(family="Inter", size=13, weight="normal"),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=("#374151", "#d1d5db"),
                hover_color=("#e5e7eb", "#1f1f2e"),
                anchor="w",
                command=command
            )
            btn.grid(row=i, column=0, padx=15, pady=5, sticky="ew")
            self.menu_buttons[key] = btn

        # Bottom Section: Detected System Status
        self.sys_status_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=10, fg_color=("#f3f4f6", "#1e1e28"), border_width=1, border_color=("#e5e7eb", "#2e2e3e"))
        self.sys_status_frame.grid(row=11, column=0, padx=15, pady=20, sticky="ew")
        
        self.status_title = ctk.CTkLabel(
            self.sys_status_frame, 
            text=self.get_text("status_title"), 
            font=ctk.CTkFont(family="Inter", size=10, weight="bold"),
            text_color=("#4b5563", "#9ca3af")
        )
        self.status_title.pack(anchor="w", padx=12, pady=(8, 0))

        self.status_value_frame = ctk.CTkFrame(self.sys_status_frame, fg_color="transparent")
        self.status_value_frame.pack(fill="x", padx=12, pady=(2, 8))

        # Green/Red Indicator Status Dot
        indicator_color = ("#059669", "#10b981") if self.system_family != "Unknown" else "#ef4444"
        self.indicator_dot = ctk.CTkLabel(
            self.status_value_frame, 
            text="●", 
            font=ctk.CTkFont(size=14),
            text_color=indicator_color
        )
        self.indicator_dot.pack(side="left", padx=(0, 5))

        self.status_value = ctk.CTkLabel(
            self.status_value_frame, 
            text=f"{self.system_family} ({self.package_manager.upper()})", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        self.status_value.pack(side="left")

        # ------------------ Right Content Panel (Content Frames) ------------------
        self.content_container = ctk.CTkFrame(self, corner_radius=0, fg_color=("#f3f4f6", "#0d0d11"))
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        # Create frames for different tabs
        self.frames = {}
        self.init_sistemim_frame()
        self.init_debian_frame()
        self.init_arch_frame()
        self.init_fedora_frame()
        self.init_ceviri_frame()
        self.init_komutlar_frame()
        self.init_troubleshoot_frame()
        self.init_settings_frame()

        # Initial tab: My System (Sistemim)
        self.show_sistemim()

    def get_text(self, key, **kwargs):
        """Helper to retrieve values from the global translations dictionary."""
        lang = self.active_lang
        val = self.translations.get(lang, {}).get(key, self.translations["en"].get(key, ""))
        if kwargs:
            return val.format(**kwargs)
        return val

    # =========================================================================
    # BACKEND: System Info Detection
    # =========================================================================
    def detect_system_info(self):
        """
        Reads the /etc/os-release file to detect the distribution family
        and package manager in the background. Also gathers basic system information.
        """
        sys_info = {
            "pretty_name": "Generic Linux",
            "family": "Unknown",
            "package_manager": "apt"
        }

        if platform.system() != "Linux":
            # Fallback for local development or non-linux systems
            sys_info["pretty_name"] = f"{platform.system()} {platform.release()}"
            return sys_info

        # Parse os-release file
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("PRETTY_NAME="):
                            sys_info["pretty_name"] = line.split("=")[1].strip().replace('"', '')
                        elif line.startswith("ID=") or line.startswith("ID_LIKE="):
                            val = line.split("=")[1].strip().replace('"', '').lower()
                            if "ubuntu" in val or "debian" in val or "mint" in val or "pop" in val:
                                sys_info["family"] = "Debian"
                                sys_info["package_manager"] = "apt"
                            elif "arch" in val or "manjaro" in val or "endeavouros" in val:
                                sys_info["family"] = "Arch"
                                sys_info["package_manager"] = "pacman"
                            elif "fedora" in val or "rhel" in val or "centos" in val or "rocky" in val:
                                sys_info["family"] = "Fedora"
                                sys_info["package_manager"] = "dnf"
        except Exception:
            pass

        return sys_info

    def get_cpu_info(self):
        """Retrieves CPU Model name cleanly in background thread."""
        try:
            if platform.system() == "Linux":
                cpu_command = "cat /proc/cpuinfo | grep 'model name' | uniq | cut -d':' -f2"
                model = subprocess.check_output(cpu_command, shell=True).decode().strip()
                if model:
                    return model
            return platform.processor() or self.get_text("cpu_unknown")
        except Exception:
            return self.get_text("cpu_unknown")

    def get_ram_info(self):
        """Retrieves formatted RAM text value and raw ratio."""
        try:
            if platform.system() == "Linux":
                with open("/proc/meminfo", "r") as f:
                    lines = f.readlines()
                    mem_total = 0
                    mem_free = 0
                    mem_available = 0
                    for line in lines:
                        if line.startswith("MemTotal:"):
                            mem_total = int(line.split()[1])
                        elif line.startswith("MemFree:"):
                            mem_free = int(line.split()[1])
                        elif line.startswith("MemAvailable:"):
                            mem_available = int(line.split()[1])

                    # Calculate active usage
                    if mem_available > 0:
                        used = mem_total - mem_available
                    else:
                        used = mem_total - mem_free

                    total_gb = mem_total / (1024 * 1024)
                    used_gb = used / (1024 * 1024)
                    percent = (used / mem_total) * 100
                    ratio = used / mem_total

                    return f"{used_gb:.1f} GB / {total_gb:.1f} GB ({percent:.1f}%)", ratio
        except Exception:
            pass
        return self.get_text("ram_unknown"), 0.0

    # =========================================================================
    # INTERFACE MANAGEMENT: Tab Switching Logic
    # =========================================================================
    def select_frame(self, name):
        """Shows the selected frame when a sidebar menu button is clicked, hides others."""
        # Clear background of all menu buttons
        for key, btn in self.menu_buttons.items():
            if key == name:
                btn.configure(fg_color=("#2563eb", "#3b82f6"), text_color=("#000000", "#ffffff"))  # Active button blue
            else:
                btn.configure(fg_color="transparent", text_color=("#374151", "#d1d5db"))

        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show selected frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def show_sistemim(self): self.select_frame("Sistemim")
    def show_debian(self): self.select_frame("Debian")
    def show_arch(self): self.select_frame("Arch")
    def show_fedora(self): self.select_frame("Fedora")
    def show_ceviri(self): self.select_frame("Ceviri")
    def show_komutlar(self): self.select_frame("Komutlar")
    def show_troubleshoot(self): self.select_frame("Troubleshoot")
    def show_settings(self): self.select_frame("Settings")

    # =========================================================================
    # TAB 1: SISTEMIM (DASHBOARD)
    # =========================================================================
    def init_sistemim_frame(self):
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames["Sistemim"] = frame

        # Header and Welcome Banner
        welcome_frame = ctk.CTkFrame(frame, fg_color=("#ffffff", "#181824"), corner_radius=12, border_width=1, border_color=("#e5e7eb", "#2c2c3e"))
        welcome_frame.pack(fill="x", padx=30, pady=(30, 20))

        welcome_label = ctk.CTkLabel(
            welcome_frame, 
            text=self.get_text("dashboard_welcome"), 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        welcome_label.pack(anchor="w", padx=25, pady=(20, 5))

        welcome_desc = ctk.CTkLabel(
            welcome_frame, 
            text=self.get_text("dashboard_desc"), 
            font=ctk.CTkFont(family="Inter", size=13),
            text_color=("#4b5563", "#9ca3af")
        )
        welcome_desc.pack(anchor="w", padx=25, pady=(0, 20))

        # Info Cards Grid Layout (2x2)
        grid_frame = ctk.CTkFrame(frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.rowconfigure(1, weight=1)

        # Card 1: Operating System
        self.create_info_card(
            grid_frame, 0, 0, 
            title=self.get_text("card_os"), 
            value=self.os_info["pretty_name"], 
            subtext=self.get_text("os_sub_family", family=self.system_family)
        )

        # Card 2: Linux Kernel
        self.create_info_card(
            grid_frame, 0, 1, 
            title=self.get_text("card_kernel"), 
            value=platform.release(), 
            subtext=f"Arch: {platform.machine()}"
        )

        # Card 3: Processor (CPU)
        self.create_info_card(
            grid_frame, 1, 0, 
            title=self.get_text("card_cpu"), 
            value=self.get_cpu_info(), 
            subtext=self.get_text("cpu_sub")
        )

        # Card 4: System Memory (RAM) - Dynamically Updatable
        self.ram_card = self.create_info_card(
            grid_frame, 1, 1, 
            title=self.get_text("card_ram"), 
            value=self.get_ram_info()[0], 
            subtext=self.get_text("ram_sub"),
            action_btn=True,
            action_text=self.get_text("refresh_btn"),
            action_cmd=self.refresh_ram
        )

        # Bottom Info Bar (Inspiring and Short Linux Fact - Randomized on Startup)
        fact_frame = ctk.CTkFrame(frame, fg_color=("#f8fafc", "#111827"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1f2937"))
        fact_frame.pack(fill="x", padx=30, pady=(15, 30))
        
        fact_title = ctk.CTkLabel(
            fact_frame, 
            text=self.get_text("fact_title"), 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#059669", "#10b981")
        )
        fact_title.pack(side="left", padx=(20, 5), pady=12)

        facts_tr = [
            "Dünyanın en hızlı 500 süper bilgisayarının tamamı Linux ile çalışmaktadır.",
            "Dünyanın en popüler 1 milyon web sunucusunun %96.3'ü Linux kullanmaktadır.",
            "Dünyanın en popüler mobil işletim sistemi olan Android, Linux çekirdeği üzerine kurulmuştur.",
            "Linux, 1991 yılında Linus Torvalds tarafından kişisel bir hobi projesi olarak oluşturuldu.",
            "Linux'un maskotu, Linus tarafından seçilen Tux adında dost canlısı bir penguendir.",
            "Dünyadaki tüm bulut altyapısının %90'ından fazlası Linux üzerinde çalışır.",
            "Linux son derece özelleştirilebilir, güvenli ve tamamen açık kaynaklıdır.",
            "SpaceX, roketlerinde ve Falcon uzay araçlarında Linux kullanmaktadır.",
            "İnternetin ve web sunucularının çoğu Linux üzerinde kararlı ve güvenli bir şekilde çalışır.",
            "Günümüzde aktif olarak kullanılabilen 600'den fazla aktif Linux dağıtımı vardır."
        ]
        facts_en = [
            "100% of the world's top 500 fastest supercomputers run on Linux.",
            "Linux powers 96.3% of the world's top 1 million web servers.",
            "Android, the world's most popular mobile OS, is built on the Linux kernel.",
            "Linux was created by Linus Torvalds in 1991 as a personal hobby project.",
            "The mascot of Linux is a friendly penguin named Tux, chosen by Linus.",
            "Over 90% of all cloud infrastructure in the world runs on Linux.",
            "Linux is highly customizable, secure, and completely open source.",
            "SpaceX uses Linux for its rockets and Falcon space vehicles.",
            "Most of the internet and web servers run stably and securely on Linux.",
            "There are over 600 active Linux distributions available today."
        ]
        
        selected_fact = random.choice(facts_tr) if self.active_lang == "tr" else random.choice(facts_en)

        fact_text = ctk.CTkLabel(
            fact_frame, 
            text=selected_fact, 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color=("#4b5563", "#9ca3af"),
            wraplength=520,
            justify="left"
        )
        fact_text.pack(side="left", padx=(5, 20), pady=12, fill="x", expand=True)

    def create_info_card(self, parent, row, col, title, value, subtext, action_btn=False, action_text="", action_cmd=None):
        card = ctk.CTkFrame(parent, fg_color=("#ffffff", "#161622"), border_width=1, border_color=("#e5e7eb", "#232334"), corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        title_lbl = ctk.CTkLabel(
            card, 
            text=title, 
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        title_lbl.pack(anchor="w", padx=20, pady=(18, 5))

        val_lbl = ctk.CTkLabel(
            card, 
            text=value, 
            font=ctk.CTkFont(family="Inter", size=15, weight="bold"),
            text_color=("#111827", "#f3f4f6"),
            wraplength=300,
            justify="left"
        )
        val_lbl.pack(anchor="w", padx=20, pady=2)
        
        # If this is the RAM card, keep a reference to update value dynamically
        if "System Memory" in title or "Sistem Belleği" in title:
            self.ram_val_label = val_lbl

            # Create a beautiful, glowing progress bar for RAM usage status
            self.ram_progress = ctk.CTkProgressBar(
                card, 
                width=260, 
                height=6, 
                progress_color=("#059669", "#10b981"), 
                fg_color=("#e2e8f0", "#1e293b"),
                corner_radius=3
            )
            self.ram_progress.pack(anchor="w", padx=20, pady=(6, 6))
            
            # Set the initial progress value
            _, ram_ratio = self.get_ram_info()
            self.ram_progress.set(ram_ratio)

        sub_lbl = ctk.CTkLabel(
            card, 
            text=subtext, 
            font=ctk.CTkFont(family="Inter", size=11),
            text_color=("#6b7280", "#6b7280")
        )
        sub_lbl.pack(anchor="w", padx=20, pady=(2, 18))

        if action_btn and action_cmd:
            btn = ctk.CTkButton(
                card, 
                text=action_text, 
                font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                width=80, 
                height=26,
                fg_color=("#e2e8f0", "#1e293b"), 
                text_color=("#0284c7", "#38bdf8"),
                hover_color=("#cbd5e1", "#334155"),
                corner_radius=6,
                command=action_cmd
            )
            # Position at top-right (rely=0.15 is set to align with title and prevent overlap)
            btn.place(relx=0.95, rely=0.15, anchor="ne")

        return card

    def refresh_ram(self):
        """Updates RAM information dynamically."""
        new_ram_txt, new_ram_ratio = self.get_ram_info()
        self.ram_val_label.configure(text=new_ram_txt)
        if hasattr(self, "ram_progress"):
            self.ram_progress.set(new_ram_ratio)

    # =========================================================================
    # DISTRO TEMPLATE & PACKAGE INSTALLER
    # =========================================================================
    def build_distro_tab(self, key, title, quote, description, status_msg, is_compatible):
        """A shared template method to build Debian, Arch, and Fedora tabs."""
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames[key] = frame

        # 1. Header Intro Card
        header_card = ctk.CTkFrame(frame, fg_color=("#ffffff", "#181824"), corner_radius=12, border_width=1, border_color=("#e5e7eb", "#2c2c3e"))
        header_card.pack(fill="x", padx=30, pady=(20, 15))

        title_lbl = ctk.CTkLabel(
            header_card, 
            text=title, 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 2))

        quote_lbl = ctk.CTkLabel(
            header_card, 
            text=quote, 
            font=ctk.CTkFont(family="Inter", size=12, slant="italic"),
            text_color=("#059669", "#10b981")
        )
        quote_lbl.pack(anchor="w", padx=20, pady=2)

        desc_lbl = ctk.CTkLabel(
            header_card, 
            text=description, 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color=("#4b5563", "#9ca3af"),
            wraplength=650,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(2, 12))

        # Compatibility Notification Strip
        compat_bg = ("#d1fae5", "#064e3b") if is_compatible else ("#fef3c7", "#78350f")
        compat_border = ("#047857", "#059669") if is_compatible else "#d97706"
        compat_text_color = ("#065f46", "#a7f3d0") if is_compatible else ("#92400e", "#fef3c7")

        compat_frame = ctk.CTkFrame(header_card, fg_color=compat_bg, corner_radius=8, border_width=1, border_color=compat_border)
        compat_frame.pack(fill="x", padx=20, pady=(0, 15))

        compat_lbl = ctk.CTkLabel(
            compat_frame,
            text=status_msg,
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            text_color=compat_text_color
        )
        compat_lbl.pack(padx=15, pady=6, anchor="w")

        # 2. Popular Applications Section
        apps_frame = ctk.CTkFrame(frame, fg_color="transparent")
        apps_frame.pack(fill="x", padx=30, pady=5)
        
        apps_frame.columnconfigure(0, weight=1)
        apps_frame.columnconfigure(1, weight=1)

        # Terminal Log Area
        terminal_box = ctk.CTkTextbox(
            frame, 
            fg_color=("#f3f4f6", "#07070a"), 
            text_color=("#059669", "#10b981"), 
            font=ctk.CTkFont(family="monospace", size=12),
            border_width=1,
            border_color=("#e5e7eb", "#1e1e2d"),
            corner_radius=10
        )
        terminal_box.pack(fill="both", expand=True, padx=30, pady=(15, 20))
        terminal_box.insert("1.0", self.get_text("terminal_log_header"))
        terminal_box.configure(state="disabled")

        # Dynamic App Names & Descriptions from global dictionaries
        if key.lower() == "debian":
            apps = [
                (self.get_text("app_chrome_name"), self.get_text("app_chrome_desc"), "chrome"),
                (self.get_text("app_discord_name"), self.get_text("app_discord_desc"), "discord"),
                (self.get_text("app_steam_name"), self.get_text("app_steam_desc"), "steam"),
                (self.get_text("app_vlc_name"), self.get_text("app_vlc_desc"), "vlc")
            ]
        elif key.lower() == "arch":
            apps = [
                (self.get_text("app_vscode_name"), self.get_text("app_vscode_desc"), "vscode"),
                (self.get_text("app_discord_name"), self.get_text("app_discord_desc"), "discord"),
                (self.get_text("app_steam_name"), self.get_text("app_steam_desc"), "steam"),
                (self.get_text("app_spotify_name"), self.get_text("app_spotify_desc"), "spotify")
            ]
        else: # fedora
            apps = [
                (self.get_text("app_chrome_name"), self.get_text("app_chrome_desc"), "chrome"),
                (self.get_text("app_vscode_name"), self.get_text("app_vscode_desc"), "vscode"),
                (self.get_text("app_vlc_name"), self.get_text("app_vlc_desc"), "vlc"),
                (self.get_text("app_libreoffice_name"), self.get_text("app_libreoffice_desc"), "libreoffice")
            ]

        for i, (name, app_desc, pkg_key) in enumerate(apps):
            r = i // 2
            c = i % 2
            
            app_card = ctk.CTkFrame(apps_frame, fg_color=("#f9fafb", "#14141e"), border_width=1, border_color=("#e5e7eb", "#222232"), corner_radius=10)
            app_card.grid(row=r, column=c, padx=8, pady=6, sticky="nsew")

            app_title = ctk.CTkLabel(
                app_card, 
                text=name, 
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color=("#111827", "#f3f4f6")
            )
            app_title.pack(anchor="w", padx=15, pady=(15, 2))

            app_sub = ctk.CTkLabel(
                app_card, 
                text=app_desc, 
                font=ctk.CTkFont(family="Inter", size=11),
                text_color=("#4b5563", "#9ca3af"),
                wraplength=280,
                justify="left"
            )
            app_sub.pack(anchor="w", padx=15, pady=(0, 15))

            # Determine install command
            cmd_str = self.get_clean_shell_command(key.lower(), pkg_key)

            # Copy button (perfectly aligned bottom right corner)
            btn = ctk.CTkButton(
                app_card,
                text=self.get_text("copy_btn_text"),
                font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                height=30,
                fg_color=("#059669", "#10b981"),
                hover_color=("#047857", "#059669"),
                corner_radius=6,
                command=lambda n=name, c=cmd_str, t=terminal_box: self.copy_app_command_to_clipboard(n, c, t)
            )
            btn.pack(anchor="e", padx=15, pady=(0, 15))

    def get_install_command(self, distro_family, pkg_key):
        """Returns corrected raw installation argument sequences."""
        commands = {
            "debian": {
                "chrome": ["sudo", "apt-get", "install", "-y", "chromium-browser"],
                "discord": ["sudo", "apt-get", "install", "-y", "discord"],
                "steam": ["sudo", "apt-get", "install", "-y", "steam"],
                "vlc": ["sudo", "apt-get", "install", "-y", "vlc"]
            },
            "arch": {
                "vscode": ["sudo", "pacman", "-S", "--noconfirm", "code"],
                "discord": ["sudo", "pacman", "-S", "--noconfirm", "discord"],
                "steam": ["sudo", "pacman", "-S", "--noconfirm", "steam"],
                "spotify": ["curl", "-sS", "https://download.spotify.com"]
            },
            "fedora": {
                "chrome": ["sudo", "dnf", "install", "-y", "chromium"],
                "vscode": ["sudo", "dnf", "install", "-y", "code"],
                "vlc": ["sudo", "dnf", "install", "-y", "vlc"],
                "libreoffice": ["sudo", "dnf", "install", "-y", "libreoffice"]
            }
        }
        return commands.get(distro_family, {}).get(pkg_key, ["echo", "Package not defined"])

    def get_clean_shell_command(self, distro_family, pkg_key):
        """Combines and returns shell arguments formatted as a clean terminal statement."""
        cmd_args = self.get_install_command(distro_family, pkg_key)
        if not cmd_args:
            return ""
        if cmd_args[0] == "bash" and len(cmd_args) > 2:
            raw_cmd = cmd_args[2]
            raw_cmd = raw_cmd.replace("apt-get", "sudo apt-get").replace("snap", "sudo snap")
            raw_cmd = raw_cmd.replace("sudo sudo", "sudo")
            return raw_cmd
        else:
            return "sudo " + " ".join(cmd_args) if not cmd_args[0].startswith("sudo") and not cmd_args[0].startswith("curl") else " ".join(cmd_args)

    def copy_app_command_to_clipboard(self, app_name, command_str, terminal_box):
        """Copies the package install command to clipboard and shows instructions in terminal box."""
        if not command_str:
            messagebox.showerror("Error", "Command not found!")
            return

        self.clipboard_clear()
        self.clipboard_append(command_str)

        # Update the beautiful terminal log area with instruction guide
        terminal_box.configure(state="normal")
        terminal_box.delete("1.0", "end")
        terminal_box.insert("end", self.get_text("app_copied_log_header", app_name=app_name.upper()))
        terminal_box.insert("end", f"------------------------------------------------------------\n")
        terminal_box.insert("end", f" 👉 {command_str}\n\n")
        terminal_box.insert("end", self.get_text("app_copied_log_help"))
        terminal_box.insert("end", self.get_text("app_copied_log_step1"))
        terminal_box.insert("end", self.get_text("app_copied_log_step2"))
        terminal_box.insert("end", self.get_text("app_copied_log_step3"))
        terminal_box.insert("end", f"------------------------------------------------------------\n")
        terminal_box.see("end")
        terminal_box.configure(state="disabled")

        messagebox.showinfo(
            self.get_text("app_copied_title"), 
            self.get_text("app_copied_info", command_str=command_str)
        )

    # =========================================================================
    # TABS 2, 3, 4: DEBIAN, ARCH, FEDORA TAB INITIALIZATION
    # =========================================================================
    def init_debian_frame(self):
        is_debian = (self.system_family == "Debian")
        status_msg = self.get_text("compatible_yes", family="Debian") if is_debian else \
                      self.get_text("compatible_no", family="Debian")
        
        self.build_distro_tab(
            key="Debian",
            title=self.get_text("debian_title"),
            quote=self.get_text("debian_quote"),
            description=self.get_text("debian_desc"),
            status_msg=status_msg,
            is_compatible=is_debian
        )

    def init_arch_frame(self):
        is_arch = (self.system_family == "Arch")
        status_msg = self.get_text("compatible_yes", family="Arch") if is_arch else \
                      self.get_text("compatible_no", family="Arch")

        self.build_distro_tab(
            key="Arch",
            title=self.get_text("arch_title"),
            quote=self.get_text("arch_quote"),
            description=self.get_text("arch_desc"),
            status_msg=status_msg,
            is_compatible=is_arch
        )

    def init_fedora_frame(self):
        is_fedora = (self.system_family == "Fedora")
        status_msg = self.get_text("compatible_yes", family="Fedora") if is_fedora else \
                      self.get_text("compatible_no", family="Fedora")

        self.build_distro_tab(
            key="Fedora",
            title=self.get_text("fedora_title"),
            quote=self.get_text("fedora_quote"),
            description=self.get_text("fedora_desc"),
            status_msg=status_msg,
            is_compatible=is_fedora
        )

    # =========================================================================
    # TAB 5: UNIVERSAL ERROR & DOCUMENT TRANSLATOR (deep-translator)
    # =========================================================================
    def init_ceviri_frame(self):
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames["Ceviri"] = frame

        # Header Info Card
        header_card = ctk.CTkFrame(frame, fg_color=("#ffffff", "#181824"), corner_radius=12, border_width=1, border_color=("#e5e7eb", "#2c2c3e"))
        header_card.pack(fill="x", padx=30, pady=(25, 15))

        title_lbl = ctk.CTkLabel(
            header_card, 
            text=self.get_text("ceviri_title"), 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 2))

        desc_lbl = ctk.CTkLabel(
            header_card, 
            text=self.get_text("ceviri_desc"), 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color=("#4b5563", "#9ca3af"),
            wraplength=650,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(2, 15))

        # Textboxes Container
        textbox_container = ctk.CTkFrame(frame, fg_color="transparent")
        textbox_container.pack(fill="both", expand=True, padx=30, pady=5)
        
        textbox_container.columnconfigure(0, weight=1)
        textbox_container.columnconfigure(1, weight=1)
        textbox_container.rowconfigure(0, weight=1)

        # Left: Source Text Input
        left_box_frame = ctk.CTkFrame(textbox_container, fg_color="transparent")
        left_box_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        left_lbl = ctk.CTkLabel(
            left_box_frame, 
            text=self.get_text("ceviri_source"), 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#4b5563", "#9ca3af")
        )
        left_lbl.pack(anchor="w", pady=(0, 5))

        self.en_textbox = ctk.CTkTextbox(
            left_box_frame, 
            fg_color=("#f9fafb", "#14141e"), 
            border_width=1, 
            border_color=("#e5e7eb", "#222232"),
            corner_radius=10, 
            font=ctk.CTkFont(family="Inter", size=12)
        )
        self.en_textbox.pack(fill="both", expand=True)
        self.en_textbox.insert("1.0", self.get_text("ceviri_source_placeholder"))

        # Right: Target Language Translation Output
        right_box_frame = ctk.CTkFrame(textbox_container, fg_color="transparent")
        right_box_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self.right_lbl = ctk.CTkLabel(
            right_box_frame, 
            text="🇹🇷 Turkish Translation Result:" if self.active_lang == "tr" else "🇬🇧 English Translation Result:", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#4b5563", "#9ca3af")
        )
        self.right_lbl.pack(anchor="w", pady=(0, 5))

        self.tr_textbox = ctk.CTkTextbox(
            right_box_frame, 
            fg_color=("#f9fafb", "#14141e"), 
            border_width=1, 
            border_color=("#e5e7eb", "#222232"),
            corner_radius=10, 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color=("#0284c7", "#38bdf8")
        )
        self.tr_textbox.pack(fill="both", expand=True)
        self.tr_textbox.insert("1.0", self.get_text("ceviri_result_placeholder"))
        self.tr_textbox.configure(state="disabled")

        # Buttons and Status Bar
        action_frame = ctk.CTkFrame(frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=30, pady=(15, 25))

        # Target Language Menu
        self.lang_codes = {
            "Turkish": "tr",
            "English": "en",
            "German": "de",
            "Spanish": "es",
            "French": "fr",
            "Russian": "ru",
            "Italian": "it"
        }
        
        self.lang_label = ctk.CTkLabel(
            action_frame,
            text=self.get_text("ceviri_target_lang"),
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#4b5563", "#9ca3af")
        )
        self.lang_label.pack(side="left", padx=(0, 5))
        
        self.target_lang_menu = ctk.CTkOptionMenu(
            action_frame,
            values=list(self.lang_codes.keys()),
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            dropdown_font=ctk.CTkFont(family="Inter", size=11),
            width=110,
            height=36,
            corner_radius=8,
            fg_color=("#e2e8f0", "#1e293b"),
            button_color=("#2563eb", "#3b82f6"),
            button_hover_color=("#1d4ed8", "#2563eb"),
            dropdown_fg_color=("#ffffff", "#1c1c24"),
            dropdown_hover_color=("#e5e7eb", "#2c2c3e"),
            dropdown_text_color=("#111827", "#f3f4f6"),
            command=self.on_target_language_change
        )
        self.target_lang_menu.pack(side="left", padx=(0, 15))
        self.target_lang_menu.set("Turkish" if self.active_lang == "tr" else "English")

        # Translate Button (Threaded)
        self.translate_btn = ctk.CTkButton(
            action_frame, 
            text=self.get_text("ceviri_btn_translate"), 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            fg_color=("#059669", "#10b981"), 
            hover_color=("#047857", "#059669"),
            height=36,
            corner_radius=8,
            command=self.run_translation
        )
        self.translate_btn.pack(side="left", padx=(0, 10))

        # Clear Button
        self.clear_btn = ctk.CTkButton(
            action_frame, 
            text=self.get_text("ceviri_btn_clear"), 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            fg_color=("#e5e7eb", "#374151"), 
            hover_color=("#d1d5db", "#4b5563"),
            height=36,
            corner_radius=8,
            command=self.clear_translation_fields
        )
        self.clear_btn.pack(side="left", padx=10)

        # Copy Button
        self.copy_btn = ctk.CTkButton(
            action_frame, 
            text=self.get_text("ceviri_btn_copy"), 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            fg_color=("#e2e8f0", "#1e293b"), 
            hover_color=("#cbd5e1", "#334155"),
            height=36,
            corner_radius=8,
            command=self.copy_translation_to_clipboard
        )
        self.copy_btn.pack(side="left", padx=10)

        # Translation Status Indicator
        self.translate_status = ctk.CTkLabel(
            action_frame, 
            text="", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color=("#0284c7", "#38bdf8")
        )
        self.translate_status.pack(side="right", padx=10)

    def on_target_language_change(self, selected_lang):
        """Updates labels dynamically when target language is changed."""
        flags = {
            "Turkish": "🇹🇷",
            "English": "🇬🇧",
            "German": "🇩🇪",
            "Spanish": "🇪🇸",
            "French": "🇫🇷",
            "Russian": "🇷🇺",
            "Italian": "🇮🇹"
        }
        flag = flags.get(selected_lang, "🌐")
        self.right_lbl.configure(text=self.get_text("result_title", flag=flag, lang=selected_lang))

    def run_translation(self):
        """Runs the translation in a background thread to prevent UI freezing."""
        source_text = self.en_textbox.get("1.0", "end-1c").strip()
        if not source_text:
            messagebox.showwarning(self.get_text("ceviri_warning_title"), self.get_text("ceviri_warning_empty"))
            return

        self.translate_btn.configure(state="disabled", text=self.get_text("ceviri_translating"))
        self.translate_status.configure(text=self.get_text("ceviri_connecting"), text_color=("#d97706", "#f59e0b"))

        target_lang = self.target_lang_menu.get()
        target_code = self.lang_codes.get(target_lang, "tr")

        def worker():
            try:
                # Run deep-translator (source set to auto)
                translated = GoogleTranslator(source='auto', target=target_code).translate(source_text)
                
                # Update GUI safely
                self.after(0, lambda: self.update_translation_ui(translated))
            except Exception as e:
                self.after(0, lambda: self.handle_translation_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def update_translation_ui(self, result_text):
        """Displays the translated text safely."""
        self.tr_textbox.configure(state="normal")
        self.tr_textbox.delete("1.0", "end")
        self.tr_textbox.insert("1.0", result_text)
        self.tr_textbox.configure(state="disabled")
        
        self.translate_btn.configure(state="normal", text=self.get_text("ceviri_btn_translate"))
        self.translate_status.configure(text=self.get_text("ceviri_success"), text_color=("#059669", "#10b981"))

    def handle_translation_error(self, err_msg):
        """Resets the UI states and displays an error box."""
        self.translate_btn.configure(state="normal", text=self.get_text("ceviri_btn_translate"))
        self.translate_status.configure(text=self.get_text("ceviri_conn_error"), text_color="#ef4444")
        messagebox.showerror(
            self.get_text("error_translation"), 
            self.get_text("ceviri_error_desc", e=err_msg)
        )

    def clear_translation_fields(self):
        """Clears translation input and output text boxes."""
        self.en_textbox.delete("1.0", "end")
        self.tr_textbox.configure(state="normal")
        self.tr_textbox.delete("1.0", "end")
        self.tr_textbox.configure(state="disabled")
        self.translate_status.configure(text="")

    def copy_translation_to_clipboard(self):
        """Copies the translation to clipboard."""
        translated_text = self.tr_textbox.get("1.0", "end-1c").strip()
        if not translated_text or self.get_text("ceviri_result_placeholder") in translated_text:
            messagebox.showwarning(self.get_text("ceviri_warning_title"), self.get_text("ceviri_warning_no_translation"))
            return
        
        self.clipboard_clear()
        self.clipboard_append(translated_text)
        self.translate_status.configure(text=self.get_text("ceviri_copied"), text_color=("#059669", "#10b981"))
        self.after(2000, lambda: self.translate_status.configure(text=""))

    # =========================================================================
    # TAB 6: LIFESAVER BASIC COMMANDS
    # =========================================================================
    def init_komutlar_frame(self):
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames["Komutlar"] = frame

        # Header Info Card
        header_card = ctk.CTkFrame(frame, fg_color=("#ffffff", "#181824"), corner_radius=12, border_width=1, border_color=("#e5e7eb", "#2c2c3e"))
        header_card.pack(fill="x", padx=30, pady=(25, 10))

        title_lbl = ctk.CTkLabel(
            header_card, 
            text=self.get_text("commands_title"), 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=("#2563eb", "#3b82f6")
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 2))

        desc_lbl = ctk.CTkLabel(
            header_card, 
            text=self.get_text("commands_desc"), 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color=("#4b5563", "#9ca3af"),
            wraplength=650,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(2, 15))

        # Scrollable Commands Container
        scroll_frame = ctk.CTkScrollableFrame(
            frame, 
            fg_color="transparent", 
            scrollbar_button_color=("#e5e7eb", "#1e1e2d"),
            scrollbar_button_hover_color=("#e5e7eb", "#2c2c3e")
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(5, 20))

        # Commands Dataset
        pkg_update_cmd = "sudo apt update && sudo apt upgrade"
        pkg_install_cmd = "sudo apt install <package-name>"
        if self.package_manager == "pacman":
            pkg_update_cmd = "sudo pacman -Syu"
            pkg_install_cmd = "sudo pacman -S <package-name>"
        elif self.package_manager == "dnf":
            pkg_update_cmd = "sudo dnf upgrade"
            pkg_install_cmd = "sudo dnf install <package-name>"

        pkg_vscode_cmd = "sudo apt install code || sudo snap install --classic code"
        if self.package_manager == "pacman":
            pkg_vscode_cmd = "sudo pacman -S code"
        elif self.package_manager == "dnf":
            pkg_vscode_cmd = "sudo dnf install code"

        categories = [
            (self.get_text("cat_files"), [
                ("ls", self.get_text("cmd_ls_desc"), "ls -la"),
                ("cd", self.get_text("cmd_cd_desc"), "cd /path/to/folder"),
                ("mkdir", self.get_text("cmd_mkdir_desc"), "mkdir new_folder"),
                ("rm", self.get_text("cmd_rm_desc"), "rm -rf file_or_folder")
            ]),
            (self.get_text("cat_resources"), [
                ("df -h", self.get_text("cmd_df_desc"), "df -h"),
                ("free -h", self.get_text("cmd_free_desc"), "free -h"),
                ("uname -a", self.get_text("cmd_uname_desc"), "uname -a")
            ]),
            (self.get_text("cat_packages"), [
                ("System Update", self.get_text("cmd_update_desc"), pkg_update_cmd),
                ("Install New Package", self.get_text("cmd_install_desc"), pkg_install_cmd),
                ("Install VS Code", self.get_text("cmd_vscode_desc"), pkg_vscode_cmd)
            ]),
            (self.get_text("cat_network"), [
                ("ping", self.get_text("cmd_ping_desc"), "ping -c 4 google.com"),
                ("ip a", self.get_text("cmd_ipa_desc"), "ip a")
            ]),
            (self.get_text("cat_shortcuts"), [
                ("Alt + F2", self.get_text("cmd_altf2_desc"), "Alt + F2"),
                ("Ctrl + Alt + T", self.get_text("cmd_ctrlaltt_desc"), "Ctrl + Alt + T"),
                ("Ctrl + Shift + C", self.get_text("cmd_ctrlshiftc_desc"), "Ctrl + Shift + C"),
                ("Ctrl + Shift + V", self.get_text("cmd_ctrlshiftv_desc"), "Ctrl + Shift + V"),
                ("Super Key", self.get_text("cmd_super_desc"), "Super / Windows Key"),
                ("Ctrl + Alt + L", self.get_text("cmd_ctrlaltl_desc"), "Ctrl + Alt + L"),
                ("Ctrl + Alt + D", self.get_text("cmd_ctrlaltd_desc"), "Ctrl + Alt + D"),
                ("Alt + Tab", self.get_text("cmd_alttab_desc"), "Alt + Tab"),
                ("Ctrl + Esc", self.get_text("cmd_ctrlesc_desc"), "Ctrl + Esc"),
                ("Ctrl + Alt + Arrows", self.get_text("cmd_ctrlaltarrows_desc"), "Workspace Switch")
            ])
        ]

        # Place category frames
        for cat_title, cmd_list in categories:
            cat_frame = ctk.CTkFrame(scroll_frame, fg_color=("#ffffff", "#13131e"), border_width=1, border_color=("#e5e7eb", "#1e1e2d"), corner_radius=10)
            cat_frame.pack(fill="x", padx=5, pady=8)

            cat_lbl = ctk.CTkLabel(
                cat_frame, 
                text=cat_title, 
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color=("#059669", "#10b981")
            )
            cat_lbl.pack(anchor="w", padx=15, pady=(12, 10))

            for name, desc, cmd_str in cmd_list:
                item_frame = ctk.CTkFrame(cat_frame, fg_color=("#f9fafb", "#1a1a26"), corner_radius=8)
                item_frame.pack(fill="x", padx=15, pady=6)

                # 1. Top Section: Title & Description
                top_lbl = ctk.CTkLabel(
                    item_frame,
                    text=f"✨ {name}: {desc}",
                    font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                    text_color=("#111827", "#f3f4f6"),
                    anchor="w"
                )
                top_lbl.pack(fill="x", padx=12, pady=(10, 4), anchor="w")

                # 2. Bottom Section: Command and Copy Button Container
                bottom_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                bottom_frame.pack(fill="x", padx=12, pady=(0, 10))

                # Copy Button (Packed FIRST on the right to preserve its space!)
                copy_btn = ctk.CTkButton(
                    bottom_frame,
                    text="Copy 📋",
                    font=ctk.CTkFont(family="Inter", size=10, weight="bold"),
                    width=70,
                    height=24,
                    fg_color=("#e2e8f0", "#1e293b"),
                    hover_color=("#cbd5e1", "#334155"),
                    corner_radius=5,
                    command=lambda c=cmd_str: self.copy_command_to_clipboard(c)
                )
                copy_btn.pack(side="right", padx=(10, 0))

                # Command Label (Monospace Font, packed left with wraplength to adapt seamlessly)
                cmd_lbl = ctk.CTkLabel(
                    bottom_frame, 
                    text=f" $ {cmd_str} ", 
                    font=ctk.CTkFont(family="monospace", size=11, weight="bold"),
                    fg_color=("#f3f4f6", "#07070a"),
                    text_color=("#be123c", "#e11d48"),
                    corner_radius=4,
                    wraplength=480,
                    justify="left"
                )
                cmd_lbl.pack(side="left", anchor="w", fill="x", expand=True)

    # =========================================================================
    # TAB 7: TROUBLESHOOTER (COMMON FIXES)
    # =========================================================================
    def init_troubleshoot_frame(self):
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames["Troubleshoot"] = frame

        # Header and Welcome Banner
        title_lbl = ctk.CTkLabel(
            frame, 
            text=self.get_text("fixes_title"), 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        title_lbl.pack(anchor="w", padx=25, pady=(25, 5))

        desc_lbl = ctk.CTkLabel(
            frame, 
            text=self.get_text("fixes_desc"),
            font=ctk.CTkFont(family="Inter", size=13),
            text_color=("#4b5563", "#9ca3af"),
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=25, pady=(2, 15))

        # Scrollable Commands Container
        scroll_frame = ctk.CTkScrollableFrame(
            frame, 
            fg_color="transparent", 
            scrollbar_button_color=("#e5e7eb", "#1e1e2d"),
            scrollbar_button_hover_color=("#e5e7eb", "#2c2c3e")
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(5, 20))

        # Commands Dataset
        pkg_pavu_cmd = "sudo apt install -y pavucontrol && pavucontrol"
        if self.package_manager == "pacman":
            pkg_pavu_cmd = "sudo pacman -S --noconfirm pavucontrol && pavucontrol"
        elif self.package_manager == "dnf":
            pkg_pavu_cmd = "sudo dnf install -y pavucontrol && pavucontrol"

        pkg_lock_cmd = "sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock /var/cache/apt/archives/lock"
        if self.package_manager == "pacman":
            pkg_lock_cmd = "sudo rm -f /var/lib/pacman/db.lck"
        elif self.package_manager == "dnf":
            pkg_lock_cmd = "sudo rm -f /var/lib/dnf/hashcache/lock /var/lib/rpm/.rpm.lock"

        pkg_clean_cmd = "sudo apt clean"
        if self.package_manager == "pacman":
            pkg_clean_cmd = "sudo pacman -Sc --noconfirm"
        elif self.package_manager == "dnf":
            pkg_clean_cmd = "sudo dnf clean all"

        categories = [
            (self.get_text("cat_fixes_audio"), [
                ("Launch Pavucontrol", self.get_text("fix_pavucontrol_desc"), pkg_pavu_cmd),
                ("Launch Alsamixer", self.get_text("fix_alsamixer_desc"), "alsamixer"),
                ("Restart Audio Services", self.get_text("fix_restart_audio_desc"), "systemctl --user restart pipewire wireplumber || pulseaudio -k && pulseaudio --start")
            ]),
            (self.get_text("cat_fixes_network"), [
                ("Restart Network Manager", self.get_text("fix_restart_nm_desc"), "sudo systemctl restart NetworkManager"),
                ("Flush DNS Cache", self.get_text("fix_flush_dns_desc"), "sudo resolvectl flush-caches")
            ]),
            (self.get_text("cat_fixes_graphics"), [
                ("Force Screen Auto Sync", self.get_text("fix_auto_sync_desc"), "xrandr --auto"),
                ("List Loaded Graphics Drivers", self.get_text("fix_list_gpu_desc"), "lspci -k | grep -A 2 -i 'VGA'")
            ]),
            (self.get_text("cat_fixes_maintenance"), [
                ("Unlock Package Manager", self.get_text("fix_unlock_pkg_desc"), pkg_lock_cmd),
                ("Clean Local Cache Space", self.get_text("fix_clean_cache_desc"), pkg_clean_cmd)
            ])
        ]

        # Place category frames
        for cat_title, cmd_list in categories:
            cat_frame = ctk.CTkFrame(scroll_frame, fg_color=("#ffffff", "#13131e"), border_width=1, border_color=("#e5e7eb", "#1e1e2d"), corner_radius=10)
            cat_frame.pack(fill="x", padx=5, pady=8)

            cat_lbl = ctk.CTkLabel(
                cat_frame, 
                text=cat_title, 
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color=("#2563eb", "#3b82f6")
            )
            cat_lbl.pack(anchor="w", padx=15, pady=(12, 10))

            for name, desc, cmd_str in cmd_list:
                item_frame = ctk.CTkFrame(cat_frame, fg_color=("#f9fafb", "#1a1a26"), corner_radius=8)
                item_frame.pack(fill="x", padx=15, pady=6)

                # 1. Top Section: Title & Description
                top_lbl = ctk.CTkLabel(
                    item_frame,
                    text=f"✨ {name}: {desc}",
                    font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                    text_color=("#111827", "#f3f4f6"),
                    anchor="w"
                )
                top_lbl.pack(fill="x", padx=12, pady=(10, 4), anchor="w")

                # 2. Bottom Section: Command and Copy Button Container
                bottom_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                bottom_frame.pack(fill="x", padx=12, pady=(0, 10))

                # Copy Button (Packed FIRST on the right to preserve its space!)
                copy_btn = ctk.CTkButton(
                    bottom_frame,
                    text="Copy 📋",
                    font=ctk.CTkFont(family="Inter", size=10, weight="bold"),
                    width=70,
                    height=24,
                    fg_color=("#e2e8f0", "#1e293b"),
                    hover_color=("#cbd5e1", "#334155"),
                    corner_radius=5,
                    command=lambda c=cmd_str: self.copy_command_to_clipboard(c)
                )
                copy_btn.pack(side="right", padx=(10, 0))

                # Command Label (Monospace Font, packed left with wraplength to adapt seamlessly)
                cmd_lbl = ctk.CTkLabel(
                    bottom_frame, 
                    text=f" $ {cmd_str} ", 
                    font=ctk.CTkFont(family="monospace", size=11, weight="bold"),
                    fg_color=("#f3f4f6", "#07070a"),
                    text_color=("#be123c", "#e11d48"),
                    corner_radius=4,
                    wraplength=480,
                    justify="left"
                )
                cmd_lbl.pack(side="left", anchor="w", fill="x", expand=True)

    # =========================================================================
    # TAB 8: APPLICATION SETTINGS
    # =========================================================================
    def init_settings_frame(self):
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.frames["Settings"] = frame

        # Header and Welcome Banner
        title_lbl = ctk.CTkLabel(
            frame, 
            text=self.get_text("settings_title"), 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        title_lbl.pack(anchor="w", padx=25, pady=(25, 5))

        desc_lbl = ctk.CTkLabel(
            frame, 
            text=self.get_text("settings_desc"),
            font=ctk.CTkFont(family="Inter", size=13),
            text_color=("#4b5563", "#9ca3af"),
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=25, pady=(2, 25))

        # Main Settings Container
        settings_container = ctk.CTkFrame(frame, fg_color=("#ffffff", "#13131e"), border_width=1, border_color=("#e5e7eb", "#1e1e2d"), corner_radius=12)
        settings_container.pack(fill="x", padx=30, pady=10)

        # 1. Row: Theme Setting
        theme_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=15)

        theme_lbl = ctk.CTkLabel(
            theme_frame,
            text=self.get_text("setting_theme"),
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        theme_lbl.pack(side="left")

        # Map current theme for selection
        current_theme = ctk.get_appearance_mode()
        theme_options = ["Koyu (Dark)", "Açık (Light)", "Sistem (System)"]
        if self.active_lang == "en":
            theme_options = ["Dark", "Light", "System"]

        # Find matching default option
        default_theme_option = theme_options[0] # Dark default
        if current_theme.lower() == "light":
            default_theme_option = theme_options[1]
        elif current_theme.lower() == "system":
            default_theme_option = theme_options[2]

        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=theme_options,
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            fg_color=("#e2e8f0", "#1e293b"),
            button_color=("#2563eb", "#3b82f6"),
            button_hover_color=("#1d4ed8", "#2563eb"),
            dropdown_fg_color=("#e5e7eb", "#1e1e2d"),
            dropdown_hover_color=("#e5e7eb", "#2c2c3e"),
            dropdown_text_color=("#111827", "#f3f4f6"),
            corner_radius=6,
            command=self.change_theme
        )
        self.theme_menu.pack(side="right")
        self.theme_menu.set(default_theme_option)

        # Separator line
        sep = ctk.CTkFrame(settings_container, height=1, fg_color=("#e5e7eb", "#1e1e2d"))
        sep.pack(fill="x", padx=20, pady=5)

        # 2. Row: Language Setting
        lang_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        lang_frame.pack(fill="x", padx=20, pady=15)

        lang_lbl = ctk.CTkLabel(
            lang_frame,
            text=self.get_text("setting_lang"),
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        lang_lbl.pack(side="left")

        lang_options = ["Türkçe", "English", "Español", "Deutsch", "Русский"]
        lang_map = {"tr": "Türkçe", "en": "English", "es": "Español", "de": "Deutsch", "ru": "Русский"}
        default_lang_option = lang_map.get(self.active_lang, "Türkçe")

        self.lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=lang_options,
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            fg_color=("#e2e8f0", "#1e293b"),
            button_color=("#2563eb", "#3b82f6"),
            button_hover_color=("#1d4ed8", "#2563eb"),
            dropdown_fg_color=("#e5e7eb", "#1e1e2d"),
            dropdown_hover_color=("#e5e7eb", "#2c2c3e"),
            dropdown_text_color=("#111827", "#f3f4f6"),
            corner_radius=6,
            command=self.change_language
        )
        self.lang_menu.pack(side="right")
        self.lang_menu.set(default_lang_option)

    def change_theme(self, selected_theme):
        """Changes the CustomTkinter visual mode dynamically."""
        mode_map = {
            "Koyu (Dark)": "dark",
            "Açık (Light)": "light",
            "Sistem (System)": "system",
            "Dark": "dark",
            "Light": "light",
            "System": "system"
        }
        target_mode = mode_map.get(selected_theme, "dark")
        ctk.set_appearance_mode(target_mode)

    def change_language(self, selected_lang):
        """Triggers the global translation engine to reconfigure all labels dynamically."""
        lang_reverse_map = {"Türkçe": "tr", "English": "en", "Español": "es", "Deutsch": "de", "Русский": "ru"}
        new_lang = lang_reverse_map.get(selected_lang, "tr")
        if self.active_lang == new_lang:
            return
        
        self.active_lang = new_lang
        
        # Track the name of the current active frame
        current_active = "Sistemim"
        for key, frame in self.frames.items():
            if frame.winfo_ismapped():
                current_active = key
                break
        
        # Destroy all active frames
        for frame in list(self.frames.values()):
            frame.destroy()
        self.frames.clear()

        # Create a beautiful loading/animation frame in the center
        loading_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        loading_frame.grid(row=0, column=0, sticky="nsew")
        
        loading_label = ctk.CTkLabel(
            loading_frame,
            text="⏳ " + self.get_text("ceviri_translating").replace(" ⏳", "") + "\n\n. . .",
            font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
            text_color=("#111827", "#f3f4f6")
        )
        loading_label.place(relx=0.5, rely=0.5, anchor="center")

        # Let Tkinter render the loading screen, then trigger the actual rebuild
        self.after(100, lambda: self._apply_language_change(current_active, loading_frame))

    def _apply_language_change(self, current_active, loading_frame):
        # Re-initialize all frames in the new language!
        self.init_sistemim_frame()
        self.init_debian_frame()
        self.init_arch_frame()
        self.init_fedora_frame()
        self.init_ceviri_frame()
        self.init_komutlar_frame()
        self.init_troubleshoot_frame()
        self.init_settings_frame()

        # Update sidebar menu buttons text
        self.menu_buttons["Sistemim"].configure(text=self.get_text("menu_dashboard"))
        self.menu_buttons["Debian"].configure(text=self.get_text("menu_debian"))
        self.menu_buttons["Arch"].configure(text=self.get_text("menu_arch"))
        self.menu_buttons["Fedora"].configure(text=self.get_text("menu_fedora"))
        self.menu_buttons["Ceviri"].configure(text=self.get_text("menu_translator"))
        self.menu_buttons["Komutlar"].configure(text=self.get_text("menu_commands"))
        self.menu_buttons["Troubleshoot"].configure(text=self.get_text("menu_fixes"))
        self.menu_buttons["Settings"].configure(text=self.get_text("menu_settings"))

        # Update static labels in the sidebar
        self.logo_label.configure(text=self.get_text("sidebar_title"))
        self.subtitle_label.configure(text=self.get_text("sidebar_subtitle"))
        self.status_title.configure(text=self.get_text("status_title"))
        self.status_value.configure(text=f"{self.system_family} ({self.package_manager.upper()})")

        # Update window title
        self.title(self.get_text("app_title"))

        # Destroy loading frame
        loading_frame.destroy()

        # Show the same active tab!
        self.select_frame(current_active)

    def copy_command_to_clipboard(self, command_str):
        """Copies the selected terminal command and shows a quick info message."""
        self.clipboard_clear()
        self.clipboard_append(command_str)
        
        title = self.get_text("dialog_copied_title")
        body = self.get_text("dialog_copied_body", command_str=command_str)
        messagebox.showinfo(title, body)


if __name__ == "__main__":
    # Start the application
    app = ZenithLinuxAssistant()
    app.mainloop()
