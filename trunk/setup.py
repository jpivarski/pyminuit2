#!/usr/bin/env python

from distutils.core import setup, Extension
import os, sys, subprocess

##################################################################################################

from subprocess import Popen, PIPE
def root_config(*opts):
    args = ['root-config'] + ['--'+o for o in opts]
    return Popen(args, stdout=PIPE).communicate()[0].strip().split(' ')

def find_library(lib):
    from distutils import ccompiler
    libdirs = ['/usr/lib', '/usr/local/lib']
    libdirs += os.environ.get('DYLD_LIBRARY_PATH', '').split(':')
    libdirs += os.environ.get('LD_LIBRARY_PATH', '').split(':')
    cc = ccompiler.new_compiler()
    return cc.find_library_file(libdirs, lib) 

libs = ["Minuit2"]
libdirs = []
incdirs = []

minuit2_standalone = find_library('Minuit2')
if minuit2_standalone:
    print("Linking against standalone Minuit2 library")
    dirname = os.path.dirname(minuit2_standalone)
    libdirs += [dirname]
    incdirs += [os.path.join(os.path.split(dirname)[0],'include')]
else:
    try:
        version, incdir, libdir = root_config('version', 'incdir', 'libdir')
        incdirs.append(incdir)
        libdirs.append(libdir)
        libs += ["Core","Cint","RIO","Net","Hist","Graf","Rint","Matrix","MathCore"]
        print("Linking against Minuit2 library from ROOT %s" % version)
    except OSError:
        print("Neither the standalone Minuit2 library nor root-config could be found.")
        sys.exit(1)
    
setup(name="pyMinuit2",
      version="1.0.0",
      description="pyMinuit2: Minuit2 interface for minimizing Python functions",
      author="Johann Cohen-Tanugi",
      author_email="johann.cohentanugi@gmail.com",
      url="http://code.google.com/p/pyminuit2/",
      classifiers=['Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Mathematics',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
		   'Development Status :: 5 - Production/Stable',
		   ],
      ext_modules=[Extension("minuit2",
                             ["minuit2.cpp"],
                             library_dirs=libdirs,
                             libraries=libs,
                             include_dirs=incdirs
                             )])
