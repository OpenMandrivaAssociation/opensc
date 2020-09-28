%define major 6
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Library for accessing SmartCard devices
Name:		opensc
Version:	0.20.0
Release:	3
License:	LGPLv2+
Group:		System/Kernel and hardware
Url:		https://github.com/OpenSC
Source0:	https://github.com/OpenSC/OpenSC/archive/%{version}.tar.gz
Source1:	oberthur.profile
Patch0:	opensc-0.20.0-no-common.patch	
# https://github.com/OpenSC/OpenSC/commit/8551e84d
Patch1:	opensc-0.20.0-lto-build.patch
BuildRequires:	docbook-style-xsl
BuildRequires:	flex
BuildRequires:	xsltproc
BuildRequires:	libltdl-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(cmocka)
BuildRequires:	pkgconfig(bash-completion)
Conflicts:	%{mklibname opensc 4} < 0.16.0-2
Conflicts:	%{mklibname opensc 3} < 0.16.0-2
Requires:	pcsc-lite

%description
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

%package -n %{libname}
Summary:	Library for accessing SmartCard devices
Group:		System/Libraries
Obsoletes:	%{mklibname opensc 3} < %{EVRD}

%description -n %{libname}
%{name} is a library for accessing smart card devices using PC/SC Lite
middleware package. It is also the core library of the OpenSC project.
Basic functionality (e.g. SELECT FILE, READ BINARY) should work on any
ISO 7816-4 compatible smart card. Encryption and decryption using private
keys on the SmartCard is at the moment possible only with PKCS #15
compatible cards.

%package -n %{devname}
Summary:	Development related files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

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
%autosetup -n OpenSC-%{version} -p1

install -m 0644 %{SOURCE1} oberthur-alternate.profile

%build
./bootstrap
sed -i 's!-Werror!!g' configure configure.ac
sed -i -e 's|"/lib /usr/lib\b|"/%{_lib} %{_libdir}|' configure # lib64 rpaths

%configure \
	--disable-static \
	--disable-assert \
	--enable-openssl \
	--enable-pcsc \
	--enable-sm \
	--enable-zlib \
	--enable-notify \
	--disable-autostart-items

%make_build

%install
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_libdir}/pkcs11
%make_install

%files
%doc NEWS README COPYING
%doc oberthur-alternate.profile
%doc %{_docdir}/opensc/opensc.conf
%config(noreplace) %{_sysconfdir}/opensc.conf
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/dnie-tool
%{_bindir}/egk-tool
%{_bindir}/eidenv
%{_bindir}/iasecc-tool
%{_bindir}/netkey-tool
%{_bindir}/openpgp-tool
%{_bindir}/opensc-asn1
%{_bindir}/opensc-explorer
%{_bindir}/opensc-notify
%{_bindir}/opensc-tool
%{_bindir}/npa-tool
%{_bindir}/piv-tool
%{_bindir}/pkcs11-tool
%{_bindir}/pkcs15-crypt
%{_bindir}/pkcs15-init
%{_bindir}/pkcs15-tool
%{_bindir}/sc-hsm-tool
%{_bindir}/gids-tool
%{_bindir}/goid-tool
%{_bindir}/pkcs11-register
%{_sysconfdir}/bash_completion.d/*
%{_datadir}/%{name}
%{_datadir}/applications/org.opensc.notify.desktop
%{_libdir}/pkcs11-spy.*
%{_libdir}/pkcs11/*.so
%{_libdir}/opensc-pkcs11.*
%{_libdir}/onepin-opensc-pkcs11.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%{_bindir}/westcos-tool
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
