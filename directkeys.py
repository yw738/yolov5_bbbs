# coding=utf-8
import win32api
import win32con

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "LEFT": 75, "UP": 73, "RIGHT": 76,
    "DOWN": 74, "CTRL": 17, "ALT": 18, "F2": 113, "ESC": 27, "SPACE": 32, "NUM0": 96
}
#                 i          k            l              j
# direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}
direct_dic = {"UP": 73, "DOWN": 74, "LEFT": 75, "RIGHT": 76}

def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), 0, 0)


def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def key_press(key):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(0.02)
    key_up(key)
    time.sleep(0.01)

####################################
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# W = 0x11
# A = 0x1E
# S = 0x1F
# D = 0x20

# M = 0x32
# J = 0x24
# K = 0x25
# LSHIFT = 0x2A
# R = 0x13  # 用R代替识破
# V = 0x2F

# Q = 0x10
# I = 0x17
# O = 0x18
# P = 0x19
# C = 0x2E
# F = 0x21

# up = 0xC8
# down = 0xD0
# left = 0xCB
# right = 0xCD

# direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}
direct_dic = {"UP": 73, "DOWN": 74, "LEFT": 75, "RIGHT": 76}

esc = 0x01

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# def go_back():
#     PressKey(S)
#     time.sleep(0.4)
#     ReleaseKey(S)


if __name__ == "__main__":
    time1 = time.time()
    k = "LEFT"
    s = "A"
    while True:
        if abs(time.time() - time1) > 3:
            break
        else:
            # if k not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            #     key_press(k)
            # else:
            #     PressKey(direct_dic[k])
            #     time.sleep(0.1)
            #     ReleaseKey(direct_dic[k])
            #     time.sleep(0.2)
            # PressKey(direct_dic[k])
            key_down('L')
            # key_down(s)
            time.sleep(0.02)
            # key_up(s)lllllllllll
            # key_up('L')
            # ReleaseKey(direct_dic[k])
            time.sleep(0.02)

