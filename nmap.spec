%{!?withgtk1:%define withgtk1 0}

Summary: Network exploration tool and security scanner
Name: nmap
Version: 3.78
Release: 2
License: GPL
Group: Applications/System
Source0: http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2
#Source1: nmapfe.desktop
Patch0: inet_aton.patch
Patch1: makefile.patch
Patch2: nmap-3.78-gtk2.patch
URL: http://www.insecure.org/nmap/
BuildRoot: %{_tmppath}/%{name}-root
Epoch: 2
BuildRequires: openssl-devel, gtk+-devel, pcre-devel, libpcap

%description
Nmap is a utility for network exploration or security auditing.  It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, reverse-identd scanning, and more.

%package frontend
Summary: Gtk+ frontend for nmap
Group: Applications/System
Requires: nmap = %{epoch}:%{version}, gtk+
BuildRequires: gtk+-devel
%description frontend
This package includes nmapfe, a Gtk+ frontend for nmap. The nmap package must
be installed before installing nmap-frontend.

%prep
%setup -q
%if ! %{withgtk1}
%patch2 -p1 -b .gtk2
%endif

%build
%configure  --with-libpcap=/usr
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall nmapdatadir=$RPM_BUILD_ROOT%{_datadir}/nmap

mv $RPM_BUILD_ROOT%{_datadir}/applications/nmapfe.desktop .

 desktop-file-install --vendor nmap --delete-original       \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
    --add-category X-Red-Hat-Base                             \
    nmapfe.desktop;


%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc COPYING*
%doc docs/README docs/nmap-fingerprinting-article.txt
%doc docs/nmap.deprecated.txt docs/nmap.usage.txt docs/nmap_doc.html
%doc docs/nmap_manpage.html 
%{_bindir}/nmap
%{_datadir}/nmap
%{_mandir}/man1/nmap.1.gz

%files frontend
%defattr(-,root,root)
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_datadir}/applications/nmapfe.desktop
%{_mandir}/man1/nmapfe.1.gz
%{_mandir}/man1/xnmap.1.gz

%changelog
* Wed Feb 02 2005 Harald Hoyer <harald@redhat.com> - 2:3.78-2
- evil port of nmapfe to gtk2

* Fri Dec 17 2004 Harald Hoyer <harald@redhat.com> - 2:3.78-1
- version 3.78

* Mon Sep 13 2004 Harald Hoyer <harald@redhat.com> - 2:3.70-1
- version 3.70

* Tue Jul 13 2004 Harald Hoyer <harald@redhat.com> - 2:3.55-1
- new version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Harald Hoyer <harald@redhat.com> - 2:3.50-2
- added BuildRequires: openssl-devel, gtk+-devel, pcre-devel, libpcap

* Thu Jan 22 2004 Harald Hoyer <harald@redhat.com> - 2:3.50-1
- version 3.50

* Wed Oct  8 2003 Harald Hoyer <harald@redhat.de> 2:3.48-1
- version 3.48

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow disabling frontend if gtk1 is not available

* Mon Jul 30 2003 Harald Hoyer <harald@redhat.de> 2:3.30-1
- version 3.30

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 26 2003 Harald Hoyer <harald@redhat.de> 2:3.27-1
- version 3.27

* Mon May 12 2003 Harald Hoyer <harald@redhat.de> 2:3.20-2
- changed macro comments to double %% for changelog entries

* Mon Apr 14 2003 Harald Hoyer <harald@redhat.de> 2:3.20-1
- version 3.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Harald Hoyer <harald@redhat.de> 3.0-3
- nmap-3.00-nowarn.patch added

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches
- remove old desktop file from $$RPM_BUILD_ROOT so rpm won't complain

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de>
- version 3.0

* Mon Jul 29 2002 Harald Hoyer <harald@redhat.de> 2.99.2-1
- bumped version

* Fri Jul 26 2002 Harald Hoyer <harald@redhat.de> 2.99.1-2
- bumped version to 2.99RC1

* Fri Jul 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add an epoch

* Mon Jul  1 2002 Harald Hoyer <harald@redhat.de> 2.54.36-1
- removed desktop file
- removed "BETA" name from version
- update to BETA36

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 2.54BETA34-1
- update to 2.54BETA34

* Mon Mar 25 2002 Harald Hoyer <harald@redhat.com>
- more recent version (#61490)

* Mon Jul 23 2001 Harald Hoyer <harald@redhat.com>
- buildprereq for nmap-frontend (#49644)

* Sun Jul 22 2001 Heikki Korpela <heko@iki.fi>
- buildrequire gtk+ 

* Tue Jul 10 2001 Tim Powers <timp@redhat.com>
- fix bugs in desktop file (#48341)

* Wed May 16 2001 Tim Powers <timp@redhat.com>
- updated to 2.54BETA22

* Mon Nov 20 2000 Tim Powers <timp@redhat.com>
- rebuilt to fix bad dir perms

* Fri Nov  3 2000 Tim Powers <timp@redhat.com>
- fixed nmapdatadir in the install section, forgot lto include
  $RPM_BUILD_ROOT in the path

* Thu Nov  2 2000 Tim Powers <timp@redhat.com>
- update to nmap-2.54BETA7 to possibly fix bug #20199
- use the desktop file provided by the package instead of using my own
- patches in previous version are depreciated. Included in SRPM for
  reference only

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 28 2000 Tim Powers <timp@redhat.com>
- rebuilt package

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man pages so that they are in an FHS compliant location
- use %%makeinstall
- use predefined RPM macros wherever possible

* Tue May 16 2000 Tim Powers <timp@redhat.com>
- updated to 2.53
- using applnk now
- use %%configure, and %%{_prefix} where possible
- removed redundant defines at top of spec file

* Mon Dec 13 1999 Tim Powers <timp@redhat.com>
- based on origional spec file from
	http://www.insecure.org/nmap/index.html#download
- general cleanups, removed lots of commenrts since it madethe spec hard to
	read
- changed group to Applications/System
- quiet setup
- no need to create dirs in the install section, "make
	prefix=$RPM_BUILD_ROOT&{prefix} install" does this.
- using defined %%{prefix}, %%{version} etc. for easier/quicker maint.
- added docs
- gzip man pages
- strip after files have been installed into buildroot
- created separate package for the frontend so that Gtk+ isn't needed for the
	CLI nmap 
- not using -f in files section anymore, no need for it since there aren't that
	many files/dirs
- added desktop entry for gnome

* Sun Jan 10 1999 Fyodor <fyodor@dhp.com>
- Merged in spec file sent in by Ian Macdonald <ianmacd@xs4all.nl>

* Tue Dec 29 1998 Fyodor <fyodor@dhp.com>
- Made some changes, and merged in another .spec file sent in
  by Oren Tirosh <oren@hishome.net>

* Mon Dec 21 1998 Riku Meskanen <mesrik@cc.jyu.fi>
- initial build for RH 5.x
