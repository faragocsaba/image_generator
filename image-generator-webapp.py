# Kaggle notebook, see https://www.kaggle.com/code/csabafarago/image-generator-backend/
!pip install diffusers transformers accelerate fastapi uvicorn pyngrok nest-asyncio -q

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
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")
print("Model loaded successfully!")

app = FastAPI(title="Kaggle AI Backend")

@app.get("/generate")
def generate_image(prompt: str):
    print(f" Incoming prompt: '{prompt}'")
    
    with torch.no_grad():
        image = pipe(
            prompt=prompt, 
            num_inference_steps=1, 
            guidance_scale=0.0
        ).images[0]
    
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    
    return Response(content=buffer.getvalue(), media_type="image/png")

user_secrets = UserSecretsClient()
NGROK_TOKEN = user_secrets.get_secret("NGROK_TOKEN")
ngrok.set_auth_token(NGROK_TOKEN)
public_url = ngrok.connect(8000, domain="abreast-calm-refining.ngrok-free.dev").public_url

print("\n" + "="*60)
print(f" KAGGLE BACKEND API IS RUNNING SUCCESSFULLY!")
print(f" Copy this public URL to your Streamlit app:")
print(f" >>> {public_url} <<<")
print("="*60 + "\n")

config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="info")
server = uvicorn.Server(config)

server_thread = threading.Thread(target=server.run, daemon=True)
server_thread.start()
