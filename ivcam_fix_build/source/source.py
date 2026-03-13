import psutil
import subprocess
import time
import os
import threading
import tkinter as tk
import tempfile

exe_path = r"D:\iVCam\iVCam.exe"
monitoring = False
selected_action = None


def is_running(exe_name):
    for proc in psutil.process_iter(['exe']):
        try:
            if proc.info['exe'] and os.path.abspath(proc.info['exe']) == os.path.abspath(exe_name):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def monitor():
    global monitoring
    while monitoring:
        if not is_running(exe_path):
            subprocess.Popen(exe_path)
        time.sleep(0.1)


def start_fix():
    global monitoring
    if not monitoring:
        monitoring = True
        status_label.config(text="Status: Monitoring iVCam", fg="#00ff9c")
        threading.Thread(target=monitor, daemon=True).start()


def optimize_pc():
    status_label.config(text="Status: Optimizing PC...", fg="#ffaa00")

    try:
        temp = tempfile.gettempdir()

        for root_dir, dirs, files in os.walk(temp):
            for name in files:
                try:
                    os.remove(os.path.join(root_dir, name))
                except:
                    pass

        subprocess.Popen("cleanmgr", shell=True)

        status_label.config(text="Status: Optimization Complete", fg="#00ff9c")

    except:
        status_label.config(text="Status: Error during optimization", fg="red")


def show_reasons(action):
    global selected_action
    selected_action = action

    for widget in root.winfo_children():
        widget.destroy()

    if action == "crash":
        text = (
            "Keeps Crashing Fix\n\n"
            "This will constantly monitor iVCam.\n"
            "If iVCam ever closes or crashes,\n"
            "the program will automatically reopen it."
        )
    else:
        text = (
            "Lag Fix\n\n"
            "This will clean temporary files\n"
            "and run Windows cleanup tools\n"
            "to help your PC run faster."
        )

    label = tk.Label(root, text=text, bg="#1e1e1e", fg="white",
                     font=("Segoe UI", 11), justify="center")
    label.pack(pady=20)

    cont_btn = tk.Button(
        root,
        text="Continue",
        command=start_selected,
        bg="#3a7afe",
        fg="white",
        width=20,
        height=2
    )
    cont_btn.pack(pady=10)

    back_btn = tk.Button(
        root,
        text="Back",
        command=build_main,
        bg="#444",
        fg="white",
        width=20
    )
    back_btn.pack(pady=5)


def start_selected():
    build_main()

    if selected_action == "crash":
        start_fix()
    elif selected_action == "lag":
        optimize_pc()


def close_app():
    global monitoring
    monitoring = False
    root.destroy()


def build_main():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text="What's your problem?",
                     font=("Segoe UI", 16, "bold"),
                     bg="#1e1e1e", fg="white")
    title.pack(pady=20)

    crash_btn = tk.Button(
        root,
        text="Keeps Crashing",
        command=lambda: show_reasons("crash"),
        font=("Segoe UI", 11),
        bg="#3a7afe",
        fg="white",
        width=20,
        height=2
    )
    crash_btn.pack(pady=8)

    lag_btn = tk.Button(
        root,
        text="Lagging",
        command=lambda: show_reasons("lag"),
        font=("Segoe UI", 11),
        bg="#ff9f1c",
        fg="white",
        width=20,
        height=2
    )
    lag_btn.pack(pady=8)

    close_btn = tk.Button(
        root,
        text="Close",
        command=close_app,
        bg="#444",
        fg="white",
        width=20
    )
    close_btn.pack(pady=10)

    global status_label
    status_label = tk.Label(
        root,
        text="Status: Idle",
        font=("Segoe UI", 10),
        bg="#1e1e1e",
        fg="#aaaaaa"
    )
    status_label.pack(pady=10)


root = tk.Tk()
root.title("iVCam Helper")
root.geometry("380x300")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

build_main()

root.mainloop()