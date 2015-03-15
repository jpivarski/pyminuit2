# PyMinuit2 #
_Minuit2 numerical function minimization in Python_

## Minuit ##

Minuit has been the standard package for minimizing general N-dimensional functions in high-energy physics since its introduction in 1972.  It features a robust set of algorithms for optimizing the search, correcting mistakes, and measuring non-linear error bounds.  It is the minimization engine used behind-the-scenes in most high-energy physics curve fitting applications.

## Python interface ##

PyMinuit2 is an extension module for Python that passes low-level Minuit functionality to Python functions.  Interaction and data exploration is more user-friendly, in the sense that the user is protected from segmentation faults and index errors, parameters are referenced by their names, even in correlation matrices, and Python exceptions can be passed from the objective function during the minimization process.  This extension module also makes it easier to calculate Minos errors and contour curves at an arbitrary number of sigmas from the minimum, and features a new N-dimensional scanning utility.

## PyMinuit versus PyMinuit2 ##

There are two versions of Minuit, both of which are C++ re-writes of the original Fortran Minuit.  The first of these, "[SEAL-Minuit](http://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/)", is an independent software package that has all the functionality of the original Minuit, but is no longer maintained.  The second, "[Minuit2](http://seal.web.cern.ch/seal/MathLibs/5_0_8/Minuit2/html/)", is a part of the [ROOT](http://root.cern.ch) package and is actively being developed.  There are correspondingly two versions of PyMinuit, which appeal to different users:

  * [PyMinuit](http://code.google.com/p/pyminuit): contains SEAL-Minuit 1.7.9 and the Python interface to it; installs in one step.  Use this if you don't have ROOT (or don't know what it is) and you just want to find the minimum of functions.

  * [PyMinuit2](http://code.google.com/p/pyminuit2)  (this package): only contains an interface to Minuit2 and must be linked to an existing ROOT distribution.  Use this if you want to use the algorithms contained in a specific ROOT version.

PyMinuit and PyMinuit2 present the same interface to the Python user, so the documentation on the [PyMinuit](http://code.google.com/p/pyminuit) site applies to PyMinuit2.  See [Minuit2Features](Minuit2Features.md) for extra features specific to PyMinuit2.

## Versions and system requirements ##

PyMinuit2 requires Python 2.4 or later and version of [ROOT](http://root.cern.ch) with Minuit2.  It has only been tested on Linux.

In principle, it should compile and run on Mac OS X, and it might work on Windows.  If you get PyMinuit2 working on one of these systems, please send me a instructions, so that I can post them for the benefit of other users.