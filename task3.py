import network
import urequests
import time
from machine import Pin
import dht

# -------- SETTINGS --------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

BOT_TOKEN = "8248231488:AAFBMXPj3F_Jrb6SagTzHGv4ed_LbOoSGxk"
CHAT_ID = "-5215382558"

# -------- RELAY / LED --------
led = Pin(2, Pin.OUT)
led.value(0)

# -------- DHT SENSOR --------
sensor = dht.DHT22(Pin(4))   # change to DHT11 if needed

# -------- WIFI --------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("WiFi connected")

# -------- TELEGRAM SEND --------
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

            if "message" not in msg:
                continue

            text = msg["message"].get("text", "")
            chat_id = msg["message"]["chat"]["id"]

            if str(chat_id) == CHAT_ID:

                if text == "/on":
                    led.value(1)
                    send_message(CHAT_ID, "Relay ON")

                elif text == "/off":
                    led.value(0)
                    send_message(CHAT_ID, "Relay OFF")

                elif text == "/status":
                    try:
                        sensor.measure()
                        temp = sensor.temperature()
                        hum = sensor.humidity()
                    except:
                        temp = "N/A"
                        hum = "N/A"

                    relay_state = "ON" if led.value() else "OFF"

                    status_msg = (
                        "Status\n"
                        "Temperature: {:.2f} °C\n"
                        "Humidity: {:.2f} %\n"
                        "Relay: {}"
                    ).format(temp, hum, relay_state)

                    send_message(CHAT_ID, status_msg + "\n" )

    except:
        pass

    time.sleep(2)
