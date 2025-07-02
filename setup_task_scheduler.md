# 🛠️ Shakthi_1.1v — Setup Task Scheduler (Optional)

> This guide helps you auto-launch `Shakthi_1.1v.exe` when you **log in**, ensuring seamless voice-based access control every time your system starts.

---

## ⚙️ Why Use Task Scheduler?

Running `Shakthi_1.1v.exe` at **log in** ensures your **voice authentication system is always active** — without requiring manual launch.  
It also helps you integrate the system with your daily workflow, just like a native boot-lock app.

---

## 🪜 Step-by-Step Setup

### 1️⃣ Open Task Scheduler

- Press `Win + R`, type:  
    taskschd.msc
and press Enter
- This opens the **Task Scheduler** window.

---

### 2️⃣ Create a New Task

- In the right pane, click **Create Task...** (avoid using "Basic Task")
- Under the **General** tab:
- **Name:** `Shakthi_1.1v Boot Auth`
- ✅ Check: `Run with highest privileges`
- Set: `Configure for: Windows 10 / Windows 11`

---

### 3️⃣ Set the Trigger

> 🔄 **Recommended:** Run the task **At log on**

- Go to the **Triggers** tab → Click **New...**
- Begin the task: `At log on`
- ✅ Choose: `Any user` *(or select your user account)*
- Delay task for `10 seconds` *(optional but recommended to allow system services to load)*
- Click OK

> 🧠 **Why not “At startup”?**  
> Starting at system boot can cause glitches if audio drivers or GUI systems aren’t fully initialized.  
> **“At log on” is more reliable** for GUI-based authentication systems like Shakthi_1.1v.

---

### 4️⃣ Add the Action

- Go to the **Actions** tab → Click **New...**
- Action: `Start a program`
- Program/script:
  ```
  C:\Users\<YourUsername>\Shakthi_1.1v\dist\Shakthi_1.1v.exe
  ```
  *(Replace with your actual path)*

---

### 5️⃣ Set Conditions (Optional)

- ✅ Uncheck: “Start the task only if the computer is on AC power”
- ✅ Uncheck: “Start only if the computer is idle”

---

### 6️⃣ Finalize and Save

- Click **OK** to save the task
- Provide Admin credentials if prompted

---

## ✅ Done!

Every time you **log in** (after a system boot or restart — not just unlocking), your Shakthi_1.1v GUI will launch automatically and prompt for voice authentication.

---

## 🧼 To Edit or Remove the Task

- Open Task Scheduler
- Right-click on `Shakthi_1.1v Boot Auth`
- Choose `Disable`, `Delete`, or `Properties` to modify it

---

> 🗒️ **Note:** This file is intentionally kept separate from `README.md` for clarity. Only use this guide if you are building and deploying the `.exe` version of the app.

---

