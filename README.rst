rpm-haproxy
==============

An RPM spec file to build and install the is HAProxy TCP/HTTP reverse proxy.

ClinicalInk customized the build flags passed to make for gzip support::

 %{__make} USE_PCRE=1 DEBUG="" ARCH=%{_target_cpu} TARGET=linux26 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 USE_CRYPT_H=1 USE_LIBCRYPT=1


Build server dependencies
---------------------------------

::

 sudo yum -y install rpmdevtools pcre-devel gcc make openssl-devel


Jenkins Job
-------------------------------------

::

 SRC_VER="1.6.7"
 SRC_VER_MAJOR="1.6"
 SRC_URI="http://www.haproxy.org/download/$SRC_VER_MAJOR/src/haproxy-$SRC_VER.tar.gz"

 SPEC_URI="https://raw.githubusercontent.com/ClinicalInk-Centros/rpm-haproxy/master/haproxy.spec"

 # regenerate rpmbuild tree ~/rpmbuild tree.
 rm -rf ~/rpmbuild
 rpmdev-setuptree

 # get the spec file.
 wget -N $SPEC_URI -O ~/rpmbuild/SPECS/haproxy.spec

 # get the source tarball.
 wget -N $SRC_URI -O ~/rpmbuild/SOURCES/haproxy-$SRC_VER.tar.gz

 rpmbuild -bb ~/rpmbuild/SPECS/haproxy.spec --define "version $SRC_VER" --define "release $BUILD_NUMBER"
 
 # copy the resulting rpms to work directory so jenkins can archive them.
 cp ~/rpmbuild/RPMS/x86_64/*.rpm .
