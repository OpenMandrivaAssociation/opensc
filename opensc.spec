%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Library for accessing SmartCard devices
Name:		opensc
Version:	0.11.13
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Kernel and hardware
URL:		http://www.opensc.org/
Source:		http://www.opensc-project.org/files/opensc/%{name}-%{version}.tar.gz
Source1:	oberthur.profile
Patch0:		opensc-libassuan-2.patch
Patch1:		opensc-0.11.13-pcsclite-1.6.patch
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
Requires: 	%{_lib}pcsclite1
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
Provides: 	%{libname} = %{version}-%{release}
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
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides: 	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Conflicts:	%{mklibname opensc 0 -d}
Obsoletes:      %{mklibname opensc 2 -d} < 0.11.3

%description -n	%{develname}
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
# could be just opensc-pkcs11.so instead of %{libname}, but
# the opensc-pkcs11.so object doesn't have a versioned soname so we
# can't risk using it
Requires:	%{libname} = %{version}
Requires:	mozilla-firefox

%description -n	mozilla-plugin-%{name}
This mozilla plugins handles web signatures using OpenSC
smartcard library.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

install -m 0644 %{_sourcedir}/oberthur.profile oberthur-alternate.profile

%build
./bootstrap
%configure2_5x \
    --enable-nsplugin \
    --enable-pcsc \
    --enable-openct \
    --with-pin-entry=%{_bindir}/pinentry \
    --with-plugindir=%{_libdir}/mozilla/plugins
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
%doc doc/README oberthur-alternate.profile
%exclude %{_mandir}/man1/opensc-config*
%{_bindir}/cardos-info
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
%{_libdir}/lib*.so.*
%{_libdir}/onepin-opensc-pkcs11.so

%files -n %{develname}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/opensc-config
%{_bindir}/opensc-config
%{_bindir}/westcos-tool
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man1/opensc-config*
%{_mandir}/man3/*
%{_libdir}/onepin-opensc-pkcs11.la

%files -n mozilla-plugin-%{name}
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/*.so
