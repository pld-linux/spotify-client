# These refer to the installer, not the main package:
%define commit      23b12878e8f544bff886babf0978c1b24d087fb1
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
Version:	0.9.1.55.gbdd3b79.203
Release:	0.7
# http://community.spotify.com/t5/Desktop-Linux/What-license-does-the-linux-spotify-client-use/td-p/173356
License:	No modification permitted, non-redistributable
Group:		Applications/Multimedia
URL:		http://www.spotify.com/se/blog/archives/2010/07/12/linux/
Source0:	%{github_repo}/spotify-make-%{shortcommit}.tar.gz
# Source0-md5:	42a54aa575096ee392d4c53bf464b777
Source1:	%{repo}/%{name}_%{version}-1_i386.deb
# NoSource1-md5:	4aeb0de3138d9b89a805bde84a2ac6c8
NoSource:	1
Source2:	%{repo}/%{name}_%{version}-1_amd64.deb
# NoSource2-md5:	5be8c87214685bab303f4c4ec02d8264
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

# use libs from openssl.spec@OPENSSL_0_9_8
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/libcrypto.so.0.9.8
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/libssl.so.0.9.8

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
%{_libdir}/spotify-client/Data
%{_libdir}/spotify-client/chrome.pak
%{_libdir}/spotify-client/devtools_resources.pak
%{_libdir}/spotify-client/licenses.xhtml
%{_libdir}/spotify-client/locales
%attr(755,root,root) %{_libdir}/spotify-client/spotify
%attr(755,root,root) %{_libdir}/spotify-client/libcef.so
# nss/nspr
%attr(755,root,root) %{_libdir}/spotify-client/libnspr4.so.0d
%attr(755,root,root) %{_libdir}/spotify-client/libnss3.so.1d
%attr(755,root,root) %{_libdir}/spotify-client/libnssutil3.so.1d
%attr(755,root,root) %{_libdir}/spotify-client/libplc4.so.0d
%attr(755,root,root) %{_libdir}/spotify-client/libsmime3.so.1d
