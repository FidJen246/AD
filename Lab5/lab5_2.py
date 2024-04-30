import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, CheckboxButtonGroup
from bokeh.plotting import figure


def simple_lowpass_filter(signal, alpha=0.1):
    filtered_signal = np.zeros_like(signal)
    filtered_signal[0] = signal[0]
    for i in range(1, len(signal)):
        filtered_signal[i] = alpha * signal[i] + (1 - alpha) * filtered_signal[i - 1]
    return filtered_signal


class HarmonicPlotter:
    def __init__(self):
        self.amplitude = 1.0
        self.frequency = 1.0
        self.phase = 0.0
        self.noise_mean = 0.0
        self.noise_covariance = 0.01
        self.show_noise = True
        self.alpha = 0.01

        self.source = ColumnDataSource(data=dict(x=[], y=[], filtered_y=[]))

        self.create_plot()
        self.create_widgets()
        self.update(True)

    def create_plot(self):
        self.plot = figure(title="Harmonic Plotter", height=400, width=800)
        self.plot.line('x', 'y', source=self.source, line_width=2, line_color="blue", legend_label="Original Signal")
        self.plot.line('x', 'filtered_y', source=self.source, line_width=2, line_color="red", legend_label="Filtered Signal")
        self.plot.legend.location = "top_left"
        self.plot.xaxis.axis_label = "Time"
        self.plot.yaxis.axis_label = "Amplitude"
        self.t = np.linspace(0, 10, 500)

    def create_widgets(self):
        self.slider_amplitude = Slider(title="Amplitude", start=1, end=100, value=self.amplitude*10, step=1)
        self.slider_amplitude.on_change('value', self.update_parameters)

        self.slider_frequency = Slider(title="Frequency", start=1, end=100, value=self.frequency*10, step=1)
        self.slider_frequency.on_change('value', self.update_parameters)

        self.slider_phase = Slider(title="Phase", start=0, end=628, value=self.phase*100, step=1)
        self.slider_phase.on_change('value', self.update_parameters)

        self.slider_noise_mean = Slider(title="Noise Mean", start=-10, end=10, value=self.noise_mean*100, step=1)
        self.slider_noise_mean.on_change('value', self.update_parameters_noise)

        self.slider_noise_covariance = Slider(title="Noise Covariance", start=1, end=100, value=self.noise_covariance*100, step=1)
        self.slider_noise_covariance.on_change('value', self.update_parameters_noise)

        self.slider_alpha = Slider(title="Alpha", start=1, end=100, value=self.alpha*100, step=1)
        self.slider_alpha.on_change('value', self.update_parameters)

        self.checkbox_show_noise = CheckboxButtonGroup(labels=["Show Noise"], active=[0])
        self.checkbox_show_noise.on_change('active', self.update_parameters)

    def update_parameters(self, attr, old, new):
        self.amplitude = self.slider_amplitude.value / 10.0
        self.frequency = self.slider_frequency.value / 10.0
        self.phase = self.slider_phase.value / 100.0
        self.show_noise = 0 in self.checkbox_show_noise.active
        self.alpha = self.slider_alpha.value / 100.0
        self.update(False)

    def update_parameters_noise(self, attr, old, new):
        self.noise_mean = self.slider_noise_mean.value / 100.0
        self.noise_covariance = self.slider_noise_covariance.value / 100.0
        self.update(True)

    def signal_with_noise(self, param):
        signal = self.amplitude * np.sin(self.frequency * self.t + self.phase)
        if param:
            self.noise = np.random.normal(self.noise_mean, np.sqrt(self.noise_covariance), size=self.t.shape)
        if self.show_noise:
                signal += self.noise
        return signal

    def update(self, param):
        signal = self.signal_with_noise(param)
        filtered_signal = simple_lowpass_filter(signal, self.alpha)
        
        self.source.data = dict(x=self.t, y=signal, filtered_y=filtered_signal)
        curdoc().add_root(column(self.plot, 
                                  self.slider_amplitude, 
                                  self.slider_frequency, 
                                  self.slider_phase, 
                                  self.slider_noise_mean, 
                                  self.slider_noise_covariance,
                                  self.slider_alpha,  
                                  self.checkbox_show_noise))

plotter = HarmonicPlotter()
