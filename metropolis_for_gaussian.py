# ================================================================
# Monte Carlo sampling from a Gaussian distribution
# using the Metropolis algorithm
#
# Here we want to GENERATE NUMBERS DISTRIBUITED
#  with a specific distribution
# in this case a Gaussian
#
#
# I suggest to read this to remember the basi steps
# if the Metropolis
#
# ================================================================

import pylab
import math
import random
import numpy

# ------------------------------------------------
# 1. Parameters of the target Gaussian distribution
# ------------------------------------------------

# Number of Monte Carlo steps
nstat = 10000

# Initial value of the Markov chain
start = 0.0

# Mean (center) of the Gaussian distribution
aver = 5.0

# Variance of the Gaussian distribution
sigma2 = 1.0

# Maximum size of the proposed step
delta = 0.8

# At each iteration, the algorithm proposes a new value
# in the interval:
#
#       q - delta <= qtry <= q + delta
#
# A larger delta means larger proposed moves.
#
# Note: using a delta similar to sigma reduce the thermalization time


# ------------------------------------------------
# 2. Create the output file
# ------------------------------------------------

# Open the file in write mode.
# This erases any previous content.
scrivi = open("gauss.txt", "w")
scrivi.close()

# Re-open the file in append mode.
# We will add one line for each Monte Carlo iteration.
scrivi = open("gauss.txt", "a")


# ------------------------------------------------
# 3. Initialize the random number generator
# ------------------------------------------------

# Initialize the pseudo-random number generator.
# Here no seed is explicitly specified

random.seed()
# Note: that given a seed the sequence of "random"
#is fixed

# ------------------------------------------------
# 4. Initialize the Markov chain
# ------------------------------------------------

# q is the current position of the Markov chain.
#
# We start from q = 0
q = start


# ------------------------------------------------
# 5. Metropolis Monte Carlo loop
# ------------------------------------------------

for i in range(0, nstat):

    # ------------------------------------------------
    # Generate two random numbers uniformly distributed
    # between 0 and 1.
    # ------------------------------------------------

    x = random.random()
    y = random.random()


    # ------------------------------------------------
    # Propose a new value of q
    # ------------------------------------------------

    # The quantity (1 - 2*x) is uniformly distributed
    # between -1 and +1.
    #
    # Therefore:
    #
    #       delta * (1 - 2*x)
    #
    # is uniformly distributed between -delta and +delta.
    #
    # The proposed value is therefore:
    #
    #       qtry = q + random_step
    #
    # This is called the "proposal" in the Metropolis algorithm.

    qtry = q + delta * (1.0 - 2.0 * x)


    # ------------------------------------------------
    # Calculate the Metropolis acceptance probability
    # ------------------------------------------------

    # The target probability distribution is Gaussian:
    #
    #
    #
    # P(q) ~ exp[-(q- mu)^2/(2 sigma^2)]
    #
    #
    # where:
    #
    #     mu     = aver
    #     sigma2 = variance
    #
    # The ratio between the probability of the proposed
    # state and the current state is:
    #
    #
    # z =  P(qtry)/ P(q)
    #
    #
    # The normalization constant of the Gaussian cancels
    # out in this ratio.
    #


    z = math.exp(
        (q - aver)**2 / (2.0 * sigma2)
        - (qtry - aver)**2 / (2.0 * sigma2)
    )


    # ------------------------------------------------
    # Accept or reject the proposed value
    # ------------------------------------------------

    # y is a random number uniformly distributed between
    # 0 and 1.
    #
    # If y < z, we accept the proposed value.
    #
    #
    # This means that, (for z < 1),  the proposal is accepted with
    # probability z.
    #
    #
    # Note: if z >= 1, the proposal is always accepted because
    # y is necessarily smaller than 1.
    #
    #
    #
    # If the proposal is rejected, q keeps its old value.

    if y < z:
        q = qtry


    # ------------------------------------------------
    # Save the current state of the Markov chain
    # ------------------------------------------------

    # Each line contains:
    #
    #     iteration_number    current_value_of_q
    #
    # This allows us to study the evolution of the chain
    # after the simulation has finished.

    scrivi.write(str(i))
    scrivi.write(" ")
    scrivi.write(str(q))
    scrivi.write("\n")


# ------------------------------------------------
# 6. Close the output file
# ------------------------------------------------

scrivi.close()

##plot
# ================================================================
# 7. Plot the Monte Carlo chain trajectory
# ================================================================


# x = iteration number
# y = value of q

x, y = pylab.loadtxt("gauss.txt", unpack=True)


# Plot q as a function of the iteration number.
#
# This plot shows the trajectory of the Markov chain.
# It does NOT directly show the Gaussian probability
# distribution.

pylab.plot(x, y, marker='.')

pylab.show()

# ================================================================
# IMPORTANT Tell python to crate a new figure
# needed to create another plot at the same time
# I have experienced that in some environment, this is the
# only way to create more then one plot


pylab.figure()
# ================================================================



# ================================================================
# 7. Plot the Distribution
# ================================================================

therm=1000

pylab.hist(y[therm:], bins=80, density=True)

# y[1000:] means to start from the 10001, we are cutting off the thermalization
#density true means normalized, bins= in how many part the interval is divided

# Create x values for the theoretical Gaussian
xx = numpy.linspace(aver-4*sigma2, aver+4*sigma2, 500)

# Gaussian probability density
gaussian = (1.0 / numpy.sqrt(2.0 * numpy.pi * sigma2)) * \
           numpy.exp(-(xx - aver)**2 / (2.0 * sigma2))

# Plot the theoretical distribution
pylab.plot(xx, gaussian, 'r-', linewidth=2,
           label="Theoretical Gaussian")


# Show all the plots
pylab.show()

