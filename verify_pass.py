import os
import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa
import noisereduce as nr
from fastdtw import fastdtw
from numba import njit
from scipy.signal import butter, lfilter
from sklearn.preprocessing import normalize

# === CONFIGURATION ===
fs = 44100
duration = 4  # seconds
COST_THRESHOLD = 46

# === Bandpass Filter ===
def bandpass_filter(data, lowcut=300.0, highcut=3400.0, fs=44100, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# === MFCC Extraction ===
def load_and_extract_mfcc(path):
    try:
        y, sr = librosa.load(path, sr=fs)
        y = y / np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else y
        y = bandpass_filter(y, fs=sr)
        y = nr.reduce_noise(y=y, sr=sr)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc = mfcc - np.mean(mfcc, axis=1, keepdims=True)
        return mfcc.T
    except Exception as e:
        print(f"⚠️ MFCC extraction error: {e}")
        return None

# === Euclidean Distance Optimized with Numba ===
@njit
def euclidean_dist(v1, v2):
    dist = 0.0
    for i in range(len(v1)):
        diff = v1[i] - v2[i]
        dist += diff * diff
    return dist ** 0.5

# === Main Authentication Function ===
def run_ath():
    try:
        print("🔐 Starting Voice Authentication")

        # === Paths ===
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_dir = os.path.join(script_dir, "samples_folder")
        test_path = os.path.join(script_dir, "voice_test.wav")

        # === Pre-checks ===
        if not os.path.exists(sample_dir) or not os.listdir(sample_dir):
            print("⚠️ Sample folder missing or empty.")
            return False

        try:
            devices = sd.query_devices()
        except Exception as e:
            print(f"⚠️ Audio device error: {e}")
            return False

        # === Record New Test Sample ===
        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            sf.write(test_path, recording.flatten(), fs)
            print("📁 Test recording saved.")
        except Exception as e:
            print(f"🎤 Recording failed: {e}")
            return False

        # === Load Reference Samples ===
        def load_all_mfcc(sample_dir):
            mfccs = []
            for filename in os.listdir(sample_dir):
                if filename.endswith(".wav"):
                    path = os.path.join(sample_dir, filename)
                    mfcc = load_and_extract_mfcc(path)
                    if mfcc is not None:
                        mfccs.append(mfcc)
            return mfccs

        reference_mfccs = load_all_mfcc(sample_dir)
        if not reference_mfccs:
            print("⚠️ No valid MFCCs extracted from samples.")
            return False

        test_mfcc = load_and_extract_mfcc(test_path)
        if test_mfcc is None:
            print("⚠️ Failed to extract MFCC from test sample.")
            return False

        print(f"📊 Test MFCC shape: {test_mfcc.shape}")

        # === DTW Comparison ===
        def min_avg_cost(test_mfcc, reference_mfccs):
            min_cost = float('inf')
            for r in reference_mfccs:
                distance, path = fastdtw(test_mfcc, r, dist=euclidean_dist)
                if len(path) == 0:
                    continue
                avg_cost = distance / len(path)
                if avg_cost < min_cost:
                    min_cost = avg_cost
            return min_cost

        min_cost = min_avg_cost(test_mfcc, reference_mfccs)
        print(f"💰 Minimum Average Cost: {min_cost:.2f}")

        # === Decision ===
        if min_cost < COST_THRESHOLD:
            print("✅ Access Granted")
            return True
        else:
            print("❌ Access Denied")
            return False

    except Exception as e:
        print(f"🔥 Unexpected error: {e}")
        return False

# === CLI test ===
if __name__ == "__main__":
    run_ath()
