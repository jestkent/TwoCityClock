import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import customtkinter as ctk
import pytz
import random

class WorldClockApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("World Clock")
        self.root.geometry("700x400")
        
        self.countries = {
            "New York": "America/New_York",
            "Tokyo": "Asia/Tokyo",
            "London": "Europe/London",
            "Paris": "Europe/Paris",
            "Sydney": "Australia/Sydney",
            "Dubai": "Asia/Dubai",
            "Moscow": "Europe/Moscow",
            "Los Angeles": "America/Los_Angeles",
            "Beijing": "Asia/Shanghai",
            "Singapore": "Asia/Singapore",
            "Manila": "Asia/Manila",
            "Arizona": "America/Phoenix"
        }
        
        self.country1 = ctk.StringVar(value="Manila")
        self.country2 = ctk.StringVar(value="Arizona")
        
        self.create_ui()
        self.create_fish()
        self.create_bubbles()
        self.animate_fish()
        self.animate_bubbles()
        self.update_time()
        self.root.mainloop()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, bg="#0a192f", highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="gray20")
        main_frame.place(relx=0.5, rely=0.65, anchor='center', relwidth=0.7, relheight=0.5)
        
        time_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="gray15")
        time_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        first_container = ctk.CTkFrame(time_frame, corner_radius=10, fg_color="gray10")
        first_container.pack(side='left', expand=True, padx=5, pady=5, fill='both')
        
        self.time1_label = ctk.CTkLabel(first_container, text='00:00:00', font=('Roboto', 36, 'bold'), text_color="#00ffcc")
        self.time1_label.pack(pady=(5, 2))
        
        self.date1_label = ctk.CTkLabel(first_container, text='', font=('Roboto', 14), text_color="#66d9ef")
        self.date1_label.pack(pady=(0, 2))
        
        self.country1_selector = ctk.CTkOptionMenu(
            first_container, values=list(self.countries.keys()),
            variable=self.country1, command=self.update_time, fg_color="#0a3d62"
        )
        self.country1_selector.pack(pady=2)
        
        second_container = ctk.CTkFrame(time_frame, corner_radius=10, fg_color="gray10")
        second_container.pack(side='right', expand=True, padx=5, pady=5, fill='both')
        
        self.time2_label = ctk.CTkLabel(second_container, text='00:00:00', font=('Roboto', 36, 'bold'), text_color="#00ffcc")
        self.time2_label.pack(pady=(5, 2))
        
        self.date2_label = ctk.CTkLabel(second_container, text='', font=('Roboto', 14), text_color="#66d9ef")
        self.date2_label.pack(pady=(0, 2))
        
        self.country2_selector = ctk.CTkOptionMenu(
            second_container, values=list(self.countries.keys()),
            variable=self.country2, command=self.update_time, fg_color="#0a3d62"
        )
        self.country2_selector.pack(pady=2)
        
    def update_time(self, *args):
        tz1 = pytz.timezone(self.countries[self.country1.get()])
        tz2 = pytz.timezone(self.countries[self.country2.get()])
        
        time1 = datetime.now(tz1).strftime('%H:%M:%S')
        date1 = datetime.now(tz1).strftime('%A, %B %d, %Y')
        
        time2 = datetime.now(tz2).strftime('%H:%M:%S')
        date2 = datetime.now(tz2).strftime('%A, %B %d, %Y')
        
        self.time1_label.configure(text=time1)
        self.date1_label.configure(text=date1)
        
        self.time2_label.configure(text=time2)
        self.date2_label.configure(text=date2)
        
        self.root.after(1000, self.update_time)
    
    def create_fish(self):
        self.fish = []
        for _ in range(5):
            x = random.randint(0, 650)
            y = random.randint(50, 350)
            dx = random.choice([-2, -1, 1, 2])
            dy = random.choice([-1, 0, 1])
            fish_text = "🐠" if dx > 0 else "🐟"  # Right-facing or left-facing fish
            fish = self.canvas.create_text(x, y, text=fish_text, font=('Arial', 20))
            self.fish.append([fish, dx, dy])

    def animate_fish(self):
        for fish_data in self.fish:
            fish, dx, dy = fish_data
            x, y = self.canvas.coords(fish)

            # Randomly change direction occasionally
            if random.random() < 0.02:  
                dx = random.choice([-3, -2, -1, 1, 2, 3])
                dy = random.choice([-2, -1, 0, 1, 2])

            # Bounce off the edges
            if x + dx < 0 or x + dx > 700:
                dx = -dx
            if y + dy < 50 or y + dy > 350:
                dy = -dy

            # Update fish emoji based on direction
            new_fish_text = "🐠" if dx > 0 else "🐟"
            self.canvas.itemconfig(fish, text=new_fish_text)

            self.canvas.coords(fish, x + dx, y + dy)

            # Update stored velocity
            fish_data[1] = dx
            fish_data[2] = dy

        self.root.after(100, self.animate_fish)
    
    def create_bubbles(self):
        self.bubbles = []
        for _ in range(10):
            x = random.randint(50, 650)
            y = random.randint(350, 400)
            bubble = self.canvas.create_text(x, y, text='o', font=('Arial', 12))
            self.bubbles.append(bubble)
    
    def animate_bubbles(self):
        for bubble in self.bubbles:
            x, y = self.canvas.coords(bubble)
            new_y = y - random.randint(1, 3)
            if new_y < 50:
                new_y = random.randint(350, 400)
                x = random.randint(50, 650)
            self.canvas.coords(bubble, x, new_y)
        
        self.root.after(100, self.animate_bubbles)

if __name__ == "__main__":
    WorldClockApp()
