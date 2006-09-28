Summary:	sawdog
Name:		sawdog
Version:	2.4
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://open.digicomp.ch/gpl/sawdog/download/%{name}-%{version}.tar.gz
# Source0-md5:	d98d60a7b16d9333b2d716eee454ddb9
URL:		http://open.digicomp.ch/gpl/sawdog/
Requires:	expect
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sawdog (Simple Active Watch-DOG) is a suite of scripts that informs
the system operators of mission critical servers in the case of a
failure. A set of small executables (i.e. expect scripts) are
executed, and if one executable fails, it sends an email or an SMS to
the sysop. There are 3 states known to sawdog: alive, unknown, and
dead. Only certain state transitions trigger a notification. On a Web
interface, the states of all hosts are visible. So far, there are
scripts to check for DNS, FTP, HTTP, HTTPS, ICMP, IMAP, MS SQL, MySQL,
Notes, NTP, POP3, PostgreSQL, SMB, SMTP, SNMP, SSH, telnet, TWS, VNM,
and Webmin.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/var/sawdog
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sawdog
install -d $RPM_BUILD_ROOT/home/services/httpd/html/sawdog

install sawdog.pl $RPM_BUILD_ROOT%{_bindir}
for i in `ls -1 services/`; do install services/$i $RPM_BUILD_ROOT%{_bindir}/sawdog.$i ; done
install sawdog.conf $RPM_BUILD_ROOT%{_sysconfdir}/sawdog
cp -r www $RPM_BUILD_ROOT/home/services/httpd/html/sawdog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README

%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sawdog/sawdog.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /home/services/httpd/html/*
