%global apiversion   0.2
%global spaversion   0.1

#global snap       20141103
#global gitrel     327
#global gitcommit  aec811798cd883a454b9b5cd82c77831906bbd2d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

# where/how to apply multilib hacks
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 ppc64le

Name:           pipewire
Summary:        Media Sharing Server
Version:        0.2.3
Release:        1%{?snap:.%{snap}git%{shortcommit}}%{?dist}
License:        LGPLv2+
URL:            https://pipewire.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/pipewire
# cd pipewire; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        pipewire-%{version}-%{gitrel}-g%{shortcommit}.tar.gz
%else
Source0:	https://github.com/PipeWire/pipewire/archive/%{version}.tar.gz
%endif

## upstream patches


## upstreamable patches

BuildRequires:  meson >= 0.35.0
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:  systemd-devel >= 184
BuildRequires:  alsa-lib-devel
BuildRequires:  libv4l-devel
BuildRequires:  doxygen
BuildRequires:  xmltoman
BuildRequires:  graphviz
BuildRequires:  sbc-devel

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd >= 184
Requires:       rtkit

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

## enable systemd activation
%global systemd 1

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
License:        LGPLv2+

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package doc
Summary:        PipeWire media server documentation
License:        LGPLv2+

%description doc
This package contains documentation for the PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%prep
%setup -q -T -b0 -n %{name}-%{version}%{?gitrel:-%{gitrel}-g%{shortcommit}}

%build
%meson -D docs=true -D man=true -D gstreamer=true -D systemd=true
%meson_build

%install
%meson_install

%check
%meson_test

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d /var/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%ldconfig_scriptlets

%files
%license LICENSE GPL LGPL
%doc README
%if 0%{?systemd}
%{_userunitdir}/pipewire.*
%endif
%{_bindir}/pipewire
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/gstreamer-1.0/libgstpipewire.*
%{_libdir}/pipewire-%{apiversion}/
%{_libdir}/spa/
%{_mandir}/man1/pipewire.1*
%{_sysconfdir}/pipewire/pipewire.conf

%files libs
%license LICENSE GPL LGPL
%doc README
%dir %{_sysconfdir}/pipewire/
#%dir %{_libdir}/pipewire/

%files devel
%{_libdir}/libpipewire-%{apiversion}.so
%{_includedir}/pipewire/
%{_includedir}/spa/
%{_libdir}/pkgconfig/libpipewire-%{apiversion}.pc
%{_libdir}/pkgconfig/libspa-%{spaversion}.pc

%files doc
%{_datadir}/doc/pipewire/html

%files utils
%{_bindir}/pipewire-monitor
%{_bindir}/pipewire-cli
%{_mandir}/man1/pipewire.conf.5*
%{_mandir}/man1/pipewire-monitor.1*
%{_mandir}/man1/pipewire-cli.1*
%{_bindir}/spa-monitor
%{_bindir}/spa-inspect

%changelog
* Thu Aug 30 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Tue Jul 31 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Fri Jul 20 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Tue Jul 17 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.9-1
- Update to 0.1.9

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.8-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 23 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Fri Nov 24 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.7-1
- Update to 0.1.7
- Add to build when memfd_create is already defined

* Fri Nov 03 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-2
- Add patch to avoid segfault when probing

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 0.1.4-3
- Rebuilt for GNOME 3.26.0 megaupdate

* Fri Sep 08 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.4-2
- Install SPA hooks

* Wed Aug 23 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Wed Aug 09 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.3-1
- Update to 0.1.3

* Tue Jul 04 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Added more build requirements
- Make separate doc package

* Mon Jun 26 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.1-1
- Update to 0.1.1
- Add dbus-1 to BuildRequires
- change libs-devel to -devel

* Wed Sep 9 2015 Wim Taymans <wtaymans@redhat.com> - 0.1.0-2
- Fix BuildRequires to use pkgconfig, add all dependencies found in configure.ac
- Add user and groups  if needed
- Add license to %%licence

* Tue Sep 1 2015 Wim Taymans <wtaymans@redhat.com> - 0.1.0-1
- First version
