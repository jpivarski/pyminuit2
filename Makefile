ROOTLIBS = \
`$(ROOTSYS)/bin/root-config --libs`
ROOTINC = \
`$(ROOTSYS)/bin/root-config --incdir`

minuit:
	mkdir build;mkdir build/temp.linux-i686-2.5;mkdir build/lib.linux-i686-2.5
	gcc -pthread -fno-strict-aliasing -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m32 -march=i386 -mtune=generic -fasynchronous-unwind-tables -D_GNU_SOURCE -fPIC -fPIC -I$(ROOTINC) -I/usr/include/python2.5 -c minuit2.cpp -o build/temp.linux-i686-2.5/minuit2.o
	g++ -pthread -shared build/temp.linux-i686-2.5/minuit2.o $(ROOTLIBS) -lMinuit2 -L/usr/lib/python2.5/config -lpython2.5 -o build/lib.linux-i686-2.5/minuit.so
