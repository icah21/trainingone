# main.py

import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

from cam import CameraDetection
from servo_controller import ServoController

# Initialize modules
camera = CameraDetection()
servo_controller = ServoController()

# Setup Tkinter window
root = tk.Tk()
root.title("Cacao Detection and Segregation")

video_label = tk.Label(root)
video_label.grid(row=0, column=0, rowspan=2)

dashboard = tk.Frame(root)
dashboard.grid(row=0, column=1, padx=10, sticky="n")

status_var = tk.StringVar()
tk.Label(dashboard, text="🧠 Current Detection", font=("Arial", 14, "bold")).pack()
tk.Label(dashboard, textvariable=status_var).pack()

history_box = tk.Listbox(dashboard, width=40, height=10)
history_box.pack(pady=(10, 0))

def update():
    frame, detected_type = camera.detect_frame()
    if frame is not None:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Update dashboard
        status_var.set(f"Detected: {detected_type}")

        # Save detection in history
        timestamp = time.strftime("%H:%M:%S")
        history_box.insert(0, f"[{timestamp}] {detected_type}")
        if history_box.size() > 10:
            history_box.delete(10)

        # Trigger servo based on detection
        if detected_type in ["Criollo", "Forastero", "Trinitario"]:
            threading.Thread(target=servo_controller.move_to_variety, args=(detected_type,)).start()

    root.after(500, update)

def close_app():
    print("[System] Closing...")
    camera.release()
    servo_controller.cleanup()
    root.destroy()

exit_button = tk.Button(dashboard, text="❌ Exit", font=("Arial", 12), command=close_app, bg="red", fg="white")
exit_button.pack(pady=10)

update()
root.mainloop()
