#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SpuR - An Spectral Signature Reader System in Chipless Tags Using Software Defined Radio (SDR)
# Author: Frate, M.
# Description: SpuR - An Spectral Signature Reader System in Chipless Tags Using Software Defined Radio (SDR)
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import iio
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import SpuR_Reader_python_mod as python_mod  # embedded python module
import configparser
import time
import threading



from gnuradio import qtgui

class SpuR_Reader(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SpuR - An Spectral Signature Reader System in Chipless Tags Using Software Defined Radio (SDR)", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SpuR - An Spectral Signature Reader System in Chipless Tags Using Software Defined Radio (SDR)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SpuR_Reader")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.fun_prob = fun_prob = 0
        self._gain_conf_config = configparser.ConfigParser()
        self._gain_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        try: gain_conf = self._gain_conf_config.getint('main', 'rx_gain')
        except: gain_conf = 72
        self.gain_conf = gain_conf
        self.freqc = freqc = python_mod.sweeper(fun_prob)
        self._freq_conf_config = configparser.ConfigParser()
        self._freq_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        try: freq_conf = self._freq_conf_config.getfloat('main', 'freq')
        except: freq_conf = 10
        self.freq_conf = freq_conf
        self._attenua_conf_config = configparser.ConfigParser()
        self._attenua_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        try: attenua_conf = self._attenua_conf_config.getint('main', 'attenua')
        except: attenua_conf = 9
        self.attenua_conf = attenua_conf
        self._ampl_conf_config = configparser.ConfigParser()
        self._ampl_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        try: ampl_conf = self._ampl_conf_config.getfloat('main', 'a_s')
        except: ampl_conf = 1
        self.ampl_conf = ampl_conf
        self.taps = taps = 64
        self.samp_rate = samp_rate = 25000000
        self.rx_gain = rx_gain = gain_conf
        self.frequency = frequency = freqc
        self.freq = freq = freq_conf
        self.attenua = attenua = attenua_conf
        self.amplitude = amplitude = fun_prob
        self.a_s = a_s = ampl_conf

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_range = Range(0, 73, 1, gain_conf, 100)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "RX Gain (dB)", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rx_gain_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.probSign = blocks.probe_signal_f()
        self._freq_range = Range(0, 1000, 0.1, freq_conf, 100)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._attenua_range = Range(0, 73, 1, attenua_conf, 100)
        self._attenua_win = RangeWidget(self._attenua_range, self.set_attenua, "Attenuation TX (dB)", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._attenua_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._a_s_range = Range(0, 50, 0.1, ampl_conf, 100)
        self._a_s_win = RangeWidget(self._a_s_range, self.set_a_s, "Saw Tooth amplitude", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._a_s_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-20, 20)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0, 14)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', '', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0_0_0_0 = iio.fmcomms2_source_fc32('ip:192.168.2.1' if 'ip:192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0_0_0_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0_0_0_0.set_frequency(freqc)
        self.iio_pluto_source_0_0_0_0.set_samplerate(520834)
        self.iio_pluto_source_0_0_0_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0_0_0_0.set_gain(0, rx_gain)
        self.iio_pluto_source_0_0_0_0.set_quadrature(False)
        self.iio_pluto_source_0_0_0_0.set_rfdc(False)
        self.iio_pluto_source_0_0_0_0.set_bbdc(False)
        self.iio_pluto_source_0_0_0_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0_0 = iio.fmcomms2_sink_fc32('ip:192.168.2.1' if 'ip:192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0_0.set_len_tag_key('')
        self.iio_pluto_sink_0_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0_0.set_frequency(freqc)
        self.iio_pluto_sink_0_0.set_samplerate(520834)
        self.iio_pluto_sink_0_0.set_attenuation(0, attenua)
        self.iio_pluto_sink_0_0.set_filter_params('Auto', '', 0, 0)
        self.hilbert_fc_0_0_0_0 = filter.hilbert_fc(64, window.WIN_HAMMING, 6.76)
        def _fun_prob_probe():
          while True:

            val = self.probSign.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_fun_prob,val))
              except AttributeError:
                self.set_fun_prob(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _fun_prob_thread = threading.Thread(target=_fun_prob_probe)
        _fun_prob_thread.daemon = True
        _fun_prob_thread.start()
        self._frequency_tool_bar = Qt.QToolBar(self)

        if None:
            self._frequency_formatter = None
        else:
            self._frequency_formatter = lambda x: eng_notation.num_to_str(x)

        self._frequency_tool_bar.addWidget(Qt.QLabel("Frequency"))
        self._frequency_label = Qt.QLabel(str(self._frequency_formatter(self.frequency)))
        self._frequency_tool_bar.addWidget(self._frequency_label)
        self.top_grid_layout.addWidget(self._frequency_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(10)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(500000, 0.000002, 4000, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, freq, a_s, 0, 0)
        self._amplitude_tool_bar = Qt.QToolBar(self)

        if None:
            self._amplitude_formatter = None
        else:
            self._amplitude_formatter = lambda x: str(x)

        self._amplitude_tool_bar.addWidget(Qt.QLabel("Amplitude"))
        self._amplitude_label = Qt.QLabel(str(self._amplitude_formatter(self.amplitude)))
        self._amplitude_tool_bar.addWidget(self._amplitude_label)
        self.top_grid_layout.addWidget(self._amplitude_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.hilbert_fc_0_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.probSign, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.hilbert_fc_0_0_0_0, 0), (self.iio_pluto_sink_0_0, 0))
        self.connect((self.iio_pluto_source_0_0_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SpuR_Reader")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_fun_prob(self):
        return self.fun_prob

    def set_fun_prob(self, fun_prob):
        self.fun_prob = fun_prob
        self.set_amplitude(self.fun_prob)
        self.set_freqc(python_mod.sweeper(self.fun_prob))

    def get_gain_conf(self):
        return self.gain_conf

    def set_gain_conf(self, gain_conf):
        self.gain_conf = gain_conf
        self.set_rx_gain(self.gain_conf)

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.set_frequency(self.freqc)
        self.iio_pluto_sink_0_0.set_frequency(self.freqc)
        self.iio_pluto_source_0_0_0_0.set_frequency(self.freqc)

    def get_freq_conf(self):
        return self.freq_conf

    def set_freq_conf(self, freq_conf):
        self.freq_conf = freq_conf
        self.set_freq(self.freq_conf)

    def get_attenua_conf(self):
        return self.attenua_conf

    def set_attenua_conf(self, attenua_conf):
        self.attenua_conf = attenua_conf
        self.set_attenua(self.attenua_conf)

    def get_ampl_conf(self):
        return self.ampl_conf

    def set_ampl_conf(self, ampl_conf):
        self.ampl_conf = ampl_conf
        self.set_a_s(self.ampl_conf)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self._gain_conf_config = configparser.ConfigParser()
        self._gain_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        if not self._gain_conf_config.has_section('main'):
        	self._gain_conf_config.add_section('main')
        self._gain_conf_config.set('main', 'rx_gain', str(self.rx_gain))
        self._gain_conf_config.write(open('/mnt/d/Compartilhada/SpuR/conf.txt', 'w'))
        self.iio_pluto_source_0_0_0_0.set_gain(0, self.rx_gain)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        Qt.QMetaObject.invokeMethod(self._frequency_label, "setText", Qt.Q_ARG("QString", str(self._frequency_formatter(self.frequency))))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_conf_config = configparser.ConfigParser()
        self._freq_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        if not self._freq_conf_config.has_section('main'):
        	self._freq_conf_config.add_section('main')
        self._freq_conf_config.set('main', 'freq', str(self.freq))
        self._freq_conf_config.write(open('/mnt/d/Compartilhada/SpuR/conf.txt', 'w'))
        self.analog_sig_source_x_0_0.set_frequency(self.freq)

    def get_attenua(self):
        return self.attenua

    def set_attenua(self, attenua):
        self.attenua = attenua
        self._attenua_conf_config = configparser.ConfigParser()
        self._attenua_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        if not self._attenua_conf_config.has_section('main'):
        	self._attenua_conf_config.add_section('main')
        self._attenua_conf_config.set('main', 'attenua', str(self.attenua))
        self._attenua_conf_config.write(open('/mnt/d/Compartilhada/SpuR/conf.txt', 'w'))
        self.iio_pluto_sink_0_0.set_attenuation(self.attenua)

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude
        Qt.QMetaObject.invokeMethod(self._amplitude_label, "setText", Qt.Q_ARG("QString", str(self._amplitude_formatter(self.amplitude))))

    def get_a_s(self):
        return self.a_s

    def set_a_s(self, a_s):
        self.a_s = a_s
        self._ampl_conf_config = configparser.ConfigParser()
        self._ampl_conf_config.read('/mnt/d/Compartilhada/SpuR/conf.txt')
        if not self._ampl_conf_config.has_section('main'):
        	self._ampl_conf_config.add_section('main')
        self._ampl_conf_config.set('main', 'a_s', str(self.a_s))
        self._ampl_conf_config.write(open('/mnt/d/Compartilhada/SpuR/conf.txt', 'w'))
        self.analog_sig_source_x_0_0.set_amplitude(self.a_s)




def main(top_block_cls=SpuR_Reader, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
