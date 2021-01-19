/* -*- c++ -*- */

#define MDR_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "mdr_swig_doc.i"

%{
#include "mdr/mdrfLL.h"
%}

%include "mdr/mdrfLL.h"
GR_SWIG_BLOCK_MAGIC2(mdr, mdrfLL);
