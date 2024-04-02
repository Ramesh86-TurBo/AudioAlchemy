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

# Function to read file into bytes
def read_to_bytes(file_path):
    try:
        print("Reading file into bytes..")
        
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the contents of the file into bytes
            out_bytes = file.read()
        
        return out_bytes
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to download audio from a YouTube video
def download_audio(url, output_path, filename):
    try:
        print("downloading the audio..")

        # Create a YouTube object from the URL
        yt = YouTube(url)

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        audio_stream.download(output_path=output_path, filename=filename)

        print(f"Audio downloaded to {output_path}/{filename}")

        # Read the downloaded audio file into bytes
        audio_bytes = read_to_bytes(os.path.join(output_path, filename))

        print('Reading audio file into bytes done!')

        return audio_bytes
        
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

# Function to transcribe the audio using Whisper Model
def transcribe_audio(model_name, audio_path):
    try:
        print("Transcribing audio file..")
        
        model = whisper.load_model(model_name, device=check_device())
        result = model.transcribe(audio_path)
        return result["text"]
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Function to format the transcription
def format_result(file_name, text):
    try:
        format_text = re.sub('\.', '.\n', text)
        with open(file_name, 'a', encoding="utf-8") as file:
            print("Writing transcription to text file..")
            file.write(format_text)

        # Read the downloaded audio file into bytes
        transcribe_bytes = read_to_bytes(file_name)

        print('Reading transcribe file into bytes done!')

        return transcribe_bytes
    
    except Exception as e:
        print(f"Error creating file: {e}")
        return None
    

# Function to format the transcription and optionally translate it to English
def translate_text(org_file, trans_file):

    try:
        translator = Translator()
        with open(org_file, 'r', encoding="utf-8") as transcription:
            contents = transcription.read()
            print("Translating text.")
            translation = translator.translate(contents)
        with open(trans_file, 'a', encoding="utf-8") as file:
            print("Writing translation to text file..")
            translated_text = translation.text
            file.write(translated_text)

        return translated_text
    
    except Exception as e:
        print(f"Error translating transcription: {e}")
        return None

# function to read translate file into bytes
def translate_into_byte(file_name):

    try:

        # Read the downloaded audio file into bytes
        translate_bytes = read_to_bytes(file_name)

        print('Reading translate file into bytes done!')

        return translate_bytes
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None




# ROUTES

# home route
@app.route('/', methods = ['GET', 'POST'])
def home():
    
    if request.method == 'POST':

        name = request.form['name']
        model = request.form['option']

        # Download audio and save to database
        audio_bytes = download_audio(name, 'static', 'audio.mp3')

        # Transcribe audio and save to database
        transcription = transcribe_audio(model, 'static/audio.mp3')

        # Saving transcription into a file
        transcribed_data = format_result('static/transcription.txt', transcription)

        # Translate transcription and save to database
        translation = translate_text('static/transcription.txt', 'static/translation.txt')

        # translated file readed into bytes
        translated_data = translate_into_byte('static/translation.txt')

        if ((audio_bytes != None) or (format_result != None) or (translation != None)):

            data1 = Data(youtube_url=name, model_chosen=model, audio_file=audio_bytes, transcription_file=transcribed_data, translation_file=translated_data)
            db.session.add(data1)
            db.session.commit()


        return render_template('index.html', var1 = 'home', var2 = name, var3 = check_device(), var5 = transcription, var6 = translation)
    
    else:

        return render_template('index.html')

# Start with flask web app with debug as True only if this is the starting page
if __name__ == '__main__':
   app.run(debug=True)