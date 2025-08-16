import os
import requests
from gtts import gTTS
from dotenv import load_dotenv
import gradio as gr

# 🔐 Charger le token Hugging Face depuis le fichier .env
load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")

# 🔗 URL du modèle GPT4All hébergé sur Hugging Face
API_URL = "https://api-inference.huggingface.co/models/nomic-ai/gpt4all-j"

# 🧠 Fonction pour interroger GPT4All
def generate_response(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
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

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        return "Désolé, je n'ai pas compris ta question."
    except Exception as error:
        return f"Erreur lors de la génération : {str(error)}"

# 🔊 Fonction principale du chatbot
def chat_fn(message: str, history: list) -> tuple:
    response = generate_response(message)

    # Générer la réponse vocale
    tts = gTTS(text=response, lang='fr')
    audio_path = "reponse.mp3"
    tts.save(audio_path)

    # Mettre à jour l'historique du chat
    history.append((message, response))
    return history, audio_path

# 💬 Interface Gradio façon messagerie
gr.ChatInterface(
    fn=chat_fn,
    title="Assistant IA vocal de Nass 💬",
    description="Discute avec ton assistant comme dans une messagerie. Il te répond à l'écrit et à l'oral.",
    additional_inputs=gr.Audio(sources=["microphone"], type="filepath", label="Réponse vocale"),
    theme="soft"
).launch()