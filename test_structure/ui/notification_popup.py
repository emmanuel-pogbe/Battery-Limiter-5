import tkinter as tk
import threading
import time
import pyautogui
class Notification:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Unplug Reminder")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Always on top
        self.root.update_idletasks()

        self.root.configure(bg="blue")
        self.root.bind("<Button-1>",self.dismiss)
        self.root.bind("<Button-3>",self.dismiss)
        # Get the current width and height
        # self.current_width = self.root.winfo_screenwidth()
        # self.current_height = self.root.winfo_screenheight()
        self.window_size_x = 400
        self.window_size_y = 200
        self.current_width = getattr(pyautogui.size(),"width")
        self.current_height = getattr(pyautogui.size(),"height")

        self.popup_position_x = self.current_width - self.window_size_x
        self.popup_position_y = self.current_height - self.window_size_y
        self.root.geometry(
            f"{self.window_size_x}x{self.window_size_y}+{self.popup_position_x}+{self.popup_position_y}"
            )  # Initial position
        tk.Frame()

        self.status = "high" #This is the variable that determines what information is displayed in the notification
        #high means the upper battery limit has been reached and user should unplug his/her device
        #low means the lower battery limit has been reached and user should plug his/her device
        if self.status == "high":
            self.notification_header = "⚠️ Unplug your device!"
            self.notification_body = "Your battery percentage upper limit has been reached\nUnplug your device now to stop seeing this notification"
        else:
            self.notification_header = "⚠️ Plug your device!"
            self.notification_body = "Your battery percentage lower limit has been reached\nPlug your device now to stop seeing this notification"
        
        self.header_label = tk.Label(self.root, text=self.notification_header, font=("Arial", 14, "bold"), bg="blue")
        self.header_label.pack(pady=20, padx=5)

        self.body_label = tk.Label(self.root, text=self.notification_body, font=("Calibri", 10), bg="blue", wraplength=360, justify="center")
        self.body_label.pack(padx=5)

        self.dismissed = False

        # Optional: Add a button to simulate the condition being met
        # self.dismiss_button = tk.Button(self.root, text="I've unplugged it\nIs this below it", command=self.dismiss)
        # self.dismiss_button.pack()

        # Start shaking in a separate thread
        threading.Thread(target=self.shake_window, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.block_close)  # Disable close button
        self.root.mainloop()

    def shake_window(self):
        while not self.dismissed:
            for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
                self.root.geometry(f"+{self.popup_position_x+dx}+{self.popup_position_y+dy}")
                time.sleep(0.08)
        self.root.destroy()

    def dismiss(self,event):
        # You can replace this with a real condition, like checking battery status
        self.dismissed = True

    def block_close(self):
        pass  # Prevent manual closing

if __name__ == "__main__":
    x = Notification()
