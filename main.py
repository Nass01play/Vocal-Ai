import os
import requests
from gtts import gTTS
import gradio as gr
from dotenv import load_dotenv

# 🔐 Charger les variables d'environnement depuis le fichier .env
load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")

# 🔗 URL du modèle GPT4All hébergé sur Hugging Face
API_URL = "https://api-inference.huggingface.co/models/nomic-ai/gpt4all-j"

# 🧠 Fonction pour interroger l'API Hugging Face
def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 100
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # Vérifie si la réponse est bien structurée
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "Désolé, je n'ai pas pu générer de réponse."
    except Exception as e:
        return f"Erreur : {str(e)}"

# 🔊 Fonction principale appelée par Gradio
def assistant(question):
    response = generate_response(question)

    # Générer le fichier audio avec gTTS
    tts = gTTS(text=response, lang='fr')
    audio_path = "reponse.mp3"
    tts.save(audio_path)

    return response, audio_path

# 🎙️ Interface Gradio avec texte + audio
gr.Interface(
    fn=assistant,
    inputs=gr.Textbox(label="Pose ta question ici"),
    outputs=[
        gr.Textbox(label="Réponse écrite"),
        gr.Audio(label="Réponse vocale", type="filepath")
    ],
    title="Assistant IA vocal de Nass 🎧",
    description="Pose une question et écoute la réponse générée par GPT4All"
).launch()