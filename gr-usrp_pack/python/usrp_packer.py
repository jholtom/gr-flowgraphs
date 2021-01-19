#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import os
import numpy
from gnuradio import gr
from gnuradio.gr import block
from math import pi
from gnuradio.digital import packet_utils
import gnuradio.digital as gr_digital
import Queue
import time
import math
from struct import *
import sys
import pmt
from pmt import pmt_to_python

class usrp_packer(gr.basic_block):
    """
    Takes the given packet/frame and pads it for compatibility with the USRP
    """
    _out_port = pmt.intern("out")
    _in_port = pmt.intern("in")
    MAX_SIZE_OF_QUEUE = 1000
    MAX_TIMEOUT_DELAY = 5

    data_queue = Queue.Queue(MAX_SIZE_OF_QUEUE)
    samples_per_bit = 0
    bits_per_symbol = 0

    def __init__(self,samples_per_bit,bits_per_symbol):
        gr.basic_block.__init__(self,
            name="usrp_packer",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages
        self.samples_per_symbol = samples_per_bit
        self.bits_per_symbol = bits_per_symbol

    def msg_handler_method(self, msg):
        #msg1 = self.msgq.delete_head() #blocking read of message queue
        if pmt.is_pair(msg):
            msg_str = pmt.cdr(msg)
            #msg_str = str(pmt.symbol_to_string(msg2)) #changes the data back into usable data
            self.data_queue.put(msg_str,False)
        else:
            print "ERROR: PACK: wrong type came through message\n"
        while not(self.data_queue.empty()):
            try:
                self.payload = self.data_queue.get(False)
                data_length = len(self.payload)
                print "USRP: Data Length:",data_length,"\n"
                usrp_packing = (_npadding_bytes(data_length,self.samples_per_symbol,self.bits_per_symbol) * '\x55')
                deliver_data = self.payload + usrp_packing
                self.message_port_pub(self._out_port, deliver_data)
                #self.msgq.insert_tail(deliver_current_packet)
            except:
                print "USRP:ERROR: hit exception in msg handler\n"

    def _npadding_bytes(pkt_byte_len, samples_per_symbol, bits_per_symbol):
        """
        Generate sufficient padding such that each packet ultimately ends
        up being a multiple of 512 bytes when sent across the USB.  We
        send 4-byte samples across the USB (16-bit I and 16-bit Q), thus
        we want to pad so that after modulation the resulting packet
        is a multiple of 128 samples.
        Args:
            ptk_byte_len: len in bytes of packet, not including padding.
            samples_per_symbol: samples per bit (1 bit / symbolwidth GMSK) (int)
            bits_per_symbol: bits per symbol (log2(modulation order)) (int)
        Returns:
            number of bytes of padding to append.
        """
        modulus = 128
        byte_modulus = gru.lcm(modulus/8, samples_per_symbol) * bits_per_symbol / samples_per_symbol
        r = pkt_byte_len % byte_modulus
        if r == 0:
            return 0
        return byte_modulus - r

   # def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        #for i in range(len(ninput_items_required)):
            #ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        #output_items[0][:] = input_items[0]
        #consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
