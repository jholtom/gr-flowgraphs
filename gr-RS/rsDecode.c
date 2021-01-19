#include <stdio.h>
#include <stdint.h>
//#include "rs_decoder.h"
#include <string.h>

#define mm  8           /* RS code over GF(2**8) - change to suit */
#define nn  255          /* nn=2**mm -1   length of codeword */
#define tt  16           /* number of errors that can be corrected */
#define kk  223           /* kk = nn-2*tt  */
#define ii  8           /* Interleaving depth*/
#define SDLP_TM_MAX_TF_LEN_RS 2040
static const uint8_t sequence[nn*ii] = {255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88,255,72,14,192,154,13,112,188,142,44,147,173,167,183,70,206,90,151,125,204,50,162,191,62,10,16,241,136,148,205,234,177,254,144,29,129,52,26,225,121,28,89,39,91,79,110,141,156,181,46,251,152,101,69,126,124,20,33,227,17,41,155,213,99,253,32,59,2,104,53,194,242,56,178,78,182,158,221,27,57,106,93,247,48,202,138,252,248,40,67,198,34,83,55,170,199,250,64,118,4,208,107,133,228,113,100,157,109,61,186,54,114,212,187,238,97,149,21,249,240,80,135,140,68,166,111,85,143,244,128,236,9,160,215,11,200,226,201,58,218,123,116,108,229,169,119,220,195,42,43,243,224,161,15,24,137,76,222,171,31,233,1,216,19,65,174,23,145,197,146,117,180,246,232,217,203,82,239,185,134,84,87,231,193,66,30,49,18,153,189,86,63,210,3,176,38,131,92,47,35,139,36,235,105,237,209,179,150,165,223,115,12,168,175,207,130,132,60,98,37,51,122,172,127,164,7,96,77,6,184,94,71,22,73,214,211,219,163,103,45,75,190,230,25,81,95,159,5,8,120,196,74,102,245,88};

static const uint8_t alpha_to [nn+1] = {1,2,4,8,16,32,64,128,195,69,138,215,109,218,119,238,31,62,124,248,51,102,204,91,182,175,157,249,49,98,196,75,150,239,29,58,116,232,19,38,76,152,243,37,74,148,235,21,42,84,168,147,229,9,18,36,72,144,227,5,10,20,40,80,160,131,197,73,146,231,13,26,52,104,208,99,198,79,158,255,61,122,244,43,86,172,155,245,41,82,164,139,213,105,210,103,206,95,190,191,189,185,177,161,129,193,65,130,199,77,154,247,45,90,180,171,149,233,17,34,68,136,211,101,202,87,174,159,253,57,114,228,11,22,44,88,176,163,133,201,81,162,135,205,89,178,167,141,217,113,226,7,14,28,56,112,224,3,6,12,24,48,96,192,67,134,207,93,186,183,173,153,241,33,66,132,203,85,170,151,237,25,50,100,200,83,166,143,221,121,242,39,78,156,251,53,106,212,107,214,111,222,127,254,63,126,252,59,118,236,27,54,108,216,115,230,15,30,60,120,240,35,70,140,219,117,234,23,46,92,184,179,165,137,209,97,194,71,142,223,125,250,55,110,220,123,246,47,94,188,187,181,169,145,225,0};

static const int16_t index_of [nn+1] = {-1,0,1,157,2,59,158,151,3,53,60,132,159,70,152,216,4,118,54,38,61,47,133,227,160,181,71,210,153,34,217,16,5,173,119,221,55,43,39,191,62,88,48,83,134,112,228,247,161,28,182,20,72,195,211,242,154,129,35,207,218,80,17,204,6,106,174,164,120,9,222,237,56,67,44,31,40,109,192,77,63,140,89,185,49,177,84,125,135,144,113,23,229,167,248,97,162,235,29,75,183,123,21,95,73,93,196,198,212,12,243,200,155,149,130,214,36,225,208,14,219,189,81,245,18,240,205,202,7,104,107,65,175,138,165,142,121,233,10,91,223,147,238,187,57,253,68,51,45,116,32,179,41,171,110,86,193,26,78,127,64,103,141,137,90,232,186,146,50,252,178,115,85,170,126,25,136,102,145,231,114,251,24,169,230,101,168,250,249,100,98,99,163,105,236,8,30,66,76,108,184,139,124,176,22,143,96,166,74,234,94,122,197,92,199,11,213,148,13,224,244,188,201,239,156,254,150,58,131,52,215,69,37,117,226,46,209,180,15,33,220,172,190,42,82,87,246,111,19,27,241,194,206,128,203,79};

static const uint8_t gg [nn-kk+1] = {18,8,217,200,128,88,229,37,157,182,181,103,220,158,213,147,117,114,147,59,88,193,238,206,148,250,154,235,242,26,10,23,0};

//randomize data
static void ccsds_xor_sequence(uint8_t *data, const uint8_t *sequence, int16_t length)
{
    int16_t i;

    for (i = 0; i < length; i++)
        data[i] ^= sequence[i];
}

static void decode_rs(int16_t recd[nn]){
    /* assume we have received bits grouped into mm-bit symbols in recd[i],
     i=0..(nn-1),  and recd[i] is index form (ie as powers of alpha).
     We first compute the 2*tt syndromes by substituting alpha**i into rec(X) and
     evaluating, storing the syndromes in s[i], i=1..2tt (leave s[0] zero) .
     Then we use the Berlekamp iteration to find the error location polynomial
     elp[i].   If the degree of the elp is >tt, we cannot correct all the errors
     and hence just put out the information symbols uncorrected. If the degree of
     elp is <=tt, we substitute alpha**i , i=1..n into the elp to get the roots,
     hence the inverse roots, the error location numbers. If the number of errors
     located does not equal the degree of the elp, we have more than tt errors
     and cannot correct them.  Otherwise, we then solve for the error value at
     the error location and correct the error.  The procedure is that found in
     Lin and Costello. For the cases where the number of errors is known to be too
     large to correct, the information symbols as received are output (the
     advantage of systematic encoding is that hopefully some of the information
     symbols will be okay and that if we are in luck, the errors are in the
     parity part of the transmitted codeword).  Of course, these insoluble cases
     can be returned as error flags to the calling routine if desired.   */

    register int16_t i,j,u,q ;
    int16_t elp[nn-kk+2][nn-kk], d[nn-kk+2], l[nn-kk+2], u_lu[nn-kk+2], s[nn-kk+1] ;
    int16_t count=0, syn_error=0, root[tt], loc[tt], z[tt+1], err[nn], reg[tt+1] ;
    //swap recd order
    int16_t temp[nn];
    for (uint16_t i = 0; i < nn; i++){
        temp[i] = recd[i];
    }
    for (uint8_t i = 0; i < (nn-kk); i++){
        recd[i] = temp[i+kk];
    }
    for (uint8_t i = 0; i < kk; i++){
        recd[i+(nn-kk)] = temp[i];
    }


    /* first form the syndromes */
    for (i=1; i<=nn-kk; i++)
    { s[i] = 0 ;
        for (j=0; j<nn; j++)
            if (recd[j]!=-1)
                s[i] ^= alpha_to[(recd[j]+i*j)%nn] ;      /* recd[j] in index form */
        /* convert syndrome from polynomial form to index form  */
        if (s[i]!=0)  syn_error=1 ;        /* set flag if non-zero syndrome => error */
        s[i] = index_of[s[i]] ;
    } ;

    if (syn_error)       /* if errors, try and correct */
    {
        /* compute the error location polynomial via the Berlekamp iterative algorithm,
         following the terminology of Lin and Costello :   d[u] is the 'mu'th
         discrepancy, where u='mu'+1 and 'mu' (the Greek letter!) is the step number
         ranging from -1 to 2*tt (see L&C),  l[u] is the
         degree of the elp at that step, and u_l[u] is the difference between the
         step number and the degree of the elp.
         */
        /* initialise table entries */
        d[0] = 0 ;           /* index form */
        d[1] = s[1] ;        /* index form */
        elp[0][0] = 0 ;      /* index form */
        elp[1][0] = 1 ;      /* polynomial form */
        for (i=1; i<nn-kk; i++)
        { elp[0][i] = -1 ;   /* index form */
            elp[1][i] = 0 ;   /* polynomial form */
        }
        l[0] = 0 ;
        l[1] = 0 ;
        u_lu[0] = -1 ;
        u_lu[1] = 0 ;
        u = 0 ;

        do
        {
            u++ ;
            if (d[u]==-1)
            { l[u+1] = l[u] ;
                for (i=0; i<=l[u]; i++)
                {  elp[u+1][i] = elp[u][i] ;
                    elp[u][i] = index_of[elp[u][i]] ;
                }
            }
            else
            /* search for words with greatest u_lu[q] for which d[q]!=0 */
            { q = u-1 ;
                while ((d[q]==-1) && (q>0)) q-- ;
                /* have found first non-zero d[q]  */
                if (q>0)
                { j=q ;
                    do
                    { j-- ;
                        if ((d[j]!=-1) && (u_lu[q]<u_lu[j]))
                            q = j ;
                    }while (j>0) ;
                } ;

                /* have now found q such that d[u]!=0 and u_lu[q] is maximum */
                /* store degree of new elp polynomial */
                if (l[u]>l[q]+u-q)  l[u+1] = l[u] ;
                else  l[u+1] = l[q]+u-q ;

                /* form new elp(x) */
                for (i=0; i<nn-kk; i++)    elp[u+1][i] = 0 ;
                for (i=0; i<=l[q]; i++)
                    if (elp[q][i]!=-1)
                        elp[u+1][i+u-q] = alpha_to[(d[u]+nn-d[q]+elp[q][i])%nn] ;
                for (i=0; i<=l[u]; i++)
                { elp[u+1][i] ^= elp[u][i] ;
                    elp[u][i] = index_of[elp[u][i]] ;  /*convert old elp value to index*/
                }
            }
            u_lu[u+1] = u-l[u+1] ;

            /* form (u+1)th discrepancy */
            if (u<nn-kk)    /* no discrepancy computed on last iteration */
            {
                if (s[u+1]!=-1)
                    d[u+1] = alpha_to[s[u+1]] ;
                else
                    d[u+1] = 0 ;
                for (i=1; i<=l[u+1]; i++)
                    if ((s[u+1-i]!=-1) && (elp[u+1][i]!=0))
                        d[u+1] ^= alpha_to[(s[u+1-i]+index_of[elp[u+1][i]])%nn] ;
                d[u+1] = index_of[d[u+1]] ;    /* put d[u+1] into index form */
            }
        } while ((u<nn-kk) && (l[u+1]<=tt)) ;

        u++ ;
        if (l[u]<=tt)         /* can correct error */
        {
            /* put elp into index form */
            for (i=0; i<=l[u]; i++)   elp[u][i] = index_of[elp[u][i]] ;

            /* find roots of the error location polynomial */
            for (i=1; i<=l[u]; i++)
                reg[i] = elp[u][i] ;
            count = 0 ;
            for (i=1; i<=nn; i++)
            {  q = 1 ;
                for (j=1; j<=l[u]; j++)
                    if (reg[j]!=-1)
                    { reg[j] = (reg[j]+j)%nn ;
                        q ^= alpha_to[reg[j]] ;
                    } ;
                if (!q)        /* store root and error location number indices */
                { root[count] = i;
                    loc[count] = nn-i ;
                    count++ ;
                };
            } ;
            if (count==l[u])    /* no. roots = degree of elp hence <= tt errors */
            {
                /* form polynomial z(x) */
                for (i=1; i<=l[u]; i++)        /* Z[0] = 1 always - do not need */
                { if ((s[i]!=-1) && (elp[u][i]!=-1))
                    z[i] = alpha_to[s[i]] ^ alpha_to[elp[u][i]] ;
                else if ((s[i]!=-1) && (elp[u][i]==-1))
                    z[i] = alpha_to[s[i]] ;
                else if ((s[i]==-1) && (elp[u][i]!=-1))
                    z[i] = alpha_to[elp[u][i]] ;
                else
                    z[i] = 0 ;
                    for (j=1; j<i; j++)
                        if ((s[j]!=-1) && (elp[u][i-j]!=-1))
                            z[i] ^= alpha_to[(elp[u][i-j] + s[j])%nn] ;
                    z[i] = index_of[z[i]] ;         /* put into index form */
                } ;

                /* evaluate errors at locations given by error location numbers loc[i] */
                for (i=0; i<nn; i++)
                { err[i] = 0 ;
                    if (recd[i]!=-1)        /* convert recd[] to polynomial form */
                        recd[i] = alpha_to[recd[i]] ;
                    else  {
                        recd[i] = 0 ;
                        //printf("here!");
                    }
                }
                for (i=0; i<l[u]; i++)    /* compute numerator of error term first */
                { err[loc[i]] = 1;       /* accounts for z[0] */
                    for (j=1; j<=l[u]; j++)
                        if (z[j]!=-1)
                            err[loc[i]] ^= alpha_to[(z[j]+j*root[i])%nn] ;
                    if (err[loc[i]]!=0)
                    { err[loc[i]] = index_of[err[loc[i]]] ;
                        q = 0 ;     /* form denominator of error term */
                        for (j=0; j<l[u]; j++)
                            if (j!=i)
                                q += index_of[1^alpha_to[(loc[j]+root[i])%nn]] ;
                        q = q % nn ;
                        err[loc[i]] = alpha_to[(err[loc[i]]-q+nn)%nn] ;
                        recd[loc[i]] ^= err[loc[i]] ;  /*recd[i] must be in polynomial form */
                    }
                }
            }
            else    /* no. roots != degree of elp => >tt errors and cannot solve */
                for (i=0; i<nn; i++)        /* could return error flag if desired */
                    if (recd[i]!=-1)        /* convert recd[] to polynomial form */
                        recd[i] = alpha_to[recd[i]] ;
                    else  {
                        recd[i] = 0 ;     /* just output received codeword as is */
                    }
        }
        else         /* elp has degree has degree >tt hence cannot solve */
            for (i=0; i<nn; i++)       /* could return error flag if desired */
                if (recd[i]!=-1)        /* convert recd[] to polynomial form */
                    recd[i] = alpha_to[recd[i]] ;
                else{
                    recd[i] = 0 ;     /* just output received codeword as is */
                    //printf("here!");
                }
    }
    else       /* no non-zero syndromes => no errors: output received codeword */
        for (i=0; i<nn; i++)
            if (recd[i]!=-1)        /* convert recd[] to polynomial form */
                recd[i] = alpha_to[recd[i]] ;
            else  {
                recd[i] = 0 ;
                //printf("here!");
            }
    //swap recd order
    for (uint16_t i = 0; i < nn; i++){
        temp[i] = recd[i];
    }
    for (uint8_t i = 0; i < kk; i++){
        recd[i] = temp[i+(nn-kk)];
    }
    for (uint8_t i = 0; i < (nn-kk) ; i++){
        recd[i+kk] = temp[i];
    }
}

static void seperate_data_parity_unleave(uint8_t tf_buffer[2040], uint8_t tf_buffer_deinterleave[2040]){
    /* put the transmitted codeword, made up of data plus parity, in recd[] */
    //parity bits and then message
    uint16_t j = 0;
    for (uint8_t q = 0; q < ii; q++){
        for (uint16_t i=q; i< (nn) * ii; i+= ii){
            tf_buffer_deinterleave[j] = tf_buffer[i]; // how to seperate data? probaly just data bits next to eachother
            j++;
        }
    }
}

void derandomize_deinterleave_decode_rs(uint8_t tf_buffer[2040],uint8_t data_final[kk*ii]){
    //deradomize the data before decoding
    ccsds_xor_sequence(tf_buffer, sequence, (nn+1)*ii);

    //unleave the data so they are in sequential codeblocks
    uint8_t tf_buffer_deinterleave[2040];
    seperate_data_parity_unleave(tf_buffer,tf_buffer_deinterleave);

    FILE *inter = fopen("/home/spacecraft/RS/deint_data.bin", "wb");
    fwrite(tf_buffer_deinterleave, sizeof(uint8_t), sizeof(tf_buffer_deinterleave), inter);
    fclose(inter);


    //Decode each codeblock seperately
    int16_t recd[nn];
    for (uint8_t j = 0; j < ii; j++ ){
        for (uint8_t i=0; i<nn; i++){
            recd[i] = index_of[tf_buffer_deinterleave[i+(nn)*j]] ;/* put recd[i] into index form */
        }
        decode_rs(recd) ;         /* recd[] is returned in polynomial form */
        for (uint8_t i=0; i<nn; i++){
            tf_buffer_deinterleave[i+(nn)*j] = recd[i];
        }
        for (uint8_t i=0; i<kk; i++){    //copy the final data to datafinal
            data_final[i+(kk)*j] = recd[i]; // i + 32?
        }
    }
}

int main(){
    FILE *dataIn;
    dataIn = fopen("/home/spacecraft/RS/received_data.bin", "rb");
    uint8_t tf_buffer[SDLP_TM_MAX_TF_LEN_RS] = {0};
    for(uint32_t i=0; i<SDLP_TM_MAX_TF_LEN_RS; i++){
        fread(&tf_buffer[i], sizeof(uint8_t), 1, dataIn);
    }
    uint8_t data_output[kk*ii] = {0};
    derandomize_deinterleave_decode_rs(tf_buffer, data_output);
    FILE *f = fopen("/home/spacecraft/RS/decoded_data.bin", "wb");
    fwrite(data_output, sizeof(uint8_t), sizeof(data_output), f);
    fclose(f);
    return 0;
}
