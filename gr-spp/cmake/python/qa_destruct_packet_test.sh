#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/jacob/cygnus/gnuradio/gr-spp/python
export PATH=/home/jacob/cygnus/gnuradio/gr-spp/cmake/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/jacob/cygnus/gnuradio/gr-spp/cmake/swig:$PYTHONPATH
/usr/bin/python2 /home/jacob/cygnus/gnuradio/gr-spp/python/qa_destruct_packet.py 
