import sys

def check_requirements():
    try:
        import cv2
        import mediapipe
        import pygame
        import moderngl
        import numpy
        import psutil
        import speech_recognition
        import pyaudio
        import win32api
        import PIL
        import requests
        import ollama
        import kokoro_onnx
        import sounddevice
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        # For development ease, we'll allow it to continue if some are missing 
        # but it will crash when accessing those modules.
        # sys.exit(1)

if __name__ == "__main__":
    check_requirements()
    
    from main import main
    main()
