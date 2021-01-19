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

import sys
import os
import ast
import numpy as np
import pmt
from pmt import pmt_to_python
import queue
from struct import *
from gnuradio import gr, digital
from gnuradio import blocks
from gnuradio.digital import packet_utils

class virtual_channel():
    """ This is a virtual channel which is part of a master channel """
    header1_1 = 0
    TFSecondaryHeaderFlag = 0
    FEC = 0

    def __init__(self,vcid):
        self.vcid = vcid
        self.VCframeCount = 0

class master_channel():
    """ This is a master channel which will contain virtual channels """
    FEC=0

    def __init__(self,name,second_header=False,ocf=False):
        self.MC_FSH = second_header #will this channel have a second header?
        self.MC_OCF = ocf
        self.name = name
        self.virtual_channels = []
        self.MCframeCount = 0

    def add_virtual_channel(self,vcid):
        self.virtual_channels.append(virtual_channel(vcid))

class physical_channel():
    """ This defines a physical channel which can hold multiple master channels """
    
    def __init__(self,number,FEC=0):
        self.number = number
        self.master_channels = []
        self.FEC = FEC




def Virtual_channel_multiplexing(vcid,MC,physical_channel,FirstHeaderPointer):
    #If there is only one Master Channel on the Physical Channel, the Virtual Channel
    #Multiplexing Function shall create an OID Transfer Frame to preserve the continuity of the
    #transmitted stream in the event that there are no valid Transfer Frames available for
    #transmission at a release time. The OID Transfer Frame shall have its First Header Pointer
    travel_on_VC = True #will be sent over a VC
    travel_on_MC = False 
    MCframeCount = 0 #Master Channel Frame Count in Transfer Frames on the Virtual Channel Frame Service shall be empty 

    if not(vcid in MC.virtual_channels):
        MC.add_virtual_channel(vcid)
    else: #set the specific virtual channel
        for x in range(len(MC.virtual_channels)):
            if MC.virtual_channels[x].vcid == vcid:
                VC = MC.virtual_channels[x]

    #4.2.4.4 (also see 4.1.4.6)
    """If  there  is  only  one  Master  Channel  on  th
    e  Physical  Channel,  the  Virtual  Channel  
    Multiplexing  Function  shall  create  an  OID  Transfer
    Frame to preserve the continuity of the 
    transmitted  stream  in  the  event  that  there  
    are  no  valid  Transfer  Frames  available  for  
    transmission at a release time.  The OID Transf
    er Frame shall have its First Header Pointer 
    set to ‘11111111110’ and its VCID set to that of a Virtual Channel that carries Packets. """
    if len(physical_channel.master_channels) == 1: #there is only one master channel on this physical channel
        print("TOOK EXCEPTION IN Virtual_channel_multiplexing")
        #create OID TF to preserve continuity of the transmitted stream in the event that there are no valid TFs available for transmission at a release time
        FirstHeaderPointer = 0b11111111110 #this stands for an OID frame
        vcid = 0 #virtual channel that carries packets

    return FirstHeaderPointer,MCframeCount,travel_on_VC,travel_on_MC

def packet_too_big(queue,size_needed,SIZE_OF_FRAMING_PARTS,packet,TFSecondaryHeaderFlag,TFSecondaryHeaderLength,len_header1_1):
        #PACKET IS TOO LARGE FOR A SINGLE FRAME TO SEND MUST SPLIT IT
    print("ERROR: packet is too large to be sent in a single frame must be split")
    next_packet = packet[size_needed-SIZE_OF_FRAMING_PARTS:] #get the rest of the packet that will not fit
    if TFSecondaryHeaderFlag:
        packet = packet[TFSecondaryHeaderLength+len_header1_1:size_needed-SIZE_OF_FRAMING_PARTS]
    else:
        packet = packet[:size_needed-SIZE_OF_FRAMING_PARTS] #get the part that will fit
    queue.put(next_packet,False) #puts the next part of the packet onto the queue
    return packet

Frame_Sequence_number = 0
#  Loads the packets into a frame
def frame(packet, scid, TF_version, physical_channel,queue,Frame_Sequence_number,vcid=None, FirstHeaderPointer=0, ocf=0, fecf=0,bypass_flag=0,control_command_flag=0):
    length_of_packet = len(packet)
    #print("CF:frame:starting frame")

    TM_SIZE = 1042 #frame size for all TM frames
    TC_SIZE = 1024 #frame size for all TC frames
    SIZE_OF_FRAMING_PARTS = 12 #bytes that includes header0_0,0_1,0_2 and ending0_0,0_1 defualt TM packet

    #initialize frame blocks of 2 bytes each
    header0_0 = 0x0000
    header0_1 = 0x0000
    header0_2 = 0x0000
    header0_2_TC = 0x00
    header1_1 = 0x00 #beginning of optional second header
    ending0_0 = 0x00000000
    ending0_1 = 0x0000

    empty = 0
    travel_on_VC = False
    travel_on_MC = True
    MC = physical_channel.master_channels[0] #defualt
    size_needed = TM_SIZE #defualt

    #set the master channel
    #TF_version = convert_TF_Version(TF_version) #set the bits according to type
    if TF_version == 0:
        MC = physical_channel.master_channels[0]
    elif TF_version == 1:
        MC = physical_channel.master_channels[1]
    elif TF_version == 2:
        MC = physical_channel.master_channels[2]
    elif TF_version == 3:
        MC = physical_channel.master_channels[3]

    #determine the frame size:
    if TF_version == 0:
        size_needed = TM_SIZE
    elif TF_version == 1:
        size_needed = TC_SIZE
        SIZE_OF_FRAMING_PARTS = 11 #header is only 5 bytes for TC
    else:
        print("CF:ERROR:Frame is not TM or TC default to TM")
        size_needed = TM_SIZE


    MCframeCount = 0
    VCframeCount = 0
    TFSecondaryHeaderFlag = 0
    SynchFlag = 0
    PacketOrderFlag = 0
    SegmentLengthID = 0
    TFSecondaryHeaderVersionNumber = 0
    TFSecondaryHeaderLength = 0
    ocf_flag = 0 #set bit low
    RSVD_spare = 00 #always 00 because they are reserved for future use

    if ocf != 0:
        ocf_flag = 1 #set bit high

    #RULES
        #Transfer Frames transferred by the Virtual Channel Frame and Master Channel Frame
        #Services shall be partially formatted TM Transfer Frames, and the following restrictions
        #apply:
    if vcid != 7: #there will be 2: 0 for microprocessor and 1: elysium
        FirstHeaderPointer,MCframeCount,travel_on_VC,travel_on_MC = Virtual_channel_multiplexing(vcid,MC,physical_channel,FirstHeaderPointer)
    else:
        travel_on_VC = False
        travel_on_MC = True
        VCframeCount = 0
 
    if MC.MC_FSH: #master channel has a secondary header
        for VC in MC.virtual_channels:
            VC.header1_1 = empty  #TF second header and flag for the Virtual Channel on the same Master Channel must be empty 3.2.6
            VC.TFSecondaryHeaderFlag = 0
 
    if MC.MC_OCF:
        for VC in MC.virtual_channels:
            VC.OCF = empty  #ocf and ocf_flag of the TF on the Virtual Channel of the same Master Channel shall be empty 
            VC.ocf_flag = empty

    if physical_channel.FEC: #if physical channel has an FEC master and virtual should not
        MC.FEC = empty #the Frame Error Control Field of the Transfer Frames submitted to the Master or Virtual Channel shall be empty
        for VC in mc.virtual_channels:
            VC.FEC = empty
    if MC.MCframeCount == 255:
        #must reset the counter to avoid going out of bounds
        MC.MCframeCount = 0
        MCframeCount = MC.MCframeCount
    elif travel_on_MC:
        MC.MCframeCount += 1 #add one for each frame sent across the master channel.
        MCframeCount = MC.MCframeCount
    for VC in MC.virtual_channels:
        if VC.vcid == vcid:
            if VC.VCframeCount == 255 and travel_on_VC:
                #must reset the counter to avoid going out of bounds
                VC.VCframeCount = 0
                VCframeCount = VC.VCframeCount
            elif travel_on_VC:
                VC.VCframeCount += 1 #add one for each frame sent across the virtual channel.
                #  ?? VCframeCount = VC.sent_partial = TrueVCframeCount
            break
    if SynchFlag == 0:
        SegmentLengthID = 3 #If Synchronization Flag is ‘0’ the SegmentLength ID will be ‘11’(3 in decimal). #if synch flag is '1' SegLenID is undefined 

    #TM FRAME(6 bytes)
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

        #header1_1 contains bits 48-up to 560 which include:
            #TF Secondary Header
                #TF Secondary Header ID
                    #TF Secondary Header Version Number(2 bits)
                    #TF Secondary Header Length(6 bits)
            #up to 63 bytes of TF Secondary Header Data Field
    
    #TC FRAME(5 bytes)
        #header0_0
            #add in TransferFrame_version(2 bits)
            #bypass flag(1 bit)
            #control command flag(1 bit)
            #RSVD spare(2 bits)
            #add in SCID or Spacecraft Identifier(10 bits)
        #header0_1
            #add in VCID or Virtual Channel Identifier(6 bits)
            #length of the frame(10 bits) #spec says total number of bytes in frame - 1
        #header0_2
            #Frame sequence Number(8 bits)
    #ending0_0 contains OperationalControlField or OCF (32 bits)
    #ending0_1 contains Frame Error Control Field or FECF (16 bits)

    if TF_version == 0:
        header0_0 |= TF_version << 14 #add in TransferFrame_version(2 bits)
        header0_0 |= scid << 4        #add in SCID or Spacecraft Identifier(10 bits)
        header0_0 |= vcid << 1        #add in VCID or Virtual Channel Identifier(3 bits)
        header0_0 |= ocf_flag         #add in OCF or Operational Control Field Flag(1 bit)

        header0_1 |= MCframeCount << 8 #add in MC Frame Count(8 bits)
        header0_1 |= VCframeCount #add in VC Frame Count(8 bits)

        #add in Transfer Frame Data Field Status(16 bits)
        header0_2 |= TFSecondaryHeaderFlag << 15
        header0_2 |= SynchFlag << 14
        header0_2 |= PacketOrderFlag << 13
        header0_2 |= SegmentLengthID << 11
        header0_2 |= FirstHeaderPointer

    elif TF_version == 1: #TC Frame header 5 bytes long
        header0_0 |= 00 << 14               #add in TransferFrame_version(2 bits), This should be 00 for the TC Standard
        header0_0 |= bypass_flag << 13              #bypass flag(1 bit)
        header0_0 |= control_command_flag << 12     #control command flag(1 bit)
        header0_0 |= RSVD_spare << 10               #RSVD spare(2 bits)
        header0_0 |= scid                           #add in SCID or Spacecraft Identifier(10 bits)

        header0_1 |= vcid << 10      #add in VCID or Virtual Channel Identifier(6 bits)
        header0_1 |= TC_SIZE - 1   #length of the frame(10 bits) #spec says total number of bytes in frame - 1

        header0_2_TC |= Frame_Sequence_number #Frame sequence Number(8 bits)
        #print("header0_2_TC",header0_2_TC)

    #secondary header
    header1_1 |= TFSecondaryHeaderVersionNumber << 6
    header1_1 |= TFSecondaryHeaderLength

    #ending0_0 contains OperationalControlField or OCF (32 bits)
    #ending0_1 contains Frame Error Control Field or FECF (16 bits)
    ending0_0 |= ocf
    ending0_1 |= fecf
    
    len_header1_1 = 1#len(header1_1)

    if TFSecondaryHeaderFlag: #packet contains second header bytes so length is different
        length_tot = TFSecondaryHeaderLength + len_header1_1 + length_of_packet
        if length_tot > (size_needed-SIZE_OF_FRAMING_PARTS):
            packet = packet_too_big(queue,size_needed,SIZE_OF_FRAMING_PARTS,packet,TFSecondaryHeaderFlag,TFSecondaryHeaderLength,len_header1_1)
            length_of_packet = len(packet)
        pad_size = size_needed - calcsize('!HHH%(length_total)dsLH' % {"length_total" : length_tot}) #set needed padding
        frame = pack('!HHH%(total_len)ds%(padding_needed)dxLH' % {"total_len" : length_tot, "padding_needed" : pad_size}, header0_0, header0_1, header0_2, packet, ending0_0, ending0_1)
        print("CF:final length of frame:",len(frame),"total padding:",pad_size,"length before padding or framing:",length_tot,"")
    elif TF_version == 0:
        if length_of_packet > (size_needed-SIZE_OF_FRAMING_PARTS):
            print("CF:frame:length_of_packet",length_of_packet,"")
            packet = packet_too_big(queue,size_needed,SIZE_OF_FRAMING_PARTS,packet,TFSecondaryHeaderFlag,TFSecondaryHeaderLength,len_header1_1)
            length_of_packet = len(packet)
            print("CF:frame:length_of_packet2",length_of_packet,"")
        pad_size = size_needed - calcsize('!HHH%(length_packet)dsLH' % {"length_packet" : length_of_packet}) #set needed padding
        if length_of_packet == 6:
            #there is no payload so set the first header pointer to declare this a OID packet
            FirstHeaderPointer = 2046  #0b11111111110:
        frame = pack('!HHH%(length_packet)ds%(padding_needed)dxLH' % {"length_packet" : length_of_packet, "padding_needed" : pad_size}, header0_0, header0_1, header0_2, packet, ending0_0, ending0_1) #HHH refers to the 3 blocks of 2 bytes each that are being packed(header0_0-0_2)
        print("CF: final FirstHeaderPointer:",FirstHeaderPointer,"")
        print("CF:final length of frame:",len(frame),"total padding:",pad_size,"length before padding or framing:",length_of_packet,"")
        print("CF: header(TM):",bin(header0_0),bin(header0_1),bin(header0_2),"")
    else:
        #TC frame
        if length_of_packet > (size_needed-SIZE_OF_FRAMING_PARTS):
            print("CF:frame:length_of_packet",length_of_packet,"")
            packet = packet_too_big(queue,size_needed,SIZE_OF_FRAMING_PARTS,packet,TFSecondaryHeaderFlag,TFSecondaryHeaderLength,len_header1_1)
            length_of_packet = len(packet)
            print("CF:frame:length_of_packet2",length_of_packet,"")
        pad_size = size_needed - calcsize('!HHB%(length_packet)dsLH' % {"length_packet" : length_of_packet}) #set needed padding
        if length_of_packet == 5:
            #there is no payload so set the first header pointer to declare this a OID packet
            FirstHeaderPointer = 2046  #0b11111111110:
        frame = pack('!HHB%(length_packet)ds%(padding_needed)dxLH' % {"length_packet" : length_of_packet, "padding_needed" : pad_size}, header0_0, header0_1, header0_2_TC, packet, ending0_0, ending0_1) #HHH refers to the 3 blocks of 2 bytes each that are being packed(header0_0-0_2)
        print("CF: final FirstHeaderPointer:",FirstHeaderPointer,"")
        print("CF:final length of frame:",len(frame),"total padding:",pad_size,"length before padding or framing:",length_of_packet,"")
        print("CF: header(TC):",bin(header0_0),bin(header0_1),bin(header0_2_TC),"")
        if Frame_Sequence_number < 255:
            Frame_Sequence_number += 1 #increment for the next frame
        else:
            Frame_Sequence_number = 0 #rollover
        print(Frame_Sequence_number)
    return frame,Frame_Sequence_number


class create_frame(gr.basic_block):
    """
         block create_frame
         take in a packet and other needed data to create a new frame around the packet
    """
    #Constants
    _out_port = pmt.intern("out")
    _in_port = pmt.intern("in")
    NUMBER_OF_INPUTS_PER_FRAME = 7
    MAX_SIZE_OF_QUEUE = 1000
    data_queue = queue.Queue(MAX_SIZE_OF_QUEUE)
    unfinished_queue = queue.Queue(MAX_SIZE_OF_QUEUE)
    holding_queue = queue.Queue(MAX_SIZE_OF_QUEUE)
    ##how many messages in a queue
    

    physical_channel = physical_channel(0)

    MC_00 = master_channel("TM")
    MC_01 = master_channel("TC")
    MC_10 = master_channel("other 10")
    MC_11 = master_channel("other 11")
    master_channels = [MC_00,MC_01,MC_10,MC_11]
    physical_channel.master_channels = master_channels

    def __init__(self,scid,vcid=7,TF_version=0,ocf=0,fecf=0,bypass_flag=0,control_command_flag=0):
        gr.basic_block.__init__(self,
            name="create_frame",
            in_sig=[],
            out_sig=[]) 

        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages

        self.FirstHeaderPointer = 0 #default to no offset
        self.frame = 0 #will be sent out as a stream
        self.packet = 0 #will be coming in as a message
        self.scid = scid #static throughout mission
        if not vcid:
            self.vcid = None
        else:
            self.vcid = vcid
        self.TF_version = TF_version
        self.ocf = ocf
        self.fecf = fecf
        self.bypass_flag = bypass_flag
        self.control_command_flag = control_command_flag
        DEFAULT_MSGQ_LIMIT = 10
        #self.msgq = msgq#gr.msg_queue(DEFAULT_MSGQ_LIMIT) #create the message queue
        print("INIT Create Frame")

    def msg_handler_method(self, msg):
        global Frame_Sequence_number
        """msg1 = self.msgq.delete_head() #blocking read of message queue
        msg1 = msg1.to_string()
        print msg_1,"msg1"
        self.packet = msg1"""
        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
        elif pmt.is_pair(msg):
            msg_cdr = pmt.cdr(msg)
            #Take this vector to bytes...
            msg_str = pmt.to_python(msg_cdr).tobytes()
            print(msg_str)
            self.data_queue.put(msg_str,False)
        else:
            print("ERROR: wrong type came through message")
        self.packet = msg_str
        #if not(self.data_queue.empty()):
         #   print("CF:Queue was not empty")
          #  self.holding_queue.put(self.packet,False) #since we are not done with the previous one
           # while not(self.data_queue.empty()):
            #    next_part = self.data_queue.get(False) #pulls off of the queue
             #   self.packet = next_part #adds the last part of the previous packet
              #  self.FirstHeaderPointer = len(next_part) #offset by the length of the leftover part
               # if self.FirstHeaderPointer > 1024:
               #     print("CF:we are in create at set first header to 11111")
               #     self.FirstHeaderPointer = 0b11111111111
               # else:
               #     print("CF:adding in second message to tail, FirstHeaderPointer:",self.FirstHeaderPointer,"")
               #     pull_next = self.holding_queue.get(False)
               #     print("got here")
               #     self.packet = self.packet + pull_next #adds the upcoming packet to the end of the previous one that is ending
               #     break
               # my_frame, Frame_Sequence_number =  frame(self.packet, self.scid, self.TF_version, self.physical_channel,self.data_queue, Frame_Sequence_number, self.vcid, self.FirstHeaderPointer, self.ocf, self.fecf, self.bypass_flag, self.control_command_flag) #creates the frame
               # print("got here2")
               # #p = ast.literal_eval(my_frame)
               # #p = [ int(x) for x in p ]
               # out_frame = pmt.init_u8vector(len(my_frame),my_frame)
               # deliver_current_frame = pmt.cons(pmt.to_pmt(None), out_frame)
               # #deliver_current_frame = pmt.cons(pmt.PMT_NIL, pmt.to_pmt(np.array(p,np.uint8)))
               # self.message_port_pub(self._out_port, deliver_current_frame) #send the frame in a message
               # print("sent the first time")
               # return
        # access_code = (0x555555558AD8BB2A).to_bytes(8, 'big')
        my_frame, Frame_Sequence_number =  frame(self.packet, self.scid, self.TF_version, self.physical_channel,self.data_queue, Frame_Sequence_number,self.vcid, self.FirstHeaderPointer, self.ocf, self.fecf,self.bypass_flag, 
        self.control_command_flag) #creates the frame
        #p = [ ord(x) for x in my_frame ]
        # frame_length_test = len(my_frame)
        # test_frame = access_code+my_frame
        out_frame = pmt.init_u8vector(len(my_frame),my_frame)
        deliver_current_frame = pmt.cons(pmt.to_pmt(None), out_frame)
        #deliver_current_frame = pmt.cons(pmt.PMT_NIL, pmt.to_pmt(np.array(p,np.uint8)))
        self.message_port_pub(self._out_port, deliver_current_frame) #send the frame in a message

    def general_work(self, input_items, output_items):
        print("CF:general Work ever called?")
        return len(output_items)


