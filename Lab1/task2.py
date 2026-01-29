import network
import urequests
import time
from machine import Pin

# -------- SETTINGS --------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

BOT_TOKEN = "8248231488:AAFBMXPj3F_Jrb6SagTzHGv4ed_LbOoSGxk"
CHAT_ID = "-5215382558"

# -------- LED --------
led = Pin(2, Pin.OUT)
led.value(0)

# -------- WIFI --------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("WiFi connected")

# -------- TELEGRAM SEND MESSAGE (ADDED) --------
def send_message(chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)
    data = "chat_id={}&text={}".format(chat_id, text)
    try:
        r = urequests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data
        )
        r.close()
    except:
        pass

# -------- SEND TEST MESSAGE (ADDED) --------
send_message(CHAT_ID, "ESP connected successfully")

# -------- TELEGRAM --------
URL = "https://api.telegram.org/bot{}/getUpdates".format(BOT_TOKEN)
last_id = 0

# -------- MAIN LOOP --------
while True:
    try:
        r = urequests.get(URL + "?offset={}".format(last_id + 1))
        messages = r.json()["result"]
        r.close()

        for msg in messages:
            last_id = msg["update_id"]
            text = msg["message"].get("text", "")
            chat_id = msg["message"]["chat"]["id"]

            if str(chat_id) == CHAT_ID:
                print("Receive")
                print(text)

    except:
        pass

    time.sleep(2)
