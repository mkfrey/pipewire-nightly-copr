%global apiversion   0.3
%global spaversion   0.2

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

# where/how to apply multilib hacks
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 ppc64le

%global enable_alsa 1

%if 0%{?fedora}
%global enable_jack 1
%global enable_pulse 1
%global enable_vulkan 1
%endif

# libpulse and libjack subpackages shouldn't have library provides
# as the files they ship are not in the linker path. We also have
# to exclude requires or else the subpackages wind up requiring the
# libs they're no longer providing
# FIXME: the jack-audio-connection-kit and pulseaudio subpackages
# should get the auto-generated Provides: instead, but they do not,
# either with or without the lines below, not sure how to fix that
%global __provides_exclude_from ^%{_libdir}/pipewire-%{apiversion}/.*$
%global __requires_exclude_from ^%{_libdir}/pipewire-%{apiversion}/.*$

Name:           pipewire
Summary:        Media Sharing Server
Version:        0.3.13
Release:        nightly_%(date +%%y%%m%%d)%{?dist}
License:        MIT
URL:            https://pipewire.org/
Source0:	https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/master/pipewire-master.tar.gz

## upstreamable patches

## fedora patches
Patch0:         0001-conf-disable-bluez5.patch

BuildRequires:  meson >= 0.49.0
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
%if 0%{?enable_vulkan}
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(bluez)
BuildRequires:  systemd-devel >= 184
BuildRequires:  alsa-lib-devel
BuildRequires:  libv4l-devel
BuildRequires:  doxygen
BuildRequires:  xmltoman
BuildRequires:  graphviz
BuildRequires:  sbc-devel
BuildRequires:  libsndfile-devel

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd >= 184
Requires:       rtkit

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package gstreamer
Summary:        GStreamer elements for PipeWire
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description gstreamer
This package contains GStreamer elements to interface with a
PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
License:        MIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package doc
Summary:        PipeWire media server documentation
License:        MIT

%description doc
This package contains documentation for the PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%if 0%{?enable_alsa}
%package alsa
Summary:        PipeWire media server ALSA support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description alsa
This package contains an ALSA plugin for the PipeWire media server.
%endif

%if 0%{?enable_jack}
%package libjack
Summary:        PipeWire libjack library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
# Renamed in F32
Obsoletes:      pipewire-jack < 0.2.96-2

%description libjack
This package contains a PipeWire replacement for JACK audio connection kit
"libjack" library.

%package jack-audio-connection-kit
Summary:        PipeWire JACK implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libjack%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
Conflicts:      jack-audio-connection-kit
Conflicts:      jack-audio-connection-kit-dbus
Provides:       jack-audio-connection-kit

%description jack-audio-connection-kit
This package provides a JACK implementation based on PipeWire

%package plugin-jack
Summary:        PipeWire media server JACK support
License:        MIT
BuildRequires:  jack-audio-connection-kit-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       jack-audio-connection-kit

%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.
%endif

%if 0%{?enable_pulse}
%package libpulse
Summary:        PipeWire libpulse library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
# Renamed in F32
Obsoletes:      pipewire-pulseaudio < 0.2.96-2

%description libpulse
This package contains a PipeWire replacement for PulseAudio "libpulse" library.

%package pulseaudio
Summary:        PipeWire PulseAudio implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libpulse%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
Conflicts:      pulseaudio-libs
Conflicts:      pulseaudio-libs-glib2
Provides:       pulseaudio-libs
Provides:       pulseaudio-libs-glib2

%description pulseaudio
This package provides a PulseAudio implementation based on PipeWire
%endif

%prep
%setup -q -T -b0 -n %{name}-master

%patch0 -p1 -b .0000

%build
%meson \
    -D docs=true -D man=true -D gstreamer=true -D systemd=true 		\
    -D gstreamer-device-provider=false					\
    %{!?enable_jack:-D jack=false -D pipewire-jack=false} 		\
    %{!?enable_pulse:-D pipewire-pulseaudio=false}			\
    %{!?enable_alsa:-D pipewire-alsa=false}				\
    %{!?enable_vulkan:-D vulkan=false}
%meson_build

%install
%meson_install

%if 0%{?enable_jack}
ln -s pipewire-%{apiversion}/jack/libjack.so.0 %{buildroot}%{_libdir}/libjack.so.0.1.0
ln -s libjack.so.0.1.0 %{buildroot}%{_libdir}/libjack.so.0
ln -s pipewire-%{apiversion}/jack/libjackserver.so.0 %{buildroot}%{_libdir}/libjackserver.so.0.1.0
ln -s libjackserver.so.0.1.0 %{buildroot}%{_libdir}/libjackserver.so.0
ln -s pipewire-%{apiversion}/jack/libjacknet.so.0 %{buildroot}%{_libdir}/libjacknet.so.0.1.0
ln -s libjacknet.so.0.1.0 %{buildroot}%{_libdir}/libjacknet.so.0
%endif

%if 0%{?enable_pulse}
ln -s pipewire-%{apiversion}/pulse/libpulse.so.0 %{buildroot}%{_libdir}/libpulse.so.0
ln -s pipewire-%{apiversion}/pulse/libpulse-simple.so.0 %{buildroot}%{_libdir}/libpulse-simple.so.0
ln -s pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so.0 %{buildroot}%{_libdir}/libpulse-mainloop-glib.so.0
%endif

%if 0%{?enable_alsa}
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

# upstream should use udev.pc
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d


%check
%ifarch s390x
# FIXME: s390x FAIL: pw-test-stream, pw-test-endpoint
%global tests_nonfatal 1
%endif
%meson_test || TESTS_ERROR=$?
if [ "${TESTS_ERROR}" != "" ]; then
echo "test failed"
%{!?tests_nonfatal:exit $TESTS_ERROR}
fi

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%post
%{?ldconfig}
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%ldconfig_postun

%triggerun -- %{name} < 0.3.6-2
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pipewire.socket >/dev/null 2>&1 || :

%files
%license LICENSE COPYING
%doc README.md
%{_userunitdir}/pipewire.*
%{_bindir}/pipewire
%{_bindir}/pipewire-media-session
%{_mandir}/man1/pipewire.1*
%dir %{_sysconfdir}/pipewire/
%config(noreplace) %{_sysconfdir}/pipewire/pipewire.conf
%{_mandir}/man5/pipewire.conf.5*

%files libs
%license LICENSE COPYING
%doc README.md
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%dir %{_libdir}/spa-%{spaversion}
%{_libdir}/spa-%{spaversion}/alsa/
%{_libdir}/spa-%{spaversion}/audioconvert/
%{_libdir}/spa-%{spaversion}/audiomixer/
%{_libdir}/spa-%{spaversion}/bluez5/
%{_libdir}/spa-%{spaversion}/control/
%{_libdir}/spa-%{spaversion}/support/
%{_libdir}/spa-%{spaversion}/v4l2/
%{_libdir}/spa-%{spaversion}/videoconvert/
%if 0%{?enable_vulkan}
%{_libdir}/spa-%{spaversion}/vulkan/
%endif

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstpipewire.*

%files devel
%{_libdir}/libpipewire-%{apiversion}.so
%{_includedir}/pipewire-%{apiversion}/
%{_includedir}/spa-%{spaversion}/
%{_libdir}/pkgconfig/libpipewire-%{apiversion}.pc
%{_libdir}/pkgconfig/libspa-%{spaversion}.pc

%files doc
%{_datadir}/doc/pipewire/html

%files utils
%{_bindir}/pw-mon
%{_bindir}/pw-metadata
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*

%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-monitor
%{_bindir}/spa-resample

%if 0%{?enable_alsa}
%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%if 0%{?enable_jack}
%files libjack
%{_libdir}/pipewire-%{apiversion}/jack/libjack.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so*
%{_bindir}/pw-jack
%{_mandir}/man1/pw-jack.1*

%files jack-audio-connection-kit
%{_libdir}/libjack.so.*
%{_libdir}/libjackserver.so.*
%{_libdir}/libjacknet.so.*

%files plugin-jack
%{_libdir}/spa-%{spaversion}/jack/
%endif

%if 0%{?enable_pulse}
%files libpulse
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-simple.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so*
%{_bindir}/pw-pulse
%{_mandir}/man1/pw-pulse.1*

%files pulseaudio
%{_libdir}/libpulse.so.0
%{_libdir}/libpulse-simple.so.0
%{_libdir}/libpulse-mainloop-glib.so.0
%endif
