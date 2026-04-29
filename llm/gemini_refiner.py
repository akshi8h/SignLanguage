from google import genai

class GeminiRefiner:
    def __init__(self):
        self.client = genai.Client(
            api_key="AIzaSyAQrj0bpDqIZ3dtUyuzFbPuGeHlGivPmNI"
        )

    def refine_sentence(self, text: str) -> str:
        prompt = f"Act as a professional grammar auto-correct system. Correct the input text strictly for grammar, spelling, and word usage. Return ONLY the corrected sentence, without explanations, notes, or punctuation changes beyond what is necessary. Do not add a full stop at the end. Ensure all nouns, pronouns, adjectives, and articles are recognized and used properly:\n{text}"

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return response.text.strip()
