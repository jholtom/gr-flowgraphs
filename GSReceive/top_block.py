#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

exec(open("/home/spacecraft/cygnus/gnuradio/gr-sdlp/python/create_frame.py").read())
exec(open("/home/spacecraft/cygnus/gnuradio/gr-sdlp/python/destruct_frame.py").read())
exec(open("/home/spacecraft/cygnus/gnuradio/gr-spp/python/create_packet.py").read())
exec(open("/home/spacecraft/cygnus/gnuradio/gr-spp/python/destruct_packet.py").read())
exec(open("/home/spacecraft/cygnus/gnuradio/preamble_insert_jbh_jej.py").read())
exec(open("/home/spacecraft/cygnus/gr-RS/reed_solomon.py").read())
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import epy_block_0
import epy_block_1

from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.tx_baud_rate = tx_baud_rate = 55652
        self.samp_sym = samp_sym = 8
        self.rx_baud_rate = rx_baud_rate = 19200
        self.tx_samp_rate = tx_samp_rate = samp_sym*tx_baud_rate
        self.transition_bw = transition_bw = 1000
        self.sensitivity = sensitivity = 1.5
        self.rx_samp_rate = rx_samp_rate = rx_baud_rate * samp_sym
        self.fsk_deviation_hz = fsk_deviation_hz = 75000
        self.frame_length = frame_length = 2040
        self.bandwidth_time = bandwidth_time = .5
        self.B_tx_freq = B_tx_freq = 459000000
        self.B_tftp_out_0 = B_tftp_out_0 = 5914
        self.B_tftp_out = B_tftp_out = 5914
        self.B_tftp_in_0 = B_tftp_in_0 = 51114
        self.B_tftp_in = B_tftp_in = "51114"
        self.B_rx_freq = B_rx_freq = 903400000
        self.B_out_0 = B_out_0 = 5900
        self.B_out = B_out = 5900
        self.B_beacons_0 = B_beacons_0 = 5913
        self.B_beacons = B_beacons = 5913
        self.A_tx_freq = A_tx_freq = 459193000
        self.A_tftp_out_0 = A_tftp_out_0 = 5814
        self.A_tftp_out = A_tftp_out = 5814
        self.A_tftp_in_0 = A_tftp_in_0 = 51014
        self.A_tftp_in = A_tftp_in = "51014"
        self.A_rx_freq = A_rx_freq = 903789000
        self.A_out_apid = A_out_apid = 5800
        self.A_out = A_out = 5800
        self.A_beacons_0 = A_beacons_0 = 5813
        self.A_beacons = A_beacons = 5813

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'USRP')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Squelch')
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, 'Constellation')
        self.tab_widget_3 = Qt.QWidget()
        self.tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_3)
        self.tab_grid_layout_3 = Qt.QGridLayout()
        self.tab_layout_3.addLayout(self.tab_grid_layout_3)
        self.tab.addTab(self.tab_widget_3, 'FFT')
        self.top_grid_layout.addWidget(self.tab)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_subdev_spec('A:A', 0)
        self.uhd_usrp_source_0.set_center_freq(A_rx_freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_bandwidth(rx_samp_rate, 0)
        self.uhd_usrp_source_0.set_samp_rate(rx_samp_rate)
        # No synchronization enforced.
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            'mod_packet_len',
        )
        self.uhd_usrp_sink_0_0.set_subdev_spec('A:B', 0)
        self.uhd_usrp_sink_0_0.set_center_freq(A_tx_freq, 0)
        self.uhd_usrp_sink_0_0.set_gain(65, 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(tx_samp_rate, 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(tx_samp_rate)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec())
        self.spp_destruct_packet_0 = destruct_packet(830, 811, 814, 813, 1, 'loremipsumdolore')
        self.spp_create_packet_0 = create_packet(1014, 1, 1, 'loremipsumdolore')
        self.sdlp_destruct_frame_0 = destruct_frame()
        self.sdlp_create_frame_0 = create_frame(47, 31, 1, 0, 0, 0, 0)
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rx_samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            A_rx_freq, #fc
            rx_samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            A_rx_freq, #fc
            rx_samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_3.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.001)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["black", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [1, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [8, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_const_sink_x_0_win)
        self.epy_block_1 = epy_block_1.blk(frame_size=frame_length, access_code='00011010110011111111110000011101', threshold=2)
        self.epy_block_0 = epy_block_0.blk()
        self.digital_gfsk_mod_1 = digital.gfsk_mod(
            samples_per_symbol=samp_sym,
            sensitivity=sensitivity,
            bt=bandwidth_time,
            verbose=False,
            log=False)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc(firdes.window(firdes.WIN_HANN, 50,0), 10, 10, True, 'mod_packet_len')
        self.ccsds_reed_solomon_0 = reed_solomon()
        self.burst_preamble_insert_0 = preamble_insert(0x8ad8bb2a)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_tagged_stream_to_pdu_0_1 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, 1036*8, "mod_packet_len")
        self.blocks_socket_pdu_1_0 = blocks.socket_pdu('TCP_SERVER', '127.0.0.1', '5830', 10000, False)
        self.blocks_socket_pdu_1 = blocks.socket_pdu('TCP_SERVER', '127.0.0.1', '5814', 10000, False)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu('UDP_SERVER', '127.0.0.1', '51014', 10000, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu('UDP_CLIENT', '127.0.0.1', '5813', 10000, False)
        self.blocks_pdu_to_tagged_stream_0_0_1 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                rx_samp_rate,
                -rx_baud_rate/1.5,
                rx_baud_rate/1.5,
                2000,
                firdes.WIN_HAMMING,
                6.76))
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(-70, 1e-3, 100, False)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.spp_create_packet_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_1, 'pdus'), (self.burst_preamble_insert_0, 'in'))
        self.msg_connect((self.burst_preamble_insert_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0_1, 'pdus'))
        self.msg_connect((self.ccsds_reed_solomon_0, 'out'), (self.sdlp_destruct_frame_0, 'in'))
        self.msg_connect((self.epy_block_0, 'out'), (self.epy_block_1, 'in'))
        self.msg_connect((self.epy_block_1, 'out'), (self.ccsds_reed_solomon_0, 'in'))
        self.msg_connect((self.sdlp_create_frame_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.sdlp_destruct_frame_0, 'out'), (self.spp_destruct_packet_0, 'in'))
        self.msg_connect((self.spp_create_packet_0, 'out'), (self.sdlp_create_frame_0, 'in'))
        self.msg_connect((self.spp_destruct_packet_0, 'beacon'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.spp_destruct_packet_0, 'tftp'), (self.blocks_socket_pdu_1, 'pdus'))
        self.msg_connect((self.spp_destruct_packet_0, 'sf2cmd'), (self.blocks_socket_pdu_1_0, 'pdus'))
        self.msg_connect((self.spp_destruct_packet_0, 'out'), (self.blocks_socket_pdu_1_0, 'pdus'))
        self.msg_connect((self.spp_destruct_packet_0, 'elysium'), (self.blocks_socket_pdu_1_0, 'pdus'))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.epy_block_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0_1, 0), (self.digital_gfsk_mod_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_tagged_stream_to_pdu_0_1, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.digital_gfsk_mod_1, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_baud_rate(self):
        return self.tx_baud_rate

    def set_tx_baud_rate(self, tx_baud_rate):
        self.tx_baud_rate = tx_baud_rate
        self.set_tx_samp_rate(self.samp_sym*self.tx_baud_rate)

    def get_samp_sym(self):
        return self.samp_sym

    def set_samp_sym(self, samp_sym):
        self.samp_sym = samp_sym
        self.set_rx_samp_rate(self.rx_baud_rate * self.samp_sym)
        self.set_tx_samp_rate(self.samp_sym*self.tx_baud_rate)

    def get_rx_baud_rate(self):
        return self.rx_baud_rate

    def set_rx_baud_rate(self, rx_baud_rate):
        self.rx_baud_rate = rx_baud_rate
        self.set_rx_samp_rate(self.rx_baud_rate * self.samp_sym)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.rx_samp_rate, -self.rx_baud_rate/1.5, self.rx_baud_rate/1.5, 2000, firdes.WIN_HAMMING, 6.76))

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.tx_samp_rate)
        self.uhd_usrp_sink_0_0.set_bandwidth(self.tx_samp_rate, 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(self.tx_samp_rate, 1)

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        self.transition_bw = transition_bw

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.rx_samp_rate, -self.rx_baud_rate/1.5, self.rx_baud_rate/1.5, 2000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.A_rx_freq, self.rx_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.A_rx_freq, self.rx_samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.rx_samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.rx_samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.rx_samp_rate, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.rx_samp_rate, 1)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz

    def get_frame_length(self):
        return self.frame_length

    def set_frame_length(self, frame_length):
        self.frame_length = frame_length
        self.epy_block_1.frame_size = self.frame_length

    def get_bandwidth_time(self):
        return self.bandwidth_time

    def set_bandwidth_time(self, bandwidth_time):
        self.bandwidth_time = bandwidth_time

    def get_B_tx_freq(self):
        return self.B_tx_freq

    def set_B_tx_freq(self, B_tx_freq):
        self.B_tx_freq = B_tx_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.B_tx_freq, 1)

    def get_B_tftp_out_0(self):
        return self.B_tftp_out_0

    def set_B_tftp_out_0(self, B_tftp_out_0):
        self.B_tftp_out_0 = B_tftp_out_0

    def get_B_tftp_out(self):
        return self.B_tftp_out

    def set_B_tftp_out(self, B_tftp_out):
        self.B_tftp_out = B_tftp_out

    def get_B_tftp_in_0(self):
        return self.B_tftp_in_0

    def set_B_tftp_in_0(self, B_tftp_in_0):
        self.B_tftp_in_0 = B_tftp_in_0

    def get_B_tftp_in(self):
        return self.B_tftp_in

    def set_B_tftp_in(self, B_tftp_in):
        self.B_tftp_in = B_tftp_in

    def get_B_rx_freq(self):
        return self.B_rx_freq

    def set_B_rx_freq(self, B_rx_freq):
        self.B_rx_freq = B_rx_freq
        self.uhd_usrp_source_0.set_center_freq(self.B_rx_freq, 1)

    def get_B_out_0(self):
        return self.B_out_0

    def set_B_out_0(self, B_out_0):
        self.B_out_0 = B_out_0

    def get_B_out(self):
        return self.B_out

    def set_B_out(self, B_out):
        self.B_out = B_out

    def get_B_beacons_0(self):
        return self.B_beacons_0

    def set_B_beacons_0(self, B_beacons_0):
        self.B_beacons_0 = B_beacons_0

    def get_B_beacons(self):
        return self.B_beacons

    def set_B_beacons(self, B_beacons):
        self.B_beacons = B_beacons

    def get_A_tx_freq(self):
        return self.A_tx_freq

    def set_A_tx_freq(self, A_tx_freq):
        self.A_tx_freq = A_tx_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.A_tx_freq, 0)

    def get_A_tftp_out_0(self):
        return self.A_tftp_out_0

    def set_A_tftp_out_0(self, A_tftp_out_0):
        self.A_tftp_out_0 = A_tftp_out_0

    def get_A_tftp_out(self):
        return self.A_tftp_out

    def set_A_tftp_out(self, A_tftp_out):
        self.A_tftp_out = A_tftp_out

    def get_A_tftp_in_0(self):
        return self.A_tftp_in_0

    def set_A_tftp_in_0(self, A_tftp_in_0):
        self.A_tftp_in_0 = A_tftp_in_0

    def get_A_tftp_in(self):
        return self.A_tftp_in

    def set_A_tftp_in(self, A_tftp_in):
        self.A_tftp_in = A_tftp_in

    def get_A_rx_freq(self):
        return self.A_rx_freq

    def set_A_rx_freq(self, A_rx_freq):
        self.A_rx_freq = A_rx_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.A_rx_freq, self.rx_samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.A_rx_freq, self.rx_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.A_rx_freq, 0)

    def get_A_out_apid(self):
        return self.A_out_apid

    def set_A_out_apid(self, A_out_apid):
        self.A_out_apid = A_out_apid

    def get_A_out(self):
        return self.A_out

    def set_A_out(self, A_out):
        self.A_out = A_out

    def get_A_beacons_0(self):
        return self.A_beacons_0

    def set_A_beacons_0(self, A_beacons_0):
        self.A_beacons_0 = A_beacons_0

    def get_A_beacons(self):
        return self.A_beacons

    def set_A_beacons(self, A_beacons):
        self.A_beacons = A_beacons





def main(top_block_cls=top_block, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
