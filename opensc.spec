%define major	3
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Library for accessing SmartCard devices
Name:		opensc
Version:	0.13.0
Release:	3
License:	LGPLv2+
Group:		System/Kernel and hardware
Url:		http://sourceforge.net/projects/opensc/
Source0:	http://downloads.sourceforge.net/project/opensc/OpenSC/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:	oberthur.profile

BuildRequires:	docbook-style-xsl
BuildRequires:	flex
BuildRequires:	xsltproc
BuildRequires:	libltdl-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(zlib)

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

%description -n	%{libname}
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

%package -n	%{devname}
Summary:	Development related files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
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
install -m 0644 %{SOURCE1} oberthur-alternate.profile

%build
%configure2_5x \
	--disable-static \
	--enable-sm
%make

%install
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_libdir}/pkcs11
%makeinstall_std

%files
%doc NEWS README COPYING
%doc oberthur-alternate.profile
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/eidenv
%{_bindir}/iasecc-tool
%{_bindir}/netkey-tool
%{_bindir}/openpgp-tool
%{_bindir}/opensc-explorer
%{_bindir}/opensc-tool
%{_bindir}/piv-tool
%{_bindir}/pkcs11-tool
%{_bindir}/pkcs15-crypt
%{_bindir}/pkcs15-init
%{_bindir}/pkcs15-tool
%{_bindir}/sc-hsm-tool
%{_datadir}/%{name}
%{_libdir}/pkcs11-spy.*
%{_libdir}/pkcs11/*.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%config(noreplace) %{_sysconfdir}/opensc.conf
%{_libdir}/opensc-pkcs11.*
%{_libdir}/lib*.so.%{major}*
#{_libdir}/onepin-opensc-pkcs11.so

%files -n %{devname}
%{_bindir}/westcos-tool
%{_libdir}/lib*.so

