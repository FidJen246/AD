import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from scipy.signal import iirfilter, lfilter


def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    signal = amplitude * np.sin(frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=t.shape)
        signal += noise
    return signal


class HarmonicPlotter(QWidget):
    def __init__(self):
        super().__init__()

        self.amplitude = 1.0
        self.frequency = 1.0
        self.phase = 0.0
        self.noise_mean = 0.0
        self.noise_covariance = 0.01
        self.show_noise = True

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.line_original, = self.ax1.plot([], label='Original Signal', color='blue')
        self.line_filtered, = self.ax2.plot([], label='Filtered Signal', color='red')
        
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.legend()
        self.ax1.grid(True)
        
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.legend()
        self.ax2.grid(True)

        self.slider_amplitude = QSlider(Qt.Horizontal)
        self.slider_amplitude.setMinimum(1)
        self.slider_amplitude.setMaximum(100)
        self.slider_amplitude.setValue(int(self.amplitude * 10))
        self.slider_amplitude.valueChanged.connect(self.update_amplitude)
        self.label_amplitude = QLabel("Amplitude")
        layout.addWidget(self.label_amplitude)
        layout.addWidget(self.slider_amplitude)

        self.slider_frequency = QSlider(Qt.Horizontal)
        self.slider_frequency.setMinimum(1)
        self.slider_frequency.setMaximum(100)
        self.slider_frequency.setValue(int(self.frequency * 10))
        self.slider_frequency.valueChanged.connect(self.update_frequency)
        self.label_frequency = QLabel("Frequency")
        layout.addWidget(self.label_frequency)
        layout.addWidget(self.slider_frequency)

        self.slider_phase = QSlider(Qt.Horizontal)
        self.slider_phase.setMinimum(0)
        self.slider_phase.setMaximum(628)
        self.slider_phase.setValue(int(self.phase * 100))
        self.slider_phase.valueChanged.connect(self.update_phase)
        self.label_phase = QLabel("Phase")
        layout.addWidget(self.label_phase)
        layout.addWidget(self.slider_phase)

        self.slider_noise_mean = QSlider(Qt.Horizontal)
        self.slider_noise_mean.setMinimum(-10)
        self.slider_noise_mean.setMaximum(10)
        self.slider_noise_mean.setValue(int(self.noise_mean * 100))
        self.slider_noise_mean.valueChanged.connect(self.update_noise_mean)
        self.label_noise_mean = QLabel("Noise Mean")
        layout.addWidget(self.label_noise_mean)
        layout.addWidget(self.slider_noise_mean)

        self.slider_noise_covariance = QSlider(Qt.Horizontal)
        self.slider_noise_covariance.setMinimum(1)
        self.slider_noise_covariance.setMaximum(100)
        self.slider_noise_covariance.setValue(int(self.noise_covariance * 100))
        self.slider_noise_covariance.valueChanged.connect(self.update_noise_covariance)
        self.label_noise_covariance = QLabel("Noise Covariance")
        layout.addWidget(self.label_noise_covariance)
        layout.addWidget(self.slider_noise_covariance)

        self.checkbox_show_noise = QCheckBox('Show Noise')
        self.checkbox_show_noise.setChecked(self.show_noise)
        self.checkbox_show_noise.stateChanged.connect(self.update_show_noise)
        layout.addWidget(self.checkbox_show_noise)

        self.button_reset = QPushButton('Reset')
        self.button_reset.clicked.connect(self.reset_parameters)
        layout.addWidget(self.button_reset)

        self.setLayout(layout)
        self.setWindowTitle('Harmonic Plotter')
        self.update_plot()
        self.show()

    def update_amplitude(self, value):
        self.amplitude = value / 10.0
        self.update_plot()

    def update_frequency(self, value):
        self.frequency = value / 10.0
        self.update_plot()

    def update_phase(self, value):
        self.phase = value / 100.0
        self.update_plot()

    def update_noise_mean(self, value):
        self.noise_mean = value / 100.0
        self.update_plot()

    def update_noise_covariance(self, value):
        self.noise_covariance = value / 100.0
        self.update_plot()

    def update_show_noise(self, state):
        self.show_noise = state == Qt.Checked
        self.update_plot()

    def reset_parameters(self):
        self.amplitude = 1.0
        self.frequency = 1.0
        self.phase = 0.0
        self.noise_mean = 0.0
        self.noise_covariance = 0.01
        self.show_noise = True

        self.slider_amplitude.setValue(int(self.amplitude * 10))
        self.slider_frequency.setValue(int(self.frequency * 10))
        self.slider_phase.setValue(int(self.phase * 100))
        self.slider_noise_mean.setValue(int(self.noise_mean * 100))
        self.slider_noise_covariance.setValue(int(self.noise_covariance * 100))
        self.checkbox_show_noise.setChecked(self.show_noise)

        self.update_plot()

    def update_plot(self):
        t = np.linspace(0, 10, 500)
        y = harmonic_with_noise(t, self.amplitude, self.frequency, self.phase, self.noise_mean, self.noise_covariance, self.show_noise)

        fs = 1 / (t[1] - t[0]) #Середня частота дискретизації
        b, a = iirfilter(4, 10 / (0.5 * fs), btype='lowpass', ftype='butter')
        y_filtered = lfilter(b, a, y)

        self.line_original.set_data(t, y)
        self.line_filtered.set_data(t, y_filtered)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.figure.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HarmonicPlotter()
    sys.exit(app.exec_())
