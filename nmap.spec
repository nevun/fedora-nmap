Summary: Network exploration tool and security scanner
Name: nmap
Version: 2.54BETA22
Release: 2
Copyright: GPL
Group: Applications/System
Source0: http://www.insecure.org/nmap/%{name}-%{version}.tgz
Source1: nmapfe.desktop
Patch0: inet_aton.patch
Patch1: makefile.patch
URL: http://www.insecure.org/nmap/
BuildRoot: %{_tmppath}/%{name}-root

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
Requires: nmap = %{PACKAGE_VERSION} , gtk+
%description frontend
This package includes nmapfe, a Gtk+ frontend for nmap. The nmap package must
be installed before installing nmap-frontend.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall nmapdatadir=$RPM_BUILD_ROOT%{_datadir}/nmap

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/Utilities/
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/Utilities/

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc COPYING
%doc docs/README docs/copying.html docs/nmap-fingerprinting-article.txt
%doc docs/nmap.deprecated.txt docs/nmap.usage.txt docs/nmap_doc.html
%doc docs/nmap_manpage.html 
%{_bindir}/nmap
%{_datadir}/nmap
%{_mandir}/man1/nmap.1.gz

%files frontend
%defattr(-,root,root)
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_sysconfdir}/X11/applnk/Utilities/nmapfe.desktop
%{_mandir}/man1/nmapfe.1.gz
%{_mandir}/man1/xnmap.1.gz

%changelog
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
- use %configure, and %{_prefix} where possible
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
- using defined %{prefix}, %{version} etc. for easier/quicker maint.
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
