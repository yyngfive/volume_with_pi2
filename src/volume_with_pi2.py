import tkinter as tk
from icecream import ic #debug
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class Volume():
    def __init__(self) -> None:
        pass

    def volume_system(self) -> int:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = round(volume.GetMasterVolumeLevelScalar() * 100)
        ic(volume.GetVolumeRange())
        ic(current)
        ic(volume.GetMute())
        if volume.GetMute():
            return 0
        else:
            return current

    def set_volume(self, value) -> None:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        ic(value)
        volume.SetMasterVolumeLevelScalar(value / 100,None)

def check(event):
    num = entry_pi.get()
    if len(num) <= 2:
        pass
    elif num == pi[:len(num)]:
        current.set(f'Current Volume: {len(num) - 2}%')
        volume.set_volume(len(num) - 2)
        is_failed.set('')
    else:
        is_failed.set('Fail, try again. ')

def set_focus(event):
    pass

root = tk.Tk()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
window_w = 500
window_h = 100
root.geometry(f'{window_w}x{window_h}+' + 
              f'{int((screen_w-window_w)/2)}+{int((screen_h-window_h)/2)}')
root.resizable(0,0)
root.title('Volume_with_pi2')

pi_100 = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'
pi = pi_100
volume = Volume()

current = tk.StringVar()
is_failed = tk.StringVar()
current.set(f'Current Volume: {volume.volume_system()}%')
#is_failed.set('Fail, try again. ')
is_failed.set('')
label_current = tk.Label(root,textvariable=current)
frame_input = tk.Frame(root)
label_enter = tk.Label(frame_input,text='Please enter pi for volume')
entry_pi    = tk.Entry(frame_input,width=35)
label_failed = tk.Label(frame_input,textvariable=is_failed,fg='Red')

entry_pi.bind('<FocusIn>',set_focus)
entry_pi.bind('<KeyRelease>',check)

label_current.pack(anchor='nw')
frame_input.pack(anchor='nw')
label_enter.pack(side='left')
entry_pi.pack(side='left')
label_failed.pack(side='left')

root.mainloop()