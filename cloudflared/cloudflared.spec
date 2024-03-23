# disable debuginfo subpackage
%global debug_package %{nil}

Name:          cloudflared
Version:       2024.3.0
Release:       4%{?dist}
Summary:       Cloudflare Tunnel client (formerly Argo Tunnel)
License:       Apache-2.0
URL:           https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/

Source0:       https://github.com/cloudflare/cloudflared/archive/%{version}.tar.gz

BuildRequires: golang

%description
A command-line client for Cloudflare Tunnel, a tunneling daemon that proxies traffic from the Cloudflare network to your origins.

%prep
%setup -q -n %{name}-%{version}

%install
make install \
    VERSION=%{version} \
    DATE=$(date -u +"%Y-%m-%dT%H:%M") \
    PACKAGE_MANAGER=dnf \
    PREFIX=%{buildroot} \
    INSTALL_BINDIR=%{buildroot}%{_bindir} \
    INSTALL_MANDIR=%{buildroot}%{_mandir}

%files
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/%{name}.1

%changelog
* Sat Mar 23 2024 M3DZIK <me@medzik.dev> - 2024.3.0-3
- Fixed cloudflared

* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 2024.3.0-1
- Initial release
