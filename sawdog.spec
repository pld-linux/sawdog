Summary:	sawdog - suite of server monitoring scripts
Summary(pl):	sawdog - zestaw skryptów monitoruj±cych serwery
Name:		sawdog
Version:	2.4
Release:	0.3
License:	GPL v2
Group:		Applications
Source0:	http://open.digicomp.ch/gpl/sawdog/download/%{name}-%{version}.tar.gz
# Source0-md5:	d98d60a7b16d9333b2d716eee454ddb9
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
URL:		http://open.digicomp.ch/gpl/sawdog/
Requires:	expect
Requires:	perl-base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sawdogdir	/usr/share/sawdog
%define		_sysconfdir	/etc/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Sawdog (Simple Active Watch-DOG) is a suite of scripts that informs
the system operators of mission critical servers in the case of a
failure. A set of small executables (i.e. expect scripts) are
executed, and if one executable fails, it sends an email or an SMS to
the sysop.

There are 3 states known to sawdog: alive, unknown, and dead. Only
certain state transitions trigger a notification. On a Web interface,
the states of all hosts are visible.

So far, there are scripts to check for DNS, FTP, HTTP, HTTPS, ICMP,
IMAP, MS SQL, MySQL, Notes, NTP, POP3, PostgreSQL, SMB, SMTP, SNMP,
SSH, telnet, TWS, VNM, and Webmin.

%description -l pl
Sawdog (prosty aktywny watchdog) to zestaw skryptów informuj±cych
operatorów systemów o usterce serwerów krytycznych dla dzia³ania
projektu. Je¿eli jeden z zestawu ma³ych plików wykonywalnych (n.p.
skryptów expect) zwróci b³±d, wysy³any jest email lub SMS to
operatora.

Sawdog okre¶la stan maszyny na trzy sposoby: sprawny, nieznany,
niesprawny. Powiadomienie jest wysy³ane tylko przy z góry okre¶lonym
przej¶ciu z jednego stanu do drugiego. Za pomoc± interfejsu www
mo¿liwy jest podgl±d stanów wszystkich dostêpnych maszyn.

Na chwilê obecn± sawdog posiada skrypt do sprawdzania us³ug DNS, FTP.
HTTP, HTTPS, ICMP, IMAP, MS SQL, MySQL, NTP, POP3, PostgreSQL, SMB,
SMTP, SNMP, SSH, telnet, TWS, VNM oraz webmin.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/var/sawdog
install -d $RPM_BUILD_ROOT/var/log
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sawdog
install -d $RPM_BUILD_ROOT%{sawdogdir}

install sawdog.pl $RPM_BUILD_ROOT%{_bindir}
for i in `ls -1 services/`; do install services/$i $RPM_BUILD_ROOT%{_bindir}/sawdog.$i ; done
install sawdog.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -r www/* $RPM_BUILD_ROOT%{sawdogdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
> $RPM_BUILD_ROOT/var/log/sawdog.log

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README

%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sawdog.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{sawdogdir}/*
%{sawdogdir}/config.php

%dir /var/sawdog
%dir /var/log
%ghost %attr(770,root,http) /var/log/sawdog.log
