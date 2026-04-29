class TextBuffer:
    def __init__(self):
        self.text = ""

    def apply(self, label):
        if label == "space":
            self.text += " "
        elif label == "delete":
            self.text = self.text[:-1]
        elif label not in ["nothing", None]:
            self.text += label.upper()

    def clear(self):
        self.text = ""

    def get(self):
        return self.text
