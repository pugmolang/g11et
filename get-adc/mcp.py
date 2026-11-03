import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.11
PIN = 14
CHARGE_TIME = 50
DISCHARGE_TIME = 50
CYCLES = 1
ZERO_LEVEL = 0.05
FILE_NAME = "rc_data.csv"
PLOT_NAME = "rc_plot.png"


def discharge_to_zero(adc):
    GPIO.output(PIN, 0)
    print("Разряжаю конденсатор до нуля...")
    while adc.get_voltage() > ZERO_LEVEL:
        time.sleep(0.1)
    time.sleep(1)


def record(adc, duration, start, times, voltages):
    t_end = time.time() + duration
    last_print = 0
    while time.time() < t_end:
        v = adc.get_voltage()
        t = time.time() - start
        voltages.append(v)
        times.append(t)
        if t - last_print >= 1:
            print(f"t = {t:5.1f} с, U = {v:.3f} В")
            last_print = t


def save_csv(times, voltages):
    with open(FILE_NAME, "w") as f:
        f.write("time_s,voltage_V\n")
        for t, v in zip(times, voltages):
            f.write(f"{t:.6f},{v:.4f}\n")


def plot(times, voltages):
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages)
    plt.title("Зарядка и разрядка конденсатора")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, max(times))
    plt.ylim(0, DYNAMIC_RANGE * 1.05)
    plt.grid(True)
    plt.savefig(PLOT_NAME)
    plt.show()


if __name__ == "__main__":
    times, voltages = [], []
    adc = None

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT, initial=0)
        adc = MCP3021(DYNAMIC_RANGE)

        discharge_to_zero(adc)

        start = time.time()
        for i in range(CYCLES):
            print(f"Цикл {i + 1}: зарядка")
            GPIO.output(PIN, 1)
            record(adc, CHARGE_TIME, start, times, voltages)

            print(f"Цикл {i + 1}: разрядка")
            GPIO.output(PIN, 0)
            record(adc, DISCHARGE_TIME, start, times, voltages)

    finally:
        GPIO.output(PIN, 0)
        if adc is not None:
            adc.deinit()
        GPIO.cleanup()

    save_csv(times, voltages)
    print(f"Измерений: {len(times)}, частота ~{len(times) / times[-1]:.0f} Гц")
    print(f"Данные: {FILE_NAME}, график: {PLOT_NAME}")
    plot(times, voltages)