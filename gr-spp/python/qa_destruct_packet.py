#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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
import sys
sys.path.insert(0, '/home/jacob/cygnus/gnuradio/spp')
import os
from spp import *
import numpy
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from create_packet import create_packet
from destruct_packet import destruct_packet

class qa_destruct_packet (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
                # set up fg
        src = blocks.file_source(96,"/home/jacob/Downloads/hex.dat",True) #52 or 53??? is the current size of a packet in bytes.. maybe
        
        crt_packet = create_packet()
        input_req = [0,0,0]
        #crt_packet.forecast(1,input_req)
        nonsense = "/home/jacob/Downloads/hex.dat"
        output_from_create = [0]
        #crt_packet.general_work(nonsense,output_from_create)
        incoming_packet = output_from_create[0]


        destruct_pkt = destruct_packet()
        number_of_inputs_needed = [0,0,0]
        #destruct_pkt.forecast(5,number_of_inputs_needed)
        output_stuff = [0,0,0,0,0]
        #destruct_pkt.general_work(incoming_packet,output_stuff)
        
        snk = blocks.file_sink(20,"my_end_result.dat") #20 ????


        self.tb.connect(src,destruct_pkt)

        self.tb.connect(destruct_pkt,snk)
        #self.tb.connect(crt_packet,snk)
        self.tb.run ()
        #check the output
        print output_stuff[0]," :packetType"
        print output_stuff[1]," :APID"
        print output_stuff[2]," :packetSequenceCount"
        print output_stuff[3]," :length"
        print output_stuff[4]," :payload"
        


if __name__ == '__main__':
    gr_unittest.run(qa_destruct_packet, "qa_destruct_packet.xml")
