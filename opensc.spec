%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Library for accessing SmartCard devices
Name:		opensc
Version:	0.12.2
Release:	1
License:	LGPLv2+
Group:		System/Kernel and hardware
URL:		http://www.opensc.org/
Source0:	http://www.opensc-project.org/files/opensc/%{name}-%{version}.tar.gz
Source1:	oberthur.profile
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	libltdl-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
#Requires:	%{_lib}pcsclite1

%description
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

%package -n	%{libname}
Summary:	Library for accessing SmartCard devices
Group:		System/Libraries
# because we moved the config file and some modules from the %{name} package
# to the %{libname} package
Conflicts:	%{name} < 0.10.0-1mdk
Obsoletes:	%{_lib}opensc2 < 0.12.0

%description -n	%{libname}
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

%package -n	%{develname}
Summary:	Development related files for %{name}
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Conflicts:	%{mklibname opensc 0 -d}
Obsoletes:	%{mklibname opensc 2 -d} < 0.11.3

%description -n	%{develname}
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

This package contains all necessary files to develop or compile any
applications or libraries that use %{name}. 

%prep
%setup -q

install -m 0644 %{_sourcedir}/oberthur.profile oberthur-alternate.profile

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

# install conf file
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 etc/opensc.conf %{buildroot}%{_sysconfdir}

%files
%doc NEWS README
%doc oberthur-alternate.profile
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/eidenv
%{_bindir}/piv-tool
%{_bindir}/netkey-tool
%{_bindir}/opensc-explorer
%{_bindir}/opensc-tool
%{_bindir}/pkcs11-tool
%{_bindir}/pkcs15-crypt
%{_bindir}/pkcs15-init
%{_bindir}/pkcs15-tool
%{_datadir}/%{name}
%{_libdir}/pkcs11-spy.*
%{_libdir}/pkcs11/*.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%doc COPYING
%config(noreplace) %{_sysconfdir}/opensc.conf
%{_libdir}/opensc-pkcs11.*
%{_libdir}/lib*.so.%{major}*
%{_libdir}/onepin-opensc-pkcs11.so

%files -n %{develname}
%{_bindir}/westcos-tool
%{_libdir}/lib*.so


%changelog
* Thu May 19 2011 Funda Wang <fwang@mandriva.org> 0.12.1-1mdv2011.0
+ Revision: 676107
- update file list
- update to new version 0.12.1

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.12.0-4
+ Revision: 666964
- mass rebuild

* Thu Dec 23 2010 Funda Wang <fwang@mandriva.org> 0.12.0-3mdv2011.0
+ Revision: 624022
- obsoletes old lib

* Thu Dec 23 2010 Funda Wang <fwang@mandriva.org> 0.12.0-2mdv2011.0
+ Revision: 624017
- update BR
- lock libmajor
- new version 0.12.0
- drop old patches
- there is no mozilla plugin any more

* Sat Dec 04 2010 Tomas Kindl <supp@mandriva.org> 0.11.13-3mdv2011.0
+ Revision: 609453
- bump mkrel
- make OpenSC PKCS#11 compliant by not locking access to token when in use...

* Mon Aug 30 2010 Funda Wang <fwang@mandriva.org> 0.11.13-2mdv2011.0
+ Revision: 574305
- rebuild for new pcsclite

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 0.11.13-1mdv2010.1
+ Revision: 537442
- New version 0.11.13
- add patch to build against libassuan 2.0 (http://www.opensc-project.org/opensc/ticket/217), though not tested
- rebuild for new openssl

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against openssl-0.9.8m

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.12-1mdv2010.1
+ Revision: 484031
- update to new version 0.11.12
- Remove pcsc provider hack because it was fixed upstream
  (http://www.opensc-project.org/opensc/changeset/3787/trunk)

* Sat Nov 21 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.11-1mdv2010.1
+ Revision: 468598
- Update to new version 0.11.11

* Sun Sep 20 2009 Funda Wang <fwang@mandriva.org> 0.11.9-1mdv2010.0
+ Revision: 445077
- New version 0.11.9
- hard requires libpcsclite.so.1

* Sun Sep 20 2009 Funda Wang <fwang@mandriva.org> 0.11.8-2mdv2010.0
+ Revision: 444993
- correctly specify pcsc-provider (bug#49675)

* Fri May 08 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.8-1mdv2010.0
+ Revision: 373487
- update to new version 0.11.8

* Tue Mar 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.11.7-1mdv2009.1
+ Revision: 347707
- 0.11.7

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 0.11.6-5mdv2009.1
+ Revision: 344704
- rebuilt against new readline

* Wed Jan 28 2009 Funda Wang <fwang@mandriva.org> 0.11.6-4mdv2009.1
+ Revision: 334857
- add static lib
- rebuild

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 0.11.6-3mdv2009.1
+ Revision: 292783
- enable openct build

* Thu Aug 28 2008 Frederik Himpe <fhimpe@mandriva.org> 0.11.6-2mdv2009.0
+ Revision: 276944
- Bump release number in order to get it submitted
- update to new version 0.11.6

* Sat Aug 02 2008 Funda Wang <fwang@mandriva.org> 0.11.5-1mdv2009.0
+ Revision: 260528
- New version 0.11.5
- drop path0, fixed upstream

  + Frederik Himpe <fhimpe@mandriva.org>
    - Fix source location

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.11.4-1mdv2009.0
+ Revision: 232970
- fix build (again...)
- fix build (whoops!)
- 0.11.4
- fix linkage (P0)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.11.3-2mdv2008.1
+ Revision: 179112
- rebuild
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Andreas Hasenack <andreas@mandriva.com>
    - updated to version 0.11.4

* Thu Aug 30 2007 Andreas Hasenack <andreas@mandriva.com> 0.11.3-1mdv2008.0
+ Revision: 76288
- updated to version 0.11.3
- adopted new devel library policy

* Fri May 04 2007 Andreas Hasenack <andreas@mandriva.com> 0.11.2-1mdv2008.0
+ Revision: 22528
- updated to version 0.11.2
- dropped patches that were already applied


* Fri Sep 29 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-29 20:05:45 (62765)
- fixed oberthur support (#26248)

* Wed Jun 07 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-06-07 21:57:49 (36790)
- New upstream version 0.11.1

* Wed Jun 07 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-06-07 19:37:01 (36783)
- Raise epoch and recompile to allow x86_64 be up-to-date too

* Wed Jun 07 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-06-07 19:30:09 (36781)
- import opensc-0.10.1-3mdv2007.0

* Mon May 29 2006 Andreas Hasenack <andreas@mandriva.com> 0.10.1-3mdk
- make the mozilla plugin require mozilla-firefox, and not mozila as it was
  requiring in 1mdk. The plugin package needs a mozilla-type browser

* Thu Apr 06 2006 Götz Waschk <waschk@mandriva.org> 0.10.1-2mdk
- don't depend on mozilla

* Thu Mar 09 2006 ANdreas Hasenack <andreas@mandriva.com> 0.10.1-1mdk
- updated to version 0.10.1

* Thu Jan 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-7mdk
- rebuilt to fix one /lib6464 issue in openssl-devel

* Fri Dec 09 2005 Andreas Hasenack <andreas@mandriva.com> 0.10.0-6mdk
- added alternative oberthur profile to %%doc

* Wed Dec 07 2005 Andreas Hasenack <andreas@mandriva.com> 0.10.0-5mdk
- added patch for pkcs15-crypt to accept the PIN on stdin

* Tue Dec 06 2005 Andreas Hasenack <andreas@mandriva.com> 0.10.0-4mdk
- added openssl-devel to buildrequires (thanks Stefan)

* Sat Dec 03 2005 Andreas Hasenack <andreas@mandriva.com> 0.10.0-3mdk
- rebuild with pcsc-lite support
- buildrequires libpcsclite-devel >= 1.2.9 (or else opensc won't build with pcsc
  support)
- dropped openldap-devel buildrequires since it is not used anymore

* Thu Nov 24 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.10.0-2mdk
- add BuildRequires: libltdl-devel

* Wed Nov 23 2005 Andreas Hasenack <andreas@mandriva.com> 0.10.0-1mdk
- updated to version 0.10.0 (Closes: #17883)
- removed parallel build patch, no longer necessary
- removed gcc4 patch, no longer necessary
- pam module has been removed from opensc version 0.10.0
- added opensc.conf file
- we don't have man7 anymore
- no more libscam
- more docs
- no more /usr/lib/pkcs11
- removed buildrequires for automake1.7, no longer needed
- major is 2 now, added appropriate conflicts
- moved config file and main opensc-pkcs11 module to the library package
- changed mozilla plugin requires from the main package (opensc) to just the
  library package
- fixed 
usage for opensc-config

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-9mdk
- rebuilt against openssl-0.9.8a

* Tue Aug 30 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.8.1-8mdk
- Rebuild for libldap2.3

* Sun Aug 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.1-7mdk
- added one gcc4 patch (andreas)

* Mon Feb 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.8.1-6mdk
- rebuild for ldap2.2_7
- fix multiarch

* Sat Jan 22 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.1-5mdk
- rebuild for new readline

* Thu Dec 02 2004 Abel Cheung <deaddog@mandrake.org> 0.8.1-4mdk
- Fix BuildRequires

* Thu Aug 19 2004 Abel Cheung <deaddog@deaddog.org> 0.8.1-3mdk
- Rebuild
- Enable libtoolize
- P0: Fix parallel build and compatibility with automake > 1.5

* Mon Feb 09 2004 Abel Cheung <deaddog@deaddog.org> 0.8.1-2mdk
- Fix directory ownership

* Tue Oct 14 2003 Abel Cheung <deaddog@deaddog.org> 0.8.1-1mdk
- First Mandrake package

