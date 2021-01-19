"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
from pmt import *
from pmt import pmt_to_python

def str_to_bits(data):
    out_data = list()
    for i in range(len(data)):
        out_data.append(int(data[i]))
    return out_data

class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    _in_port = pmt.intern("in")
    _out_port = pmt.intern("out")

    def __init__(self, frame_size=2040, access_code='00011010110011111111110000011011', threshold=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Detect Packet',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.frame_size = frame_size
        self.access_code = str_to_bits(access_code)
        self.threshold = threshold
        
        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages
        
    def find_access_code(self):
        ac_len = len(self.access_code)
        found = False
        i = 0
        while len(self.data[i:]) >= ac_len:
            wrong = 0
            j = 0
            while wrong < self.threshold:
                if self.data[i+j] != self.access_code[j]:
                    wrong += 1
                j += 1
                if j == ac_len:
                    print("Detect Packet: Found access code, extracting packet")
                    self.extract_packet(i+ac_len)
                    return
            i += 1
                
    def extract_packet(self, idx):
        self.packet.clear()
        if len(self.data[idx:])/8 < self.frame_size:
            print("Detect Packet: Not enough data for frame size")
        for i in range(self.frame_size):
            sum = 0
            for j in range(8):
                sum += self.data[idx+8*i+j] << (7-j)
            self.packet.append(sum)
        
    def msg_handler_method(self, msg):
        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
            self.data = msg_str
        elif pmt.is_pair(msg):
            incoming_dict = pmt.car(msg)
            incoming_data = pmt.cdr(msg)
            self.data = pmt.to_python(incoming_data).tobytes()
            self.packet = list()
            self.find_access_code()
            if len(self.packet) > 0:
                out_msg = pmt.init_u8vector(len(self.packet), self.packet)
                deliver_msg = pmt.cons(pmt.to_pmt(None), out_msg)
                self.message_port_pub(self._out_port, deliver_msg)

    def general_work(self, input_items, output_items):
        print("Detect Packet: general_work called?")
        return len(output_items[0])
