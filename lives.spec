%define major 0
%define libname %mklibname weed %{major}
%define devname %mklibname -d weed

Summary:	Linux Video Editing System
Name:		lives
Version:	2.2.5
Release:	2
License:	GPLv3+
Group:		Video
Url:		http://lives.sourceforge.net/
Source0:	http://www.xs4all.nl/~salsaman/lives/current/LiVES-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Source100:  %{name}.rpmlintrc
Patch0:		lives-1.6.1-mdv-symlink.patch
#
# Reversed (or previously applied) patch detected!
# Patch1:         lives-decoders.patch
#
BuildRequires:	bison
BuildRequires:	imagemagick
BuildRequires:	gpm-devel
BuildRequires:	libpth-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(gdk-3.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	ffmpeg-devel >= 2.0.1
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(libvisual-0.4) >= 0.1.7
BuildRequires:	pkgconfig(mjpegtools)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(theora)
BuildRequires:	tirpc-devel
Requires:	cdrecord-cdda2wav
Requires:	dvgrab
Requires:	frei0r-plugins
Requires:	imagemagick
Requires:	libvisual-plugins
Requires:	mencoder
Requires:	mkvtoolnix
Requires:	mplayer
Requires:	ogmtools
Requires:	sox
Requires:	vorbis-tools
Requires:	xset
Requires:	youtube-dl

%description
The Linux Video Editing System (LiVES) is intended to be a simple yet powerful
video effects and editing system.  It uses common tools for most of its work
(mplayer, ImageMagick, GTK+, sox).

%files -f lives.lang
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/LiVES.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Linux Video Editing System - shared libs
Group:		Video

%description -n %{libname}
This package contains shared libs for LiVES.

%files -n %{libname}
%doc COPYING FEATURES NEWS README GETTING.STARTED 
%{_libdir}/*.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Linux Video Editing System - Development files
Group:		Video
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains development files needed to build LiVES plug-ins.

%files -n %{devname}
%doc BUGS ABOUT-NLS AUTHORS
%{_includedir}/weed
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%setup -q

%patch0 -p1 -b .symlink~
# Reversed (or previously applied) patch detected!
# %%patch1 -p1 -b .decoders
#

# fix debug spurious-executable
chmod a-x src/giw/{giwvslider,giwled,giwknob}.h
chmod a-x src/giw/{giwvslider,giwled,giwknob}.c
chmod a-x lives-plugins/weed-plugins/bump2d.c
chmod a-x lives-plugins/weed-plugins/syna.h

aclocal
automake
perl -p -i -e 's|"/usr/local/"|&get_home_dir||g' smogrify

%build
%define _disable_ld_no_undefined 1
%configure2_5x --disable-static --enable-threads=posix
%make

%install
%makeinstall_std



rm -f %{buildroot}%{_datadir}/pixmaps/lives.xpm
rm -rf %{buildroot}/%{_datadir}/app-install

#fix linting
chmod a-x %{buildroot}%{_libdir}/lives/plugins/effects/realtime/weed/data/fourKlives/songs/{examples,newlives,regrlives,roselives,modulations}.txt


# icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE1} \
	%{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %{SOURCE2} \
	%{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{SOURCE3} \
	%{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%find_lang lives