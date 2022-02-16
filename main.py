#from tkinter import
import tkinter as tk
import tkinter.ttk
import _tkinter


from paho.mqtt import client as mqtt_client
from paho import mqtt
import json
from pynput.keyboard import Key, Controller, Listener

#https://highvoltages.co/iot-internet-of-things/how-to-mqtt/mqtt-in-python/

#pi@raspberrypi:~ $ mkdir /home/pi/.config/autostart/
#move into this directory
#pi@raspberrypi:~ $ cd /home/pi/.config/autostart/
#Now create a file MyApp.desktop in the above directory with the following content.
#[Desktop Entry]
#Name=Your Application Name
#Type=Application
#Comment=Some Comments about your program
#Exec=/usr/bin/python {replace with file path}.py
#Allow File to be executable.
#pi@raspberrypi:~ $ chmod +x /home/pi/.config/autostart/MyApp.desktop


#broker = '2d26458bc2e741eeabc3f87bca1feb69.s1.eu.hivemq.cloud'
#port = 8883


broker = '2d26458bc2e741eeabc3f87bca1feb69.s1.eu.hivemq.cloud'
port = 8883

topic = "clicker/action"
topic_sub = "clicker/action"
# generate client ID with pub prefix randomly
client_id = 'Klicker_Master'
username = 'xj83JSDLcj'
password = '20394089234LKHJCLKBJEHOdsfkjl-#apxmbhrwk'
#username = 'openhab'
#password = 'openhab'


deviceId = "1"
role = "sender"
device_receiver_id = "1"

def on_press(key):
    if role == "sender":
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))

        except AttributeError:
            print('special key {0} pressed'.format(
                key))
            if key == Key.right:
                publish(client, "Key.right")

def on_release(key):
    print('{0} released'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def press_key(key_to_press):
    keyboard.press(key_to_press)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt_client.Client(client_id)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, click_direction):
    msg = "{\"action\":\"clicked\",\"deviceId\":\"" + deviceId + "\",\"direction\":\"" + click_direction + "\"}"
    result = client.publish(topic, msg)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("some message received")
        print(role)
        if role == "receiver":
            print("message received as role reviever")
            print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
            y = json.loads(msg.payload.decode())

            deviceId = str(y["deviceId"])
            direction = str(y["direction"])
            action = str(y["action"])

            if deviceId == device_receiver_id:
                info_label.config(text=direction,
                                  fg="black")
                print("buttonpress executed")
                press_key(Key.right)

    client.subscribe(topic_sub)
    client.on_message = on_message


root = tk.Tk()
root.title("21 LIVE Remote Clicker")
root.geometry('300x200')
root.resizable(False, False)
root.configure(bg="white")


#T = Text(root, height=1, width=30)
#T.pack()
#T.insert(END, "Wähle deine Rolle")
#T.config(state=DISABLED)

role_options_list = ["sender", "receiver"]
auswahl_rolle = tk.StringVar(root)
auswahl_rolle.set("Wähle eine Rolle aus")
auswahl_rolle_menu = tk.OptionMenu(root, auswahl_rolle, *role_options_list)
auswahl_rolle_menu.pack()


options_list = ["1", "2", "3", "4"]
value_inside = tk.StringVar(root)
value_inside.set("Wähle die Clicker Nummer")
question_menu = tk.OptionMenu(root, value_inside, *options_list)
question_menu.pack()

# Function to print the submitted option-- testing purpose
def print_answers():
    print("Selected Option: {}".format(value_inside.get()))
    print("Selected Option: {}".format(auswahl_rolle.get()))

    global role
    role = auswahl_rolle.get()

    if role == "receiver":
        global device_receiver_id
        device_receiver_id = value_inside.get()
    else:
        global deviceId
        deviceId = value_inside.get()
    return None


# Submit button
# Whenever we click the submit button, our submitted
# option is printed ---Testing purpose
submit_button = tk.Button(root, text='Submit', command=print_answers)
submit_button.pack()



def switch():
    #print("Klick rechts")
    publish(client, "Key.right")

plusminus = tk.Button(root, text="→", command=switch)
plusminus.pack()


# Create Labeln

info_label = tk.Label(root,
                   text="",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

info_label.place(x=80, y=120)

client = connect_mqtt()
subscribe(client)
client.loop_start()
print("loop started")

keyboard = Controller()
listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

root.mainloop()
client.loop_stop()

