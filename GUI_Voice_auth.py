import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="black")

    width, height = 500, 150
    x = (splash.winfo_screenwidth() - width) // 2
    y = (splash.winfo_screenheight() - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(splash, text="🚀 Shakthi_1.1 is initializing...Have pateince...", font=("Helvetica", 16), bg="black", fg="#00ffee")
    label.pack(expand=True)

    splash.after(3000, splash.destroy)  # auto close after 3 sec
    splash.mainloop()


import sounddevice as sd
import soundfile as sf

try:
    sd.query_devices()
    sd.default.device = (1, None)
except Exception as e:
    print("⚠️ Mic device not ready:", e)
    time.sleep(3)

try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception as e:
    print("⚠️ pyttsx3 init failed:", e)
    engine = None

from verify_pass import run_ath

fs = 44100
record_duration = 4
safe_exit_pin = ""# PLACE YOUR SAFE EXIT PIN HERE

class VoiceAuthGUI:
    def __init__(self, master):
        self.master = master
        master.title("Shakthi 1.1 - Secure Voice Access")
        master.attributes("-fullscreen", True)
        master.configure(bg="black")

        self.auth_active = True
        self.auth_loop_started = False

        self.label = tk.Label(master, text="🔐 Shakthi 1.1 - Voice Protected", font=("Helvetica", 18), bg="black", fg="white")
        self.label.pack(pady=40)

        self.wave_label = tk.Label(master, text="🎤", font=("Helvetica", 60), bg="black", fg="#00ffe4")
        self.wave_label.pack(pady=50)
        self.pulse_mic()

        self.status = tk.Label(master, text="Press Start to Authenticate", font=("Helvetica", 14), bg="black", fg="lightgray")
        self.status.pack(pady=20)

        self.start_button = tk.Button(master, text="🎤 Start Voice Auth", command=self.start_auth_loop_thread, bg="#4CAF50", fg="white", width=25, height=2)
        self.start_button.pack(pady=10)

        self.exit_frame = tk.Frame(master, bg="black")
        self.exit_frame.pack(side="bottom", pady=40)

        self.exit_label = tk.Label(self.exit_frame, text="Enter PIN for Booting:", font=("Helvetica", 12), bg="black", fg="white")
        self.exit_label.pack(pady=(10, 5))

        self.pin_entry = tk.Entry(self.exit_frame, show="*", width=20, font=("Helvetica", 14), justify='center')
        self.pin_entry.pack(pady=5)

        self.exit_button = tk.Button(self.exit_frame, text="🔓 Click to login via pin", command=self.trigger_pin_check, bg="#f44336", fg="white", width=25, height=2)
        self.exit_button.pack(pady=5)

        self.pin_attempt_flag = False  # Used to trigger PIN check

        self.start_auth_loop_thread()

    def pulse_mic(self):
        try:
            current_color = self.wave_label.cget("fg")
            next_color = "#00ffe4" if current_color == "black" else "black"
            self.wave_label.config(fg=next_color)
            self.master.after(600, self.pulse_mic)
        except tk.TclError:
            return

    def trigger_pin_check(self):
        self.pin_attempt_flag = True

    def start_auth_loop_thread(self):
        if not self.auth_loop_started:
            self.auth_loop_started = True
            threading.Thread(target=self.auth_loop, daemon=True).start()

    def run_voice_auth(self):
        self.status.config(text="🔒 Voice authentication required", fg="yellow")
        self.master.update()

        if engine:
            engine.say("Voice  Activation  Required. System  authorized  only  to  Arvind. Speak up in:")
            engine.runAndWait()

        for i in range(3, 0, -1):
            self.status.config(text=f"🎙️ Speak in {i}...", fg="cyan")
            self.master.update()
            if engine:
                engine.say(str(i))
                engine.runAndWait()

        self.status.config(text="🎤 Please speak now...", fg="cyan")
        self.master.update()
        time.sleep(1)

        self.status.config(text="Processing...This may take some time", fg="orange")
        self.master.update()

        try:
            return run_ath()
        except Exception as e:
            print("⚠️ Error during run_ath:", e)
            return False

    
    def shutdown_with_warning(self):
      self.shutdown_window = tk.Toplevel(self.master)
      self.shutdown_window.attributes('-fullscreen', True)
      self.shutdown_window.configure(bg='red')
      self.shutdown_window.title("Critical System Security")

      logo = tk.Label(self.shutdown_window, text="🛡️ Shakthi Bootloader", font=("Helvetica", 30, "bold"), bg="red", fg="white")
      logo.pack(pady=40)

      warning = tk.Label(self.shutdown_window, text="❌ Too  many  failed  attempts.\nSystem  will  shut  down  for  security.",
                       font=("Helvetica", 24), bg="red", fg="yellow")
      warning.pack(pady=30)

      self.countdown_label = tk.Label(self.shutdown_window, text="", font=("Helvetica", 20), bg="red", fg="white")
      self.countdown_label.pack(pady=20)
      threading.Thread(target=self.countdown_and_shutdown, daemon=True).start()

    def countdown_and_shutdown(self):
        for i in range(3, 0, -1):
            self.countdown_label.config(text=f"Shutting down in {i} seconds...")
            self.shutdown_window.update()
            time.sleep(1)

        if engine:
            engine.say("Unauthorized access. Shutting down system.")
            engine.runAndWait()

        os.system("shutdown /s /t 2")

    # Access granter
    def access_granted(self, msg="✅ Access Granted. Welcome AKN!"):
        self.auth_active = False
        self.status.config(text=msg, fg="lightgreen")
        self.master.update()
        if engine:
            engine.say("Access Granted. Welcome AKN")
            engine.runAndWait()
        time.sleep(2)
        self.master.attributes("-fullscreen", False)
        self.master.destroy()

    def auth_loop(self):
        while self.auth_active:
            # 3 voice attempts
            for attempt in range(3):
                success = self.run_voice_auth()
                if success:
                    self.access_granted()
                    return
                self.status.config(text=f"❌ Voice Attempt {attempt+1}/3 Failed", fg="red")
                self.master.update()
                if engine:
                    engine.say("Access Denied")
                    engine.runAndWait()
                time.sleep(1)
            if engine:
                engine.say("Maximum   access   reached   now    try    pin")
                engine.runAndWait()
            time.sleep(1)
            # 3 PIN attempts
            for pin_attempt in range(3):
                self.status.config(text=f"🔑 Enter PIN Attempt {pin_attempt+1}/3", fg="orange")
                self.master.update()

                self.pin_attempt_flag = False
                while not self.pin_attempt_flag and self.auth_active:
                    time.sleep(0.5)
                    self.master.update()

                pin = self.pin_entry.get()
                self.pin_entry.delete(0, tk.END)
                if pin == safe_exit_pin:
                    self.access_granted("✅ PIN Access Granted.")
                    return
                else:
                    messagebox.showerror("Wrong PIN", f"Attempts left: {2 - pin_attempt}")
                    if engine:
                        engine.say("Wrong PIN")
                        engine.runAndWait()
            # If all fail: Lock and restart
            self.shutdown_with_warning()
            return

if __name__ == "__main__":
    show_splash()
    root = tk.Tk()
    app = VoiceAuthGUI(root)
    root.mainloop()
