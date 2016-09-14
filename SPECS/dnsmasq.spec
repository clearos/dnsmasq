%define testrelease 0
%define releasecandidate 0
%if 0%{testrelease}
  %define extrapath test-releases/
  %define extraversion test30
%endif
%if 0%{releasecandidate}
  %define extrapath release-candidates/
  %define extraversion rc5
%endif

%define _hardened_build 1

Name:           dnsmasq
Version:        2.66
Release:        14%{?extraversion}%{?dist}.1
Summary:        A lightweight DHCP/caching DNS server

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://www.thekelleys.org.uk/dnsmasq/
Source0:        http://www.thekelleys.org.uk/dnsmasq/%{?extrapath}%{name}-%{version}%{?extraversion}.tar.gz
Source1:        %{name}.service

#include upstream bug fix patches committed after stable release
# commit 4582c0efe7d7af93517b1f3bcc7af67685ab3e5c
Patch0:         %{name}-2.66-Fix-wrong_size_in_memset_call.patch
# commit bd08ae67f9a0cae2ce15be885254cad9449d4551
Patch1:         %{name}-2.66-Allow-option_number_zero_in_encapsulated_DHCP_options.patch
# commit 4b5ea12e90024ade5033b3b83a8b2620035952ba
Patch2:         %{name}-2.66-Send-TCP-DNS-messages-in-one-write-call.patch
# commit 797a7afba477390bc016c647cfb792c85ee6102d
Patch3:         %{name}-2.66-Fix-crash-on-SERVFAIL-when-using-conntrack.patch
# commit aa63a21ce0b20dfe988e0bcdf14b8b930de20311
Patch4:         %{name}-2.66-Fix-regression-in-dhcp_lease_time-utility.patch
# commit a66d36ea1112c861ad2f11ed40cc26973873e5be
Patch5:         %{name}-2.66-Manpage-typos.patch
# commit 1c10b9de118c951a5aedc130e55101987dcc3feb
Patch6:         %{name}-2.66-Note-that-dhcp_lease_time-and-dhcp_release-work-for-IPv4.patch
# commit 86e92f998379d219e10517dfa2c42f544ba164ce
Patch7:         %{name}-2.66-dhcp-match-now-work-with-BOOTP.patch
# commit 7abb69b5dc8dbe369be36bd7bf23c039b036acd1
Patch8:         %{name}-2.66-Tighten_checks_in_legal_hostname.patch
# commit ddd9a6b499ae601231070854c562611a79e004c0
Patch9:         %{name}-2.66-replace-inet_addr-with-inet_pton-in-option-c.patch
# commit b915f837c1db9b8b095158b41028ea71246d68d
Patch10:        %{name}-2.66-Use-dnsmasq-as-default-DNS-server-for-RA-only-if-it-is-doing-DNS.patch
# commit 3f2873d42c4d7e7dba32b6e64a3687d43928bc8e - Bug #962246
Patch11:        %{name}-2.66-Handle_IPv4_interface_address_labels_in_Linux.patch
# commit cfcad42ff1ddee8e64d120f18016a654152d0215 - Bug #962874
Patch12:        %{name}-2.66-Fix_failure_to_start_with_ENOTSOCK.patch
# commit 3e8ed78bf1b2649b13129327700d5d55bd2040e2
Patch13:        %{name}-2.66-Fix-option-parsing-for-dhcp-host.patch
# commit baa80ae5125beabd49edae2cdfaf3817a88a2ab6
Patch14:        %{name}-2.66-Remove-limit-in-prefix-length-in-auth-zone.patch
# commit 0da5e8979b5e5466d0f7bb836f2716cbcf1d4589
Patch15:        %{name}-2.66-Log-forwarding-table-overflows.patch
# commit 429805dbbc3888abc0d472c45935e92057964384
Patch16:        %{name}-2.66-Allow-constructed-ranges-from-interface-address-at-end-of-range.patch
# commit e2ba0df2d4798e52e188c2f7f74613867d5aa82a
Patch17:        %{name}-2.66-Dont-BIND-DHCP-socket-if-more-interfaces-may-come.patch
# commit 625ac28c61b0a5e6a252db00d72fbac6d88718fd
Patch18:        %{name}-2.66-Fix_crash_with_empty_DHCP_string_options.patch
# commit ffbad34b310ab2db6a686c85f5c0a0e52c0680c8
Patch19:        %{name}-2.66-Set-SOREUSEADDR-as-well-as-SOREUSEPORT-on-DHCP-socke.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1179756
Patch20:        %{name}-2.66-Support-IPv6-assignment-based-on-MAC-for-DHCPv6.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1232677
Patch21:        %{name}-2.66-dhcp-v4-v6.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1358427
Patch23:	%{name}-2.66-numeric-hostnames.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-devel
BuildRequires:  pkgconfig
BuildRequires:  libidn-devel

BuildRequires:  systemd
Requires(post): systemd systemd-sysv chkconfig
Requires(preun): systemd
Requires(postun): systemd


%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server.
It is designed to provide DNS and, optionally, DHCP, to a small network.
It can serve the names of local machines which are not in the global
DNS. The DHCP server integrates with the DNS server and allows machines
with DHCP-allocated addresses to appear in the DNS with names configured
either in each host or in a central configuration file. Dnsmasq supports
static and dynamic DHCP leases and BOOTP for network booting of diskless
machines.

%package        utils
Summary:        Utilities for manipulating DHCP server leases
Group:          System Environment/Daemons

%description    utils
Utilities that use the standard DHCP protocol to
query/remove a DHCP server's leases.


%prep
%setup -q -n %{name}-%{version}%{?extraversion}

%patch0 -p1 -b .wrong_size
%patch1 -p1 -b .zero_DHCP_option
%patch2 -p1 -b .tcp_dns_in_one_packet
%patch3 -p1 -b .SERVFAIL_crash
%patch4 -p1 -b .dhcp_lease_time-regression
%patch5 -p1
%patch6 -p1 -b .utils_work_only_ipv4
%patch7 -p1 -b .dhcp-match_bootp
%patch8 -p1 -b .hosname_checks
%patch9 -p1 -b .inet_pton
%patch10 -p1 -b .default_dns_server
%patch11 -p1 -b .interface_aliases
%patch12 -p1 -b .enotsock_failure
%patch13 -p1 -b .option_parsing
%patch14 -p1 -b .auth_zone_limit
%patch15 -p1 -b .log_overflow
%patch16 -p1 -b .constr_range
%patch17 -p1 -b .bindtodevice
%patch18 -p1 -b .empty_dhcp_opts
%patch19 -p1 -b .reuseport
%patch20 -p1
%patch21 -p1
%patch23 -p1

# use /var/lib/dnsmasq instead of /var/lib/misc
for file in dnsmasq.conf.example man/dnsmasq.8 man/es/dnsmasq.8 src/config.h; do
    sed -i 's|/var/lib/misc/dnsmasq.leases|/var/lib/dnsmasq/dnsmasq.leases|g' "$file"
done

#enable dbus
sed -i 's|/\* #define HAVE_DBUS \*/|#define HAVE_DBUS|g' src/config.h

#enable IDN support
sed -i 's|/\* #define HAVE_IDN \*/|#define HAVE_IDN|g' src/config.h

#enable /etc/dnsmasq.d fix bz 526703
sed -i 's|#conf-dir=/etc/dnsmasq.d|conf-dir=/etc/dnsmasq.d|g' dnsmasq.conf.example


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
make -C contrib/wrt %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
# normally i'd do 'make install'...it's a bit messy, though
mkdir -p $RPM_BUILD_ROOT%{_sbindir} \
        $RPM_BUILD_ROOT%{_mandir}/man8 \
        $RPM_BUILD_ROOT%{_var}/lib/dnsmasq \
        $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.d \
        $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install src/dnsmasq $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
install dnsmasq.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 $RPM_BUILD_ROOT%{_mandir}/man8/

# utils sub package
mkdir -p $RPM_BUILD_ROOT%{_bindir} \
         $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 contrib/wrt/dhcp_release $RPM_BUILD_ROOT%{_bindir}/dhcp_release
install -m 644 contrib/wrt/dhcp_release.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_release.1
install -m 755 contrib/wrt/dhcp_lease_time $RPM_BUILD_ROOT%{_bindir}/dhcp_lease_time
install -m 644 contrib/wrt/dhcp_lease_time.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_lease_time.1

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post dnsmasq.service

%preun
%systemd_preun dnsmasq.service

%postun
%systemd_postun_with_restart dnsmasq.service

%triggerun -- dnsmasq < 2.52-3
%{_bindir}/systemd-sysv-convert --save dnsmasq >/dev/null 2>&1 ||:
/sbin/chkconfig --del dnsmasq >/dev/null 2>&1 || :
/bin/systemctl try-restart dnsmasq.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING FAQ doc.html setup.html dbus/DBus-interface
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dnsmasq.conf
%dir /etc/dnsmasq.d
%dir %{_var}/lib/dnsmasq
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/dnsmasq.conf
%{_unitdir}/%{name}.service
%{_sbindir}/dnsmasq
%{_mandir}/man8/dnsmasq*

%files utils
%{_bindir}/dhcp_*
%{_mandir}/man1/dhcp_*

%changelog
* Tue Aug 30 2016 Pavel Šimerda <pavlix@pavlix.net> - 2.66-14.1
- Resolves: #1371460 - dhcp errors with hostnames beginning with numbers

* Thu Jun 25 2015 Pavel Šimerda <psimerda@redhat.com> - 2.66-14
- Resolves: #1232677 - handle IPv4 and IPv6 host entries properly

* Wed Feb 25 2015 Pavel Šimerda <psimerda@redhat.com> - 2.66-13
- Resolves: #1179756 - dnsmasq does not support MAC address based matching for
  IPv6

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.66-12
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.66-11
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Tomas Hozza <thozza@redhat.com> - 2.66-10
- Use SO_REUSEPORT and SO_REUSEADDR if possible for DHCPv4/6 (#981973)

* Mon Aug 12 2013 Tomas Hozza <thozza@redhat.com> - 2.66-9
- Don't use SO_REUSEPORT on DHCPv4 socket to prevent conflicts with ISC DHCP (#981973)

* Tue Jul 23 2013 Tomas Hozza <thozza@redhat.com> - 2.66-8
- Fix crash when specified empty DHCP option

* Tue Jun 11 2013 Tomas Hozza <thozza@redhat.com> - 2.66-7
- use _hardened_build macro instead of hardcoded flags
- include several fixies from upstream repo:
  - Allow constructed ranges from interface address at end of range
  - Dont BINDTODEVICE DHCP socket if more interfaces may come
  - Fix option parsing for dhcp host
  - Log forwarding table overflows
  - Remove limit in prefix length in auth zone

* Fri May 17 2013 Tomas Hozza <thozza@redhat.com> - 2.66-6
- include several fixies from upstream repo:
  - Tighten hostname checks in legal hostname() function
  - Replace inet_addr() with inet_pton() in src/option.c
  - Use dnsmasq as default DNS server for RA only if it's doing DNS
  - Handle IPv4 interface address labels (aliases) in Linux (#962246)
  - Fix failure to start with ENOTSOCK (#962874)

* Tue Apr 30 2013 Tomas Hozza <thozza@redhat.com> - 2.66-5
- dnsmasq unit file cleanup
  - drop forking Type and PIDfile and rather start dnsmasq with "-k" option
  - drop After syslog.target as this is by default

* Thu Apr 25 2013 Tomas Hozza <thozza@redhat.com> - 2.66-4
- include several fixes from upstream repo:
  - Send TCP DNS messages in one packet
  - Fix crash on SERVFAIL when using --conntrack option
  - Fix regression in dhcp_lease_time utility
  - Man page typos fixes
  - Note that dhcp_lease_time and dhcp_release work only for IPv4
  - Fix for --dhcp-match option to work also with BOOTP protocol

* Sat Apr 20 2013 Tomas Hozza <thozza@redhat.com> - 2.66-3
- Use Full RELRO when linking the daemon
- compile the daemon with PIE
- include two fixes from upstream git repo

* Thu Apr 18 2013 Tomas Hozza <thozza@redhat.com> - 2.66-2
- New stable version dnsmasq-2.66
- Drop of merged patch

* Fri Apr 12 2013 Tomas Hozza <thozza@redhat.com> - 2.66-1.rc5
- Update to latest dnsmasq-2.66rc5
- Include fix for segfault when lease limit is reached

* Fri Mar 22 2013 Tomas Hozza <thozza@redhat.com> - 2.66-1.rc1
- Update to latest dnsmasq-2.66rc1
- Dropping unneeded patches
- Enable IDN support

* Fri Mar 15 2013 Tomas Hozza <thozza@redhat.com> - 2.65-5
- Allocate dhcp_buff-ers also if daemon->ra_contexts to prevent SIGSEGV (#920300)

* Thu Jan 31 2013 Tomas Hozza <thozza@redhat.com> - 2.65-4
- Handle locally-routed DNS Queries (#904940)

* Thu Jan 24 2013 Tomas Hozza <thozza@redhat.com> - 2.65-3
- build dnsmasq with $RPM_OPT_FLAGS, $RPM_LD_FLAGS explicitly (#903362) 

* Tue Jan 22 2013 Tomas Hozza <thozza@redhat.com> - 2.65-2
- Fix for CVE-2013-0198 (checking of TCP connection interfaces) (#901555)

* Sat Dec 15 2012 Tomas Hozza <thozza@redhat.com> - 2.65-1
- new version 2.65

* Wed Dec 05 2012 Tomas Hozza <thozza@redhat.com> - 2.64-1
- New version 2.64
- Merged patches dropped

* Tue Nov 20 2012 Tomas Hozza <thozza@redhat.com> - 2.63-4
- Remove EnvironmentFile from service file (#878343)

* Mon Nov 19 2012 Tomas Hozza <thozza@redhat.com> - 2.63-3
- dhcp6 support fixes (#867054)
- removed "-s $HOSTNAME" from .service file (#753656, #822797)

* Tue Oct 23 2012 Tomas Hozza <thozza@redhat.com> - 2.63-2
- Introduce new systemd-rpm macros in dnsmasq spec file (#850096)

* Thu Aug 23 2012 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.63-1
- Use .tar.gz compression, in upstream site there is no .lzma anymore
- New version 2.63

* Sat Feb 11 2012 Pádraig Brady <P@draigBrady.com> - 2.59-5
- Compile DHCP lease management utils with RPM_OPT_FLAGS

* Thu Feb  9 2012 Pádraig Brady <P@draigBrady.com> - 2.59-4
- Include DHCP lease management utils in a subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-2
- do not enable service by default

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-1
- New version 2.59
- Fix regression in 2.58 (IPv6 issue) - bz 744814

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.58-1
- Fixed License
- New version 2.58

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-5
- Include systemd unit file

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-3
- Applied Jóhann's patch, minor cleanup

* Tue Jul 26 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 2.52-3
- Introduce systemd unit file, drop SysV support

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 26 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.52-1
- New Version 2.52
- fix condrestart() in initscript bz 547605
- fix sed to enable DBUS(the '*' need some escaping) bz 553161

* Sun Nov 22 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-2
- fix bz 512664

* Sat Oct 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-1
- move initscript from patch to a plain text file
- drop (dnsmasq-configuration.patch) and use sed instead
- enable /etc/dnsmasq.d fix bz 526703
- change requires to package name instead of file
- new version 2.51

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2.48-4
- Fix multiple TFTP server vulnerabilities (CVE-2009-2957, CVE-2009-2958)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.48-3
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.48-1
- Bugfix/feature enhancement update
- Fixing BZ#494094

* Fri May 29 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.47-1
- Bugfix/feature enhancement update

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matěj Cepl <mcepl@redhat.com> - 2.45-2
- rebuilt

* Mon Jul 21 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.45-1
- Upstream release (bugfixes)

* Wed Jul 16 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.43-2
- New upstream release, contains fixes for CVE-2008-1447/CERT VU#800113
- Dropped patch for newer glibc (merged upstream)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.8
- Added upstream-authored patch for newer glibc (thanks Simon!)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.7
- New upstream release

* Wed Jan 30 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.6.rc1
- Release candidate
- Happy Birthday Isaac!

* Wed Jan 23 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.5.test30
- Bugfix update

* Mon Dec 31 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.4.test26
- Bugfix/feature enhancement update

* Thu Dec 13 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.3.test24
- Upstream fix for fairly serious regression

* Tue Dec 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.2.test20
- New upstream test release
- Moving dnsmasq.leases to /var/lib/dnsmasq/ as per BZ#407901
- Ignoring dangerous-command-in-%%post rpmlint warning (as per above fix)
- Patch consolidation/cleanup
- Removed conditionals for Fedora <= 3 and Aurora 2.0

* Tue Sep 18 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-1
- Finalized upstream release
- Removing URLs from patch lines (CVS is the authoritative source)
- Added more magic to make spinning rc/test packages more seamless

* Sun Aug 26 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-0.1.rc2
- New upstream release candidate (feature-frozen), thanks Simon!
- License clarification

* Tue May 29 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.39-1
- New upstream version (bugfixes, enhancements)

* Mon Feb 12 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.38-1
- New upstream version with bugfix for potential hang

* Tue Feb 06 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.37-1
- New upstream version

* Wed Jan 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.36-1
- New upstream version

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-2
- Stop creating /etc/sysconfig on %%install
- Create /etc/dnsmasq.d on %%install

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-1
- Update to 2.35
- Removed UPGRADING_to_2.0 from %%doc as per upstream change
- Enabled conf-dir in default config as per RFE BZ#214220 (thanks Chris!)
- Added %%dir /etc/dnsmasq.d to %%files as per above RFE

* Tue Oct 24 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-2
- Fixed BZ#212005
- Moved %%postun scriptlet to %%post, where it made more sense
- Render scriptlets safer
- Minor cleanup for consistency

* Thu Oct 19 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-1
- Hardcoded version in patches, as I'm getting tired of updating them
- Update to 2.34

* Mon Aug 28 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-2
- Rebuild for FC6

* Tue Aug 15 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-1
- Update

* Sat Jul 22 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-3
- Added pkgconfig BuildReq due to reduced buildroot

* Thu Jul 20 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-2
- Forced update due to dbus version bump

* Mon Jun 12 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-1
- Update from upstream
- Patch from Dennis Gilmore fixed the conditionals to detect Aurora Linux

* Mon May  8 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.31-1
- Removed dbus config patch (now provided upstream)
- Patched in init script (no longer provided upstream)
- Added DBus-interface to docs

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4.2
- More upstream-recommended cleanups :)
- Killed sysconfig file (provides unneeded functionality)
- Tweaked init script a little more

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4
- Moved options out of init script and into /etc/sysconfig/dnsmasq
- Disabled DHCP_LEASE in sysconfig file, fixing bug #190379
- Simon Kelley provided dbus/dnsmasq.conf, soon to be part of the tarball

* Thu Apr 27 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-3
- Un-enabled HAVE_ISC_READER, a hack to enable a deprecated feature (request)
- Split initscript & enable-dbus patches, conditionalized dbus for FC3
- Tweaked name field in changelog entries (trying to be consistent)

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-2
- Disabled stripping of binary while installing (oops)
- Enabled HAVE_ISC_READER/HAVE_DBUS via patch
- Added BuildReq for dbus-devel

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-1
- Initial Fedora Extras RPM
