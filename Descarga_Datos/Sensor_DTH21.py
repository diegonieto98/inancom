import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4 #PIN DIGITAL DE LECTURA

global temperatura, humedad
while True:
    humedad, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humedad is not None and temperatura is not None:
        if humedad<100:
            print("Temp={0:0.1f}C Humedad={1:0.1f}%".format(temperatura, humedad))
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(10)