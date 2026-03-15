from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

# processor = ViltProcessor.from_pretrained(
#     "dandelin/vilt-b32-finetuned-vqa", local_files_only=True
# )
# model = ViltForQuestionAnswering.from_pretrained(
#     "dandelin/vilt-b32-finetuned-vqa", local_files_only=True
# )

from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

MODEL_PATH = "./vilt-model"

processor = ViltProcessor.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)
model = ViltForQuestionAnswering.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)


def vqa(image_path: str, question: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")
    outputs = model(**inputs)
    idx = outputs.logits.argmax(-1).item()
    return model.config.id2label[idx]
