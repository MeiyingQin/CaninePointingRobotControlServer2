import speech_recognition as sr
import pydub
from pydub import AudioSegment
from pydub.playback import play

def save_segment(file_name, new_name):
    raw_audio_file = AudioSegment.from_wav(file_name)
    print("slicing video...")
    chunks = pydub.silence.split_on_silence(raw_audio_file, min_silence_len=500, silence_thresh=-30, keep_silence=500)
    if len(chunks) != 3:
        print("video not sliced correctly")
    else:
        print("save segment")
        segment = chunks[2].export(new_name, format="wav")
        print("play segment...")
        play(chunks[2])

quit = False

while not quit:
    print("---------------------------------------------")
    user_input = input("Press any key to start or q to quit: ")
    if user_input == "q":
        quit = True
        continue
    
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 4
    recognizer.non_speaking_duration = 2
    mic = sr.Microphone()
    output_file_name = "test.wav"
    new_file_name = "new.wav"
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("start listening")
        audio = recognizer.listen(source)
        print("finish listening")
        
        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            #new_file_name = recognizer.recognize_google(audio).replace(" ", "_") + ".wav"
            output = open(output_file_name, "wb")
            output.write(audio.get_wav_data())
            output.close()
            save_segment(output_file_name, new_file_name)
        except sr.RequestError:
            # API was unreachable or unresponsive
            print("API unavailable")
        except sr.UnknownValueError:
            # speech was unintelligible
            print("Unable to recognize speech")