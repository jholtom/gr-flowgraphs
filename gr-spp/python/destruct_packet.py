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
import ast
import os
import queue
import numpy as np
import pmt
from pmt import *
from pmt import pmt_to_python
from gnuradio import gr
from gnuradio.gr import block
from struct import *
from Crypto.Cipher import AES

def utf8len(s):
    return len(s.encode('utf-8'))


LENGTH_OF_TIMESTAMP = 4 #number of bytes in timestamp data
LENGTH_OF_PFIELD = 1 #number of bytes in pfield data

class SPP_Packet():

    def __init__(self):
        self.apid = 2000
        self.payload = str(0xFFFFFFFFFFFFFF) #this length still needs to be set???? also what type of data will this be????
        self.length = utf8len(self.payload) #if optional second header will be included this will also include 4 bytes timestamp and maybe 1 byte pfield
        self.packet = None

#  unloads the packets based on specific format
def unpacketize(packet, beaconapid, pfield=False,encrypt=False,enckey=False):
    """
     The SPP header (the first 6 bytes) is unpacked into 3 chunks that are each 2 bytes long
     Bit 0 is the leftmost bit
     Header0 contains bits 0-15 of the packet which include:
        Packet Version Number(3 bits)
        Packet Type(1 bit)
        Second Header Flag(1 bit)
        Applicatoin Process ID(APID)(11 bits)
     Header1 contains bits 16-31 of the packet which include:
        Sequence Flags(2 bits)
        Packet Sequence Count(14 bits)
     Length contains bits 32-45 of the packet which include:
        Packet Data Length(16 bits)
    """
    # This handles a packet that is a little bit too short...
    if len(packet) < 7:
        if len(packet) == 6:
            print("DP: ERROR - the payload seems to be empty adding default values: 0")
            header0 = header1 = length = 0
            int(header0)
            int(header1)
            int(length)
            packetVersionNumber = header0 & 0xE000 #select bits 0-2 of header0( bits 0-2 of the packet)
            packetType = header0 & 0x1000 #select bit 3 of header0( bit 3 of the packet)
            secondHeaderFlag = header0 & 0x0800 #select bit 4 of header0( bit 4 of the packet)
            apid = header0 & 0x07FF #select bits 5-15 of header0( bits 5-15 of the packet)
            sequenceFlags = header1 & 0xC000 #select bits 0-1 of header1( bits 16-17 of the packet)
            packetSequenceCount = header1 & 0x3FFF #select bits 2-15 of header1( bits 18-31 of the packet)
            unloaded_payload = 0
            return packetType, apid, packetSequenceCount, length, unloaded_payload

        print("DP: ERROR - packet too short for unpacking length of packet:",len(packet),"\tReturning default values")
        packetType = 0
        apid = 0
        packetSequenceCount = 0
        length = 0
        unloaded_payload = 0
        return packetType, apid, packetSequenceCount, length, unloaded_payload

    header0,header1,length = unpack('!HHH', packet[:6])
    packetVersionNumber = header0 & 0xE000 #select bits 0-2 of header0( bits 0-2 of the packet)
    packetType = header0 & 0x1000 #select bit 3 of header0( bit 3 of the packet)
    secondHeaderFlag = header0 & 0x0800 #select bit 4 of header0( bit 4 of the packet)
    apid = header0 & 0x07FF #select bits 5-15 of header0( bits 5-15 of the packet)
    sequenceFlags = header1 & 0xC000 #select bits 0-1 of header1( bits 16-17 of the packet)
    packetSequenceCount = header1 & 0x3FFF #select bits 2-15 of header1( bits 18-31 of the packet)
    length += 1 #Restore packet length according to SDLP Specification
    if secondHeaderFlag: #checks bit 4(secondHeaderFlag) to see if a second header is present
        #packet contains a second header meaning timestamp bytes(4)
        if pfield:
            pfield, timestamp = unpack('!BL', packet[6:11])
            unloaded_payload = packet[11:length+11]
        else:
            print("DP: SHF len packet ",len(packet[6:10]))
            if len(packet[6:10]) == 0:
                print("DP: ERROR - Packet is not big enough")
            timestamp = unpack('!L', packet[6:10])
            unloaded_payload = packet[10:length+10]
    else: #packet does not contain second header
        unloaded_payload = packet[6:length+6]

    if packetVersionNumber != 0 and packetVersionNumber != 1:
        #ERROR: packet version number is incorrect
        print("DP: ERROR - packetVersionNumber is incorrect: ",packetVersionNumber,"")
    if hex(packetType) != '0x0' and hex(packetType) != '0x1000':
        #ERROR: packetType is incorrect
        print("DP: ERROR - packetType is incorrect: ",hex(packetType),"")
    if len(unloaded_payload) != length:
        #ERROR: packet is incorrect length
        print("DP: ERROR - payload is incorrect length: current length: ",len(unloaded_payload)," correct length: ",length,"")

    if encrypt == 1 and (apid == beaconapid - 2 or apid == beaconapid + 1):
        enc = AES.new(enckey, AES.MODE_ECB)
        decryptedtext = enc.decrypt(unloaded_payload)
        unloaded_payload = decryptedtext

    # return the pfield if there was one
    if secondHeaderFlag and pfield:
        return apid, packetSequenceCount, length, unloaded_payload, pfield
    return packetType, apid, packetSequenceCount, length, unloaded_payload

#######################################################################################################################################
#######################################################################################################################################

class destruct_packet(gr.basic_block):

    #           block destruct_packet
    #     Take packet and pick apart the pieces into individual data again
    data = 0
    _out_port = pmt.intern("out")
    _elysium_port = pmt.intern("elysium")
    _sf2cmd_port = pmt.intern("sf2cmd")
    _tftp_port = pmt.intern("tftp")
    _beacon_port = pmt.intern("beacon")
    _in_port = pmt.intern("in")
    MAX_SIZE_OF_QUEUE = 1000
    MAX_TIMEOUT_DELAY = 5
    NUMBER_OF_ITEMS_PULLED_FROM_PACKET = 5 #number of items returned in spp::unpacketize
    SPP_PACKET_EXAMPLE = SPP_Packet()
    size_of_payload = utf8len(SPP_PACKET_EXAMPLE.payload)
    size_of_packet = sys.getsizeof(SPP_PACKET_EXAMPLE.packet)
    data_queue = queue.Queue(MAX_SIZE_OF_QUEUE)

    def __init__(self,ely,sf2,tftp,beacon,encrypt,enckey):
        gr.basic_block.__init__(self,
            name="destruct_packet",
            in_sig = [],out_sig = [])
        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages
        self.message_port_register_out(self._elysium_port) #this creates the output port for messages
        self.message_port_register_out(self._sf2cmd_port) #this creates the output port for messages
        self.message_port_register_out(self._tftp_port) #this creates the output port for messages
        self.message_port_register_out(self._beacon_port) #this creates the output port for messages

        self.elysiumapid = ely
        self.sf2cmdapid = sf2
        self.tftpapid = tftp
        self.beaconapid = beacon
        if encrypt != 0 and encrypt != 1:
            print("DP: ERROR - Invalid encryption mode and defaulting to no encryption (type 0)")
            self.encrypt = 0
        else:
            self.encrypt = encrypt
        if not enckey:
            print("DP: ERROR - Invalid encryption key and defaulting to default key: TEMPORARYKEY")
            self.enckey = "TEMPORARYKEY"
        else:
            self.enckey = enckey

        print("DP: Destruct Packet Initialized")

    def msg_handler_method(self, msg):
        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
            self.data = msg_str
        elif pmt.is_pair(msg):
            incoming_dict = pmt.car(msg)
            incoming_data = pmt.cdr(msg)
            self.data = pmt.to_python(incoming_data).tobytes()
            print("DP: Length of Received Packet Data: ",len(self.data),"")
        else:
            print("DP: ERROR - wrong type came through message")
            self.data = "default string"
        packet = self.data
        pfield = False #default for now to assume there is no second header
        packetType, apid, packetSequenceCount, length, payload = unpacketize(packet, self.beaconapid,pfield,self.encrypt,self.enckey)
        self.data_queue.put(payload,False)
        while(not self.data_queue.empty()):
            current_payload = self.data_queue.get(False)
            out_payload = pmt.init_u8vector(len(current_payload), current_payload)
            deliver_current_payload = pmt.cons(pmt.to_pmt(None), out_payload) #preps the current_payload for being sent in a message
            if apid == self.elysiumapid:
                self.message_port_pub(self._elysium_port, deliver_current_payload) #sends out deliver_current_payload as a message on self._out_port
            if apid == self.sf2cmdapid:
                self.message_port_pub(self._sf2cmd_port, deliver_current_payload) #sends out deliver_current_payload as a message on self._out_port
            if apid == self.tftpapid:
                self.message_port_pub(self._tftp_port, deliver_current_payload) #sends out deliver_current_payload as a message on self._out_port
            if apid == self.beaconapid:
                self.message_port_pub(self._beacon_port, deliver_current_payload) #sends out deliver_current_payload as a message on self._out_port
            else:
                self.message_port_pub(self._out_port, deliver_current_payload) # Default to the extra out port

    def general_work(self, input_items, output_items):
        print("DP: General work has been called")
        return  len(output_items)
