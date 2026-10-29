import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    print("Ai Said:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech synthesis error: {e}")


def listen():
    text = ""
    print("Listening...")
    try:
        with sr.Microphone() as source:
            # recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print("Text:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Microphone or speech input error: {e}")

    return text