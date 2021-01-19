#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/spacecraft/cygnus/gnuradio/gr-spp/python
export PATH=/home/spacecraft/cygnus/gnuradio/gr-spp/python/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/spacecraft/cygnus/gnuradio/gr-spp/python/swig:$PYTHONPATH
/usr/bin/python2 /home/spacecraft/cygnus/gnuradio/gr-spp/python/qa_destruct_packet.py 
