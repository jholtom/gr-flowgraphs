#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Jacob Holtom and Wes Rogers.
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

#import numpy
#from numpy import *
#from numpy import ndarray
from gnuradio import gr
import sys
import os
import pmt
from pmt import *
from pmt import pmt_to_python
import queue
from struct import *
import binascii



#  unloads the frames based on specific format
def unframe(frame):
    TM_CUTOFF = 1778
    TC_CUTOFF = 1025
    CUTOFF = TM_CUTOFF #default to TM-CUTOFF for initializing

    #unpacks the first 6 bytes(48 bits) into 3 chunks that are 2 bytes long
    #bit 0 is the leftmost bit
    #header0_0 contains bits 0-15 of the frame which include:
        #TF_version or TransferFrame_version(2 bits)
        #SCID or Spacecraft Identifier(10 bits)
        #VCID or Virtual Channel Identifier(3 bits)
        #OCF or Operational Control Field Flag(1 bit)
    #header0_1 contains bits 16-31 of the frame which include:
        #MC Frame Count or Master Channel Frame Count(8 bits)
        #VC Frame Count or Virtual Channel Frame Count(8 bits)
    #header0_2 contains bits 32-47 of the frame which include:
        #Transfer Frame Data Field Status(16 bits)
            #TF Secondary Header Flag(1 bit)
            #Synchronization Flag(1 bit)
            #Packet Order Flag(1 bit)
            #Segment Length Identifier(2 bits)
            #First Header Pointer(11 bits)

    #If frame contains a second header
    #header1_1 contains bits 48-up to 560 which include:
        #TF Secondary Header
            #TF Secondary Header ID
                #TF Secondary Header Version Number(2 bits)
                #TF Secondary Header Length(6 bits)
        #up to 63 bytes of TF Secondary Header Data Field

    #ending0_0 contains OperationalControlField or OCF (32 bits)
    #ending0_1 contains Frame Error Control Field or FECF (16 bits)

    header0_0, header0_1, header0_2 = unpack('!HHH', frame[:6])
    header0_0, = unpack('!H',frame[:2]) #check type of frame to determine unpacking
    TF_version = (header0_0 & 0xC000) #select bits 0-1 of header0_0( bits 0-1 of the frame)
    scid = header0_0 & 0x3FF0 #select bit 2-11 of header0_0( bit 2-11 of the frame)
    vcid = header0_0 & 0x000E #select bit 12-14 of header0_0( bit 12-14 of the frame)
    OCF_flag = header0_0 & 0x0001 #select bit 15 of header0_0( bit 15 of the frame)

    MCframeCount = header0_1 & 0xFF00 #select bits 0-7 of header0_1( bits 16-23 of the frame)
    VCframeCount = header0_1 & 0x00FF #select bits 8-15 of header0_1( bits 24-31 of the frame)

    TFSecondaryHeaderFlag = header0_2 & 0x8000 #selcts bit 0 of header0_2
    SynchFlag = header0_2 & 0x4000 #selects bit 1 of header0_2
    PacketOrderFlag = header0_2 & 0x2000 #selects bit 2 of header0_2
    SegmentLengthID = header0_2 & 0x1800 #selects bits 3-4 of header0_2
    FirstHeaderPointer = header0_2 & 0x07FF #selcts bits 5-15 of header0_2 (11 bits)

    #set ranges for unpacking based on frame type
    if TF_version == 0:
        CUTOFF = TM_CUTOFF
    elif TF_version == 16384:
        CUTOFF = TC_CUTOFF
    else:
        print("DF: ERROR - frame is not TC or TM, Reports: ",TF_version,"")

    if TFSecondaryHeaderFlag: #checks bit 0 of header0_2(TFSecondaryHeaderFlag) to see if a second header is present
        header1_1 = unpack('!B', frame[6:7])
        header1_1 = header1_1[0] #take it out of a tuple
        TFSecondaryHeaderVersionNumber = header1_1 & 0xC0 #selects bits 0-1 of header1_1
        TFSecondaryHeaderLength = header1_1 & 0x3F #selects bits 2-7 of the header1_1
        TFSecondaryHeaderDataField = unpack('!%ds' % TFSecondaryHeaderLength, frame[7:7+TFSecondaryHeaderLength])
        packet = frame[7+TFSecondaryHeaderLength:CUTOFF] #the packet starts at end of second header goes until the ending
        ending0_0, ending0_1 = unpack('!LH', frame[CUTOFF:CUTOFF+6])
    else: #frame does not contain second header
        packet = frame[6:] #the packet continues until right before the ending
        #ending0_0, ending0_1 = unpack('!LH', frame[CUTOFF:CUTOFF+6])

    #print "ending0_0",hex(ending0_0),""
    #print "ending0_1",hex(ending0_1),""

    # return the TF Secondary Header Data Field if there was one
    if TFSecondaryHeaderFlag:
        return packet, scid, vcid, FirstHeaderPointer

    return packet, scid, vcid, FirstHeaderPointer



class destruct_frame(gr.basic_block):
        # block destruct_frame takes in a SDLP frame and removes the frame structure and passes on the contents

    #constants
    _out_port = pmt.intern("out")
    _in_port = pmt.intern("in")
    MAX_SIZE_OF_QUEUE = 10000
    data_queue = queue.Queue(MAX_SIZE_OF_QUEUE)
    message_queue = queue.Queue(MAX_SIZE_OF_QUEUE)

    def __init__(self):
        gr.basic_block.__init__(self,
            name="destruct_frame",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages

        self.frame = "" #this will be recieved in a stream
        self.contents = "" #this will be output in a message
        print("DF: Destruct Frame Initialized")

    def msg_handler_method(self, msg):
        #OID_send = False #default value

        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
            self.data = msg_str
        elif pmt.is_pair(msg):
            incoming_dict = pmt.car(msg)
            incoming_data = pmt.cdr(msg)
            self.data = pmt.to_python(incoming_data).tobytes()
            print("DF: Length of Received Frame Data: ",len(self.data),"")
        else:
            print("DF: Error - Wrong type came through message")
        frame = self.data
        packet, scid, vcid, FirstHeaderPointer = unframe(frame)
        #Dont send until we know we have the whole packet
        #if FirstHeaderPointer == 2047:
            #print("DF: we are in destruct at the first header pointer = 1111111111")
            #this entire frame is part of the previous packet but we do not know if we have the whole packet yet
            #current_packet_reconstructing = self.data_queue.get(False)
            #current_packet_reconstructing = current_packet_reconstructing + packet #add the part we just received to the whole
            #print("DF:size of the thing building:",len(current_packet_reconstructing),"")
            #self.data_queue.put(current_packet_reconstructing,False) #store this packet til the next one arrives
            #print("DF:size of the queue:",self.data_queue.qsize(),"")
            #return #nothing will be sent because we are still building it
        #elif FirstHeaderPointer == 2046:  #0b11111111110:
            #this is an OID frame(only idle data) so we will ignore it but send the previous
            #OID_send = True
        #else: #the frame started a new packet at first header pointer anything before that belongs to the previous packet
            #print("DF: Handling a First Header Pointer")
            #if not(self.data_queue.empty()):
                #previous = self.data_queue.get(False)
                #if FirstHeaderPointer == 0:
                    #pass
                #else:
                    #print(type(previous))
                    #previous = previous + packet[:FirstHeaderPointer] #add on anything before the first header pointer
                #self.data_queue.put(previous,False) #add the previous back on to be sent out next
            #ignore1,ignore2,length_of_this_packet = unpack('!HHH', frame[FirstHeaderPointer:FirstHeaderPointer+6])
            #if FirstHeaderPointer+length_of_this_packet > len(frame):
                #this packet spills over into the next frame so just take the rest of this one
                #self.data_queue.put(packet[FirstHeaderPointer:FirstHeaderPointer+length_of_this_packet],False) #store this packet til the next one arrives by putting it second on the Queue
            #else:
                #self.data_queue.put(packet[FirstHeaderPointer:FirstHeaderPointer+length_of_this_packet],False) #store this packet til the next one arrives by putting it second on the Queue
                #place_last_one_ended = FirstHeaderPointer+length_of_this_packet
                #while place_last_one_ended < len(frame):
                    #if place_last_one_ended+6 < len(frame):
                        #ignore1,ignore2,length_of_this_packet = unpack('!HHH', frame[place_last_one_ended:place_last_one_ended+6])
                        #if place_last_one_ended + length_of_this_packet < len(frame):
                            #self.data_queue.put(packet[place_last_one_ended:place_last_one_ended+length_of_this_packet],False)
                            #place_last_one_ended = place_last_one_ended + length_of_this_packet
                        #else:
                            #self.data_queue.put(packet[place_last_one_ended:],False) #take the rest and put it as the last thing on the queue which should not send this time
                            #place_last_one_ended = len(frame)
                    #else:
                        #place_last_one_ended = len(frame) #end the loop and begin sending the data

        #while self.data_queue.qsize() > 1 or OID_send: #there is a previous packet that needs to be sent now that we have the current one
        #packet_to_send = self.data_queue.get(False)
        out_packet = pmt.init_u8vector(len(packet), packet)
        deliver_current_packet = pmt.cons(pmt.to_pmt(None), out_packet)
        self.message_port_pub(self._out_port, deliver_current_packet) #send the packet in a message
        OID_send = False


    def general_work(self, input_items, output_items):
        return len(output_items)
