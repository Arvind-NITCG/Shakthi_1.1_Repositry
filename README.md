# Shakthi_1.1v — GUI-Based Voice Authentication System

Shakthi_1.1v is a **Python-powered voice authentication system** that protects access to your system using **your unique voice**. It captures a voice input, compares it to stored samples using **MFCC + Dynamic Time Warping**, and grants access only when your voice matches.

This is **not a general-purpose voice recognition tool** - it is **personalized**. It's built to recognize **you**, and only you.

---

## Features

-  Records your voice via microphone
-  Filters and cleans the audio
-  Extracts MFCC features and compares using DTW (Dynamic Time Warping)
-  Allows access only when the voice matches your stored samples
-  Falls back to PIN (optional) on repeated failure
-  Fully local and offline - no cloud or external API
-  Can be converted into an `.exe` for deployment

---

##  Project Structure 
 
  Shakthi_1.1v/
   —GUI_Voice_auth.py # Main GUI interface
├── record_pass.py # Used to record your voice samples
├── verify_pass.py # Auth engine using DTW + MFCC
├── Voice_test.wav # Voice input placeholder (used at runtime)
├── samples_folder/ # Stores your personal reference samples
│ └── .gitkeep # Keeps the folder in version control
├── Shakthi_1.1.spec # PyInstaller spec file to build .exe
├── requirements.txt # Python package dependencies
├── .gitignore # To exclude build files and logs

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Arvind-NITCG/Shakthi_1.1v.git
cd Shakthi_1.1v
```
---
# Create Conda Environment (Recommended)
 ->We recommend using a Conda environment to manage dependencies, especially if you plan to build the `.exe` or run the full voice pipeline (librosa, scipy, noisereduce)
    However, using `pip` in a virtualenv or system Python also works.

 -> **Miniconda Installation (Recommended for Developers)**
    We recommend using Miniconda to create an isolated Python environment for this project. It helps prevent package conflicts and makes it easier to manage dependencies like `scipy` and `librosa`.
    
   Download Miniconda here:  
   👉 https://docs.conda.io/en/latest/miniconda.html
    create a virtual environment in conda like:
       conda create -n shakthi_env python=3.11
       conda activate shakthi_env

# Install Dependencies
```
    pip install -r requirements.txt
```
   Having issues installing packages like `scipy` or `sounddevice` on Windows?
    You can download pre-built `.whl` files from Gohlke's Unofficial Binaries:
     https://www.lfd.uci.edu/~gohlke/pythonlibs/

   Install them using:
     ```
     pip install path/to/downloaded_file.whl
     ```

# Setting Up Your Voice
  Before running the GUI, you must register your voice samples.
  
  -> Step 1: Run record_pass.py
     This will let you record your own voice samples.
     python record_pass.py

  The .wav files will be saved inside samples_folder/. These files act as your voice "password".
  Try to make atleast 6 samples of your voice for DTW comparison

# ⚠️ Before using the app, you must **tune the DTW cost threshold** for your own voice and make your own SAFE EXIT PIN

   ### How to Find Your Threshold

   1. Run `record_pass.py` and create your voice samples in `samples_folder/`.
   2. Temporarily run `verify_pass.py **manually** several times using your own voice:
      python verify_pass.py
   3.Observe the Output
     DTW Total Distance: 64000
     Average cost per frame: 31.25
   4. Set your COST_THRESHOLD slightly above your best matching average.
      Example: If your average cost is 31.25, try COST_THRESHOLD = 35.
   5. Save the new value inside:
      COST_THRESHOLD = 35  # <- set in verify_pass.py
   6. Open GUI_Voice_auth.py and in the line 45 set your Safe Exit Pin
   7. You're now ready to run the GUI.



# Once COST_THRESHOLD and Safe-exit pin is made ready , Run th GUI
  python GUI_Voice_auth.py
  
 -> Speak when prompted.

 -> Your voice is recorded and saved to Voice_test.wav.

 ->  It is then compared against your samples in samples_folder/.

 ->  Acess is granted only if DTW cost is within the threshold.

# Optional: Build Your Own .exe (for Personal Use or Deployment)

  This project includes a `Shakthi_1.1.spec` file that you can use to build a standalone `.exe` version of the app — ideal if you want to auto-launch it on boot or deploy it on another system.

### ✅ Why Use It?
- Certain dependencies had to be hard coded in the .spec without this it may not be working
- Works well with Task Scheduler (boot protection)

### 🧱 Prerequisites
- Use a Conda environment (recommended for stable builds)
- Ensure your voice samples are ready in `samples_folder/`
- Set your own `COST_THRESHOLD` before building

### 📦 Build Instructions
 🧩 Updating DLL Paths in `.spec` File (Important for .exe Build)

 Your system may store important audio-related DLLs in a different location than ours. You **must** update these paths in the `Shakthi_1.1.spec` file before building the `.exe`.

 ### 🔍 How to Find the Correct DLL Paths

 If you're using Conda (recommended):

1. Activate your environment:
   conda activate shakthi_env

2. Find the folder containing libportaudio-64bit.dll and other DLLs as mentioned in the .spec
    In conda environment type : where libportaudio-64bit.dll
    similarly find the locations of all important DLL and add them to binaries section of .spec by removing the existing DLL which is ours.

3. Also check the datas=[] section if you're including data like:
   datas=[
    ('samples_folder', 'samples_folder'),
    ('Voice_test.wav', '.'),
   ]


⚠️ Warning:
Do not place DLL files in the `datas=[]` section of the `.spec` file.
All `.dll` files must go in `binaries=[]` so PyInstaller can correctly link them during runtime.


   
# Building .exe 

1. Activate your Conda environment:
   conda activate shakthi_env
2. Run pyinstaller
   pyinstaller Shakthi_1.1.spec
3.Your .exe will be created in the dist/ folder:
   dist/Shakthi_1.1/Shakthi_1.1.exe
4.You can now run the .exe or add it to Task Scheduler (see setup_task_scheduler.md).

📎 Note: We do not distribute the .exe file. Each user should build their own using their voice samples.

💡 Notes
 -> Voice_test.wav must exist -  the GUI writes into it. Do not delete this file.

->  The system only recognizes your voice. If someone else uses it, authentication will fail.

->  The samples_folder/ is user-specific - others must create their own samples.


   -------

🤝 Contributions
This version is built for personal use. Future versions (Shakthi_2.0 and beyond) may support multi-user or AI-based recognition. Feedback and suggestions are welcome.


📄 License
This project is open-source under the MIT License.







 
