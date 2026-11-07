# Kaggle notebook, see https://www.kaggle.com/code/csabafarago/image-generator-backend/
'''
!pip install \
    "torchao==0.18.0" \
    "peft==0.21.2" \
    "diffusers==0.41.0" \
    "transformers==5.20.2" \
    "accelerate==1.15.0" \
    "fastapi==0.115.6" \
    "uvicorn==0.54.0" \
    "pyngrok==9.0.2" \
    "nest-asyncio==1.6.0" \
    "google-cloud-bigquery-storage>=2.0.0"
'''

import io
import threading
import torch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from pyngrok import ngrok
from diffusers import AutoPipelineForText2Image
from kaggle_secrets import UserSecretsClient

print("Loading model onto Kaggle GPU...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")
pipe.load_lora_weights("fcsaba/csaba-style-sdxl-lora")
print("Model loaded successfully!")

app = FastAPI(title="Kaggle AI Backend")

@app.get("/generate")
def generate_image(prompt: str):
    print(f" Incoming prompt: '{prompt}'")

    generator = torch.Generator("cuda").manual_seed(42)
    with torch.no_grad():
        image = pipe(
            prompt=prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            cross_attention_kwargs={"scale": 1.1},
            generator=generator
        ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    return Response(content=buffer.getvalue(), media_type="image/png")

user_secrets = UserSecretsClient()
NGROK_TOKEN = user_secrets.get_secret("NGROK_TOKEN")
try:
    ngrok.set_auth_token(NGROK_TOKEN)
except Exception:
    pass
public_url = ngrok.connect(8000, url="abreast-calm-refining.ngrok-free.dev").public_url

print("\n" + "="*60)
print(f" KAGGLE BACKEND API IS RUNNING SUCCESSFULLY!")
print(f" Copy this public URL to your Streamlit app:")
print(f" >>> {public_url} <<<")
print("="*60 + "\n")

config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="info")
server = uvicorn.Server(config)

server_thread = threading.Thread(target=server.run, daemon=True)
server_thread.start()
