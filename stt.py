import snowboydecoder as snowboy
import signal
import speech_recognition as sr
import subprocess
import os

def on_wake():
    print "Wake Requested"

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

# hdmi audio has a negotiation phase, which can loose audio
warmup_hdmi = True
def speak(text, whisper = False):
    if warmup_hdmi:
        cmds = ["espeak", "\'" + text + "\'","-s", "130"]
        if whisper:
            cmds = cmds + ["-v", "whisper"]
        subprocess.Popen(cmds)
    else:
        subprocess.Popen(["espeak", "\'" + text + "\'", "-s 130"])

def on_speech(tmpFile):
    print "Processing Speech"
    speak("give me a second to process that")
    r = sr.Recognizer()

    with sr.AudioFile(tmpFile) as source:
        audio = r.record(source)

    try:
        rec_text = r.recognize_houndify(audio, client_id="cn8HNwSqNAsZIzyDdvEtMQ==", client_key="Zy2V7qsdxaU3toSvMaqYr-IpxabL4c5LHQgUPhDooCb2sSwExFvzlKo5bImrJ_M1wTFvQDVZNrPjlXgGEfJJag==")
        speak("You said, " + rec_text)
        print "[+]" + rec_text
    except LookupError:
        print "[+] I'm not sure what you said"
        speak("I'm not sure what you said")

    os.remove(tmpFile)

interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

signal.signal(signal.SIGINT, signal_handler)

wake_detector = snowboy.HotwordDetector("jarvis.umdl", sensitivity=[0.8,0.80], apply_frontend=False)

print "Listening... Press Ctrl+C to exit"

# main loop
wake_detector.start(detected_callback=on_wake,
               audio_recorder_callback=on_speech,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

wake_detector.terminate()
