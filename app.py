import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import threading, time, json, os, winsound

DATA_FILE = "data.json"

# -------------------- THEME --------------------
LIGHT = {
    "bg": "#f2f2f2",
    "card": "#ffffff",
    "text": "#111111",
    "sub": "#666666",
    "btn": "#4f8cff",
    "btn_hover": "#3b78e7",
    "entry": "#f5f5f5"
}

DARK = {
    "bg": "#1e1e1e",
    "card": "#2a2a2a",
    "text": "#ffffff",
    "sub": "#bbbbbb",
    "btn": "#3a7afe",
    "btn_hover": "#5591ff",
    "entry": "#3a3a3a"
}

# -------------------- DATA --------------------
data = {
    "settings": {"theme": "light", "total_alerts": 0},
    "reminders": []
}

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

load_data()
theme = DARK if data["settings"]["theme"] == "dark" else LIGHT

# -------------------- APP --------------------
app = tk.Tk()
app.title("เตือนฉันที")
app.geometry("620x820")
app.resizable(False, False)
app.configure(bg=theme["bg"])

FONT_T = ("Segoe UI", 24, "bold")
FONT_L = ("Segoe UI", 14, "bold")
FONT_E = ("Segoe UI", 14)

categories = ["📚 เรียน", "💼 งาน", "🎮 เล่น", "🏃 สุขภาพ"]

# -------------------- UTIL --------------------
def minutes_left(time_str):
    now = datetime.now()
    target = datetime.strptime(time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    return int((target - now).total_seconds() // 60)

def add_hover(widget):
    widget.bind("<Enter>", lambda e: widget.config(bg=theme["btn_hover"]))
    widget.bind("<Leave>", lambda e: widget.config(bg=theme["btn"]))

def apply_theme():
    app.configure(bg=theme["bg"])
    card.configure(bg=theme["card"])
    for w in widgets:
        if isinstance(w, tk.Label):
            w.configure(bg=theme["card"], fg=theme["text"])
        elif isinstance(w, tk.Entry):
            w.configure(bg=theme["entry"], fg=theme["text"], insertbackground=theme["text"])
        elif isinstance(w, tk.Listbox):
            w.configure(bg=theme["entry"], fg=theme["text"])
        elif isinstance(w, tk.Button):
            w.configure(bg=theme["btn"], fg="white")
    stat_label.configure(bg=theme["card"], fg=theme["sub"])

def toggle_theme():
    data["settings"]["theme"] = "dark" if data["settings"]["theme"] == "light" else "light"
    save_data()
    global theme
    theme = DARK if data["settings"]["theme"] == "dark" else LIGHT
    mode_btn.config(text="☀️ Light Mode" if theme == DARK else "🌙 Dark Mode")
    apply_theme()

# -------------------- SOUND & POPUP --------------------
def play_sound(path):
    if path and os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        winsound.Beep(1000, 500)

def popup(text):
    pop = tk.Toplevel(app)
    pop.overrideredirect(True)
    pop.attributes("-topmost", True)
    pop.configure(bg="#222222")

    w, h = 320, 90
    x = app.winfo_x() + app.winfo_width() - w - 20
    y = app.winfo_y() + app.winfo_height() - h - 20
    pop.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(pop, text=text, fg="white", bg="#222222",
             font=("Segoe UI", 12)).pack(expand=True)

    pop.after(2500, pop.destroy)

# -------------------- REMINDER --------------------
def choose_sound():
    path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if path:
        sound_var.set(os.path.basename(path))
        sound_var.fullpath = path

def add_reminder():
    if not task_entry.get():
        return
    item = {
        "task": task_entry.get(),
        "time": f"{hour.get().zfill(2)}:{minute.get().zfill(2)}",
        "category": cat.get(),
        "sound": getattr(sound_var, "fullpath", ""),
        "fired": False
    }
    data["reminders"].append(item)
    save_data()
    task_entry.delete(0, tk.END)
    refresh_list()

def refresh_list():
    listbox.delete(0, tk.END)
    for r in data["reminders"]:
        left = minutes_left(r["time"])
        status = "อีก {} นาที".format(left) if left > 0 else "ถึงเวลาแล้ว!" if left == 0 else "ผ่านไปแล้ว"
        listbox.insert(tk.END, f"{r['category']} | {r['time']} | {status} | {r['task']}")

# -------------------- CHECK LOOP (SAFE) --------------------
def check_loop():
    while True:
        now = datetime.now().strftime("%H:%M")
        for r in data["reminders"]:
            if r["time"] == now and not r["fired"]:
                r["fired"] = True
                data["settings"]["total_alerts"] += 1
                save_data()

                app.after(0, play_sound, r["sound"])
                app.after(0, popup, f"⏰ {r['task']}")
                app.after(0, stat_label.config,
                          {"text": f"📊 เตือนทั้งหมด: {data['settings']['total_alerts']} ครั้ง"})
                app.after(0, refresh_list)
        time.sleep(1)

# -------------------- UI --------------------
card = tk.Frame(app, bg=theme["card"])
card.pack(fill="both", expand=True, padx=25, pady=25)

widgets = []

tk.Label(card, text="⏰ เตือนฉันที", font=FONT_T).pack(pady=20)

mode_btn = tk.Button(card, text="🌙 Dark Mode", command=toggle_theme, height=2)
mode_btn.pack(pady=5)
add_hover(mode_btn)
widgets.append(mode_btn)

stat_label = tk.Label(card, text=f"📊 เตือนทั้งหมด: {data['settings']['total_alerts']} ครั้ง")
stat_label.pack(pady=10)

tk.Label(card, text="📝 สิ่งที่ต้องทำ", font=FONT_L).pack(anchor="w", padx=30)
task_entry = tk.Entry(card, font=FONT_E)
task_entry.pack(fill="x", padx=30, pady=8, ipady=8)
widgets.append(task_entry)

tk.Label(card, text="⏰ เวลา", font=FONT_L).pack(anchor="w", padx=30)
time_f = tk.Frame(card, bg=theme["card"])
time_f.pack(padx=30, pady=5)

hour = tk.StringVar(value="08")
minute = tk.StringVar(value="00")
tk.Spinbox(time_f, from_=0, to=23, width=5, font=FONT_E, textvariable=hour).pack(side="left", ipady=6)
tk.Label(time_f, text=":", font=FONT_L, bg=theme["card"]).pack(side="left", padx=10)
tk.Spinbox(time_f, from_=0, to=59, width=5, font=FONT_E, textvariable=minute).pack(side="left", ipady=6)

tk.Label(card, text="🏷 หมวดหมู่", font=FONT_L).pack(anchor="w", padx=30, pady=(10,0))
cat = tk.StringVar(value=categories[0])
tk.OptionMenu(card, cat, *categories).pack(fill="x", padx=30)

sound_var = tk.StringVar(value="เลือกเสียง (.wav)")
sound_btn = tk.Button(card, text="🔔 เลือกเสียง", command=choose_sound)
sound_btn.pack(pady=12)
add_hover(sound_btn)
widgets.append(sound_btn)

tk.Label(card, textvariable=sound_var).pack()

add_btn = tk.Button(card, text="➕ เพิ่มแจ้งเตือน", command=add_reminder,
                    font=FONT_L, height=2)
add_btn.pack(pady=18)
add_hover(add_btn)
widgets.append(add_btn)

tk.Label(card, text="📋 รายการแจ้งเตือน", font=FONT_L).pack(anchor="w", padx=30)
listbox = tk.Listbox(card, height=10, font=("Segoe UI", 12))
listbox.pack(fill="both", padx=30, pady=10)
widgets.append(listbox)

apply_theme()
refresh_list()
threading.Thread(target=check_loop, daemon=True).start()
app.mainloop()
