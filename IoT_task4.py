import network
import urequests
import time
from machine import Pin
import dht

# -------- SETTINGS --------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

BOT_TOKEN = "8248231488:AAFBMXPj3F_Jrb6SagTzHGv4ed_LbOoSGxk"
CHAT_ID = "-1003642624312"

TEMP_THRESHOLD = 30.0

# -------- RELAY / LED --------
led = Pin(2, Pin.OUT)
led.value(0)

# -------- DHT SENSOR --------
sensor = dht.DHT22(Pin(4))

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

# -------- CONTROL FLAGS --------
alert_active = False
auto_off_sent = False

# -------- MAIN LOOP --------
while True:
    try:
        # ---- Read Temperature ----
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
        except:
            temp = None

        relay_state = led.value()

        # ---- AUTO CONTROL ----
        if temp is not None:

            # Temperature HIGH
            if temp >= TEMP_THRESHOLD:
                auto_off_sent = False

                if relay_state == 0:
                    alert_active = True
                    send_message(
                        CHAT_ID,
                        "ALERT!\nTemperature {:.2f} °C\nRelay is OFF\nSend /on to activate relay\n".format(temp)
                    )

                else:
                    alert_active = False

            # Temperature NORMAL
            else:
                alert_active = False

                if relay_state == 1:
                    led.value(0)

                if not auto_off_sent:
                    send_message(
                        CHAT_ID,
                        "Temperature normal ({:.2f} °C)\nRelay AUTO-OFF\n".format(temp)
                    )
                    auto_off_sent = True

        # ---- TELEGRAM COMMANDS ----
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
                    alert_active = False
                    send_message(CHAT_ID, "Relay ON" + "\n")

                elif text == "/off":
                    led.value(0)
                    send_message(CHAT_ID, "Relay OFF" + "\n")

                elif text == "/status":
                    send_message(
                        CHAT_ID,
                        "Status\nTemp: {:.2f} °C\nHumidity: {:.2f} %\nRelay: {}\n".format(
                            temp if temp else 0,
                            hum if temp else 0,
                            "ON" if led.value() else "OFF"
                        )
                    )

    except:
        pass

    time.sleep(5)
