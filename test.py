import gradio as gr
import time
from fastapi import FastAPI

app = FastAPI()
concurrency_limit = 1

@app.get("/test1")
async def api_test1() :
    result = await click_button1()
    return {"result": result}

@app.get("/test2")
async def api_test2() :
    result = await click_button2()
    return {"result": result}

async def click_button1() :
    print('click button1 !')
    time.sleep(10)
    print('sleep finish!')
    return 'DONE'

# 약 8초 정도 수행됨
async def click_button2() :
    start_time = time.time()
    print('click button2 !')
    total = 0
    for i in range(200000000) :
        total += i
    print(f'time : {time.time() - start_time}')
    return 'DONE'

with gr.Blocks() as demo :
    with gr.Row() :
        with gr.Column() :
            input_text = gr.Textbox(label='input')
            with gr.Row() :
                button1 = gr.Button(value='button1', variant="primary")
                button2 = gr.Button(value='button2', variant="primary")

        output_text = gr.Textbox(label='output')
    
    button1.click(fn=click_button1, outputs=output_text, concurrency_limit=concurrency_limit)
    button2.click(fn=click_button2, outputs=output_text, concurrency_limit=concurrency_limit)

app = gr.mount_gradio_app(app, demo, path="/")