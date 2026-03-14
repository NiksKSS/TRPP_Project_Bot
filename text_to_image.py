from diffusers import StableDiffusionXLPipeline
import torch

def generate_image(prompt: str, filename: str = "output.png"):
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
    )
    pipe = pipe.to("mps")
    
    image = pipe(prompt).images[0]
    image.save(filename)
    print(f"Сохранено: {filename}")
    return image

# Вызов
generate_image("a cat sitting on a table, photorealistic")