import sys
from pathlib import Path
from bot.core.ml_models.ocr import ocr
from bot.core.ml_models.text_to_image import generate_image as generate_image_func
import logging
import pytesseract
from bot.core.config import settings
from bot.core.ml_models.ask_from_image import vqa
from PIL import Image

#pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

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
        res = generate_image_func(prompt, output_path)
        if isinstance(res, Image.Image):
            logger.info("Received PIL.Image, saving to disk...")
            res.save(output_path)
            logger.info(f"Saved image to {output_path}")
            return output_path
        if isinstance(res, str):
            logger.info(f"Received path: {res}")
            return res
        return output_path

    @staticmethod
    def vqa_predict(image_path: str, question: str) -> str:
        """Ответ на вопрос по изображению."""
        logger.info(f"VQA: {question}")
        return vqa(image_path, question)


ml_service = MLService()
