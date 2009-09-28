%define name 	lives
%define version 1.0.3
%define release %mkrel 1

%define major 0
%define libname %mklibname weed %major
%define develname %mklibname -d weed

Summary: 	Linux Video Editing System
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://www.xs4all.nl/~salsaman/lives/current/LiVES-%version.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name-48.png
URL: 		http://lives.sourceforge.net/
License: 	GPLv3+
Group: 		Video
BuildRoot:      %{_tmppath}/%{name}-buildroot
BuildRequires: 	gtk2-devel
BuildRequires:	bison
BuildRequires:  imagemagick
BuildRequires:	libmjpegtools-devel
BuildRequires:	SDL-devel
BuildRequires:	cairo-devel
BuildRequires:	gpm-devel
BuildRequires:	jackit-devel
BuildRequires:	libtheora-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	celt-devel
Requires:	xmms mplayer mencoder sox imagemagick
Requires:	cdrecord-cdda2wav
Requires:	xset
Requires:	gdk-pixbuf-loaders
BuildRequires:	libvisual-devel >= 0.1.7
Requires:	libvisual-plugins

%description
The Linux Video Editing System (LiVES) is intended to be a simple yet powerful
video effects and editing system.  It uses common tools for most of its work
(mplayer, ImageMagick, GTK+, sox).

%package -n %libname
Summary:	Linux Video Editing System - shared libs
Group:		Video

%description -n %libname
This package contains shared libs for LiVES.

%package -n %develname
Summary:	Linux Video Editing System - Development files
Group:		Video
Requires:	%libname = %version
Provides:	%name-devel = %version-%release

%description -n %develname
This package contains development files needed to build LiVES plugins.

%prep
%setup -q
perl -p -i -e 's|"/usr/local/"|&get_home_dir||g' smogrify

%build
%define _disable_ld_no_undefined 1
%configure2_5x --disable-static
%make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall_std

%find_lang lives

find %buildroot%_libdir/%name -name *.la|xargs rm
rm -fr %buildroot%_datadir/doc
rm -f %buildroot%_datadir/pixmaps/lives.xpm

# icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{_sourcedir}/lives-16.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %{_sourcedir}/lives-32.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{_sourcedir}/lives-48.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post 
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun 
%clean_menus
%update_icon_cache hicolor
%endif

%files -f lives.lang
%defattr(-,root,root,0755)
%doc AUTHORS BUGS C* docs/*.txt FEATURES GETTING*
%doc NEWS OMC/*.txt README* RFX/*
%_bindir/*
%_datadir/%name
%_libdir/%name
%{_datadir}/applications/LiVES.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %libname
%defattr(-,root,root,-)
%_libdir/*.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%_includedir/weed
%_libdir/*.so
%_libdir/*.la
%_libdir/*.a
