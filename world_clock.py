import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import customtkinter as ctk
import pytz
import random
from PIL import Image, ImageTk

class WorldClockApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("World Clock")
        self.root.geometry("700x400")
        
        # Add time format variable (12-hour as default)
        self.time_format = ctk.StringVar(value="12-hour")
        
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
        
        # Load fish and bubble images
        self.load_images()
        
        self.create_ui()
        self.create_fish()
        self.create_bubbles()
        self.animate_fish()
        self.animate_bubbles()
        self.update_time()
        self.root.mainloop()

    def load_images(self):
        # Load the fish images
        try:
            self.fish_right_img = ImageTk.PhotoImage(Image.open("fish_right.png").resize((40, 25)))
            self.fish_left_img = ImageTk.PhotoImage(Image.open("fish_left.png").resize((40, 25)))
        except Exception as e:
            # Fallback to text if images can't be loaded
            print(f"Could not load fish images: {e}")
            self.fish_right_img = None
            self.fish_left_img = None
            
        # Load the bubble images
        try:
            self.bubble1_img = ImageTk.PhotoImage(Image.open("Bubble1.png").resize((15, 15)))
            self.bubble2_img = ImageTk.PhotoImage(Image.open("Bubble2.png").resize((20, 20)))
            self.bubble_images = [self.bubble1_img, self.bubble2_img]
        except Exception as e:
            # Fallback to text if images can't be loaded
            print(f"Could not load bubble images: {e}")
            self.bubble_images = None

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, bg="#0a192f", highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="gray20")
        main_frame.place(relx=0.5, rely=0.65, anchor='center', relwidth=0.7, relheight=0.5)
        
        # Top frame for format selection
        format_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="gray15", height=30)
        format_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        format_label = ctk.CTkLabel(format_frame, text="Time Format:", font=('Roboto', 12))
        format_label.pack(side='left', padx=10)
        
        format_12hr = ctk.CTkRadioButton(format_frame, text="12-hour", variable=self.time_format, 
                                         value="12-hour", command=self.update_time)
        format_12hr.pack(side='left', padx=10)
        
        format_24hr = ctk.CTkRadioButton(format_frame, text="24-hour", variable=self.time_format, 
                                         value="24-hour", command=self.update_time)
        format_24hr.pack(side='left', padx=10)
        
        # Time display frame
        time_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="gray15")
        time_frame.pack(expand=True, fill='both', padx=10, pady=(5, 10))
        
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
        
        # Format time based on selected format
        time_format = '%I:%M:%S %p' if self.time_format.get() == "12-hour" else '%H:%M:%S'
        
        time1 = datetime.now(tz1).strftime(time_format)
        date1 = datetime.now(tz1).strftime('%A, %B %d, %Y')
        
        time2 = datetime.now(tz2).strftime(time_format)
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
            
            # Use the custom fish images if available, otherwise fallback to text
            if self.fish_right_img and self.fish_left_img:
                fish_img = self.fish_right_img if dx > 0 else self.fish_left_img
                fish = self.canvas.create_image(x, y, image=fish_img)
            else:
                fish_text = "🐠" if dx > 0 else "🐟"  # Right-facing or left-facing fish text as fallback
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

            # Update fish image based on direction
            if self.fish_right_img and self.fish_left_img:
                new_fish_img = self.fish_right_img if dx > 0 else self.fish_left_img
                self.canvas.itemconfig(fish, image=new_fish_img)
            else:
                # Fallback to text if images aren't available
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
            
            # Use custom bubble images if available, otherwise fallback to text
            if self.bubble_images:
                # Randomly choose between bubble1 and bubble2
                bubble_img = random.choice(self.bubble_images)
                bubble = self.canvas.create_image(x, y, image=bubble_img)
            else:
                # Text fallback if images aren't available
                bubble_sizes = ['·', 'o', 'O']
                bubble_text = random.choice(bubble_sizes)
                bubble = self.canvas.create_text(x, y, text=bubble_text, font=('Arial', 12), fill="white")
                
            self.bubbles.append(bubble)
    
    def animate_bubbles(self):
        for bubble in self.bubbles:
            x, y = self.canvas.coords(bubble)
            new_y = y - random.randint(1, 3)
            
            # Reset bubble position if it reaches the top
            if new_y < 50:
                new_y = random.randint(350, 400)
                x = random.randint(50, 650)
                
                # Randomize bubble image again if using images
                if self.bubble_images:
                    bubble_img = random.choice(self.bubble_images)
                    self.canvas.itemconfig(bubble, image=bubble_img)
                    
            self.canvas.coords(bubble, x, new_y)
        
        self.root.after(100, self.animate_bubbles)

if __name__ == "__main__":
    WorldClockApp()