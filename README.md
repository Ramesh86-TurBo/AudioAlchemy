# AudioAlchemy: Transcription Tool For YouTube

AudioAlchemy is a Python script designed to streamline the process of transcribing and translating audio from YouTube videos. Users provide a video URL, select a Whisper speech recognition model, and the script does the rest. It downloads the audio, transcribes it into text, and optionally translates the transcription to English. The script offers user-friendly prompts at each step, allowing for a tailored experience. Moreover, users have the option to delete the downloaded audio and resulting files, making it a versatile and user-friendly tool for handling YouTube video content.

# Example:

Folder Structure:

![Capture3](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/e7e3f964-bc85-46f5-b054-778611fc2a5b)

1) In English:
   
YouTube URL: https://youtu.be/zkTf0LmDqKI?si=4NFlR3tcsJZUJ3Yl

Command Line: 

![yt1](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/26363f35-5630-41d3-87ae-f59d16b2bf3b)

Output:

![yt2](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/3d7126fa-44ba-4d27-9881-d4276bd9fa41)

![yt3](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/2a7f4f74-3463-48b2-abf6-8743057e59a3)

2) In Other Language:

YouTube URL: https://youtube.com/shorts/4psrAOpjEXI?si=UVoqa44sLxiKwNBY

Command Line: 

![yt1](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/26363f35-5630-41d3-87ae-f59d16b2bf3b)

Output:

![Capture2](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/98dcf786-9f3e-41ae-ab4f-34045bd106d6)

![Capture1](https://github.com/Ramesh86-TurBo/AudioAlchemy/assets/77799590/21122d96-c5dd-4265-950a-81547a8a0922)

# Installation:

To provide installation instructions for users who want to use your code from your GitHub repository, you can follow these general steps:

1. **Clone the Repository:**

   Users should start by cloning your GitHub repository to their local machine. They can do this using the `git clone` command:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```

2. **Install Dependencies:**

   Users need to install the required Python dependencies. They can use `pip` to install the necessary packages listed in your project's `requirements.txt` file. Navigate to the project directory and run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script:**

   After installing the dependencies, users can run your script. You may want to instruct them on how to execute your script, including any necessary command-line arguments or prompts. For example:

   ```bash
   python trans.py
   ```

   Users should follow the prompts and enter the required information.

4. **Optional: Virtual Environment (Recommended):**

   It's a good practice to use a virtual environment to isolate project dependencies. Users can create and activate a virtual environment as follows:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment (Windows)
   .\venv\Scripts\activate

   # Activate the virtual environment (macOS and Linux)
   source venv/bin/activate
   ```

   Then, they can proceed with steps 2 and 3 within the activated virtual environment.
