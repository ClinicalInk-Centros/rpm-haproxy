rpm-haproxy
==============

An RPM spec file to build and install the is HAProxy TCP/HTTP reverse proxy.

Build server dependencies::

 sudo yum -y install rpmdevtools pcre-devel gcc make openssl-devel


To Build (via jenkins)::

 SRC_VER="1.6.7"
 SRC_VER_MAJOR="1.6"
 SRC_URI="http://www.haproxy.org/download/$SRC_VER_MAJOR/src/haproxy-$SRC_VER.tar.gz"
 SPEC_URI="https://raw.github.com/ClinicalInk-Centros/rpm-haproxy/master/haproxy.spec"

 # setup the build directory in ~/rpmbuild tree.
 rpmdev-setuptree

 # get the spec file.
 wget $SPEC_URI -O ~/rpmbuild/SPECS/haproxy.spec

 # get the source tarball.
 wget $SRC_URI -O ~/rpmbuild/SOURCES/haproxy-$SRC_VER.tar.gz

 rpmbuild -bb ~/rpmbuild/SPECS/haproxy.spec --define "version $SRC_VER" --define "release 1"

