import os
import subprocess
import sys

def main():
    print("Building JARVIS OS 4.0 .exe using PyInstaller...")
    
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
    build_command = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed", # Hides the console window
        "--name", "JARVIS OS",
        "run.py"
    ]
    
    print(f"Running command: {' '.join(build_command)}")
    try:
        subprocess.run(build_command, shell=True, check=True)
        print("\nBuild Successful! You can find 'JARVIS OS.exe' in the 'dist/JARVIS OS' folder.")
    except Exception as e:
        print(f"Build Failed: {e}")

if __name__ == "__main__":
    main()
