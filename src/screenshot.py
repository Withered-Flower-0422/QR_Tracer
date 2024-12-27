import tkinter as tk
from PIL import Image, ImageGrab, ImageTk

_img = None


def get_screenshot(root=None):
    screenshot = ScreenshotApp(root)
    screenshot.root.mainloop()
    return _img


class ScreenshotApp:
    def __init__(self, root):
        # init gui
        self.root = tk.Toplevel(root) if root else tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.full_screen = self.get_full_screen()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.config(cursor="crosshair")

        # init variables
        self.rect = None
        self.start_x = None
        self.start_y = None

        # crearte canvas for rectangle
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.full_screen)
        self.canvas.pack()

        # bind events
        self.canvas.bind("<ButtonPress-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<ButtonPress-3>", self.on_right_down)

    def get_full_screen(self, board_width=2):
        new_image = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        new_image.paste(
            ImageGrab.grab().crop(
                (
                    board_width,
                    board_width,
                    self.width - board_width,
                    self.height - board_width,
                )
            ),
            (board_width, board_width),
        )
        return ImageTk.PhotoImage(new_image)

    def on_left_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_left_up(self, event):
        global _img
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        _img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.root.quit()
        self.root.destroy()

    def on_right_down(self, event):
        global _img
        _img = None
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    get_screenshot().show()
