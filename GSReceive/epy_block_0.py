"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import struct
import scipy.signal


class blk(gr.basic_block):
    """GMSK Packet Decoder
    
    Looks for tags from power squelch to know where packets start and end.
    """
    _out_port = pmt.intern("out")
    packetNum = 1
    packet = []
    packetStarted = False


    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='mdr GMSK Packet Demod',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[]
        )
        self.message_port_register_out(self._out_port)
    
    def mdrBitSync(self,y):
        N1 = 8
        g = np.multiply(1/N1,np.ones((N1,1)))
        Kp = 8.7
        N2 = 2
        K0 = -1
    
        BnT = 0.02
        zeta = 1
        temp = BnT/(zeta + 0.25/zeta)
        d = 1 + 2*zeta/N2 * temp + (temp/N2)**2
        K1 = 4*zeta/N2 * temp / d
        K2 = (2/N2 * temp)**2 / d
        K1 = K1/(K0*Kp)
        K2 = K2/(K0*Kp)

        b0 = (K1 + K2)
        b1 = -K1

        # apply matched filter and downsample to 2 samples/bit
        xx = scipy.signal.decimate(y,4);
    
        # create output vector
        b = np.zeros(int(0.52*len(xx)))
        k = 0
    
        # initialize PLL states
        NCO1 = 0
        W1 = 0
        Vt1 = 0
        Et1 = 0
        MU1 = 0
    
        F1 = 0
        F2 = 0
        F3 = 0
        F4 = 0
        F5 = 0
        F6 = 0
        F7 = 0
        F8 = 0
        F9 = 0
        
        for idx in range(len(xx)):
            # check for underflow
            # if underflow, strobe = 1 compute new mu
            
            temp = NCO1 - W1
            if temp < 0:
                strobe = 1
                mu = NCO1/W1
                nco = 1 + temp
            else:
                strobe = 0
                mu = MU1
                nco = temp
            
            # if strobe, compute timing error and produce output
        
            if strobe == 0:
                et = 0
            else:
                # calculate xi(idx)
                tempFx = -0.5*xx[idx]
                v2 = -tempFx + F1 + F2 - F3
                v1 = tempFx - F1 + F6 + F2 + F3
                v0 = F7
                xi = (v2 * mu + v1) * mu + v0
            
                # calculate xi(idx-1)
                v2 = -F1 + F2 + F3 - F4
                v1 = F1 - F2 + F7 + F3 + F4
                v0 = F8
                xi1 = (v2 * mu + v1) * mu + v0
        
                # calculate xi(idx-2)
                v2 = -F2 + F3 + F4 - F5
                v1 = F2 - F3 + F8 + F4 + F5
                v0 = F9
                xi2 = (v2 * mu + v1) * mu + v0
        
                et = np.sign(xi1) * (xi - xi2)
          
                b[k] = (xi1 > 0)
                k = k + 1      
            
            # update loop filter output
        
            vt = Vt1 + b0*et + b1*Et1
        
            # update NCO input
        
            w = vt + 0.5
        
            # update states
        
            F5 = F4
            F4 = F3
            F3 = F2
            F2 = F1
            F1 = -0.5*xx[idx]
            F9 = F8
            F8 = F7
            F7 = F6
            F6 = xx[idx]
        
            Et1 = et
            Vt1 = vt
        
            NCO1 = nco
            MU1 = mu
            W1 = w
        
        b = np.uint8(b[0:k-1])
        packet = pmt.init_u8vector(len(b),b.tolist())
        out_packet = pmt.cons(pmt.to_pmt(None),packet)
        self.message_port_pub(self._out_port,out_packet)
    
    def mdrDemod(self):
        x = np.array(self.packet)
        self.packet.clear()
        if len(x) < 100000:
            return
        d = np.array([1,0,-1])
        dx = np.convolve(d,x)
        y = np.float32(np.imag(np.conj(x)*dx[1:len(dx)-1]) / np.square(np.absolute(x)))
        self.mdrBitSync(y)
    
    def checkSob(self,offset,in_data):
        tags = self.get_tags_in_window(0, offset, len(in_data),pmt.intern('squelch_sob'))
        if len(tags) != 0:
            relIdx = tags[0].offset - self.nitems_read(0)
            self.packetStarted = True
            self.checkEob(relIdx,in_data)

    def checkEob(self,offset,in_data):
        tags = self.get_tags_in_window(0, offset, len(in_data),pmt.intern('squelch_eob'))
        if len(tags) == 0:
            self.packet.extend(in_data[offset:len(in_data)])
        else:
            relIdx = tags[0].offset - self.nitems_read(0)
            self.packet.extend(in_data[offset:relIdx])
            if len(self.packet) > 125000:
                self.mdrDemod()
                self.packetNum += 1
            else:
                self.packet.clear()
            self.packetStarted = False
            self.checkSob(relIdx+1,in_data)

    def general_work(self, input_items, output_items):
         in_data = input_items[0]
         
         if self.packetStarted:
             self.checkEob(0,in_data)
         else:
             self.checkSob(0,in_data)
         
         self.consume(0, len(in_data))
         
         return len(input_items[0])
