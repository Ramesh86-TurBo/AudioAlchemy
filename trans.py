# importing libraries
import os
from pytube import YouTube
import torch
import whisper
import re
from googletrans import Translator

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
    except Exception as e:
        print(f"Error translating transcription: {e}")

def main():
    try:
        # Ask user for the YouTube video URL
        url = input("Enter the youtube video url: ")

        # Download audio
        audio_downloaded = download_audio(url, "YoutubeAudios", "audio.mp3")
        if not audio_downloaded:
            return False

        # Ask user to select the speech recognition model
        model_name = input("Select speech recognition model name (tiny, base, small, medium, large): ")

        # Transcribe the audio
        transcription = transcribe_audio(model_name, "YoutubeAudios/audio.mp3")
        if transcription is not None:
            format_result('transcription.txt', transcription)

        # Ask the user if they want to translate the transcription
        translate_choice = input("Do you want to translate audio transcription to English? (y/n): ").strip()
        if translate_choice.lower() == "y":
            translate_result('transcription.txt', 'translation.txt')
        
        # Ask the user if they want to delete the files
        delete_choice = input("Do you want to delete the audio, transcribed, and translated files? (y/n): ").strip()
        if delete_choice.lower() == "y":
            delete_files = ["YoutubeAudios/audio.mp3", "transcription.txt", "translation.txt"]
            for file_path in delete_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file_path}")

    except KeyboardInterrupt:
        print("Operation aborted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# exmaple
# "https://youtube.com/shorts/BV0taeYcKHE?feature=shared"