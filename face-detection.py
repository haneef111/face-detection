import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Load Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# GUI class
class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Face Detection App")
        self.root.configure(bg="#1e1e2f")
        self.root.geometry("750x640")
        self.root.resizable(False, False)

        self.cap = None
        self.running = False

        # Title
        tk.Label(root, text="Real-Time Face Detection", font=("Segoe UI", 22, "bold"),
                 bg="#1e1e2f", fg="white").pack(pady=(15, 5))

        # Card frame
        self.card = tk.Frame(root, bg="#2b2b3c", bd=0, relief="flat", width=680, height=500)
        self.card.pack(pady=10)
        self.card.pack_propagate(0)  # Prevent resizing to fit content

        # Video display
        self.video_label = tk.Label(self.card, bg="#2b2b3c")
        self.video_label.pack()

        # Buttons
        self.button_frame = tk.Frame(root, bg="#1e1e2f")
        self.button_frame.pack(pady=10)

        self.btn_start = tk.Button(self.button_frame, text="▶ Start Camera", width=18, command=self.start_camera,
                                   font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", bd=0,
                                   activebackground="#2ecc71", activeforeground="white", cursor="hand2")
        self.btn_start.grid(row=0, column=0, padx=10, pady=5)

        self.btn_stop = tk.Button(self.button_frame, text="■ Stop Camera", width=18, command=self.stop_camera,
                                  font=("Segoe UI", 12, "bold"), bg="#e74c3c", fg="white", bd=0,
                                  activebackground="#c0392b", activeforeground="white", cursor="hand2",
                                  state="disabled")
        self.btn_stop.grid(row=0, column=1, padx=10, pady=5)

        # Footer
        tk.Label(root, text="Developed by Shaik Mohammad Haneef • Python + OpenCV + Tkinter",
                 bg="#1e1e2f", fg="#bdc3c7", font=("Segoe UI", 9)).pack(pady=(10, 5))

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.update_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)

                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)

            self.root.after(10, self.update_frame)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
