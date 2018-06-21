import pydub
from pydub import AudioSegment

raw_audio_file = AudioSegment.from_mp3("./Recording.MP3")

chunks = pydub.silence.split_on_silence(raw_audio_file, min_silence_len=500, silence_thresh=-30, keep_silence=500)

file_name = 0
for audio in chunks:
    audio.export(str(file_name) + ".mp3", format="mp3")
    file_name += 1

"""
num_average_milisecond = 500

start_point = 0
start = 0
end = 0
file_name = 1
is_recording = False
threshold = -16


print "loop through video"
milisecond = 0
for milisecond in range(len(audio_file)):
    current_average = []
    sound_level = audio_file[milisecond].dBFS
    
    if sound_level != -float("infinity"):
        if len(current_average) >= num_average_milisecond:
            current_average.pop(0)
        current_average.append(sound_level)
    else:
        print "loop next one"
        continue
    
    current_value = sum(current_average) / len(current_average)
    #print "current value", current_value
    
    if is_recording:
        if current_value < threshold:
            print "found end"
            #end = milisecond - num_average_milisecond + 500
            end = milisecond - num_average_milisecond
            print "(start, end)", start, end
            #audio_file[start:end].export(str(file_name) + ".mp3", format="mp3")
            file_name += 1
            is_recording = False
            current_average = []
            start = end
    else:
        if current_value > threshold:
            print "found start"
            #start = milisecond - num_average_milisecond - 500
            start = milisecond - num_average_milisecond
            if start < 0:
                start = milisecond - num_average_milisecond
            is_recording = True

print "total fild generaged", file_name
"""