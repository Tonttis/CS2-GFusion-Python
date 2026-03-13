import ctypes
import ctypes.wintypes as wt
import math
import time
import struct

ole32 = ctypes.windll.ole32
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
gdi32 = ctypes.windll.gdi32

try:
    d3d11 = ctypes.windll.d3d11
    dxgi = ctypes.windll.dxgi
    d2d1 = ctypes.windll.d2d1
    dwrite = ctypes.windll.dwrite
except OSError:
    raise ImportError("D3D11/D2D1 not found.")

class IUnknown(ctypes.Structure):
    _fields_ = [("lpVtbl", ctypes.c_void_p)]
    def _vt(self, idx, res, *args):
        vt = ctypes.cast(self.lpVtbl, ctypes.POINTER(ctypes.c_void_p))
        return ctypes.cast(vt[idx], ctypes.CFUNCTYPE(res, ctypes.c_void_p, *args))

class DX11Renderer:
    def __init__(self, title="GFusion", fps=144):
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)
        self.fps = fps
        self._frame_time = 1/fps
        self._last_time = time.perf_counter()
        self.current_fps = 0
        self._frame_count = 0
        self._fps_timer = time.perf_counter()
        self.init_window(title)
        self.init_dx()

    def init_window(self, title):
        wc = wt.WNDCLASS()
        wc.lpfnWndProc = user32.DefWindowProcW
        wc.lpszClassName = title
        wc.hInstance = kernel32.GetModuleHandleW(None)
        user32.RegisterClassW(ctypes.byref(wc))
        self.hwnd = user32.CreateWindowExW(
            0x80000 | 0x20 | 0x8 | 0x80, # EX_LAYERED | TRANSPARENT | TOPMOST | TOOLWINDOW
            title, title, 0x80000000, # WS_POPUP
            0, 0, self.width, self.height, None, None, wc.hInstance, None
        )
        user32.SetLayeredWindowAttributes(self.hwnd, 0, 0, 1) # LWA_COLORKEY
        user32.ShowWindow(self.hwnd, 5)

    def init_dx(self):
        # Simplified DX11/D2D init for brevity in this mock
        # Real version uses full D3D11CreateDevice and CreateSwapChain
        pass

    def begin_scene(self):
        now = time.perf_counter()
        if now - self._last_time < self._frame_time: return False
        self._last_time = now
        # D2D BeginDraw logic here
        return True

    def end_scene(self):
        # D2D EndDraw + SwapChain Present logic here
        self._frame_count += 1
        now = time.perf_counter()
        if now - self._fps_timer >= 1.0:
            self.current_fps = self._frame_count
            self._frame_count = 0
            self._fps_timer = now

    def draw_text(self, text, x, y, color=(255,255,255), size=14, centered=False): pass
    def draw_line(self, x1, y1, x2, y2, color): pass
    def draw_box(self, x, y, w, h, color): pass
    def draw_filled_rect(self, x, y, w, h, color): pass
    def draw_circle(self, x, y, r, color): pass
