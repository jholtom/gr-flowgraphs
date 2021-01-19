from gnuradio import gr
import sys
import os
import pmt
from pmt import *
from pmt import pmt_to_python



class reed_solomon(gr.basic_block):

    # Constants:
    _in_port = pmt.intern("in")
    _out_port = pmt.intern("out")


    def __init__(self):
        gr.basic_block.__init__(self,
            name="reed_solomon",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(self._in_port) #this creates the input port for the messages
        self.set_msg_handler(self._in_port, self.msg_handler_method) #this determines what is done with any recieved messages as soon as they are recieved
        self.message_port_register_out(self._out_port) #this creates the output port for messages

        self.frame = "" #this will be recieved in a stream
        self.contents = "" #this will be output in a message
        print("RZ: Reed Solomon Initialized")


    def msg_handler_method(self, msg):
        if pmt.is_symbol(msg):
            msg_str = str(pmt.symbol_to_string(msg)) #changes the data back into usable data
            self.data = msg_str
        elif pmt.is_pair(msg):
            incoming_dict = pmt.car(msg)
            incoming_data = pmt.cdr(msg)
            self.data = pmt.to_python(incoming_data).tobytes()
            f = open('/home/spacecraft/RS/received_data.bin', 'wb')
            f.write(self.data)
            f.close()
            # os.system("/home/spacecraft/radioCode/derand /home/spacecraft/RS/received_data.bin /home/spacecraft/RS/derand_data.bin")
            # os.system("/home/spacecraft/radioCode/deint /home/spacecraft/RS/derand_data.bin /home/spacecraft/RS/deint_data.bin")
            os.system("/home/spacecraft/cygnus/gr-RS/decode /home/spacecraft/RS/received_data.bin /home/spacecraft/RS/decoded_data.bin")
        else:
            print("RZ: Error - Wrong type came through message")
        frame = open('/home/spacecraft/RS/decoded_data.bin', 'rb').read()
        out_frame = pmt.init_u8vector(len(frame), frame)
        deliver_frame = pmt.cons(pmt.to_pmt(None), out_frame)
        self.message_port_pub(self._out_port, deliver_frame)






    def general_work(self, input_items, output_items):
        return len(output_items)

