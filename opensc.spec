# THIS PACKAGE IS HOSTED AT MANDRIVA SVN
# PLEASE DO NOT UPLOAD DIRECTLY BEFORE COMMIT

%define	name	opensc
%define version 0.11.1
%define release %mkrel 2

%define major 2
%define libname %mklibname %{name}

Summary:	Library for accessing SmartCard devices
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.opensc.org/
Source:		http://www.opensc.org/files/%{name}-%{version}.tar.gz
Source1:	oberthur.profile
# based on http://keitin.net/jarpatus/projects/usbtoken/opensc.readpin.patch
Patch:		opensc-0.10.0-pinstdin.patch
# http://www.opensc-project.org/pipermail/opensc-user/2006-June/001058.html
# http://www.opensc-project.org/opensc/changeset/2977
# http://www.opensc-project.org/opensc/changeset/3030
Patch1:		opensc-0.11.1-oberthurfix.patch
BuildRequires:	flex
BuildRequires:	X11-devel
BuildRequires:	libopenct-devel
BuildRequires:	libxslt-proc
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
# opensc 0.10.0 requires at least pcsc-lite 1.2.9
BuildRequires:  libpcsclite-devel >= 1.2.9
BuildRequires:	libassuan-devel
BuildRequires:	libltdl-devel
BuildRequires:	openssl-devel
Requires:	pinentry
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.


%package -n	%{libname}%{major}
Summary:	Library for accessing SmartCard devices
Group:		System/Libraries
License:	LGPL
Provides: 	%{libname} = %{version}-%{release}
# because we moved the config file and some modules from the %{name} package
# to the %{libname}%{major} package
Conflicts:	%{name} < 0.10.0-1mdk

%description -n	%{libname}%{major}
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.


%package -n	%{libname}%{major}-devel
Summary:	Development related files for %{name}
Group:		Development/C
License:	LGPL
Provides: 	%{libname}-devel = %{version}-%{release}
Provides: 	%{name}-devel = %{version}-%{release}
Requires:	%{libname}%{major} = %{version}
Conflicts:	%{libname}0-devel

%description -n	%{libname}%{major}-devel
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

This package contains all necessary files to develop or compile any
applications or libraries that use %{name}. 


%package -n	mozilla-plugin-%{name}
Summary:	OpenSC Mozilla plugin
Group:		Networking/WWW
# could be just opensc-pkcs11.so instead of %{libname}%{major}, but
# the opensc-pkcs11.so object doesn't have a versioned soname so we
# can't risk using it
Requires:	%{libname}%{major} = %{version}
Requires:	mozilla-firefox

%description -n	mozilla-plugin-%{name}
This mozilla plugins handles web signatures using OpenSC
smartcard library.

%prep
%setup -q
%patch -p1 -b .stdin
%patch1 -p0 -b .oberthurfix
install -m 0644 %{_sourcedir}/oberthur.profile oberthur-alternate.profile

%build
%configure2_5x \
	--with-pin-entry=%{_bindir}/pinentry

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# install conf file
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 etc/opensc.conf %{buildroot}%{_sysconfdir}

pushd %{buildroot}

# move mozilla plugin to correct place
mkdir -p .%{_libdir}/mozilla/plugins
mv .%{_libdir}/opensc-signer.so .%{_libdir}/mozilla/plugins/
rm -f .%{_libdir}/opensc-signer.*

popd

# remove useless files
rm -f %{buildroot}%{_libdir}/pkcs11-spy.a \
      %{buildroot}%{_libdir}/opensc-pkcs11.a

%multiarch_binaries %{buildroot}/%{_bindir}/%{name}-config

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%post -n %{libname}%{major} -p /sbin/ldconfig
%postun -n %{libname}%{major} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS doc/*.css doc/*.html README
%doc doc/README oberthur-alternate.profile
%exclude %{_mandir}/man1/opensc-config*
%{_bindir}/cardos-info
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
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}%{major}
%defattr(-,root,root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/opensc.conf
%{_libdir}/opensc-pkcs11.*
%{_libdir}/lib*.so.*

%files -n %{libname}%{major}-devel
%defattr(-,root,root)
%doc doc/ChangeLog
%multiarch %{multiarch_bindir}/opensc-config
%{_bindir}/opensc-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man1/opensc-config*
%{_mandir}/man3/*

%files -n mozilla-plugin-%{name}
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/*.so



