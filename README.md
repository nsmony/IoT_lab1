# Lab 1 : Temperature Sensor with Relay Control (Telegram)
This project uses an ESP32 to measure temperature and humidity with a DHT22 sensor and operate a relay module through Telegram commands.

### Equipment and Wiring
- ESP32 Dev Board (MicroPython firmware flashed)
- DHT22 sensor
- Relay module
- jumper wires
- USB cable + laptop with Thonny
- Wi-Fi access (internet)
#### Wiring Connection
<img width="960" height="1280" alt="image" src="https://github.com/user-attachments/assets/50e2a4b6-8f2e-44fe-8d9a-857ba427c5ac" />

#### DHT22 → ESP32
| DHT22 Pin | ESP32 Pin |
|----------|-----------|
| VCC (+) | VCC/3V3 |
| DATA (I/O) | GPIO 4 (D4) |
| GND (-) | GND |

#### Relay Module → ESP32
| Relay Pin | ESP32 Pin |
|----------|-----------|
| VCC | VCC/5V (VIN) |
| GND | GND |
| IN | GPIO 2 (D2)|

### Configuration Steps
#### Telegram Bot Setup:
- Create your own telegram bot using @BotFather
- Get the generated Bot Token 
- Add your bot into your telegram group
- Get your group Chat ID

#### Code Configuration:
- Update the information into the code:
-- BOT_TOKEN = "YOUR_BOT_TOKEN"
-- CHAT_ID = "YOUR_CHAT_ID"
-- DHTPIN = 4
-- RELAY_PIN = 2
# Tasks & Checkpoints
### Task 1-Sensor Read & Print
- Read DHT22 every 5 seconds and print the temperature and humidity with 2
decimals.
- Evidence: serial screenshot.
<img width="991" height="769" alt="image" src="https://github.com/user-attachments/assets/5955689a-ebb8-4083-8749-237051044e82" />
<img width="970" height="749" alt="image" src="https://github.com/user-attachments/assets/64ef417d-435c-435d-97d2-704bf498eeea" />

### Task 2-Telegram Send
- Implement send_message() and post a test message to your group.
- Evidence: chat screenshot.
<img width="1280" height="675" alt="image" src="https://github.com/user-attachments/assets/0d892f34-527a-49de-a3cc-4917d2b8c1f6" />

### Task 3-Bot Command
- Implement /status to reply with current T/H and relay state.
- Implement /on and /off to control the relay.
- Evidence: chat screenshot showing all three commands working.
<img width="1280" height="677" alt="image" src="https://github.com/user-attachments/assets/ccaabe68-29b1-45d6-8ad6-636a808ef212" />


### Task 4-Bot Command
- No messages while T < 30 °C.
- If T ≥ 30 °C and relay is OFF, send an alert every loop (5 s) until /on is
received.
- After /on, stop alerts. When T < 30 °C, turn relay OFF automatically and senda one-time “auto-OFF” notice.
- Evidence: short video (60–90s) demonstrating above behavior https://youtu.be/eMreX57w4FE

### Task 5-Robustness
- Auto-reconnect Wi-Fi when dropped.
- Handle Telegram HTTP errors (print status; skip this cycle on failure).
- Avoid crashing on DHT OSError (skip cycle).
