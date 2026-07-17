JARVIS OS (Beta) 🤖

JARVIS OS adalah proyek AI Desktop Assistant yang terinspirasi dari JARVIS milik Iron Man dan dirancang khusus untuk pengguna Bahasa Indonesia. Seluruh sistem berjalan secara lokal (offline/local-first) sehingga lebih cepat, ringan, dan privasi pengguna tetap terjaga.

Tujuan utama proyek ini bukan hanya membuat asisten AI yang pintar, tetapi juga menghadirkan pengalaman yang lebih interaktif melalui tampilan HUD holografik yang futuristik, suara yang natural, serta dukungan gesture dan automasi desktop yang responsif.

Fitur Utama ✨

AI Engine Lokal

Menggunakan Ollama sebagai AI engine (default menggunakan model Qwen) yang dilengkapi sistem memori sederhana agar percakapan terasa lebih natural dan tetap memiliki konteks.

Natural Indonesian Voice

Memanfaatkan Kokoro TTS untuk menghasilkan suara Bahasa Indonesia yang lebih halus dan nyaman didengar, sehingga tidak terdengar seperti suara robot konvensional.

Holographic HUD Interface

Antarmuka dibangun menggunakan kombinasi PyGame dan ModernGL dengan efek glowing shaders 60 FPS yang mampu bereaksi secara real-time terhadap status AI, mulai dari mendengarkan, memproses perintah, hingga berbicara.

Gesture Recognition & Computer Vision

Mendukung deteksi gesture tangan menggunakan MediaPipe, seperti pose Peace Sign untuk menjalankan perintah tertentu. Sistem kamera menggunakan metode lazy loading sehingga hanya aktif saat diperlukan untuk menghemat penggunaan RAM dan daya perangkat.

Desktop Automation

Dapat menjalankan berbagai aplikasi melalui perintah suara, seperti Chrome, Spotify, VS Code, Discord, dan aplikasi desktop lainnya.

Security Core

Seluruh perintah yang bersifat sensitif akan melalui proses konfirmasi terlebih dahulu. Sebagai contoh, ketika pengguna meminta sistem untuk mematikan komputer, JARVIS OS akan meminta konfirmasi suara sebelum perintah dieksekusi.

Fault Tolerant System

Sistem dirancang agar tetap berjalan meskipun terdapat modul yang mengalami gangguan. Jika webcam terputus atau server Ollama belum aktif, modul terkait akan dinonaktifkan secara otomatis tanpa menyebabkan keseluruhan aplikasi mengalami crash.

Cara Instalasi 🚀

Pastikan Anda telah menggunakan Python 3.11 atau versi yang direkomendasikan.

Clone repository ini atau unduh file ZIP.
Install seluruh dependencies yang diperlukan.
pip install -r requirements.txt
Pastikan Ollama telah terpasang dan berjalan di latar belakang.
ollama run qwen
Jalankan aplikasi menggunakan perintah berikut.
python run.py
Build Menjadi File .exe 📦

Apabila ingin menjalankan aplikasi tanpa membuka terminal, Anda dapat melakukan proses build menjadi file .exe.

python build.py

Setelah proses selesai, file hasil build dapat ditemukan pada direktori berikut.

dist/
└── JARVIS OS/
    └── JARVIS OS.exe

Versi .exe akan secara otomatis menyembunyikan jendela terminal sehingga hanya tampilan HUD holografik yang ditampilkan kepada pengguna.

Arsitektur Sistem 🏗️

JARVIS OS dibangun menggunakan pendekatan Event-Driven Architecture dengan pola komunikasi Publish/Subscribe (Pub/Sub) yang modular. Setiap fitur dipisahkan ke dalam modul yang independen sehingga lebih mudah untuk dikembangkan dan dipelihara.

Dengan arsitektur ini, pengembang dapat menambahkan fitur maupun plugin baru tanpa perlu mengubah kode inti aplikasi. Misalnya:

Smart Home Assistant
IoT Controller
Custom AI Agent
Automation Plugin
Voice Extension Module
Computer Vision Extension

Pendekatan modular tersebut membuat JARVIS OS lebih fleksibel, mudah dikembangkan, dan siap untuk mendukung berbagai kebutuhan di masa mendatang.

JARVIS OS (Beta) masih berada dalam tahap pengembangan aktif. Berbagai fitur baru dan peningkatan performa akan terus ditambahkan seiring perkembangan proyek.
