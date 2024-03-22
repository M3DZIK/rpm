# disable debuginfo subpackage
%global debug_package %{nil}

Name:          cloudflared
Version:       2024.3.0
Release:       1%{?dist}
Summary:       Cloudflare Tunnel client (formerly Argo Tunnel)
License:       Apache-2.0
URL:           https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/

Source0:       https://github.com/cloudflare/cloudflared/archive/%{version}.tar.gz

BuildRequires: golang

%description
A command-line client for Cloudflare Tunnel, a tunneling daemon that proxies traffic from the Cloudflare network to your origins.

%prep
%setup -q -n %{name}-%{version}

%build
make cloudflared cloudflared.1

%install
install -d %{buildroot}%{_bindir}
cp -af -p %{name} %{buildroot}%{_bindir}

install -d %{buildroot}%{_mandir}
install -m 0644 -p %{name}.1 %{buildroot}%{_mandir}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 2024.3.0
- Initial release
