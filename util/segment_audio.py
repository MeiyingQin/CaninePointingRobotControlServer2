from pydub import AudioSegment

audio_file = AudioSegment.from_mp3("sentences.mp3")

num_average_milisecond = 5

current_average = []

for count in range(num_average_milisecond):
    current_average.append(audio_file[count])
    
start = 0
end = 0
file_name = 1
is_recording = False

for milisecond in range(5, len(audio_file)):
    current_average.pop(0)
    current_average.append(audio_file[milisecond])
    
    if is_recording:
        pass
    else:
        pass