import r2r_adc
import adc_plot
import time


dynamic_range = 3.3

voltage_values = []
time_values = []

duration = 3.0


try:
    adc = r2r_adc.R2R_ADC(
        dynamic_range,
        compare_time = 0.0001
        )

    start_time = time.time()

    while time.time() - start_time < duration:
        voltage = adc.get_sar_voltage()

        voltage_values.append(voltage)
        time_values.append(time.time() - start_time)

    adc_plot.plot_voltage_vs_time(
        time_values,
        voltage_values,
        dynamic_range
    )

    adc_plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
