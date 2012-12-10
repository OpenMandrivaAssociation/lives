%define major 0
%define libname %mklibname weed %{major}
%define develname %mklibname -d weed

Summary:	Linux Video Editing System
Name:		lives
Version:	1.6.4
Release:	2
License:	GPLv3+
Group:		Video
URL:		http://lives.sourceforge.net/
Source0:	LiVES-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		lives-1.6.1-mdv-symlink.patch
BuildRequires:	pkgconfig(gdk-2.0)
BuildRequires:	bison
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(mjpegtools)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	gpm-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	libpth-devel
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libvisual-0.4) >= 0.1.7
BuildRequires:  perl-base
Suggests:	xmms 
Requires:	mplayer 
Requires:	mencoder 
Requires:	sox 
Requires:	imagemagick
Requires:	cdrecord-cdda2wav
Requires:	xset
Requires:	gdk-pixbuf-loaders
Requires:	libvisual-plugins

%description
The Linux Video Editing System (LiVES) is intended to be a simple yet powerful
video effects and editing system.  It uses common tools for most of its work
(mplayer, ImageMagick, GTK+, sox).

%package -n %{libname}
Summary:	Linux Video Editing System - shared libs
Group:		Video

%description -n %{libname}
This package contains shared libs for LiVES.

%package -n %{develname}
Summary:	Linux Video Editing System - Development files
Group:		Video
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files needed to build LiVES plugins.

%prep
%setup -q
%patch0 -p1 -b .symlink
aclocal
automake
perl -p -i -e 's|"/usr/local/"|&get_home_dir||g' smogrify

%build
%define _disable_ld_no_undefined 1
%configure2_5x --disable-static --enable-threads=posix
%make

%install
%makeinstall_std

%find_lang lives

find %buildroot%_libdir/%name -name *.la|xargs rm
rm -f %buildroot%_datadir/pixmaps/lives.xpm
rm -rf %{buildroot}/%{_datadir}/app-install
rm -f %{buildroot}/%{_libdir}/*.{a,la}

# icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE1} \
	%{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %{SOURCE2} \
	%{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{SOURCE3} \
	%{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%files -f lives.lang
%doc %{_docdir}/%{name}-%{version}
%_bindir/*
%_datadir/%{name}
%_libdir/%{name}
%{_datadir}/applications/LiVES.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%_libdir/*.so.%{major}*

%files -n %{develname}
%{_includedir}/weed
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


