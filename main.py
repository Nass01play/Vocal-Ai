import requests
from gtts import gTTS
import gradio as gr

# Ton token Hugging Face
API_TOKEN = "hf_xxxxxxxxxxx"  # Remplace par ton vrai token

# Fonction pour interroger GPT4All via Hugging Face
def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7}
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/nomic-ai/gpt4all-j",
        headers=headers,
        json=payload
    )
    return response.json()[0]["generated_text"]

# Fonction principale
def assistant(question):
    response = generate_response(question)
    tts = gTTS(text=response, lang='fr')
    audio_path = "reponse.mp3"
    tts.save(audio_path)
    return response, audio_path

# Interface Gradio
gr.Interface(
    fn=assistant,
    inputs=gr.Textbox(label="Pose ta question"),
    outputs=[
        gr.Textbox(label="Réponse écrite"),
        gr.Audio(label="Réponse vocale", type="filepath")
    ],
    title="Assistant IA vocal de Nass 🎙️"
).launch()