Minuit2
=============
numerical function minimization in Python

**Before you start:** note that PyMinuit has been re-written by Piti Ongmongkolkul for modern systems, yet with a very similar interface: the project is called iminuit (https://github.com/iminuit/iminuit).  PyMinuit is over 6 years old with little development since the initial product.  If PyMinuit doesn't work on your newfangled operating system or you want better IPython or Cython integration (or just the satisfaction of using actively maintained code), try iminuit.

**Update in 2015:** Guys, PyMinuit is ancient. I'm leaving it online because no software should ever become inaccessible (who knows? you might need it for some compatibility reason), but any new work should use iminuit (see above). If you're already familiar with the way PyMinuit works, you're in luck: iminuit has the same interface. They're having trouble [consolidating adoption](https://github.com/iminuit/iminuit/issues/156) because of the split between PyMinuit (based on SEAL-Minuit), PyMinuit2 (based on Minuit2), and iminuit (the only modern one in the bunch), but that shouldn't be the case. For all normal work, use iminuit!

Minuit
----------

Minuit has been the standard package for minimizing general N-dimensional 
functions in high-energy physics since its introduction in 1972. It features a 
robust set of algorithms for optimizing the search, correcting mistakes, and 
measuring non-linear error bounds. It is the minimization engine used 
behind-the-scenes in most high-energy physics curve fitting applications.


Python interface
------------------

PyMinuit2 is an extension module for Python that passes low-level Minuit 
functionality to Python functions. Interaction and data exploration is more 
user-friendly, in the sense that the user is protected from segmentation faults 
and index errors, parameters are referenced by their names, even in correlation 
matrices, and Python exceptions can be passed from the objective function 
during the minimization process. This extension module also makes it easier to 
calculate Minos errors and contour curves at an arbitrary number of sigmas from 
the minimum, and features a new N-dimensional scanning utility.


Requirements
-------------

PyMinuit2 requires the Minuit2 library, which can be
`obtained in standalone form from CERN <http://seal.web.cern.ch/seal/work-packages/mathlibs/minuit/release/download.html>`_
or as part of `ROOT <http://root.cern.ch/drupal/content/downloading-root>`_.

Examples
===========

Importing
------------

The following examples assume that PyMinuit2 has been imported as::
	from minuit2 import Minuit2 as Minuit

Minimizing simple functions
-----------------------------
To minimize a function, we will

- create it,
- pass it to a new Minuit object, and
- call migrad(), the minimizing algorithm
- extract the results from the Minuit object

Here's an example of a simple 2-dimensional paraboloid::
	def f(x, y): return (x-1)**2 + (y-2)**2 + 3      # step 1
	m = Minuit(f)                                    # step 2
	m.migrad()                                       # step 3
	m.values["x"], m.values["y"], m.fval             # step 4
	>>> (0.99999999986011212, 1.9999999997202242, 3.0)

The optimized x value is 1 (well, almost), the y value is 2 (ditto), and the minimum value of the function is 3.

You can do this with any Python function, even functions that throw exceptions when certain parameters are not met::
	def f(x,y):
		if abs(x) < 1: raise Exception
		return x**2 + y**2
	
	m = Minuit(f)
	m.migrad()
	>>> Traceback (most recent call last):
	>>>  File "<stdin>", line 1, in ?
	>>>  File "<stdin>", line 2, in f
	>>> Exception

A function in Python can be defined using the def keyword or inline as a lambda expression. The following two statements are equivalent::
	def f(x, y):
		return x**2 + y**2
	f = lambda x, y: x**2 + y**2

but the second can be embedded in the Minuit object's constructor::
	m = Minuit(lambda x, y: x**2 + y**2)

You can also supply a class member function::
	class Paraboloid(object):
		def __init__(self, xmin, ymin):
			self.xmin = xmin
			self.ymin = ymin

		def eval(self, x, y):
			return (x - self.xmin)**2 + (y - self.ymin)**2
	p = Paraboloid(6,3)
	m = Minuit(p.eval)
	m.migrad()
	m.values['x'],m.values['y'],m.fval
	>>>6.000000,3.000000,0.000000

See FunctionReference for a warning about integer division.

Helping the minimization by setting initial values
---------------------------------------------------

Naturally, there is no guarantee that we have found the absolute minimum of the function: Minuit can be fooled by a local minimum::
	def f(x):
		if x < 10:
			return (x-1)**2 - 5
		else:
			return (x-15)**2 - 7

	m = Minuit(f)
	m.values["x"] = 2
	m.migrad()
	m.values["x"], m.fval
	>>> (1.0000000001398872, -5.0)
	
	m = Minuit(f)
	m.values["x"] = 16
	m.migrad()
	m.values["x"], m.fval
	>>> (15.000000001915796, -7.0)

You can guide Minuit away from local minima by a careful choice of initial 
values. This can also help if Minuit fails to converge: the neighborhood of 
minima are often more well-behaved (positive definite, or even parabolic) than 
regions far from minima. You can pass initial values and errors (which migrad() 
interprets as starting step sizes) in the Minuit constructor::
	m = Minuit(lambda x, y: x**2 + y**2, x=3, y=5, err_x=0.01)
or after the object has been created::
	m = Minuit(lambda x, y: x**2 + y**2)
	m.values["x"] = 3
	m.values["y"] = 5
	m.errors["x"] = 0.01

If Minuit fails to find a minimum of your function, you can set the printMode to try to diagnose the problem and choose a better starting point. (See FunctionReference for more.)::
	m = Minuit(lambda x, y: (x-1)**2 + (y-2)**2, x=3, y=4)
	m.printMode = 1
	m.migrad()
	>>>   FCN Result | Parameter values
	>>> -------------+--------------------------------------------------------
	>>>            8 |            3            4
	>>>        8.004 |        3.001            4
	>>>        7.996 |        2.999            4
	>>>      8.00586 |      3.00146            4
	>>>      7.99414 |      2.99854            4
	>>>        8.004 |            3        4.001
	>>>        7.996 |            3        3.999
	>>>      8.00586 |            3      4.00146
	>>>      7.99414 |            3      3.99854
	>>>  4.24755e-18 |            1            2
	>>>  2.38419e-07 |      1.00049            2
	>>>  2.38418e-07 |     0.999512            2
	>>>  2.38421e-07 |            1      2.00049
	>>>  2.38417e-07 |            1      1.99951
	>>>  4.24755e-18 |            1            2
	>>>  2.38419e-07 |      1.00049            2
	>>>  2.38418e-07 |     0.999512            2
	>>>  2.38421e-07 |            1      2.00049
	>>>  2.38417e-07 |            1      1.99951
	>>>  9.53677e-09 |       1.0001            2
	>>>  9.53671e-09 |     0.999902            2
	>>>  9.53714e-09 |            1       2.0001
	>>>  9.53634e-09 |            1       1.9999
	>>>  4.76839e-07 |      1.00049      2.00049

You can also help a minimization by starting with a rough scan of the parameter 
space::
	m = Minuit(lambda x, y: (x-1)**2 + (y-2)**2, x=3, y=4)
	m.scan(("x", 30, -3, 7), ("y", 30, -3, 7), output=False)
	m.values
	>>> {'y': 2.1666666666666661, 'x': 1.1666666666666663}
	m.migrad()
	m.values
	>>> {'y': 2.0000000000041425, 'x': 1.0000000000042153}

Error estimation
-----------------

For statistics applications, we're also very interested in the steepness 
(stepth?) of the function near its minimum, because that is related the the 
uncertainty in our fit parameters given by the data. These are returned in the 
errors attribute::
	m = Minuit(lambda x, y: (x-1)**2 / 9.0 + (y-2)**4)
	m.migrad()
	m.errors["x"], m.errors["y"]
	>>> (2.9999999999999463, 9.3099692500949249)

But the migrad() algorithm alone does not guarantee error estimates within tolerance. For accurate errors, run the hesse() algorithm::
	m.hesse()
	m.errors["x"], m.errors["y"]
	>>> (2.9999999999999454, 9.308850308199208)

..note::
	The quartic "y" error changed by 0.01%, much larger than the 
	quadratic "x" error. The differences can be large in more pathological cases.

The hesse() algorithm calculates the entire covariance matrix, the matrix of 
second derivatives at the minimum. For uncorrelated functions that can be 
separated into x terms and y terms (like all the ones I have presented so far), 
the off-diagonal entries of the matrix are zero. Let's illustrate the 
covariance matrix with a mixed xy term::
	m = Minuit(lambda x, y: x**2 + y**2 + x*y)
	m.migrad()
	m.hesse()
	m.errors["x"]**2, m.errors["y"]**2
	>>> (1.3333333333333337, 1.3333333333333337)
	m.covariance
	>>> {('y', 'x'): -0.66666666666666685, ('x', 'y'): -0.66666666666666685, ('y', 'y'): 1.3333333333333335, ('x', 'x'): 1.3333333333333335}

The diagonal elements (xx and yy) are equal to the squares of the errors by 
definition. Because covariance is expressed as a dictionary, we can pull any 
element from it by name::
	m.covariance["x", "x"], m.covariance["y", "y"]
	>>> (1.3333333333333335, 1.3333333333333335)
	m.covariance["x", "y"], m.covariance["y", "x"]
	>>> (-0.66666666666666685, -0.66666666666666685)

Sometimes, it is more convenient to access the covariance matrix as a square array::
	m.matrix()
	>>> ((1.3333333333333335, -0.66666666666666685), (-0.66666666666666685, 1.3333333333333335))
	import Numeric
	Numeric.array(m.matrix())
	>>> array([[ 1.33333333, -0.66666667],
	>>>        [-0.66666667,  1.33333333]])

..note::
	The second example works only if you have the Numeric, numarray, or numpy modules installed.

It's also sometimes interesting to see the correlation matrix, which is 
normalized such that all diagonal entries are 1::
	m.matrix(correlation=True)
	>>> ((1.0, -0.5), (-0.5, 1.0))

Non-linear error measurement
-------------------------------

When a function is not parabolic near its minimum, the errors from the second 
derivative (which are quadratic at heart) may not be representative. In that 
case, we use the minos() algorithm to measure 1-sigma devitions by explicitly 
calculating the function away from the minimum::
	m = Minuit(lambda x: x**4)
	m.migrad()
	m.hesse()
	m.errors["x"]
	>>> 48.82085066828526
	m.minos()
	m.merrors["x", 1]
	>>> 1.0007813246693986

Errors calculated by minos() go into the merrors attribute, rather than errors. 
They are indexed by parameter and the number of sigmas in each direction, 
because the errors are not necessarily symmetric::
	m = Minuit(lambda x: x**4 + x**3)
	m.migrad()
	>>> VariableMetricBuilder: matrix not pos.def.
	>>> gdel > 0: 0.0604704
	>>> gdel: -0.00686919
	m.minos()
	m.merrors["x", -1], m.merrors["x", 1]
	>>> (-0.60752321396926234, 1.5429599172115098)

You can also calculate minos() errors an arbitrary number of sigmas from the minimum::
	m.minos("x", 2)
	m.merrors
	>>> {('x', 2.0): 1.9581663883782807, ('x', -1.0): -0.60752321396926234, ('x', 1.0): 1.5429599172115098}

This can be useful for 90%, 95%, and 99% confidence levels.

Drawing contour curves and function density maps
--------------------------------------------------

There's a 2-dimensional equivalent of minos() errors: contour lines in two 
parameters. When you call contour("param1", "param2", sigmas), you will get a 
list of x-y pairs for an error ellipse drawn at N sigmas::
	m = Minuit(lambda x, y: x**2 + y**2 + x*y)
	m.migrad()
	m.contour("x", "y", 1)
	>>> [(-1.1547005383792515, 0.57735026918952459), (-1.1016128399175811, 0.25107843795420443), ...]

If the function has a non-linear (or really, non-parabolic) minimum, the error 
ellipse won't be elliptical.


The scan() function can also produce plotter-friendly output by setting 
output=True (the default). It outputs a matrix of evaluated function values, 
which can be plotted as a density map for the function.

Fitting
----------
If you actually want to fit anything, you need to write a chi2 or negative log likelihood function::
	data = [(1, 1.1, 0.1), (2, 2.1, 0.1), (3, 2.4, 0.2), (4, 4.3, 0.1)]
	def f(x, a, b): return a + b*x
	
	def chi2(a, b):
		c2 = 0.
		for x, y, yerr in data:
			c2 += (f(x, a, b) - y)**2 / yerr**2
		return c2
	
	m = Minuit(chi2)
	m.migrad()
	m.hesse()
	m.values
	>>> {'a': -4.8538950636611844e-13, 'b': 1.0451612903223784}
	m.errors
	>>> {'a': 0.12247448677828, 'b': 0.045790546904858835}
	m.matrix(correlation=True)
	>>> ((1.0, -0.89155582779537212), (-0.89155582779537224, 1.0))
	for x in 1, 2, 3, 4:
		print x, f(x, *m.args)
	>>> 1 1.04516129032
	>>> 2 2.09032258064
	>>> 3 3.13548387097
	>>> 4 4.18064516129

But with access to the low-level function minimization, you can do much more 
complicated fits, such as simultaneous fits to different distributions, which 
are difficult to express in a high-level application.
