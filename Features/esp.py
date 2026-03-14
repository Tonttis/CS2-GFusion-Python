import math
import time
import ctypes
import struct
from ctypes import windll, wintypes, byref, c_float, c_size_t
from ctypes.wintypes import RECT
import sys
import os
import threading
from Process.config import Config
from Process.offsets import Offsets
from Process.memory_interface import MemoryInterface
from Features import worldesp
from Performance.dx11_renderer import DX11Renderer # NEW Renderer

def main():
    hwnd = windll.user32.FindWindowW(None, "Counter-Strike 2")
    if not hwnd:
        print("[!] CS2 not running.")
        return
    
    # Use high-performance DX11 renderer
    overlay = DX11Renderer("GFusion", fps=144)
    
    # Unified loop using GPU-acceleration
    while True:
        if not overlay.begin_scene():
            continue
            
        # ... (Drawing logic) ...
        
        overlay.end_scene()
