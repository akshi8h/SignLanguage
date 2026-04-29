import cv2
import threading
from collections import deque, Counter
from PIL import Image, ImageTk

from camera import CameraHandler
from predictor_manager import PredictorManager
from ui import SignLanguageUI
from text_refiner import TextRefiner


class SignLanguageApp:
    def __init__(self):
        self.predictor = PredictorManager()
        self.camera = CameraHandler(self.predictor)

        self.generated_text = ""

        # stability / debounce
        self.label_window = deque(maxlen=20)
        self.required_consistency = 0.75
        self.cooldown_frames = 0
        self.COOLDOWN_MAX = 15

        # shorter flash duration
        self.flash_frames = 0
        self.FLASH_DURATION = 3

        # Gemini refiner
        self.text_refiner = TextRefiner()

        # UI callbacks
        self.ui = SignLanguageUI({
            "on_space": self.add_space,
            "on_delete": self.delete_char,
            "on_clear": self.clear_text,
            "on_refine": self.refine_sentence,
            "on_close": self.on_close
        })

        self.ui.after(10, self.update_loop)

    # ------------------- Main Loop -------------------
    def update_loop(self):
        frame, label, conf = self.camera.read()

        if frame is not None:
            if label:
                text = f"{label.upper()} ({conf*100:.1f}%)"
                cv2.putText(
                    frame, text, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 255, 0), 2, cv2.LINE_AA
                )

            self.process_label(label)

            if self.flash_frames > 0:
                overlay = frame.copy()
                overlay[:] = (255, 255, 255)
                cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)
                self.flash_frames -= 1

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((640, 480))
            photo = ImageTk.PhotoImage(img)
            self.ui.update_frame(photo)

        self.ui.after(10, self.update_loop)

    # ------------------- Label Processing -------------------
    def process_label(self, label):
        if label is None:
            return

        if self.cooldown_frames > 0:
            self.cooldown_frames -= 1
            return

        label = label.lower()
        self.label_window.append(label)

        if len(self.label_window) < self.label_window.maxlen:
            return

        counts = Counter(self.label_window)
        dominant, freq = counts.most_common(1)[0]
        confidence = freq / len(self.label_window)

        if dominant == "nothing" or confidence < self.required_consistency:
            return

        # ---- ACTION MAPPING ----
        DELETE_LABELS = {"delete", "del", "backspace"}

        if dominant in DELETE_LABELS:
            if self.generated_text:
                self.generated_text = self.generated_text[:-1]

        elif dominant == "space":
            self.generated_text += " "

        else:
            # only accept real letters
            if len(dominant) == 1 and dominant.isalpha():
                self.generated_text += dominant.upper()

        self.ui.update_text(self.generated_text)

        self.flash_frames = self.FLASH_DURATION
        self.cooldown_frames = self.COOLDOWN_MAX
        self.label_window.clear()

    # ------------------- Text Actions -------------------
    def add_space(self):
        self.generated_text += " "
        self.ui.update_text(self.generated_text)

    def delete_char(self):
        if self.generated_text:
            self.generated_text = self.generated_text[:-1]
            self.ui.update_text(self.generated_text)

    def clear_text(self):
        self.generated_text = ""
        self.ui.update_text(self.generated_text)

    # ------------------- Sentence-Level Refinement -------------------
    def refine_sentence(self):
        sentence = self.generated_text.strip()
        if not sentence:
            return

        def background_refine():
            try:
                refined = self.text_refiner.refine(sentence)
                self.ui.after(0, self._apply_refined_sentence, refined)
            except Exception as e:
                print("❌ Sentence refinement failed:", e)

        threading.Thread(target=background_refine, daemon=True).start()

    def _apply_refined_sentence(self, text):
        self.generated_text = text
        self.ui.update_text(self.generated_text)

    # ------------------- Cleanup -------------------
    def on_close(self):
        self.camera.release()
        self.ui.destroy()


if __name__ == "__main__":
    SignLanguageApp().ui.mainloop()
