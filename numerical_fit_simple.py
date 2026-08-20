# NUMERICAL FIT
# and residuals plot
#
#
# this script take the file nomefile.txt
# with columns x errox y errory
#
# usually the file must be in the same folder
# however you can simply write the complete path
#
#
#
# the function defined in ff is used for the fit
#
#
# curve_fit is the common minimization routine
# it easily block in local minima, so it's suggested a first attmept
# to find good initial parameter manually
#
#
#============================================================



# ------------------------------------------------------------
# LIBRERIE
# ------------------------------------------------------------

import pylab
import numpy
from scipy.optimize import curve_fit

# ============================================================



# data load
x,Dx,y,Dy=pylab.loadtxt(‘nomefile.txt', unpack=True )
#delimiter is ' ' by default for txt
#Another common file for data is .csv



# Syntax : x, Dx, y, Dy = pylab.loadtxt('nomefile.txt',unpack=True, delimiter=',')
# commons delimiters in the file : ' ', ',' , ';' , '\t' (tab)

# use subplots to display two plots in one figure
# note the syntax
pylab.subplot(2,1,2)

# scatter plot with error bars
pylab.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=18)
pylab.xlabel('$\Delta V$  [V]')
pylab.ylabel('$I$  [mA]')
pylab.minorticks_on()

# AT THE FIRST ATTEMPT COMMENT FROM HERE TO THE END

# define the function (linear, in this example)
def ff(x, aa, bb):
    return aa+bb*x

# define the initial values (STRICTLY NEEDED!!!)
init=(0,2)

# prepare a dummy xx array (with 2000 linearly spaced points)
xx=numpy.linspace(min(x),max(x),2000)

# plot the fitting curve computed with initial values
# AT THE SECOND ATTEMPT THE FOLLOWING LINE MUST BE COMMENTED
#pylab.plot(xx,ff(xx,*init), color='blue')

# set the error
sigma=Dy
w=1/sigma**2

# call the minimization routine
pars,covm=curve_fit(ff,x,y,init,sigma, absolute_sigma=False)

# calculate the chisquare for the best-fit function
chi2 = ((w*(y-ff(x,*pars))**2)).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print('pars:',pars)
print('covm:',covm)
print ('chi2, ndof:',chi2, ndof)

# plot the best fit curve
pylab.plot(xx,ff(xx,*pars), color='red')

# switch to the residual plot
pylab.subplot(2,1,1)

# build the array of the normalized residuals
r = (y-ff(x,*pars))/sigma

# bellurie
pylab.rc('font',size=18)
pylab.ylabel('Norm. res.')
pylab.minorticks_on()
# set the vertical range for the norm res
pylab.ylim((-.9,.9))

# plot residuals as a scatter plot with connecting dashed lines
pylab.plot(x,r,linestyle="--",color='blue',marker='o')


# show the plot
pylab.show()