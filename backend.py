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

# program for transcribing and translating the youtube audio to text

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
    

# home route
@app.route('/', methods = ['GET', 'POST'])
def home():
   if request.method == 'POST':
      if(request.form['name'] == ''):
         name = "Invalid"
      else:
         name = request.form['name']
         
   return render_template('index.html', title = 'home', name = name, device = check_device())


# Start with flask web app with debug as True only if this is the starting page
if __name__ == '__main__':
   app.run(debug=True)