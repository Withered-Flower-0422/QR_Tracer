import os
import cv2
import windnd
import webbrowser
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

from screenshot import get_screenshot
from source import src_path


class QR_Tracer:
    def __init__(self):
        # init variables
        self.img = None
        self.qr_data = None
        self.qr_detector = cv2.QRCodeDetector()

        # init gui
        self.root = tk.Tk()
        self.root.title("QR Tracer")
        self.root.geometry(
            f"300x150+{self.root.winfo_screenwidth() // 2 - 150}+{self.root.winfo_screenwidth() // 2-700}"
        )
        self.root.resizable(False, False)
        self.root.iconbitmap(src_path["qrcode"])
        windnd.hook_dropfiles(self.root, self.drop_img)

        # import images
        self.goto_png = tk.PhotoImage(file=src_path["goto"]).subsample(5, 5)
        self.import_png = tk.PhotoImage(file=src_path["import"]).subsample(5, 5)
        self.screenshot_png = tk.PhotoImage(file=src_path["screenshot"]).subsample(5, 5)

        # create label
        self.label_img = tk.Label(
            self.root, text="No QR Code Detected", font=("Microsoft YaHei", 12)
        )
        self.label_img.pack(pady=20)

        # create buttons
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(fill=tk.X)

        self.btn_import_img = tk.Button(
            self.btn_frame,
            image=self.import_png,
            width=50,
            height=50,
            command=self.import_img,
        )
        self.btn_import_img.grid(row=0, column=0, pady=5)

        self.btn_screenshot = tk.Button(
            self.btn_frame,
            image=self.screenshot_png,
            width=50,
            height=50,
            command=self.screenshot,
        )
        self.btn_screenshot.grid(row=0, column=1, pady=5)

        self.btn_goto = tk.Button(
            self.btn_frame,
            image=self.goto_png,
            width=50,
            height=50,
            command=self.goto,
        )
        self.btn_goto.grid(row=0, column=2, pady=5)

        for i in range(3):
            self.btn_frame.grid_columnconfigure(i, weight=1)

    def drop_img(self, filenames):
        path = filenames[0].decode("utf-8")
        if os.path.isfile(path) and path.endswith((".jpg", ".png", ".jpeg")):
            self.img = cv2.imread(filenames[0].decode("utf-8"))
            self.decode_qr()

    def import_img(self):
        path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")],
        )
        if path:
            self.img = cv2.imread(path)
            self.decode_qr()

    def screenshot(self):
        image = get_screenshot(self.root)
        x, y = image.size
        if image and x > 0 and y > 0:
            self.img = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        self.decode_qr()

    def goto(self):
        if self.qr_data:
            if self.qr_data.startswith("http"):
                webbrowser.open(self.qr_data)
            else:
                messagebox.showinfo("QR Content", self.qr_data)

    def decode_qr(self):
        if self.img is None:
            return
        qr_codes = self.qr_detector.detectAndDecode(self.img)
        self.qr_data = qr_codes[0] if len(qr_codes) and qr_codes[0] else None
        txt = self.qr_data if self.qr_data is not None else "No QR Code Detected"
        if len(txt) > 36:
            txt = txt[:16] + "..." + txt[-16:]
        self.label_img.config(text=txt)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    QR_Tracer().run()
