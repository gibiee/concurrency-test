from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

prompt = "An astronaut riding a green horse"
images = pipe(prompt=prompt, num_inference_steps=20).images
print(images)
image = images[0]
print(image)