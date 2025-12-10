import pystray
import PIL.Image
import threading
from core import battery_monitor
class SystemTray:
    def __init__(self) -> None:
        self.image = PIL.Image.open("../battery_logo.png")
        # initial menu (will be replaced by poller)
        self.icon = pystray.Icon(
            "BatteryLimiter5",
            self.image,
            title="BatteryLimiter5",
            menu=pystray.Menu(
                pystray.MenuItem("Percentage: --%", action=self._dummy_func),
                pystray.MenuItem("Open", self.on_clicked),
                pystray.MenuItem("Exit", self.on_clicked),
            ),
        )

        self._stop_event = threading.Event()
        self._poll_thread = None

    def _dummy_func(self, icon, item):
        pass

    def start_tray(self):
        # start tray icon in its own thread
        tray_thread = threading.Thread(target=self._run_cmd, daemon=True)
        tray_thread.start()

        # start background poller that updates the menu periodically
        self._poll_thread = threading.Thread(target=self._poll_percent, daemon=True)
        self._poll_thread.start()

    def _run_cmd(self):
        try:
            self.icon.run()
        finally:
            # ensure poller stops if the icon loop exits
            self._stop_event.set()

    def _poll_percent(self):
        # poll every second and update the menu text
        while not self._stop_event.wait(1.0):
            try:
                result = battery_monitor.checkBatteryHealth()
                percent = getattr(result, "percent", None) # or result.percent
                percent_text = f"Percentage: {percent}%" if percent is not None else "Percentage: --%"
                new_menu = pystray.Menu(
                    pystray.MenuItem(percent_text, action=self._dummy_func),
                    pystray.MenuItem("Open", self.on_clicked),
                    pystray.MenuItem("Exit", self.on_clicked),
                )
                # assign and request update; safe to call from background thread
                self.icon.menu = new_menu
                try:
                    self.icon.update_menu()
                except Exception:
                    # some backends may raise if menu isn't ready yet; ignore and retry next tick
                    pass
            except Exception:
                # avoid crashing the poller; ignore and continue
                pass

    def on_clicked(self, icon, item):
        text = getattr(item, "text", str(item))
        if text == "Open":
            # open your settings/window logic here
            print("Open clicked")
        elif text == "Exit":
            self._stop_event.set()
            try:
                icon.stop()
            except Exception:
                pass
if __name__ == "__main__":
    x = SystemTray()
    x.start_tray()