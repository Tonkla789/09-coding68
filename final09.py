import tkinter as tk

# ฟังก์ชันตรวจสอบเลข
def check_number():
    result_label.config(text="", fg="white")
    try:
        N = int(entry.get())   # ใช้ตัวแปรชื่อ N

        if N % 2 == 0:
            result_label.config(text=f"✅ {N} เป็นเลขคู่", fg="#00ffcc")
        else:
            result_label.config(text=f"✨ {N} เป็นเลขคี่", fg="#ffcc00")

        blink()

    except ValueError:
        result_label.config(text="⚠ กรุณากรอกตัวเลขที่ถูกต้อง", fg="#ff4d4d")


# เอฟเฟกต์กระพริบข้อความ
def blink():
    current_color = result_label.cget("fg")
    result_label.config(fg="white")
    window.after(150, lambda: result_label.config(fg=current_color))


# เอฟเฟกต์ hover ปุ่ม
def on_enter(e):
    check_btn.config(bg="#ffffff", fg="#333333")

def on_leave(e):
    check_btn.config(bg="#333333", fg="white")


# สร้างหน้าต่างหลัก
window = tk.Tk()
window.title("โปรแกรมคำนวณเลขคู่และเลขคี่")
window.geometry("450x350")
window.resizable(False, False)

# พื้นหลังไล่สี (Gradient จำลอง)
canvas = tk.Canvas(window, width=450, height=350)
canvas.pack(fill="both", expand=True)

for i in range(0, 350):
    r = int(102 + (118 - 102) * i / 350)
    g = int(126 + (75 - 126) * i / 350)
    b = int(234 + (162 - 234) * i / 350)
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 450, i, fill=color)

# Frame กลาง
frame = tk.Frame(window, bg="#000000")
frame.place(relx=0.5, rely=0.5, anchor="center")

# หัวข้อ
title = tk.Label(frame,
                 text="🔢 โปรแกรมคำนวณเลขคู่และเลขคี่",
                 font=("Segoe UI", 16, "bold"),
                 bg="#000000", fg="white")
title.pack(pady=5)

# คำทักทาย
greeting = tk.Label(frame,
                    text="ไงพวกและนี่ก็คือโปรแกรมคำนวณเลขคู่และเลขคี่",
                    font=("Segoe UI", 10),
                    bg="#000000", fg="white")
greeting.pack(pady=5)

# ช่องกรอกข้อมูล
entry = tk.Entry(frame, font=("Segoe UI", 14), justify="center")
entry.pack(pady=10)

# ปุ่มตรวจสอบ
check_btn = tk.Button(frame,
                      text="ตรวจสอบ",
                      font=("Segoe UI", 12, "bold"),
                      bg="#333333", fg="white",
                      command=check_number)
check_btn.pack(pady=10)

check_btn.bind("<Enter>", on_enter)
check_btn.bind("<Leave>", on_leave)

# แสดงผลลัพธ์
result_label = tk.Label(frame,
                        text="",
                        font=("Segoe UI", 14, "bold"),
                        bg="#000000")
result_label.pack(pady=10)

# ผู้พัฒนา
developer = tk.Label(frame,
                     text="ผู้พัฒนา: นายพรหมพิริยะ กังเที่ยงธรรม\nเลขที่ 9 ม.4/4",
                     font=("Segoe UI", 9),
                     bg="#000000", fg="white")
developer.pack(pady=5)

window.mainloop()
