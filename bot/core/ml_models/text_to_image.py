from diffusers import StableDiffusionXLPipeline
import torch


def generate_image(prompt: str, filename: str = "output.png"):
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float32,
        local_files_only=False,
    )

    pipe = pipe.to("cpu")

    image = pipe(prompt).images[0]
    image.save(filename)
    return image
