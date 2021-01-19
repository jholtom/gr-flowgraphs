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


import os
import numpy
from gnuradio import gr
from gnuradio.gr import block
from math import pi
from gnuradio.digital import packet_utils
import gnuradio.digital as gr_digital
import queue
import time
import math
from struct import *
import sys
import pmt
from pmt import pmt_to_python
import itertools
from Crypto.Cipher import AES

# PVN 0
# Packet Type 1
# SHF dual random (timestamp, pfield)
# APID random
# Sequence Flags 11
# Sequence Count incrementing from 0 to 16383
# Length random 0-65535
# if pcode it's 0x2C
# if timestamp, unix time
def utf8len(s):
    return len(bytes(s,'utf-8'))


LENGTH_OF_TIMESTAMP = 4 #number of bytes in timestamp data
LENGTH_OF_PFIELD = 1 #number of bytes in pfield data

class SPP_Packet():

    def __init__(self, apid, payload):
        self.apid = apid #2000
        self.payload = payload #str(0xFFFFFFFFFFFFFF) #this length still needs to be set???? also what type of data will this be????
        self.length = len(payload) #utf8len(self.payload) #if optional second header will be included this will also include 4 bytes timestamp and maybe 1 byte pfield
        self.packet = packetize(self.payload,self.apid)


#  Loads the packets based on a specific format for SPP(Space Packet Protocol)
#    payload is the main data, APID(Application Process ID) should be 11 bits,
#    packetType should be 1 bit(0 for TM, 1 for TC),
#    timestamp is 4 bytes and pfield is 1 byte but only needed if a second header is to be included(second header is optional)
def packetize(payload, apid, packetType=False, timestamp=False, pfield=False, encrypt=False, enckey=False):
    if not hasattr(packetize, "i"):
        packetize.i = 0xFE
    length = len(payload)
    if timestamp:
        length += LENGTH_OF_TIMESTAMP
        if pfield:
            length += LENGTH_OF_PFIELD
    #constants
    SECOND_HEADER_FLAG = 0xF7FF

    #initialize packet blocks of 2 bytes each
    header0 = 0x0000
    header1 = 0x0000
    header2 = 0x0000
    #header0 contains bits 0-15 of the packet which include:
        #packet Version Number(3 bits)
        #packet Type(1 bit)
        #second Header Flag(1 bit)
        #Aip Process ID(APID)(11 bits)
    #header1 contains bits 16-31 of the packet which include:
        #Sequence Flags(2 bits)
        #Packet Sequence Count(14 bits)
    #header2 contains bits 32-45 of the packet which include:
        #Packet Data Length(16 bits)

    if packetType: #0 for TM or 1 for TC
        header0 |= 0x1000 #set bit 0 of the packet to value:1 to make the packet TC
    header0 |= apid #add in APID(11 bits) into header0
    header0 &= SECOND_HEADER_FLAG #second header flag force flag low placed after APID just in case apid was 1 bit longer than it should have been

    header1 = 0xC000 | (packetize.i+1) #set bits 0-1 of header1 (Sequence Flags)

    if timestamp: #will only be true if including a second header(optional)
        header0 |= 0x0800 #set the second Header Flag to True
        timestamp = int(time.time())
        if pfield:
            pfield = 0x2C
    if encrypt == 0:
        payload_str = payload
        length = len(payload_str)
        header2 = length
    elif encrypt == 1:
        #Encrypt the payload here
        enc = AES.new(enckey, AES.MODE_ECB)
        payload_str = payload
        add_char = 16 - (len(payload_str) % 16)
        print("CP: ", len(payload_str), add_char)
        payload_str += bytearray(add_char)
        print("CP: ", len(payload_str))
        ciphertext = enc.encrypt(payload_str)
        length = len(ciphertext)
        payload_str = ciphertext
        header2 = length

    if timestamp: #packet contains second header bytes so length is different
        if pfield:
            packet = pack('!HHHBL%ds' % (length - (LENGTH_OF_TIMESTAMP + LENGTH_OF_PFIELD)), header0, header1, header2, pfield, timestamp, payload_str)
        else: #packet contains timestamp but no pfield bytes
            packet = pack('!HHHL%ds' % (length - LENGTH_OF_TIMESTAMP), header0, header1, header2, timestamp, payload_str)
    else:
        packet = pack('!HHH%ds' % (length), header0, header1, header2, payload_str) #HHH refers to the 3 blocks of 2 bytes each that are being packed(header0-2)
        #header0, header1, length = unpack('!HHH', packet[:6])

    return packet

#######################################################################################################################################
#######################################################################################################################################

class create_packet(gr.basic_block):

    #   Block create_packet
    #     Take incoming data stream and chop it into specified length (PAYLOAD_LENGTH)
    #     then create packet around payload

    #Constants
    _out_port = pmt.intern("out")
    _in_port = pmt.intern("in")
    MAX_SIZE_OF_QUEUE = 1000
    MAX_TIMEOUT_DELAY = 5

    MAX_VALID_APID_VALUE = 2047
    DEFAULT_APID_VALUE = 2000
    MIN_VALID_APID_VALUE = 0

    #SPP_PACKET_EXAMPLE = SPP_Packet(DEFAULT_APID_VALUE, bytes)
    #size_of_payload = utf8len(SPP_PACKET_EXAMPLE.payload) #we want this to be the maximum
    #size_of_packet = sys.getsizeof(SPP_PACKET_EXAMPLE.packet)
    #PAYLOAD_LENGTH = SPP_PACKET_EXAMPLE.length
    # variables
    apid = 0
    packetType = 0
    encrypt = 0
    enckey = False
    timestamp = 0
    pfield = 0
    payload = 0
    data_queue = queue.Queue(MAX_SIZE_OF_QUEUE)

    def __init__(self,apid,packetType,encrypt,enckey):
        gr.basic_block.__init__(self,
            name="create_packet",in_sig = [], out_sig = [])
            # Put this into the constructor to create message ports
            #in_sig = [numpy.int8],#,self.size_of_payload)],
            #out_sig = [])

        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages

        #Initialize variables
        self.apid = apid
        if self.apid > self.MAX_VALID_APID_VALUE or self.apid < self.MIN_VALID_APID_VALUE:
            print("CP: ERROR - Invalid APID value and using default value: 2000\n")
            self.apid = self.DEFAULT_APID_VALUE
        if packetType != 0 and packetType != 1:
            print("CP: ERROR - Invalid packetType and efaulting to type 0\n")
            self.packetType = 0
        else:
            self.packetType = packetType
        if encrypt != 0 and encrypt != 1:
            print("CP: ERROR - Invalid encryption mode and defaulting to no encryption (type 0)\n")
            self.encrypt = 0
        else:
            self.encrypt = encrypt
        if not enckey:
            print("CP: Error - Invalid encryption key and defaulting to default key: TEMPORARYKEY\n")
            self.enckey = "TEMPORARYKEY"
        else:
            self.enckey = enckey
        self.timestamp = 0
        DEFAULT_MSGQ_LIMIT = 10
        self.pfield = 0
        print("CP: Create Packet Initialized")

    def msg_handler_method(self, msg):
        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
            self.data_queue.put(msg_str,False)
        elif pmt.is_pair(msg):
            msg_cdr = pmt.cdr(msg)
            #Take this vector to bytes...
            msg_str = pmt.to_python(msg_cdr).tobytes()
            self.data_queue.put(msg_str,False)
        else:
            print("CP: Received wrong input type\n")
        self.payload = msg_str
        #while not(self.data_queue.empty()):
            #try:
            #self.payload = self.data_queue.get(False)
            #print("CP: Payload length is ",len(self.payload),"\n")
        packet =  packetize(self.payload,self.apid,self.packetType,self.timestamp,self.pfield,self.encrypt,self.enckey) #creates the packet
            #print("CP: DEBUG - The packets type is " + str(type(packet)))
            #print("CP: DEBUG - Packet Contents is: " + str(map(hex, bytearray(packet))))
        out_packet = pmt.init_u8vector(len(packet), packet);
        deliver_current_packet = pmt.cons(pmt.to_pmt(None),out_packet)
        self.message_port_pub(self._out_port, deliver_current_packet)
        print("CP: Packet created and sent")
            #except:
            #    print("CP: ERROR - Exception in message handler\n")

    def general_work(self, input_items, output_items):
        print("CP:general Work ever called?\n")
        return  len(output_items)


