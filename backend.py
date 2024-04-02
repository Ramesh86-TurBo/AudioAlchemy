# importing libraries
from flask import Flask, render_template, request
import os
from pytube import YouTube
import torch
import whisper
import re
from googletrans import Translator
from flask_sqlalchemy import SQLAlchemy


# Create the Flask instance and pass the Flask constructor the path of the correct module
app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# MODELS

# databse model for storing user and generated information
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_url = db.Column(db.String(500))
    model_chosen = db.Column(db.String(500))
    audio_file = db.Column(db.LargeBinary)  # Field for storing audio file as binary data
    transcription_file = db.Column(db.LargeBinary)  # Field for storing transcription as binary data
    translation_file = db.Column(db.LargeBinary)  # Field for storing translation as binary data

    def __repr__(self):
        return f"Entered YouTube URL: {self.youtube_url}"
    


# TRANSCRIBING AND TRANSLATING SCRIPT

# Function to check and select the appropriate device (CPU or CUDA)
def check_device():
    if torch.cuda.is_available() == 1:
        device = "cuda"
    else:
        device = "cpu"
    return device

# Function to download audio from a YouTube video
def download_audio(url):
    try:
        print("downloading the audio..")

        # Create a YouTube object from the URL
        yt = YouTube(url)

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Read audio stream into bytes
        audio_bytes = audio_stream.stream_to_buffer().read()
        return audio_bytes
    
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

# Function to transcribe the audio using Whisper Model
def transcribe_audio(model_name, audio_bytes):
    try:
        print("Transcribing audio file..")
        
        model = whisper.load_model(model_name, device=check_device())
        result = model.transcribe(audio_bytes)
        return result["text"]
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Function to format the transcription and optionally translate it to English
def translate_text(text):
    try:
        translator = Translator()
        translation = translator.translate(text)
        translated_text = translation.text

        # Convert translated text to bytes
        return translated_text.encode('utf-8')
    
    except Exception as e:
        print(f"Error translating text: {e}")
        return None


# ROUTES

# home route
@app.route('/', methods = ['GET', 'POST'])
def home():
    
    if(request.args.get('name') == '' or request.args.get('option') == ''):

        name = "Invalid URL"
        transcription = "Enter the URL"
        translation = "Enter the URL"

    else:
        name = request.args.get('name')
        model = request.args.get('option')

        # Download audio and save to database
        audio_bytes = download_audio(name)

        # Transcribe audio and save to database
        transcription = transcribe_audio(model, audio_bytes)

        # Translate transcription and save to database
        translation = translate_text(transcription)


        data1 = Data(youtube_url=name, model_chosen=model, audio_file=audio_bytes, transcription_file=transcription, translation_file=translation)
        db.session.add(data1)
        db.session.commit()

    return render_template('index.html', var1 = 'home', var2 = name, var3 = check_device(), var5 = transcription, var6 = translation)


# Start with flask web app with debug as True only if this is the starting page
if __name__ == '__main__':
   app.run(debug=True)