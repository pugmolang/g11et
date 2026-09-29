import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT)
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not (0 <= number <= 255):
            print("Число должно быть от 0 до 255")
            number = 0

        binary_number = [int(bit) for bit in f"{number:08b}"]

        GPIO.output(self.gpio_bits, binary_number)

        if self.verbose:
            print(f"Число: {number}")
            print(f"Двоичный код: {binary_number}")
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(
                    f"Напряжение выходит за динамический диапазон ЦАП "
                    f"(0.00 - {self.dynamic_range:.3f} В)"
                  )
            print("Устанавливаем 0.0 В")
            voltage = 0.0
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)

        if self.verbose:
            print(f"Напряжение: {voltage:.3f} B")

if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_DAC(
                [16, 20, 21, 25, 26, 17, 27 ,22], 3.183, True)
        while True:
            try:
                voltage = float(input("введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попроьуйте еще раз\n")
    finally:
        if dac is not None:
            dac.deinit()