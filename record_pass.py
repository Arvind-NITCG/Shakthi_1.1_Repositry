import sounddevice as sd
import soundfile as sf
import os

fs = 44100  
seconds = 4 

print("Please say your voice password after five seconds...")
sd.sleep(5000)

print("Recording...")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
print("Done!")

# Get the folder of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "sample5.wav")

sf.write(save_path, myrecording.flatten(), fs)
print(f"File saved at: {save_path}")
