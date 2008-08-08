%define name 	lives
%define version 0.9.9.1
%define release %mkrel 2

Summary: 	Linux Video Editing System
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://www.xs4all.nl/~salsaman/lives/current/LiVES-%version.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name-48.png
Patch0:		LiVES-0.9.8.7-fix-desktop-item.patch
URL: 		http://www.xs4all.nl/~salsaman/lives
License: 	GPLv3+
Group: 		Video
BuildRoot:      %{_tmppath}/%{name}-buildroot
BuildRequires: 	gtk2-devel
BuildRequires:	bison
BuildRequires:  ImageMagick
BuildRequires:	libmjpegtools-devel
BuildRequires:	SDL-devel
BuildRequires:	cairo-devel
BuildRequires:	gpm-devel
BuildRequires:	jackit-devel
BuildRequires:	libtheora-devel
Requires:	xmms mplayer mencoder sox ImageMagick 
Requires:	cdrecord-cdda2wav
Requires:	xset
Requires:	gdk-pixbuf-loaders

%if %mdkversion > 1019
BuildRequires:	libvisual-devel >= 0.1.7
Requires:	libvisual-plugins
%endif

%description
The Linux Video Editing System (LiVES) is intended to be a simple yet powerful
video effects and editing system.  It uses common tools for most of its work
(mplayer, ImageMagick, GTK+, sox).

%prep
%setup -q
%patch0 -p0
perl -p -i -e 's|"/usr/local/"|&get_home_dir||g' smogrify

%build
%configure2_5x
%make

%install
rm -fr $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
make DESTDIR=$RPM_BUILD_ROOT install

%find_lang lives
rm -fr $RPM_BUILD_ROOT/%_docdir

rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/lives.xpm

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
%{_datadir}/applications/LiVES.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
