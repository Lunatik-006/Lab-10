import json, time, datetime
import requests, os
from random import randint
import webbrowser
import pyttsx3, pyaudio, vosk


class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init("sapi5")

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty("voices")
        for count, voice in enumerate(self.voices):
            if count == 0:
                print("0")
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text="Готов"):
        self.tts.setProperty("voice", self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model("small_model")
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000,
        )

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer["text"]:
                    yield answer["text"]


def speak(text):
    rec.stream.stop_stream()
    speech = Speech()
    speech.text2voice(speaker=1, text=text)
    time.sleep(0.25 * len([i for i in text.split()]))
    rec.stream.start_stream()


def get_time():
    d = datetime.datetime.now()
    return d


def showfile():
    hist = open("history.txt")
    print(hist.read())
    hist.close()


def history(txt):
    try:
        with open("history.txt", "a") as f:
            f.write(txt + "\n")
    except:
        None


rec = Recognize()
text_gen = rec.listen()
speak("Starting")
history("Below is the history of your requests on " + str(get_time()) + ":")

for text in text_gen:
    print(text)
    if not os.path.exists("history.txt"):
        history("Below is the history of your requests on " + str(get_time()) + ":")
    history(text)
    if text == "закрыть":
        speak("Goodbye")
        quit()
    elif text == "покажи историю":
        try:
            showfile()
            speak("Here is the history of your requests!")
        except:
            speak("Error when executing the request!")
    elif text == "расскажи факт":
        try:
            r = requests.get(f"http://numbersapi.com/{randint(1,1000)}")
            speak(r.content)
        except:
            speak("Error when executing the request!")
    elif text == "привет":
        parts_of_day = ["morning", "afternoon", "evening", "night"]
        daypart = parts_of_day[(get_time().hour) // 6]
        speak("Good " + daypart + " !")
    elif text == "удали историю":
        try:
            os.remove("history.txt")
            speak("History has been cleared!")
        except:
            speak("Error when executing the request!")
    elif text == "банан":
        webbrowser.open("https://ru.pinterest.com/pin/859132066392585983/", new=2)
        speak("Here is your banana!")
    else:
        speak("I dont know such a request, but you can program it!")
    text = text.replace(text, "")
