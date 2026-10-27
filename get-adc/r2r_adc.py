import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        binary_number = [int(bit) for bit in f"{number:08b}"]
        GPIO.output(self.bits_gpio, binary_number)

    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)

            time.sleep(self.compare_time)

            comparator_value = GPIO.input(self.comp_gpio)

            if self.verbose:
                print(
                    f"Число: {number}, "
                    f"COMP: {comparator_value}"
                )

            if comparator_value == 1:
                return number

        return 255

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()

        voltage = number / 255 * self.dynamic_range

        return voltage




    def successive_approximation_adc(self):
        number = 0

        for bit in range(7, -1, -1):
            test_number = number | (1 << bit)

            self.number_to_dac(test_number)
            time.sleep(self.compare_time)

            comparator_value = GPIO.input(self.comp_gpio)

            if comparator_value == 0:
                number = test_number

        self.number_to_dac(number)

        return number


    def get_sar_voltage(self):
        number = self.successive_approximation_adc()

        voltage = number / 255 * self.dynamic_range

        return voltage

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3)

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")

    finally:
        adc.deinit()