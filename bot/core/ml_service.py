import sys
from pathlib import Path
from ocr import ocr
from text_to_image import generate_image
import logging
import pytesseract
from bot.core.config import settings
from ask_from_image import vqa

pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

logger = logging.getLogger(__name__)


class MLService:
    """Работа с моделями."""

    @staticmethod
    def ocr_predict(image_path: str) -> str:
        """Распознование текста по фото."""
        logger.info(f"OCR processing: {image_path}")
        return ocr(image_path)

    @staticmethod
    def generate_image(prompt: str, output_path: str) -> str:
        """Генерация изображения по тексту."""
        logger.info(f"Generating: {prompt} → {output_path}")
        return generate_image(prompt, output_path)

    @staticmethod
    def vqa_predict(image_path: str, question: str) -> str:
        """Ответ на вопрос по изображению."""
        logger.info(f"VQA: {question}")
        return vqa(image_path, question)


ml_service = MLService()
