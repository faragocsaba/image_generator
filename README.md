# 🎨 SDXL Turbo Image Generator

A full-stack Generative AI web application that produces images from text prompts in real time. The project uses a decoupled microservice architecture: a **Streamlit** frontend hosted on Streamlit Cloud communicates via a **FastAPI / ngrok** tunnel with a **Google Colab / Kaggle T4 GPU** backend executing the **Stable Diffusion XL Turbo** model.

## 🔗 Live Links

* **Live Web Application:** [fcsaba-imagegenerator.streamlit.app](https://fcsaba-imagegenerator.streamlit.app/)
* **Kaggle Backend Notebook:** [csabafarago/image-generator-backend](https://www.kaggle.com/code/csabafarago/image-generator-backend/)
* **GitHub Repository:** [faragocsaba/image_generator](https://github.com/faragocsaba/image_generator)

---

## ⚠️ Important Prerequisite

> **Note:** Because this application uses an on-demand Kaggle GPU backend to minimize hosting costs, **the Kaggle backend notebook must be actively running** for image generation to work. If the Kaggle session is offline, the Streamlit app will throw a connection timeout error.

---

## 🏗️ Architecture Overview

```
┌────────────────────────-─┐         REST API         ┌─────────────────────────┐
│   Streamlit Frontend     │ ───────────────────────> │      ngrok Tunnel       │
│ (Streamlit Cloud / Local)│ <─────────────────────── │ (Static Domain Routing) │
└────────────────────────-─┘         PNG Bytes        └────────────┬────────────┘
                                                                   │
                                                                   ▼
                                                      ┌─────────────────────────┐
                                                      │    Kaggle GPU Backend   │
                                                      │  (FastAPI + SDXL Turbo) │
                                                      └─────────────────────────┘
```

1. **Frontend:** Users input prompt descriptions into the Streamlit interface.
2. **Tunneling:** Requests are routed through a static ngrok domain (`.ngrok-free.dev`) directly to the backend.
3. **Backend:** Kaggle GPU executes single-step inference using `stabilityai/sdxl-turbo` via Hugging Face `diffusers` and returns PNG image bytes.

---

## 🛠️ Step-by-Step Setup & Deployment Guide

### 1. ngrok Configuration (Static Domain)
To avoid updating the API URL every time the backend restarts, set up an ngrok static domain:
1. Create a free account at [ngrok.com](https://ngrok.com).
2. Retrieve your **Authtoken** under `Dashboard -> Your Authtoken`.
3. Locate your default free static dev domain under `Gateway -> Domains` (e.g., `abreast-calm-refining.ngrok-free.dev`).

---

### 2. Kaggle Backend Setup

#### A. Create and Configure the Notebook
1. Go to Kaggle and create a new Notebook.
2. In the right-side **Settings** panel, configure the following:
   * **Accelerator:** Select **GPU T4 x2** (or GPU T4).
   * **Internet:** Ensure internet access is toggled **ON** (required for the ngrok tunnel to connect).
3. Title your notebook accordingly (e.g., `image-generator-backend`).

#### B. Configure Kaggle Secrets
1. In the top menu of your notebook, go to **Add-ons -> Secrets**.
2. Add a new secret:
   * **Label:** `NGROK_TOKEN`
   * **Value:** *(Paste your ngrok Authtoken)*
3. Enable the checkbox to attach the secret to the notebook.

#### C. Running and Stopping the Backend
* **Running:** Execute the notebook cells to initialize the model pipeline, fetch the ngrok secret, and start the background FastAPI server on the GPU instance.
* **Stopping the Session:** To save your weekly GPU quota when finished, manually stop the active runtime:
  * Click the **Stop** button / active session status indicator at the top right of the notebook interface.
  * Alternatively, go to **Run -> Stop session** in the top menu bar to shut down the session completely.

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

1. Push your project files (`app.py`, `requirements.txt`, and `README.md`) to your GitHub repository: [faragocsaba/image_generator](https://github.com/faragocsaba/image_generator).
2. Log in to [share.streamlit.io](https://share.streamlit.io) using your GitHub account.
3. Click **New app** and configure:
   * **Repository:** `faragocsaba/image_generator`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Click **Deploy!**

---

## 🧰 Tech Stack

* **Frontend:** Streamlit, Python, Pillow
* **Backend Framework:** FastAPI, Uvicorn, Python `threading`
* **AI/ML Model:** Stable Diffusion XL Turbo (`stabilityai/sdxl-turbo`) via Hugging Face `diffusers` & PyTorch
* **Infrastructure & Tunneling:** Kaggle Notebooks (Nvidia T4 GPU), ngrok, Streamlit Community Cloud
