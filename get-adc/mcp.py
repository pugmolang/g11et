import mcp3021_driver
import adc_plot
import time


dynamic_range = 5.0

voltage_values = []
time_values = []

duration = 10.0


try:
    adc = mcp3021_driver.MCP3021(dynamic_range)

    start_time = time.time()

    while time.time() - start_time < duration:
        voltage = adc.get_voltage()

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