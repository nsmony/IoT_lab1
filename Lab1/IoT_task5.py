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

# -------- RELAY --------
relay = Pin(2, Pin.OUT)
relay.value(0)

# -------- DHT SENSOR --------
sensor = dht.DHT22(Pin(4))

# -------- WIFI --------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

def connect_wifi():
    if not wifi.isconnected():
        print("WiFi disconnected. Reconnecting...")
        wifi.connect(SSID, PASSWORD)

        timeout = 10
        while not wifi.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

        if wifi.isconnected():
            print("WiFi reconnected:", wifi.ifconfig())
        else:
            print("WiFi reconnect failed")

connect_wifi()

# -------- TELEGRAM --------
BASE_URL = "https://api.telegram.org/bot{}".format(BOT_TOKEN)
last_id = 0

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = "chat_id={}&text={}".format(chat_id, text)

    try:
        r = urequests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data
        )

        if r.status_code != 200:
            print("Telegram send error:", r.status_code)

        r.close()

    except Exception as e:
        print("Telegram send exception:", e)

# -------- CONTROL FLAGS --------
alert_active = False
auto_off_sent = False

# -------- MAIN LOOP --------
while True:

    # ---- WiFi Check ----
    if not wifi.isconnected():
        connect_wifi()
        time.sleep(5)
        continue   # skip cycle if no WiFi

    # ---- Read DHT ----
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
    except OSError as e:
        print("DHT error:", e)
        time.sleep(5)
        continue   # skip cycle safely

    relay_state = relay.value()

    # ---- AUTO LOGIC ----
    if temp >= TEMP_THRESHOLD:
        auto_off_sent = False

        if relay_state == 0:
            alert_active = True
            send_message(
                CHAT_ID,
                "ALERT\nTemp: {:.2f} °C\nRelay OFF\nSend /on\n".format(temp)
            )
        else:
            alert_active = False

    else:
        alert_active = False

        if relay_state == 1:
            relay.value(0)

        if not auto_off_sent:
            send_message(
                CHAT_ID,
                "Temp normal ({:.2f} °C)\nRelay AUTO-OFF\n".format(temp)
            )
            auto_off_sent = True

    # ---- TELEGRAM GET UPDATES ----
    try:
        r = urequests.get(BASE_URL + "/getUpdates?offset={}".format(last_id + 1))

        if r.status_code != 200:
            print("Telegram GET error:", r.status_code)
            r.close()
            time.sleep(5)
            continue

        data = r.json()
        r.close()

        if "result" not in data:
            time.sleep(5)
            continue

        for msg in data["result"]:
            last_id = msg["update_id"]

            if "message" not in msg:
                continue

            text = msg["message"].get("text", "")
            chat_id = msg["message"]["chat"]["id"]

            if str(chat_id) == CHAT_ID:

                if text == "/on":
                    relay.value(1)
                    alert_active = False
                    send_message(CHAT_ID, "Relay ON" + "\n")

                elif text == "/off":
                    relay.value(0)
                    send_message(CHAT_ID, "Relay OFF" + "\n")

                elif text == "/status":
                    send_message(
                        CHAT_ID,
                        "Status\nTemp: {:.2f} °C\nHumidity: {:.2f} %\nRelay: {}\n".format(
                            temp, hum, "ON" if relay.value() else "OFF"
                        )
                    )

    except Exception as e:
        print("Telegram update exception:", e)

    time.sleep(5)
