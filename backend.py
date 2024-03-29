# importing libraries
from flask import Flask, render_template, request
import os
from pytube import YouTube
import torch
import whisper
import re
from googletrans import Translator

# Create the Flask instance and pass the Flask constructor the path of the correct module
app = Flask(__name__)

# TRANSCRIBING AND TRANSLATING SCRIPT

# Function to check and select the appropriate device (CPU or CUDA)
def check_device():
    if torch.cuda.is_available() == 1:
        device = "cuda"
    else:
        device = "cpu"
    return device

# Function to download audio from a YouTube video
def download_audio(url, output_path, filename):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create a YouTube object from the URL
        yt = YouTube(url)

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        audio_stream.download(output_path=output_path, filename=filename)

        print(f"Audio downloaded to {output_path}/{filename}")
        return True
    
    except Exception as e:
        
        print(f"Error downloading audio: {e}")
        return False

# Function to transcribe the audio using Whisper
def transcribe_audio(model_name, audio_path):
    try:
        print("Transcribing audio file..")
        model = whisper.load_model(model_name, device=check_device())
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Function to format the transcription and optionally translate it to English
def format_result(file_name, text):
    format_text = re.sub('\.', '.\n', text)
    with open(file_name, 'a', encoding="utf-8") as file:
        print("Writing transcription to text file..")
        file.write(format_text)

# Function to translate the transcription to English using Google Translate
def translate_result(org_file, trans_file):
    try:
        translator = Translator()
        with open(org_file, 'r', encoding="utf-8") as transcription:
            contents = transcription.read()
            print("Translating text.")
            translation = translator.translate(contents)
        with open(trans_file, 'a', encoding="utf-8") as file:
            print("Writing translation to text file..")
            file.write(translation.text)
        return translation.text
    except Exception as e:
        print(f"Error translating transcription: {e}")
        return None

# ROUTES

# home route
@app.route('/', methods = ['GET', 'POST'])
def home():
    
    if(request.args.get('name') == '' or request.args.get('option') == ''):

        name = "Invalid URL"
        audio_downloaded = "Enter the URL"
        transcription = "Enter the URL"
        translation = "Enter the URL"
    else:

        name = request.args.get('name')
        model = request.args.get('option')

        # Download audio
        audio_downloaded = download_audio(name, "static", "audio.mp3")

        # Transcribe the audio
        transcription = transcribe_audio(model, "static/audio.mp3")

        # Saving the Transcribed text into file
        if transcription is not None:
            format_result('static/transcription.txt', transcription)
        
        # Translating the Transcribed File and saving the translation in a separate File
        translation = translate_result('static/transcription.txt', 'static/translation.txt')

    return render_template('index.html', var1 = 'home', var2 = name, var3 = check_device(), var4 = audio_downloaded, var5 = transcription, var6 = translation)


# Start with flask web app with debug as True only if this is the starting page
if __name__ == '__main__':
   app.run(debug=True)