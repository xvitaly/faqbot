Name: faqbot
Version: 1.0.0
Release: 1%{?dist}

Summary: FAQ bot for the Telegram Messenger
License: GPLv3+
URL: https://github.com/xvitaly/%{name}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: doxygen
BuildRequires: systemd
BuildRequires: python3-devel
BuildRequires: python3dist(pytelegrambotapi)
BuildRequires: python3dist(requests)
BuildRequires: python3dist(wheel)
BuildRequires: python3dist(six)

%{?python_enable_dependency_generator}
Requires(pre): shadow-utils

%{?systemd_requires}
%{?python_provide:%python_provide python3-%{name}}

%description
EC AntiSpam bot for Telegram messenger will block all multimedia
messages and links from new users, block some common spam bots and
users who added them to super-groups.

%prep
%autosetup -n %{name}-%{version} -p1
sed -e 's@"logtofile": "",@"logtofile": "%{_localstatedir}/log/%{name}/%{name}.log",@g' -i config/%{name}.json

%build
doxygen
%py3_build

%install
%py3_install

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -p -m 0644 config/%{name}.json %{buildroot}%{_sysconfdir}/%{name}
install -p -m 0644 config/%{name}-env.conf %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 0644 config/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 config/%{name}.service %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_localstatedir}/log
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

%check
%{__python3} setup.py test

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d /dev/null -s /sbin/nologin \
  -c "%{name} service account" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md doxyout/html
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-*.egg-info
%dir %{_sysconfdir}/%{name}
%dir %attr(-,%{name},root) %{_sharedstatedir}/%{name}
%attr(-,%{name},root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.json
%attr(0640,root,%{name}) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-env.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,%{name},root) %dir %{_localstatedir}/log/%{name}
%ghost %{_localstatedir}/log/%{name}/*.log*
%ghost %{_sharedstatedir}/%{name}/%{name}.db
%{_unitdir}/%{name}.service

%changelog
* Mon May 25 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.0-1
- Updated to version 1.0.0.
