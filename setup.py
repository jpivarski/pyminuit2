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

def is_secretly_root(lib):
    """
    Detect an edge case where ROOT Minuit2 is detected as standalone
    because $ROOTSYS/lib is in LD_LIBRARY_PATH, and suggest
    appropriate countermeasures.
    """
    from distutils import ccompiler
    libdir = os.path.dirname(lib)
    cc = ccompiler.new_compiler()
    for rootlib in ("Core","Cint","RIO","Net","Hist","Graf","Rint","Matrix","MathCore"):
        if not cc.find_library_file([libdir], rootlib):
            return False
        else:
            try:
                root_config('libdir')
                return True
            except OSError:
                raise RuntimeError("Found %s, which appears to be part of ROOT, but could not find root-config in PATH! To build against the standalone Minuit2, remove $ROOTSYS/lib from LD_LIBRARY_PATH; to build against the ROOT version, add $ROOTSYS/bin to your PATH" % lib)

libs = ["Minuit2"]
libdirs = []
incdirs = []

minuit2_standalone = find_library('Minuit2')
if minuit2_standalone and not is_secretly_root(minuit2_standalone):
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
        raise RuntimeError("Neither the standalone Minuit2 library nor root-config could be found. Minuit2 can be obtained from your favorite package manager or from http://seal.web.cern.ch/seal/work-packages/mathlibs/minuit/release/download.html")
    
setup(name="pyMinuit2",
      version="1.1.0",
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
