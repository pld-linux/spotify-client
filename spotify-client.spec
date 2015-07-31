#
# Note for 32 bits you need to build an older release
# see the spotify-client-0.9.4 branch
#
# Requires gcrypt built from the gcrypt-1.5 branch
#

# These refer to the installer, not the main package:
%define commit      8597389ba7
%define github_repo https://github.com/leamas/spotify-make/archive/%{commit}

# main package source
%define repo        http://repository.spotify.com/pool/non-free/s/spotify-client

# We cannot strip this binary (licensing restrictions).
%define debug_package %{nil}
%define no_install_post_strip	1
%define no_install_post_chrpath	1

%ifarch %{x8664}
%define   req_64        ()(64bit)
%endif
Summary:	Spotify music player native client
Name:		spotify-client
Version:	1.0.11.131.gf4d47cb0
Release:	0.1
# http://community.spotify.com/t5/Desktop-Linux/What-license-does-the-linux-spotify-client-use/td-p/173356
License:	No modification permitted, non-redistributable
Group:		Applications/Multimedia
URL:		http://www.spotify.com/se/blog/archives/2010/07/12/linux/
Source0:	%{github_repo}/spotify-make-%{commit}.tar.gz
# Source0-md5:	42665a32532dc2a50f68c2841941f7e8
#Source1:	%{repo}/%{name}_%{version}-1_i386.deb
## NoSource1-md5:	20113ac3d6760ded6940fef8143fa9a3
#NoSource:	1
Source2:	%{repo}/%{name}_%{version}_amd64.deb
# NoSource2-md5:	af4bd4604c29d5d0ed2dde6e84453537
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
%define		_noautoreq		'^libssl.so.1.0.0\\(OPENSSL_1.0.0\\)' '^libcrypto.so.1.0.0\\(OPENSSL_1.0.0\\)' ^libcef.so ^libudev.so '^libcurl.so.4\\(CURL_OPENSSL_3\\)'

%description
Think of Spotify as your new music collection. Your library. Only this
time your collection is vast: millions of tracks and counting. Spotify
comes in all shapes and sizes, available for your PC, Mac, home audio
system and mobile phone. Wherever you go, your music follows you. And
because the music plays live, there’s no need to wait for downloads
and no big dent in your hard drive.

%prep
%setup -qc
mv spotify-make-*/* .

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
install -d $RPM_BUILD_ROOT%{_datadir}/appdata
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# avoid requiring gcrypt 1.5 at build time
ln -sf /%{_lib}/libgcrypt.so.11 $RPM_BUILD_ROOT%{_libdir}/spotify-client

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
%doc README.md usr/share/spotify/README.txt
%attr(755,root,root) %{_bindir}/spotify
%{_mandir}/man1/spotify.1*
%{_desktopdir}/spotify.desktop
%{_iconsdir}/hicolor/*/apps/spotify-client.png
%{_datadir}/appdata/spotify.xml

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Apps
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/locales
%{_datadir}/%{name}/*.bin
%{_datadir}/%{name}/*.dat
%{_datadir}/%{name}/*.pak
%{_datadir}/%{name}/control
%{_datadir}/%{name}/md5sums
%{_datadir}/%{name}/spotify.desktop
%attr(755,root,root) %{_datadir}/%{name}/libffmpegsumo.so
%attr(755,root,root) %{_datadir}/%{name}/spotify


%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/Data
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/control
%{_libdir}/%{name}/md5sums
%{_libdir}/%{name}/spotify.desktop
%attr(755,root,root) %{_libdir}/%{name}/spotify
%attr(755,root,root) %{_libdir}/%{name}/libcef.so
%attr(755,root,root) %{_libdir}/%{name}/libffmpegsumo.so
%attr(755,root,root) %{_libdir}/%{name}/libgcrypt.so.11
