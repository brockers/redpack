%global debug_package %{nil}
%global _enable_debug_package 0

# If no build number is specified default to local
%{!?BUILD_NUMBER: %define BUILD_NUMBER local}

Name:           --name--
Version:        --version--
Release:        %{BUILD_NUMBER}
Summary:        --description--

License:        --license--
URL:            --homepage--
Source0:        --homepage--/%{name}-%{version}.tar.bz2

BuildRequires:  yum-utils rpmdevtools redhat-rpm-config

Requires:       nodejs nginx systemd policycoreutils-python-utils
Requires(post): systemd
Requires(pre):  shadow-utils
Requires(preun): systemd
Requires(postun): shadow-utils systemd

# Our default install locations
%define config_dir /etc/%{name}
%define cron_dir /etc/cron.hourly
%define install_dir /opt/%{name}
%define service_dir /etc/systemd/system

%description
--description--

%pre
/usr/bin/getent group %{name} > /dev/null || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} > /dev/null || /usr/sbin/useradd -r -g %{name} -d %{install_dir} -s /sbin/nologin %{name}

%prep
%setup -q

%build
# No compile build required

%install
# Clean out everything that used to be in build root
rm -rf $RPM_BUILD_ROOT

#/ Get rid of testing node modules that we do not want in production
%{__rm} -rf ./node_modules/angular-mocks*
%{__rm} -rf ./node_modules/chai*
%{__rm} -rf ./node_modules/istanbul*
%{__rm} -rf ./node_modules/jasmine*
%{__rm} -rf ./node_modules/karma*
%{__rm} -rf ./node_modules/mocha*
%{__rm} -rf ./node_modules/mock-*
%{__rm} -rf ./node_modules/protractor*
%{__rm} -rf ./node_modules/selenium*
%{__rm} -rf ./node_modules/supertest*

# Create our target directories
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{config_dir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{cron_dir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{install_dir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{proxy_dir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{service_dir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%_sysconfdir

# Special configuration scripts for systemd and nginx
%{__mv} ./config/systemd/%{name}.service $RPM_BUILD_ROOT%{service_dir}/%{name}.service
%{__mv} ./config/etc/%{name}.conf $RPM_BUILD_ROOT%{config_dir}/%{name}.conf
%{__mv} ./config/cron.hourly/%{name}.cron $RPM_BUILD_ROOT%{cron_dir}/%{name}.cron
%{__mv} ./config/nginx $RPM_BUILD_ROOT%_sysconfdir/nginx

# Now move production files into their locations
%{__mv} ./* $RPM_BUILD_ROOT%{install_dir}/

# Here is our release number getting populated by our build system
echo %{BUILD_NUMBER} > $RPM_BUILD_ROOT%{install_dir}/BUILD_NUMBER

%post
%systemd_post %{name}.service

# Seriously, there has to be a better way to deal with selinux than this shit
semanage fcontext -a -t httpd_sys_content_t "/opt/%{name}(/.*)?"
restorecon -R -v /opt
restorecon -R -v /etc
setsebool -P httpd_can_network_connect 1

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{name},%{name},-)
%doc README.md
%config %{service_dir}/%{name}.service
%config(noreplace) %{config_dir}/%{name}.conf
%{install_dir}/*
%{cron_dir}/%{name}.cron
%_sysconfdir/nginx/default.d/%{name}.conf
%_sysconfdir/nginx/conf.d/%{name}.conf

%changelog
* --changelog.date-- --author.name-- --version--
- Log message goes here
