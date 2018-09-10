import speech_recognition as sr
import pydub
from pydub import AudioSegment
from pydub.playback import play
import os.path
import string

def save_segment(file_name, new_name):
    raw_audio_file = AudioSegment.from_wav("unique/"+ file_name + ".wav")
    print("slicing video...")
    chunks = pydub.silence.split_on_silence(raw_audio_file, min_silence_len=650, silence_thresh=-35, keep_silence=1000)
    print("slicing audio to " + str(len(chunks)))
    if len(chunks) != 2:
        print("video not sliced correctly")
    else:
        print("save segment")
        # save to unique
        blank = AudioSegment.silent(duration=3000)
        segment = blank + chunks[1] + blank
        chunks = pydub.silence.split_on_silence(segment, min_silence_len=650, silence_thresh=-60, keep_silence=120)
        if len(chunks) == 1:
            print("save to unique folder")
            chunks[0].export("unique/" + new_name + ".wav", format="wav")
            # save to all
            print("save to all folder")
            all_new_file_name = get_non_repetitve_name("all/" + new_name, ".wav")
            chunks[0].export(all_new_file_name, format="wav")
            print("play segment...")
            play(chunks[0])
        else:
            print("video not sliced correctly")

def get_non_repetitve_name(file_name, file_type):
    file_to_check = file_name + file_type
    if not os.path.exists(file_to_check):
        return file_to_check
    index = 1
    is_found = False
    while not is_found:
        file_to_check = file_name + "_" + str(index) + file_type
        if not os.path.exists(file_to_check):
            is_found = True
        else:
            index += 1
    return file_to_check

quit = False
section = ""
record_type = ""

section_choices = {1: "unexpected",
                   2: "dog_scared",
                   3: "introduction",
                   4: "warmup",
                   5: "testing",
                   6: "name"}
type_choices = {1: "full",
                2: "repeat",
                3: "choose section",
                4: "quit" }
key_json_file = open("Meiying-canine.json")
key_json = key_json_file.read()
key_json_file.close()

while not quit:
    print("---------------------------------------------")
    if not section:
        print(section_choices)
        user_input = input("Press choose the section from above 1/2/3/4/5/6: ")
        section = section_choices[int(user_input)]
    
    print(type_choices)
    user_input = input("Press choose the type to start from above 1/2/3/4: ")
    if user_input == "3":
        section = ""
        continue
    elif user_input == "4":
        quit = True
        continue
    else:
        record_type = type_choices[int(user_input)]
    
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2
    recognizer.non_speaking_duration = 1.5
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
            #text = recognizer.recognize_google(audio).lower()
            text = recognizer.recognize_google_cloud(audio, credentials_json=key_json).lower().strip()
            text = "".join([i for i in text if i not in list(string.punctuation)])
            print("recognize text: " + text)
            file_name = ""
            if section == "name":
                file_name = text.replace(" ", "_")
            else:
                file_name = section + "_" + record_type + "_" + text.replace(" ", "_")
            new_file_name = "clipped/" + file_name
            output_file_name = "raw/RAW_" + file_name
            # write into the unique folder
            print("writing to unique folder...")
            output = open("unique/" + output_file_name + ".wav", "wb")
            output.write(audio.get_wav_data())
            output.close()
            # write into the all folder
            print("writing to all folder...")
            all_output_file_name = get_non_repetitve_name("all/" + output_file_name, ".wav")
            output = open(all_output_file_name, "wb")
            output.write(audio.get_wav_data())
            output.close()
            # get segment
            save_segment(output_file_name, new_file_name)
            print("new file name: " + new_file_name)
        except sr.RequestError:
            # API was unreachable or unresponsive
            print("API unavailable")
        except sr.UnknownValueError:
            # speech was unintelligible
            print("Unable to recognize speech")