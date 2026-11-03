import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=0)
adc = MCP3021(5.11)

try:
    state = 0
    while True:
        state = 1 - state
        GPIO.output(14, state)
        print(f"GPIO14 = {state}")
        t_end = time.time() + 5
        while time.time() < t_end:
            print(f"  U = {adc.get_voltage():.3f} В")
            time.sleep(0.5)
finally:
    GPIO.output(14, 0)
    adc.deinit()
    GPIO.cleanup()