#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/spacecraft/cygnus/gnuradio/gr-usrp_pack/python
export PATH=/home/spacecraft/cygnus/gnuradio/gr-usrp_pack/python/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/spacecraft/cygnus/gnuradio/gr-usrp_pack/python/swig:$PYTHONPATH
/usr/bin/python2 /home/spacecraft/cygnus/gnuradio/gr-usrp_pack/python/qa_usrp_packer.py 
