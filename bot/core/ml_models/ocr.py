# --- Функция для распознавания текста на изображении (OCR) ---
import pytesseract
from PIL import Image


def ocr(image_path, lang: str = "rus+eng"):
    return pytesseract.image_to_string(Image.open(image_path), lang=lang).strip()
