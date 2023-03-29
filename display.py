from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
from data import getdata

BACKGROUND_COLOR = "white"
interval = 5000
cycle = 30000

class Display(Tk):
    def __init__(self):
        super().__init__()
        self.pressed = True
        self.menu = None
        self.title("Disappearing Tex Writing App")
        self.state("zoomed")
        self.config(bg=BACKGROUND_COLOR)
        self.prompts = getdata()
        self.charactercounter = 5
        self.prmpt = None
        self.time = False
        self.start = False
        self.is_on = False
        self.menu_screen()
        self.entry_field = Text(width=125, height=32, bg="grey", font=("arial", 15))
        self.entry_field.bind("<Key>", lambda event: self.start_timer())
        self.mainloop()

    def menu_screen(self):
        self.menu = Canvas(bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
        self.logo = Label(self.menu, text="Welcome to the Disappearing Text Writing App", bg=BACKGROUND_COLOR,
                          font=("Arial", 20, "bold"),
                          fg="#303030")

        self.description = Label(self.menu, text="Dont stop writing or all your work will vanish", bg=BACKGROUND_COLOR,
                                 font=("Arial", 15),
                                 fg="#303030")

        self.prompt = Label(self.menu, width=70, height=5, bg="white")

        self.regenerate = Button(self.menu, text="Generate new prompt", bg=BACKGROUND_COLOR, fg="#303030",
                                 command=self.generate)

        self.start_prompt = Button(self.menu, text="Generate Prompt", bg=BACKGROUND_COLOR, fg="#303030",
                                   command=self.generate)
        self.menu.place(x=self.winfo_screenwidth() / 3.4, y=self.winfo_screenheight() / 3.2)
        self.logo.grid(column=0, row=0, columnspan=3)
        self.description.grid(column=0, row=1, columnspan=3)
        self.prompt.grid(column=0, row=2, columnspan=3, padx=10, pady=10)
        self.start_prompt.grid(column=1, row=3)

    def game_screen(self):
        if self.is_on:
            self.progress = ttk.Progressbar(orient="horizontal", length=self.winfo_screenwidth() - 30,
                                            mode="determinate", maximum=300)
            self.progress.place(x=15, y=2)

            self.timer = Label(text=f"00:0{self.charactercounter}", font=("arial", 20, "bold"))
            self.timer.place(x=15, y=30)
            self.entry_field.delete("1.0", "end")
            self.entry_field.insert("1.0", self.random_prompt)
            self.entry_field.place(x=self.winfo_screenwidth() / 14.5, y=30)

    def start_timer(self):
        if not self.time:
            self.periodtimer()
        self.pressed = True
        self.start_counter()

    def periodtimer(self):
        self.time = True
        if self.progress["value"] >= 300:
            self.after_cancel(self.counter)
            self.after_cancel(self.period)
            self.after_cancel(self.counterinner)
            wyy = messagebox.askquestion("Save", "Wow, you kept it going! good for you. Do you want to save your work")
            if wyy == "yes":
                message = self.entry_field.get("1.0", "end")
                with open(f'{self.random_prompt}.txt', 'w', encoding='utf-8') as f:
                    f.write(message)
                self.restart()
            else:
                self.restart()
        elif self.progress["value"] < 300:
            self.progress.step(1)
            self.period = self.after(1000, self.periodtimer)

    def start_counter(self):
        self.charactercounter = 5
        self.timer.config(text=f"00:0{self.charactercounter}")
        if not hasattr(self, "timer_running") or not self.timer_running:
            self.timer_running = True
            self.counter = self.after(1000, self.charactertimer)

    def charactertimer(self):
        if self.charactercounter > 0:
            self.charactercounter -= 1
            self.timer.config(text=f"00:0{self.charactercounter}")
            self.counterinner = self.after(1000, self.charactertimer)
        else:
            hello = messagebox.askquestion("Restart", "You didnt type fast enough, do you want to restart?")
            if hello == "yes":
                self.restart()
            else:
                self.destroy()

    def restart(self):
        for widgets in self.winfo_children():
            widgets.place_forget()
        self.after_cancel(self.counter)
        self.after_cancel(self.period)
        self.charactercounter = 5
        self.time = False
        self.timer_running = False
        self.progress.config(value=0)
        self.menu_screen()

    def randomize(self):
        index = random.randint(0, len(self.prompts))
        self.random_prompt = self.prompts[index]
        self.prompts.remove(self.random_prompt)
        return self.random_prompt

    def generate(self):
        self.prompt.config(bg="grey")
        self.prmpt = self.randomize()
        self.prompt.config(text=self.prmpt)
        self.start_prompt.grid(column=2, row=3)
        self.regenerate.grid(column=0, row=3)
        self.start_prompt.config(text="Start", command=self.starter)

    def starter(self):
        self.menu.destroy()
        self.menu = Canvas(bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
        self.is_on = True
        self.game_screen()
