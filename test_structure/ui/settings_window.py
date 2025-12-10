import tkinter as tk
from core import battery_monitor
from concurrent.futures import ThreadPoolExecutor
_battery_percent = 0
class App:
    def __init__(self) -> None:
        self.app = tk.Tk()
        self.cur_percent = tk.Label(master=self.app, text="0%")
        self.cur_percent.pack()

        # reuse a single executor instead of recreating it every second
        self._executor = ThreadPoolExecutor(max_workers=1)

        # ensure we shut down cleanly
        self.app.protocol("WM_DELETE_WINDOW", self._on_close)

        # start periodic polling
        self._poll_battery()
        self.app.mainloop()

    def _check_bat(self):
        return battery_monitor.checkBatteryHealth()

    def _poll_battery(self):
        # submit task; don't block the main thread
        future = self._executor.submit(self._check_bat)
        # schedule GUI update on the main thread when done
        future.add_done_callback(lambda f: self.app.after(0, self._on_bat_result, f))
        # schedule next poll
        self.app.after(1000, self._poll_battery)

    def _on_bat_result(self, future):
        global _battery_percent
        try:
            result = future.result()
            bat_percent = getattr(result, "percent", None)
            if bat_percent is not None:
                self.cur_percent.configure(text=f"{bat_percent}%")
                _battery_percent = bat_percent
            # Example alarm checks — keep GUI actions on main thread
            if bat_percent == 100:
                # trigger full charge alarm (e.g. show dialog / change color)
                pass
            elif bat_percent <= 20:
                # low battery alarm
                pass
        except Exception:
            # handle/log errors; avoid crashing the UI
            pass

    def _on_close(self):
        try:
            # stop accepting new tasks and let worker exit
            self._executor.shutdown(wait=False)
        finally:
            self.app.destroy()
if __name__ == "__main__":
    x = App()