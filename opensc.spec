%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Library for accessing SmartCard devices
Name:		opensc
Version:	0.12.0
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Kernel and hardware
URL:		http://www.opensc.org/
Source:		http://www.opensc-project.org/files/opensc/%{name}-%{version}.tar.gz
Source1:	oberthur.profile
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	libltdl-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
Requires:	%{_lib}pcsclite1
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	%{libname} = %{version}-%{release}
# because we moved the config file and some modules from the %{name} package
# to the %{libname} package
Conflicts:	%{name} < 0.10.0-1mdk

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
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall_std

# install conf file
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 etc/opensc.conf %{buildroot}%{_sysconfdir}

# remove useless files
rm -f %{buildroot}%{_libdir}/pkcs11-spy.a \
      %{buildroot}%{_libdir}/opensc-pkcs11.a

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS README
%doc oberthur-alternate.profile
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/eidenv
%{_bindir}/piv-tool
%{_bindir}/netkey-tool
%{_bindir}/opensc-explorer
%{_bindir}/opensc-tool
%{_bindir}/rutoken-tool
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
%defattr(-,root,root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/opensc.conf
%{_libdir}/opensc-pkcs11.*
%{_libdir}/lib*.so.%{major}*
%{_libdir}/onepin-opensc-pkcs11.so

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/westcos-tool
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/onepin-opensc-pkcs11.la
