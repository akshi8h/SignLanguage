import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import os
from PIL import Image


class SignLanguageUI(tk.Tk):
    def __init__(self, callbacks: dict):
        super().__init__()

        self.callbacks = callbacks

        self.title("Sign Language to Text (ASL)")
        self.configure(bg="#1e1e1e")
        self.protocol("WM_DELETE_WINDOW", self.callbacks["on_close"])

        self._build_layout()

    def _build_layout(self):
        main = tk.Frame(self, bg="#1e1e1e")
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg="#1e1e1e")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right = tk.Frame(main, bg="#262626", width=360)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.video_label = tk.Label(left, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            left,
            text="Recognized Text",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(10, 0))

        self.text_label = tk.Label(
            left,
            text="",
            fg="#00ff99",
            bg="#1e1e1e",
            font=("Consolas", 18),
            wraplength=650,
            justify="left",
        )
        self.text_label.pack(anchor="w")

        tk.Label(
            right,
            text="Sign Reference",
            fg="white",
            bg="#262626",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=6)

        container = tk.Frame(right, bg="#262626")
        container.pack(fill=tk.BOTH, expand=True)

        self.ref_panel = self._create_scrollable_panel(container)
        self._load_reference_images()

        btn_bar = tk.Frame(self, bg="#1e1e1e")
        btn_bar.pack(fill=tk.X, pady=10)

        self._btn(btn_bar, "SPACE", self.callbacks["on_space"], "#4da6ff").pack(side=tk.LEFT, padx=8)
        self._btn(btn_bar, "DELETE", self.callbacks["on_delete"], "#ff6666").pack(side=tk.LEFT)

        # ✅ NEW BUTTON
        self._btn(
            btn_bar,
            "AUTO-CORRECT",
            self.callbacks["on_refine"],
            "#66cc99"
        ).pack(side=tk.LEFT, padx=8)

        self._btn(btn_bar, "CLEAR", self.callbacks["on_clear"], "#ff9933").pack(side=tk.LEFT, padx=8)
        self._btn(btn_bar, "QUIT", self.callbacks["on_close"], "#cc3333").pack(side=tk.RIGHT, padx=20)

    def _btn(self, parent, text, cmd, color):
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white",
            relief=tk.FLAT,
            padx=18,
            pady=6,
        )

    def _create_scrollable_panel(self, parent):
        canvas = tk.Canvas(parent, bg="#262626", highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#262626")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return scroll_frame

    def _load_reference_images(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "asl_images")

        classes = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["nothing", "space", "delete"]
        self.ref_imgs = []

        cols = 4
        thumb_size = (80, 80)

        for i, cls in enumerate(classes):
            frame = tk.Frame(self.ref_panel, bg="#262626")
            frame.grid(row=i // cols, column=i % cols, padx=6, pady=6)

            img_path = os.path.join(img_dir, f"{cls}_test.jpg")

            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGB")
                img = img.resize(thumb_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.ref_imgs.append(photo)
                tk.Label(frame, image=photo, bg="#262626").pack()
            else:
                tk.Label(frame, text="N/A", fg="red", bg="#262626").pack()

            tk.Label(
                frame,
                text=cls.upper(),
                fg="#00ffcc",
                bg="#262626",
                font=("Segoe UI", 9, "bold"),
            ).pack(pady=(2, 0))

    def update_frame(self, photo):
        self.video_label.config(image=photo)
        self.video_label.image = photo

    def update_text(self, text):
        self.text_label.config(text=text)
