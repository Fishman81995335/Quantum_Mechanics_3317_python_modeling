# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import IPython.display as d

# <codecell>

from pylab import real,imag,array,log10

# <codecell>

def mattohtml(ar1,tol=10**-5):
    """mat to html generates html code to display a matrix ar.  It works on matrices of both real and complex
    numbers.  If you have a sparse array, you need to convert it into dense form first.  It takes a second
    optional argument -- "tol".  Any entries smaller than tol are truncated"""
    ar=array(ar1) # convert to array
    # The html string will be stored as st
    st="""<div style="max-width:1000px;max-height:400px;border:1px solid #ccc;font:9px/11px  Courier, monospace;overflow:auto;"><table>"""
    for row in ar:
        st+="<tr>" # add new row in html table
        for element in row:
            st+="<td>" # add new element to html table
            st+=numform(element,tol) # add number to table
            st+="</td>"
        st+="</tr>"
    st+="</table>"
    return st

# <codecell>

def numform(element,tol):
            """numform returns a string representing num -- the string is blank if |num|<tol"""
            st=""
            reelement=real(element)
            imelement=imag(element)
            if abs(reelement)<tol: # don't print the real part
                if abs(imelement)>tol: # print the imag part
                    st+=inumform(imelement)
                    st+="i"
            elif abs(imag(element))<tol: # print real but not imag
                st+=rnumform(reelement)
            else:                       # print both
                st+=rnumform(reelement)
                if imelement>0:
                    st+="+"
                else:
                    st+="-"
                    imelement=-imelement
                st+=inumform(imelement)
                st+="i"
            return st

# <codecell>

def inumform(num):
    st=""
    if abs(num)<999 and abs(num)>0.01:
        if round(100*num)%100==0:
            st+="%.0f"%num
        elif round(100*num)%10==0:
            st+="%.1f"%num
        else:
            st+="%.2f"%num
    else:
        exp=int(log10(abs(num)))
        mant=int(10*(num/10**exp))/10.
        st+="("
        st+="$%.1f"%mant
        st+=r"\cdot10^{"
        st+=str(exp)
        st+=r"}$"
        st+=")"
        #st+="(%.1e)"%num
    return st

# <codecell>

def rnumform(num):
    st=""
    if abs(num)<999 and abs(num)>0.01:
        if round(100*num)%100==0:
            st+="%.0f"%num
        elif round(100*num)%10==0:
            st+="%.1f"%num
        else:
            st+="%.2f"%num
    else:
        exp=int(log10(abs(num)))
        mant=int(10*(num/10**exp))/10.
        st+="$%.1f"%mant
        st+=r"\cdot10^{"
        st+=str(exp)
        st+=r"}$"
        #st+="%.1e"%num
    return st

# <codecell>

def showmat(ar,tol=10**-5):
    """showmat formats a matrix ar for display in a jupyter notebook.  
        It works on matrices of both real and complex
        numbers.  If you have a sparse array, it converts it into dense form first.  It takes a second
        optional argument -- "tol".  Any entries smaller than tol are truncated"""
    try:
        ar=ar.todense()
    except:
        pass
    return d.HTML(mattohtml(array(ar),tol))

