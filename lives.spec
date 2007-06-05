%define name 	lives
%define version 0.9.8.5
%define release %mkrel 1

Summary: 	Linux Video Editing System
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://www.xs4all.nl/~salsaman/lives/current/LiVES-%version.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name-48.png
URL: 		http://www.xs4all.nl/~salsaman/lives
License: 	GPL
Group: 		Video
BuildRoot:      %{_tmppath}/%{name}-buildroot
BuildRequires: 	gtk2-devel
BuildRequires:	bison
BuildRequires:  ImageMagick libmjpegtools-devel SDL-devel
BuildRequires: cairo-devel
Requires:	xmms mplayer mencoder sox ImageMagick 
Requires:	cdrecord-cdda2wav ffmpeg

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
perl -p -i -e 's|"/usr/local/"|&get_home_dir||g' smogrify
#perl -pi -e 's/python2.3/python/' $(grep -l  -r -i bin/python2 . )

%build
%configure2_5x
%make libvis_wo_CFLAGS="`pkg-config --cflags libvisual-0.4` -fPIC"

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
rm -fr $RPM_BUILD_ROOT/%_docdir/LiVES-%version
%find_lang lives
cp smogrify midistart midistop $RPM_BUILD_ROOT/%_bindir
cd $RPM_BUILD_ROOT/%_datadir/%name/themes
rm -fr `find -name '.xvpics'`
cd $RPM_BUILD_ROOT/%_bindir
rm -fr lives
ln -s lives-exe lives
rm -fr $RPM_BUILD_ROOT/%_docdir

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
(cd $RPM_BUILD_ROOT
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}):\
needs="x11"\
section="Multimedia/Video"\
title="LiVES"\
longtitle="GTK2 Video Editing System"\
command="%{name}-exe"\
icon="%name.png"\
xdg="true"
EOF
)

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=LiVES
Comment=%{summary}
Exec=%{_bindir}/%{name}-exe
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;X-MandrivaLinux-Multimedia-Video;AudioVideo;Video;AudioVideoEditing;
Encoding=UTF-8
EOF


# icons
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cp %SOURCE1 $RPM_BUILD_ROOT/%_miconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cp %SOURCE2 $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cp %SOURCE3 $RPM_BUILD_ROOT/%_liconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%{update_menus}

%postun 
%{clean_menus}

%files -f lives.lang
%defattr(-,root,root,0755)
%doc AUTHORS BUGS C* FEATURES GETTING* NEWS README*
%doc OMC/*.txt RFX/*
%_bindir/*
%_datadir/%name
%_menudir/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%_iconsdir/%name.png
%_liconsdir/%name.png
%_miconsdir/%name.png


