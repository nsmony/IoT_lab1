from machine import Pin
import dht
import time

sensor = dht.DHT22(Pin(4))

print("DHT11 Sensor Reading Started...")

while True:
    try:
        sensor.measure() 
        
        temperature = sensor.temperature()  # °C
        humidity = sensor.humidity()        # %
        
        print("Temperature: {:.2f} °C".format(temperature))
        print("Humidity: {:.2f} %".format(humidity))
        print("---------------------------")
        
    except OSError:
        print("Failed to read from DHT11 sensor")

    time.sleep(5)  
