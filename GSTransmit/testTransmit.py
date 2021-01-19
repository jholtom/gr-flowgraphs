#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: spacecraft
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
exec(open("/home/spacecraft/cygnus/gnuradio/gr-spp/python/create_packet.py").read())
exec(open("/home/spacecraft/cygnus/gnuradio/preamble_insert_jbh_jej.py").read())
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

from gnuradio import qtgui

class testTransmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "testTransmit")

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
        self.samp_sym = samp_sym = 8
        self.baud_rate = baud_rate = 55555
        self.sensitivity = sensitivity = 0.707
        self.samp_rate = samp_rate = samp_sym * baud_rate
        self.freq = freq = 459200000
        self.frame_length = frame_length = 0x40
        self.dev = dev = 80000
        self.bandwidth_time = bandwidth_time = 0.3

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            'mod_packet_len',
        )
        self.uhd_usrp_sink_0.set_center_freq(459200000, 0)
        self.uhd_usrp_sink_0.set_gain(90, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.spp_create_packet_0 = create_packet(2002, 1, 1, 'loremipsumdolore')
        self.sdlp_create_frame_0 = create_frame(47, 31, 1, 0, 0, 0, 0)
        self.qtgui_freq_sink_x_0_1_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0.enable_control_panel(True)



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
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_win)
        self.digital_gfsk_mod_1 = digital.gfsk_mod(
            samples_per_symbol=8,
            sensitivity=1.5,
            bt=.5,
            verbose=False,
            log=False)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc(firdes.window(firdes.WIN_HANN, 50, 0), 10, 10, True, 'mod_packet_len')
        self.digital_burst_shaper_xx_0.set_block_alias("burst_shaper1")
        self.digital_additive_scrambler_bb_0 = digital.additive_scrambler_bb(0x221, 0x1ff, 8, count=0, bits_per_byte=1, reset_tag_key="packet_len")
        self.burst_preamble_insert_0 = preamble_insert(0x8ad8bb2a)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, 1036*8, "mod_packet_len")
        self.blocks_socket_pdu_0 = blocks.socket_pdu('UDP_SERVER', '127.0.0.1', '52010', 10000, False)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_char*1, '/home/spacecraft/mdrMATLAB/tT.bin', False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/spacecraft/mdrMATLAB/iqSamplesRecent.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.spp_create_packet_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.burst_preamble_insert_0, 'in'))
        self.msg_connect((self.burst_preamble_insert_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.sdlp_create_frame_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.spp_create_packet_0, 'out'), (self.sdlp_create_frame_0, 'in'))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_additive_scrambler_bb_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_gfsk_mod_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_additive_scrambler_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.qtgui_freq_sink_x_0_1_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_gfsk_mod_1, 0), (self.blocks_stream_to_tagged_stream_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "testTransmit")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_sym(self):
        return self.samp_sym

    def set_samp_sym(self, samp_sym):
        self.samp_sym = samp_sym
        self.set_samp_rate(self.samp_sym * self.baud_rate)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(self.samp_sym * self.baud_rate)

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0_1_0.set_frequency_range(self.freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0_1_0.set_frequency_range(self.freq, self.samp_rate)

    def get_frame_length(self):
        return self.frame_length

    def set_frame_length(self, frame_length):
        self.frame_length = frame_length

    def get_dev(self):
        return self.dev

    def set_dev(self, dev):
        self.dev = dev

    def get_bandwidth_time(self):
        return self.bandwidth_time

    def set_bandwidth_time(self, bandwidth_time):
        self.bandwidth_time = bandwidth_time





def main(top_block_cls=testTransmit, options=None):

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
