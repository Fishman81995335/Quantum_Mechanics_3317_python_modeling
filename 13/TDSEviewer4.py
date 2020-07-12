
# coding: utf-8

# In[1]:

import Tkinter


# In[ ]:

try:
    import Image, ImageTk, ImageDraw
except:
    import PIL
    import PIL.Image as Image
    import PIL.ImageTk as ImageTk
    import PIL.ImageDraw as ImageDraw


# In[ ]:

from pylab import *
from numpy import *


# In[3]:

#%gui tk


# In[ ]:

import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class TDSEviewer(FigureCanvasTkAgg):
    """ TDSEviewer is a class for viewing 1D wavefunctions and potentials. 
    
    The wavefunction is stored in TDSEviewer.wavefunction
    The potential is stored in TDSEviewer.potential

    To update the wavefunction (say setting it to "newwavefunction"), type
    viewer.wavefunction = newwavefunction
    viewer.updatelines()
    (The figure is only updated once the second line is called)

    To rescale axes use:
    viewer.xlim(xmin,xmax)
    viewer.ylim(ymin,ymax)

    To close the figure type:
    viewer.close()
    """
    def __init__(self, master=None,wavefunction=None,potential=None,showpotential=None,heightratio=3,grid=None):
        # if already have a root window (master) use it, otherwise create a new window
        if master is None:
            master=Tkinter.Tk()
        self.root=master
        
        self.kludge=1 # used to force redraw of figure axes
        
        # store input parameters
        self.wavefunction=wavefunction
        self.potential=potential
        self.heightratio=heightratio
        self.grid=grid
        
        
        # turn on potential showing if potential is given as an argument
        if showpotential is None:
            if self.potential is not None:
                self.showpotential=True
            else :
                self.showpotential=False
      
        # generate pylab figure
        fig = Figure() # generate figure object
        self.fig=fig   # store figure object for future reference
        gs=GridSpec(2,1,height_ratios=[self.heightratio,1]) # get figure geometry
        if self.showpotential :  # do we want two graphs?
            ax=fig.add_subplot(gs[0])
            potax=fig.add_subplot(gs[1])
            try :
                self.potlines, = potax.plot(self.grid,self.potential)
            except :
                self.potlines, = potax.plot(self.potential)
            potax.set_title("potential",va="top",color="red")
            self.potax=potax
        else:
            ax = fig.add_subplot(111)
        try:
            self.rewavefunctionlines, = ax.plot(self.grid,real(wavefunction))
            self.imwavefunctionlines, = ax.plot(self.grid,imag(wavefunction))
        except:
            self.rewavefunctionlines, = ax.plot(real(wavefunction))
            self.imwavefunctionlines, = ax.plot(imag(wavefunction))
        self.ax=ax # store pointer

        # add pylab figure to window
        FigureCanvasTkAgg.__init__(self,fig,master=master)
        self.canvas = self
        #self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        #frame.pack()
        #self.update()
        
    def force_redraw(self):
        # Change window size to force redraw
        # This should not be necessary
        # Somehow the tk dirty rectangle is not getting set right
        # -- this was unnecessary in older version
        w1=self.root.winfo_width()
        h1=self.root.winfo_height()
        self.root.geometry('{}x{}'.format(w1+self.kludge,h1+self.kludge))
        self.kludge=-self.kludge
        self.canvas.draw()
        
    def set_geometry(self,width=None,height=None):
        if width is None:
            width=self.root.winfo_width()
        if height is None:
            height=self.root.winfo_height()
        self.root.geometry('{}x{}'.format(width,height))
        self.canvas.draw
        
    def updatelines(self):
        """viewer.updatelines() redraws all of the lines"""
        if self.wavefunction is not None:
            self.rewavefunctionlines.set_ydata(real(self.wavefunction))
            self.imwavefunctionlines.set_ydata(imag(self.wavefunction))
            if self.grid is None:
                self.rewavefunctionlines.set_xdata(arange(len(self.wavefunction)))
                self.imwavefunctionlines.set_xdata(arange(len(self.wavefunction)))
            else:
                self.rewavefunctionlines.set_xdata(self.grid)
                self.imwavefunctionlines.set_xdata(self.grid)
        #self.force_redraw()
        
    def reset(self):
        """viewer.reset() redraws entire figure"""
        self.fig.clf() # clear figure
        gs=GridSpec(2,1,height_ratios=[self.heightratio,1]) # get figure geometry
        if self.showpotential :  # do we want two graphs?
            ax=self.fig.add_subplot(gs[0])
            potax=self.fig.add_subplot(gs[1])
            try:
                self.potlines, = potax.plot(self.grid,self.potential)
            except:
                self.potlines, = potax.plot(self.potential)
            potax.set_title("potential",va="top",color="red")
            self.potax=potax
        else:
            ax = self.fig.add_subplot(111)
        try:
            #print "trying"
            #print 1.*arange(len(self.wavefunction))*self.dx
            self.rewavefunctionlines, = ax.plot(self.grid,real(wavefunction))
            self.imwavefunctionlines, = ax.plot(self.grid,imag(wavefunction))
        except:
            #print "failed"
            self.rewavefunctionlines, = ax.plot(real(self.wavefunction))
            self.imwavefunctionlines, = ax.plot(imag(self.wavefunction))
        self.ax=ax # store pointer
    
    def xlim(self,min,max):
        """ viewer.xlim(min,max) rescales the x axis"""
        self.ax.set_xlim(min,max)
        
    def potxlim(self,min,max):
        """ viewer.potxlim(min,max) rescales the x axis for the potential"""
        self.potax.set_xlim(min,max)

    def ylim(self,min,max):
        """ viewer.ylim(min,max) rescales the y axis"""
        self.ax.set_ylim(min,max)
        
    def potylim(self,min,max):
        """ viewer.ylim(min,max) rescales the y axis for the potential"""
        self.potax.set_ylim(min,max)
        
    def rescale(self):
        """ viewer.rescale() zooms axes to be tight """
        xr, yr = self.rewavefunctionlines.get_data()
        xi, yi = self.imwavefunctionlines.get_data()
        maxy=max(max(yi),max(yr))
        miny=min(min(yi),min(yr))
        maxx=max(max(xi),max(xr))
        minx=min(min(xi),min(xr))
        self.xlim(minx,maxx)
        self.ylim(miny,maxy)

    def rescalepot(self):
        """ viewer.rescalepot() zooms axes to be tight """
        x, y = self.potlines.get_data()
        maxy=max(y)
        miny=min(y)
        maxx=max(x)
        minx=min(x)
        self.potxlim(minx,maxx)
        self.potylim(miny,maxy)
        #self.force_redraw()
        
    def set_title(self,title):
        """ viewer.set_title(title) sets the title"""
        self.root.wm_title(title)
        
    def close(self):
        self.root.destroy()


# In[169]:

#viewer=TDSEviewer(wavefunction=arange(10))


# In[163]:

#viewer.wavefunction=arange(10)**2+10j*arange(10)


# In[164]:

#viewer.updatelines()


# In[165]:

#viewer.rescale()


# In[166]:

#viewer.set_title("wf1")


# In[167]:

#viewer.ylim(0,100)


# In[168]:

#viewer.close()


# In[ ]:



