import tkinter as tk
from tkinter import messagebox
import random

# ================= Game State =================
state = "egg"
hunger = 3
boredom = 3
dirty = False
age = 0
alive = True

# ================= GUI =================
root = tk.Tk()
root.title("Tamagotchi")
root.geometry("420x520")
root.configure(bg="#fff7e6")

# ================= Images =================
img_egg_raw = tk.PhotoImage(file="egg.png")
img_char1_raw = tk.PhotoImage(file="image1.png")
img_char2_raw = tk.PhotoImage(file="image2.png")

img_egg = img_egg_raw.subsample(3, 3)
img_char1 = img_char1_raw.subsample(3, 3)
img_char2 = img_char2_raw.subsample(3, 3)

img_label = tk.Label(root, image=img_egg, bg="#fff7e6")
img_label.pack(pady=15)

face_label = tk.Label(root, text="🥚", font=("Arial", 40), bg="#fff7e6")
face_label.pack()

status_label = tk.Label(root, font=("Arial", 16), bg="#fff7e6")
status_label.pack(pady=10)

# ================= Helpers =================
def bar(value, good, bad):
    return good * (6 - value) + bad * (value - 1)

def update_face():
    if not alive:
        face_label.config(text="☠️")
    elif state == "egg":
        face_label.config(text="🥚")
    elif dirty:
        face_label.config(text="🤢")
    elif hunger >= 4:
        face_label.config(text="😵")
    elif boredom >= 4:
        face_label.config(text="🥱")
    else:
        face_label.config(text="😄")

def update_status():
    status_label.config(
        text=f"배고픔 {bar(hunger,'🍗','☠️')}\n심심함 {bar(boredom,'😍','☠️')}"
             + ("\n🧼 더러움!" if dirty else "")
    )
    update_face()

def game_over():
    global alive
    alive = False
    messagebox.showerror("GAME OVER", "다마고치가 죽었어요…")

# ================= Game Logic =================
def tick():
    global hunger, boredom
    if alive and state != "egg":
        hunger = min(5, hunger + 1)
        boredom = min(5, boredom + 1)
        if hunger == 5 and boredom == 5:
            game_over()
        update_status()
    root.after(3000, tick)

def after_action():
    global dirty, age, state
    if not alive or state == "egg":
        return
    if random.random() < 0.4:
        dirty = True
    age += 1
    if age >= 5 and state == "hatch":
        state = "adult"
        img_label.config(image=img_char2)
        img_label.pack(pady=15)
    update_status()

def feed():
    global hunger
    if not alive or state == "egg":
        return
    hunger = max(1, hunger - 1)
    after_action()

def play():
    global boredom
    if not alive or state == "egg":
        return
    boredom = max(1, boredom - 1)
    after_action()

def wash():
    global dirty
    if not alive or state == "egg":
        return
    dirty = False
    update_status()

# ================= Egg Hatch =================
def hatch(event=None):
    global state
    if state != "egg":
        return

    def shake(n=0):
        if n > 6:
            finish_hatch()
            return
        img_label.pack_forget()
        img_label.pack(pady=15)
        img_label.place(x=10 if n % 2 == 0 else -10, y=80)
        root.after(120, lambda: shake(n + 1))

    def finish_hatch():
        global state
        img_label.place_forget()
        img_label.config(image=img_char1)
        img_label.pack(pady=15)
        state = "hatch"
        update_status()

    shake()

img_label.bind("<Button-1>", hatch)

# ================= Buttons =================
btn_canvas = tk.Canvas(root, width=260, height=80, bg="#fff7e6", highlightthickness=0)
btn_canvas.pack(pady=15)

feed_btn = btn_canvas.create_oval(10, 10, 60, 60, fill="#ffb703")
feed_txt = btn_canvas.create_text(35, 35, text="🍚", font=("Arial", 16))

play_btn = btn_canvas.create_oval(100, 10, 150, 60, fill="#8ecae6")
play_txt = btn_canvas.create_text(125, 35, text="🎮", font=("Arial", 16))

wash_btn = btn_canvas.create_oval(190, 10, 240, 60, fill="#90db9a")
wash_txt = btn_canvas.create_text(215, 35, text="🧼", font=("Arial", 16))

btn_canvas.tag_bind(feed_btn, "<Button-1>", lambda e: feed())
btn_canvas.tag_bind(feed_txt, "<Button-1>", lambda e: feed())
btn_canvas.tag_bind(play_btn, "<Button-1>", lambda e: play())
btn_canvas.tag_bind(play_txt, "<Button-1>", lambda e: play())
btn_canvas.tag_bind(wash_btn, "<Button-1>", lambda e: wash())
btn_canvas.tag_bind(wash_txt, "<Button-1>", lambda e: wash())

# ================= Start =================
update_status()
root.after(3000, tick)
root.mainloop()
