# 🎨 SDXL LoRA Custom Style Image Generator ("Csaba Style") - Integrated Project

A full-stack Generative AI web application combining a **Streamlit** frontend, a **FastAPI / ngrok** tunnel backend running on **Google Colab / Kaggle T4 GPU**, and a custom LoRA fine-tuned **Stable Diffusion XL (SDXL 1.0)** model trained on minimalist red-and-green MS Paint illustrations.

## 🔗 Live Links & References

- **Live Web Application:** [fcsaba-imagegenerator.streamlit.app](https://fcsaba-imagegenerator.streamlit.app/)
- **Hugging Face LoRA Model:** [fcsaba/csaba-style-sdxl-lora](https://huggingface.co/fcsaba/csaba-style-sdxl-lora)
- **Kaggle Backend Notebook:** [csabafarago/image-generator-backend](https://www.kaggle.com/code/csabafarago/image-generator-backend/)
- **Google Colab Testing Notebook:** [Colab Notebook Link](https://colab.research.google.com/drive/1vd9UPUVaORQM9mpMnuKEmLK14eCUHbt3)
- **GitHub Repository:** [faragocsaba/image_generator](https://github.com/faragocsaba/image_generator)

---

## ⚠️ Important Prerequisite

> **Note:** Because this application uses an on-demand Kaggle/Colab GPU backend to minimize hosting costs, **the backend notebook must be actively running** for image generation to work. If the session is offline, the Streamlit app will throw a connection timeout error.

---

## 🏗️ Architecture Overview

```text
┌──────────────────────────┐        REST API          ┌─────────────────────────┐
│   Streamlit Frontend     │ ───────────────────────> │      ngrok Tunnel       │
│ (Streamlit Cloud / Local)│ <─────────────────────── │ (Static Domain Routing) │
└──────────────────────────┘        PNG Bytes         └────────────┬────────────┘
                                                               │
                                                               ▼
                                                      ┌─────────────────────────┐
                                                      │   GPU Backend (Kaggle)  │
                                                      │  (FastAPI + SDXL Base   │
                                                      │   + Csaba Style LoRA)   │
                                                      └─────────────────────────┘
```

1. **Frontend:** Users input prompt descriptions and select generation parameters via the Streamlit interface.
2. **Tunneling:** Requests are routed through a static ngrok domain (`.ngrok-free.dev`) directly to the backend.
3. **Backend:** GPU executes inference using `stabilityai/stable-diffusion-xl-base-1.0` combined with the `fcsaba/csaba-style-sdxl-lora` adapter via Hugging Face `diffusers`, returning customized PNG image bytes.

---

## 📁 Repository Strategy & File Structure

The project has been unified under the **`faragocsaba/image_generator`** repository to maintain seamless integration with Streamlit Cloud.

```text
image_generator/
├── app.py                      # Streamlit frontend (stílusválasztóval / Csaba Stílus kapcsolóval)
├── image-generator-backend.py  # FastAPI backend (Kaggle/Colab futtatáshoz, SDXL Base + LoRA betöltéssel)
├── requirements.txt            # Függőségek (Streamlit, FastAPI, Diffusers, PyTorch, stb.)
└── README.md                   # Frissített, egységesített dokumentáció
```

---

## 🛠️ Step-by-Step Setup & Deployment Guide

### 1. ngrok Configuration (Static Domain)
To avoid updating the API URL every time the backend restarts, set up an ngrok static domain:
1. Create a free account at [ngrok.com](https://ngrok.com).
2. Retrieve your **Authtoken** under `Dashboard -> Your Authtoken`.
3. Locate your default free static dev domain under `Gateway -> Domains` (e.g., `abreast-calm-refining.ngrok-free.dev`).

---

### 2. Backend Setup (Kaggle / Google Colab)

#### A. Configure GPU Accelerator
1. Open your Kaggle Notebook or Google Colab instance.
2. Set the runtime accelerator to **GPU T4** (or T4 x2).
3. Ensure internet access is enabled.

#### B. Configure Secrets (Kaggle Secrets / Colab User Data)
1. Add your `NGROK_TOKEN` as a secret or environment variable.
2. Ensure Hugging Face permissions are available if private models are used.

#### C. Backend Inference Code Snippet
The backend initializes the pipeline by loading the base model and attaching the custom LoRA weights:

```python
import torch
from diffusers import AutoPipelineForText2Image

# 1. Load SDXL Base 1.0
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", 
    torch_dtype=torch.float16
).to("cuda")

# 2. Load custom LoRA weights directly from Hugging Face Hub
pipe.load_lora_weights("fcsaba/csaba-style-sdxl-lora")
```

---

### 3. Local Streamlit Development

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/faragocsaba/image_generator.git
   cd image_generator
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

---

### 4. Streamlit Cloud Deployment

1. Push your project files (`app.py`, `image-generator-backend.py`, `requirements.txt`, and `README.md`) to your GitHub repository: [faragocsaba/image_generator](https://github.com/faragocsaba/image_generator).
2. Log in to [share.streamlit.io](https://share.streamlit.io) using your GitHub account.
3. Configure the app with main file path `app.py` and deploy.

---

## 🧰 Tech Stack

- **Frontend:** Streamlit, Python, Pillow
- **Backend Framework:** FastAPI, Uvicorn, Python `threading`
- **AI/ML Model:** Stable Diffusion XL Base 1.0 (`stabilityai/stable-diffusion-xl-base-1.0`) + LoRA (`fcsaba/csaba-style-sdxl-lora`) via Hugging Face `diffusers` & PyTorch
- **Infrastructure & Tunneling:** Kaggle/Colab Notebooks (Nvidia T4 GPU), ngrok, Streamlit Community Cloud
