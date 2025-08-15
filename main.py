import os
import requests
from gtts import gTTS
import gradio as gr
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment

# 🔐 Charger le token Hugging Face depuis .env
load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")

# 🔗 URL du modèle GPT4All hébergé sur Hugging Face
API_URL = "https://api-inference.huggingface.co/models/nomic-ai/gpt4all-j"

# 🧠 Fonction pour interroger GPT4All
def generate_response(prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"temperature": 0.7, "max_new_tokens": 100}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "Désolé, je n'ai pas compris ta question."
    except Exception as e:
        return f"Erreur : {str(e)}"

# 🎙️ Fonction pour convertir l'audio en texte
def transcribe(audio):
    recognizer = sr.Recognizer()
    audio_file = "input.wav"
    audio.export(audio_file, format="wav")
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language="fr-FR")
        except sr.UnknownValueError:
            return "Je n'ai pas compris ta voix."
        except sr.RequestError:
            return "Erreur de reconnaissance vocale."

# 🔊 Fonction principale
def assistant(audio):
    question = transcribe(audio)
    response = generate_response(question)
    tts = gTTS(text=response, lang='fr')
    audio_path = "reponse.mp3"
    tts.save(audio_path)
    return question, response, audio_path

# 🖼️ Interface Gradio avec entrée vocale + sortie texte + audio
gr.Interface(
    fn=assistant,
    inputs=gr.Audio(sources="microphone", type="filepath", label="Parle ici"),
    outputs=[
        gr.Textbox(label="Ce que tu as dit"),
        gr.Textbox(label="Réponse écrite"),
        gr.Audio(label="Réponse vocale", type="filepath")
    ],
    title="Assistant IA vocal de Nass 🎙️",
    description="Parle à ton assistant et écoute sa réponse intelligente"
).launch()