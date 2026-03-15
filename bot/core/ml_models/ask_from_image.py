from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

processor = ViltProcessor.from_pretrained(
    "dandelin/vilt-b32-finetuned-vqa"
)
model = ViltForQuestionAnswering.from_pretrained(
    "dandelin/vilt-b32-finetuned-vqa"
)


def vqa(image_path: str, question: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")
    outputs = model(**inputs)
    idx = outputs.logits.argmax(-1).item()
    return model.config.id2label[idx]
