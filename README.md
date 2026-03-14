# TRPP_Project_Bot

Бот для работы с изображениями на базе `aiogram 3.x` и машинного обучения.

---

## Функционал

| Команда | Описание |
|---------|----------|
| `/start` | Запустить бота |
| `/help` | Показать справку |
| `/photo_to_text` | Распознать текст на фото |
| `/text_to_photo` | Сгенерировать изображение по описанию |
| `/ask_from_image` | Задать вопрос по изображению |

---

## Требования

| Компонент | Версия |
|-----------|--------|
| Python | 3.10+ |
| pip | 23.0+ |
| Git | 2.40+ |

### Зависимости

Все зависимости устанавливаются через `requirements.txt`:

```bash
pip install -r requirements.txt
```
## Системные зависимости

| ОС | Требование |
|----|------------|
| **Windows** | Tesseract OCR + языки `rus` и `eng` |
| **macOS** | `brew install tesseract tesseract-lang` |
| **Linux** | `sudo apt install tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng` |

---

## Запуск программы

```bash
git clone https://github.com/NiksKSS/TRPP_Project_Bot.git
cd TRPP_Project_Bot
python -m bot.main
```
