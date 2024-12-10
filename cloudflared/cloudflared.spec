# disable debuginfo subpackage
%global debug_package %{nil}

Name:          cloudflared
Version: 2024.12.0
Release: 1%{?dist}
Summary:       Cloudflare Tunnel client (formerly Argo Tunnel)
License:       Apache-2.0
URL:           https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/

Source0:       https://github.com/cloudflare/cloudflared/archive/%{version}.tar.gz

BuildRequires: git
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
* Tue Dec 10 2024 M3DZIK <me@medzik.dev> - 2024.12.0-1
- Update to 2024.12.0

* Tue Nov 19 2024 M3DZIK <me@medzik.dev> - 2024.11.1-1
- Update to 2024.11.1

* Wed Nov 06 2024 M3DZIK <me@medzik.dev> - 2024.11.0-1
- Update to 2024.11.0

* Thu Oct 24 2024 M3DZIK <me@medzik.dev> - 2024.10.1-1
- Update to 2024.10.1

* Thu Oct 10 2024 M3DZIK <me@medzik.dev> - 2024.10.0-1
- Update to 2024.10.0

* Tue Sep 10 2024 M3DZIK <me@medzik.dev> - 2024.9.1-1
- Update to 2024.9.1

* Tue Sep 10 2024 M3DZIK <me@medzik.dev> - 2024.9.0-1
- Update to 2024.9.0

* Thu Aug 22 2024 M3DZIK <me@medzik.dev> - 2024.8.3-1
- Update to 2024.8.3

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.8.2-1
- Update to 2024.8.2

* Tue Jun 18 2024 M3DZIK <me@medzik.dev> - 2024.6.1-1
- Update to 2024.6.1

* Tue Jun 04 2024 M3DZIK <me@medzik.dev> - 2024.6.0-1
- Update to 2024.6.0

* Thu May 16 2024 M3DZIK <me@medzik.dev> - 2024.5.0-1
- Update to 2024.5.0

* Tue Apr 23 2024 M3DZIK <me@medzik.dev> - 2024.4.1-1
- Update to 2024.4.1

* Wed Apr 10 2024 M3DZIK <me@medzik.dev> - 2024.4.0-1
- Update to 2024.4.0

* Sat Mar 23 2024 M3DZIK <me@medzik.dev> - 2024.3.0-3
- Fixed cloudflared

* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 2024.3.0-1
- Initial release
