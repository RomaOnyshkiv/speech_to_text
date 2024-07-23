import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator


def extract_audio(input_file, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='wav')
            .run()
        )
        print(f"Audio extracted and saved to {output_file}")
    except ffmpeg.Error as e:
        print(e.stderr)
        print("Error extracting audio")


def transcribe_audio(audio_file, text_file):
    recognizer = sr.Recognizer()

    # Convert audio to the correct format
    sound = AudioSegment.from_wav(audio_file)
    sound = sound.set_channels(1)  # Mono
    sound.export("converted_audio.wav", format="wav")

    with sr.AudioFile("converted_audio.wav") as source:
        audio = recognizer.record(source)

        try:
            # Use Google Web Speech API
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Transcription: {text}")

            # Save the transcription to a text file
            with open(text_file, "w") as file:
                file.write(text)
            print(f"Transcription saved to {text_file}")
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

def translate_text(r_text, en_text):
    translator = Translator()
    with open(r_text, "r", encoding='utf-8') as input_f:
        input_text = input_f.read()
        english_translation = translator.translate(input_text, src='auto', dest='en').text
        with open(en_text, "w", encoding='utf-8') as output_f:
            output_f.write(english_translation)
    print(f"Translation saved to {en_text}")


input_mov_file = 'video.MOV'
extracted_audio_file = 'file.wav'
output_text_file = 'transcription.txt'
translated_text = 'output_english.txt'


def get_audio_and_translate():
    extract_audio(input_mov_file, extracted_audio_file)
    transcribe_audio(extracted_audio_file, output_text_file)
    translate_text(output_text_file, translated_text)


get_audio_and_translate()