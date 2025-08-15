from gtts import gTTS
import gradio as gr

def assistant(question):
    # Réponse simple (tu pourras ajouter GPT4All plus tard)
    response = f"Tu m'as demandé : {question}. Voici ma réponse vocale."

    # Créer le fichier audio
    tts = gTTS(text=response, lang='fr')
    audio_path = "reponse.mp3"
    tts.save(audio_path)

    return response, audio_path

gr.Interface(
    fn=assistant,
    inputs=gr.Textbox(label="Pose ta question"),
    outputs=[
        gr.Textbox(label="Réponse écrite"),
        gr.Audio(label="Réponse vocale", type="filepath")
    ],
    title="Assistant IA vocal de Nass 🎙️"
).launch()