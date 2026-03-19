FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /root/.cache/huggingface

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG HF_TOKEN=""
ENV HF_TOKEN=${HF_TOKEN}

RUN python -c "from diffusers import StableDiffusionXLPipeline; StableDiffusionXLPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-1.0', torch_dtype=None)"
RUN python -c "from transformers import ViltProcessor, ViltForQuestionAnswering; ViltProcessor.from_pretrained('dandelin/vilt-b32-finetuned-vqa'); ViltForQuestionAnswering.from_pretrained('dandelin/vilt-b32-finetuned-vqa')"

COPY . .

CMD ["python", "-m", "bot.main"]