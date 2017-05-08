Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments

%{!?name: %{!?name: %define name haproxy}}
%{!?version: %{!?version: %define version 1.6.9}}
%{!?release: %{!?release: %define release 1}}

Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System Environment/Daemons
URL: http://haproxy.1wt.eu/
Source0: http://www.haproxy.org/download/1.6/src/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel
Requires: /sbin/chkconfig, /sbin/service

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%pre
# add user and group is needed.
getent group %{name} >/dev/null 2>&1 || groupadd -g 188 -r %{name} 2>/dev/null
getent user %{name} >/dev/null 2>&1 || useradd -d /var/lib/haproxy -s /sbin/nologin -g 188 -G %{name} -r -u 188 %{name} 2>/dev/null

%prep
#%setup -q
%setup -n %{name}-%{version}

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true

# ClinicalInk customized the build flags passed to make for gzip support.
%build
%{__make} USE_PCRE=1 DEBUG="" ARCH=%{_target_cpu} TARGET=linux26 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 USE_CRYPT_H=1 USE_LIBCRYPT=1

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/

%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -c -m 755 examples/%{name}.init %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -c -m 755 doc/%{name}.1 %{buildroot}%{_mandir}/man1/
 
%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc CHANGELOG README doc/architecture.txt doc/configuration.txt doc/intro.txt doc/management.txt doc/proxy-protocol.txt
%doc %{_mandir}/man1/%{name}.1*

%attr(0755,root,root) %{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0755,root,root) %config %{_sysconfdir}/rc.d/init.d/%{name}

%changelog
* Mon May 08 2017 Prakash pagare <ppagare@mobiquityinc.com>
- create haproxy user group

* Wed Aug 10 2016 Russell Ballestrini <russell@ballestrini.net>
- allow support for passing version over CLI with --define flag

* Sun Nov 14 2004 Willy Tarreau <w@w.ods.org>
- updated to 1.1.29
- fixed path to config and init files
- statically linked PCRE to increase portability to non-pcre systems

* Sun Jun  6 2004 Willy Tarreau <willy@w.ods.org>
- updated to 1.1.28
- added config check support to the init script

* Tue Oct 28 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.27
- added pid support to the init script

* Wed Oct 22 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.26

* Thu Oct 16 2003 Simon Matter <simon.matter@invoca.ch>
- initial build
