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

#help(blocks) #shows more about blocks available

class qa_create_packet(gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def my_own_test(self,src,crt_packet,destruct_pkt,snk):   #this causes a segmentation fault but running it through tb.connect stuff does not
    	input_req = 0
        crt_packet.forecast(1,input_req)
        nonsense = ["5hello my nAme is john what is your name?5"]
        output_from_create = [0]
        crt_packet.general_work(nonsense,output_from_create)
        incoming_packet = output_from_create[0]

        number_of_inputs_needed = [0,0,0]
        destruct_pkt.forecast(5,number_of_inputs_needed)
        output_stuff = [0,0,0,0,0]
        destruct_pkt.general_work(incoming_packet,output_stuff)

        print output_stuff[0]," :packetType"
        print output_stuff[1]," :APID"
        print output_stuff[2]," :packetSequenceCount"
        print output_stuff[3]," :length"
        print output_stuff[4]," :payload"

    def test_001_t (self):
        # set up fg
        self.src = blocks.file_source(40,"/home/jacob/Downloads/hex.dat",False) #first parameter is the num of inputs that create_packet demands 
        																# = current size of a packet in bytes set by the class in spp.py changing the payload size
        
        self.crt_packet = create_packet()
        self.destruct_pkt = destruct_packet()
        ####  *** might never be able to read the file as is because it is writing native binary to the file so if there is data there it may be unable to display it?
        self.snk = blocks.file_sink(10,"/home/jacob/Downloads/my_end_result1.dat",True) #10 = out_sig * number of output items = float16(2 bytes) * 5 output items

        #self.my_own_test(src,crt_packet,destruct_pkt,snk)
        self.tb.connect(self.src,self.crt_packet,self.destruct_pkt,self.snk)
        self.tb.run ()
            


if __name__ == '__main__':
    gr_unittest.run(qa_create_packet, "qa_create_packet.xml")


"""
if __name__ == '__main__':
	payload = 0x3F
	apid = 0x700
	created_packet = packetize(payload, apid)


	packetType, apid, packetSequenceCount, length, payload = unpacketize(created_packet)
	print "\nFINAL:  payload: ", payload," packetType: ",packetType," apid: ",apid," packetSequenceCount: ",packetSequenceCount," length: ",length,"\n"
"""