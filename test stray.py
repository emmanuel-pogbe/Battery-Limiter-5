import pystray
import PIL.Image

image = PIL.Image.open("battery_logo.png")

def on_clicked(icon, item):
    if str(item) == "Say Hello":
        print("Hello World")
    elif str(item) == "Exit":
        print("Thank you for stopping")
        icon.stop() #Or sys.exit
    elif str(item) == "Subitem 1":
        print("You just clicked the first subitem")
    else:
        print("Not implemented yet")
icon = pystray.Icon("Neural",image,title="battery testing",menu=pystray.Menu(
    pystray.MenuItem("Say Hello",on_clicked),
    pystray.MenuItem("Exit",on_clicked),
    pystray.MenuItem("Submenu", pystray.Menu(
        pystray.MenuItem("Subitem 1",on_clicked),
        pystray.MenuItem("Subitem 2",on_clicked)
    ))
))
icon.run()