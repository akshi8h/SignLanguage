from llm.gemini_refiner import GeminiRefiner


class TextRefiner:
    def __init__(self):
        self.refiner = GeminiRefiner()

    def refine(self, text: str) -> str:
        if not text or not text.strip():
            return text
        return self.refiner.refine_sentence(text)
