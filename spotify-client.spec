# These refer to the installer, not the main package:
%define commit      5556bae39439738ebf3788363598b785068d9ba1
%define shortcommit %(c=%{commit}; echo ${c:0:7})

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
Version:	0.9.4.183.g644e24e.428
Release:	0.1
# http://community.spotify.com/t5/Desktop-Linux/What-license-does-the-linux-spotify-client-use/td-p/173356
License:	No modification permitted, non-redistributable
Group:		Applications/Multimedia
URL:		http://www.spotify.com/se/blog/archives/2010/07/12/linux/
Source0:	%{github_repo}/spotify-make-%{shortcommit}.tar.gz
# Source0-md5:	00e9f46e791c6c1e1c6c9c8d51047883
Source1:	%{repo}/%{name}_%{version}-1_i386.deb
# NoSource1-md5:	20113ac3d6760ded6940fef8143fa9a3
NoSource:	1
Source2:	%{repo}/%{name}_%{version}-1_amd64.deb
# NoSource2-md5:	e5d6049689a8ef0f3699986e47478fe2
NoSource:	1
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	zenity
# Symlinked, not picked up by autorequire (all 5).
Requires:	libnspr4.so%{?req_64}
Requires:	libnss3.so%{?req_64}
Requires:	libnssutil3.so%{?req_64}
Requires:	libplc4.so%{?req_64}
Requires:	libsmime3.so%{?req_64}
Provides:	spotify = %{version}-%{release}
# https://lists.rpmfusion.org/pipermail/rpmfusion-developers/2012-November/013934.html
Provides:	bundled(libssl) = 0.9.8
ExclusiveArch:	%{ix86} %{x8664}

# Bundled, we should not Provide these
%define		_noautoprovfiles	%{_libdir}/spotify-client/.*[.]so

# Filter away the deps of bundled libs and those substituted by symlinks and explicit Requires:.
%define		_noautoreq		'^libssl.so.0.9.8\\(OPENSSL_0.9.8\\)' '^libcrypto.so.0.9.8\\(OPENSSL_0.9.8\\)' ^libcef.so [.]so[.][0-2][a-f]

%description
Think of Spotify as your new music collection. Your library. Only this
time your collection is vast: millions of tracks and counting. Spotify
comes in all shapes and sizes, available for your PC, Mac, home audio
system and mobile phone. Wherever you go, your music follows you. And
because the music plays live, there’s no need to wait for downloads
and no big dent in your hard drive.

%prep
%setup -qn spotify-make-%{commit}

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
%{_libdir}/spotify-client/Data/apps.zip
%{_libdir}/spotify-client/Data/cef.pak
%{_libdir}/spotify-client/Data/devtools_resources.pak
%{_libdir}/spotify-client/Data/resources.zip
%{_libdir}/spotify-client/licenses.xhtml
%attr(755,root,root) %{_libdir}/spotify-client/spotify
%attr(755,root,root) %{_libdir}/spotify-client/libcef.so
%attr(755,root,root) %{_libdir}/spotify-client/libudev.so.0
