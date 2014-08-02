#
# Note for 32 bits you need to build an older release
# see the spotify-client-0.9.4 branch
#
# Requires gcrypt built from the gcrypt-1.5 branch
#

# These refer to the installer, not the main package:
%define commit      5a2e25f
%define repo        http://repository.spotify.com/pool/non-free/s/spotify
%define github_repo https://github.com/leamas/spotify-make/archive/%{commit}

# We cannot strip this binary (licensing restrictions).
%define debug_package %{nil}
%define no_install_post_strip	1
%define no_install_post_chrpath	1

%ifarch %{x8664}
%define   req_64        ()(64bit)
%endif
Summary:	Spotify music player native client
Name:		spotify-client
Version:	0.9.11.27.g2b1a638.81
Release:	0.1
# http://community.spotify.com/t5/Desktop-Linux/What-license-does-the-linux-spotify-client-use/td-p/173356
License:	No modification permitted, non-redistributable
Group:		Applications/Multimedia
URL:		http://www.spotify.com/se/blog/archives/2010/07/12/linux/
Source0:	%{github_repo}/spotify-make-%{commit}.tar.gz
# Source0-md5:	f18917d60a17758f064c93cbe025a65c
#Source1:	%{repo}/%{name}_%{version}-1_i386.deb
## NoSource1-md5:	20113ac3d6760ded6940fef8143fa9a3
#NoSource:	1
Source2:	%{repo}/%{name}_%{version}-1_amd64.deb
# NoSource2-md5:	778a0150fc9c0205f06a620a60f1365c
NoSource:	2
BuildRequires:	bash
BuildRequires:	desktop-file-utils
BuildRequires:	glibc-misc
BuildRequires:	lsb-release
BuildRequires:	nss
BuildRequires:	python-devel
BuildRequires:	python-modules
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	zenity
Provides:	spotify = %{version}-%{release}
# 0.9.10 is 64-bit only :(
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Bundled, we should not Provide these
%define		_noautoprovfiles	%{_libdir}/spotify-client/.*[.]so

# Filter away the deps not provided by our packages
%define		_noautoreq		'^libssl.so.1.0.0\\(OPENSSL_1.0.0\\)' '^libcrypto.so.1.0.0\\(OPENSSL_1.0.0\\)' ^libcef.so ^libudev.so

%description
Think of Spotify as your new music collection. Your library. Only this
time your collection is vast: millions of tracks and counting. Spotify
comes in all shapes and sizes, available for your PC, Mac, home audio
system and mobile phone. Wherever you go, your music follows you. And
because the music plays live, there’s no need to wait for downloads
and no big dent in your hard drive.

%prep
%setup -qc
mv spotify-make-%{commit}*/* .

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
%ifarch %{x8664}
	--package=%{SOURCE2} \
%else
	--package=%{SOURCE1} \
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# allow dependency gathering
chmod a+x $RPM_BUILD_ROOT%{_libdir}/spotify-client/libcef.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc opt/spotify/spotify-client/licenses.xhtml
%doc opt/spotify/spotify-client/readme.fedora
%doc opt/spotify/spotify-client/changelog
%attr(755,root,root) %{_bindir}/spotify
%{_mandir}/man1/spotify.1*
%{_desktopdir}/spotify.desktop
%{_iconsdir}/hicolor/*/apps/spotify-client.png
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/spotify-client/Data
%{_libdir}/spotify-client/Data/locales
%attr(755,root,root) %{_libdir}/spotify-client/Data/SpotifyHelper
%attr(755,root,root) %{_libdir}/spotify-client/Data/libffmpegsumo.so
%{_libdir}/spotify-client/Data/apps.zip
%{_libdir}/spotify-client/Data/cef.pak
%{_libdir}/spotify-client/Data/devtools_resources.pak
%{_libdir}/spotify-client/Data/resources.zip
%{_libdir}/spotify-client/licenses.xhtml
%attr(755,root,root) %{_libdir}/spotify-client/spotify
%attr(755,root,root) %{_libdir}/spotify-client/libcef.so
%attr(755,root,root) %{_libdir}/spotify-client/libudev.so.0
