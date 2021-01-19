#!/usr/bin/env python

from gnuradio import gr;
from gnuradio import gru;
import pmt, array

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

class preamble_insert(gr.sync_block):
    def __init__(self, preamble):
        gr.sync_block.__init__(self,"unpacker",[],[])
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("in"), self.handler);
        self.preamble = preamble.to_bytes(4, 'big');

    def handler(self, msg):
        meta = pmt.car(msg);
        data_in = pmt.cdr(msg);
        data = pmt.to_python(data_in).tobytes()
        fives = 0x5555555555555555
        fives = fives.to_bytes(8, 'big')
        #data = array.array('B', pmt.u8vector_elements(data_in))
        pre_data = fives + self.preamble + data;
        #usrp_packing = (_npadding_bytes(len(pre_pre_data),8,1) * '\x55').encode('ascii');
        #pre_data = pre_pre_data + usrp_packing;
#        print pre_data[:100];
        #burst_bits = pmt.to_pmt(pre_data);
        burst_bits = pmt.init_u8vector(len(pre_data), pre_data);
        pdu = pmt.cons(pmt.to_pmt(None), burst_bits);
        self.message_port_pub(pmt.intern("out"), pdu);
    
    def work(self, input_items, output_items):
        pass

