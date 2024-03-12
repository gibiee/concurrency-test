import os
os.environ['CUDA_VISIBLE_DEVICES']='1'

from diffusers import DiffusionPipeline
import torch
import gradio as gr
from fastapi import FastAPI
import time

app = FastAPI()
concurrency_limit = 1

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

@app.get("/generate")
def api_generate() :
    result = generate_image()
    return {"result": "DONE"}

def generate_image() :
    print('Start generating !')

    images = pipe(prompt="An astronaut riding a green horse", num_inference_steps=20).images
    image = images[0]
    print(image)

    print('Finish generating !')
    return image

with gr.Blocks() as demo :
    with gr.Row() :
        with gr.Column() :
            input_text = gr.Textbox(label='input', value="An astronaut riding a green horse")
            button = gr.Button(value='button', variant="primary")

        output_img = gr.Image(label='output')
    
    button.click(fn=generate_image, outputs=output_img, concurrency_limit=concurrency_limit)

demo.launch()
# app = gr.mount_gradio_app(app, demo, path="/")