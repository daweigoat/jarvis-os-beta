# JARVIS OS (Beta) 🤖

Project asisten AI desktop ala Iron Man yang di-tuning khusus buat Bahasa Indonesia. Berjalan 100% secara offline di Windows 11. 

Tujuan project ini adalah bikin *desktop assistant* yang nggak cuma pinter, tapi juga ringan dan punya UI hologram yang memanjakan mata. Semuanya jalan secara lokal di komputer kita, jadi privasi aman banget.

## Fitur Utama 🔥
- **Otak AI Lokal**: Menggunakan Ollama (default-nya pakai model Qwen). Punya sistem memori sederhana biar ngobrolnya bisa nyambung.
- **Suara Natural (Bahasa Indonesia)**: Pake Kokoro TTS biar suara yang keluar nggak kaku kayak robot jadul Google Translate.
- **HUD Hologram**: UI-nya dibangun pakai kombinasi PyGame dan ModernGL. Ada efek *glowing shaders* 60 FPS yang langsung bereaksi ngikutin status AI-nya (lagi dengerin, mikir, atau ngomong).
- **Gesture & Vision**: Bisa deteksi pergerakan tangan pakai MediaPipe (contoh: pose "Peace" buat trigger sesuatu). Kamera sengaja di-*lazy load* jadi nggak bakal nyedot baterai/RAM kalau lagi nggak dipakai.
- **Desktop Automation**: Bisa disuruh buka Chrome, Spotify, VS Code, Discord, dll lewat perintah suara.
- **Security Core**: Punya sistem keamanan bawaan. Kalau dia disuruh matiin PC, dia bakal nanya balik "Apakah anda yakin?" dan nunggu konfirmasi dari suara kita sebelum dieksekusi.
- **Tahan Banting (Fault Tolerant)**: Kalau misal webcam dicabut atau server Ollama belum nyala, aplikasinya nggak bakal *crash*. Modul yang error bakal otomatis di-disable tapi sisa aplikasinya tetap jalan normal.

## Cara Install & Pake 🛠️

Pastikan kamu udah pakai Python 3.11.

1. Clone repo ini atau download ZIP-nya.
2. Install semua *dependencies*:
   ```bash
   pip install -r requirements.txt
   ```
3. Pastikan [Ollama](https://ollama.com/) udah ke-install dan jalan di background (contoh: buka CMD dan ketik `ollama run qwen`).
4. Langsung jalanin file utamanya:
   ```bash
   python run.py
   ```

## Build jadi .exe 📦
Kalau males buka lewat terminal terus-terusan, tinggal compile aja jadi file `.exe`. Jendela hitam CMD-nya bakal otomatis disembunyiin jadi cuma nyisa UI HUD-nya doang.

```bash
python build.py
```
Nanti hasil jadinya bisa dicek di folder `dist/JARVIS OS/JARVIS OS.exe`.

## Arsitektur Kode 🏗️
Kodenya sengaja dibikin sangat modular (Event-Driven architecture pakai sistem Pub/Sub). Jadi kalau misal mau nambahin plugin baru (misal: agen khusus smart home atau IoT), tinggal bikin class Plugin baru aja tanpa takut ngerusak kode inti yang udah ada.
