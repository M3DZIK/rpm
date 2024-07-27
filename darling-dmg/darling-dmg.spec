%global debug_package %{nil}
%global _build_id_links none

%global _lib %{_prefix}/lib

%global git_commit a36bf0c07b16675b446377890c5f6f74563f84dd

Name:    darling-dmg
Version: 0.0.0.179.a36bf0c07b16675b446377890c5f6f74563f84dd
Release: 1%{?dist}
Summary: FUSE module for .dmg files (containing an HFS+ filesystem) 
License: GPL-3
URL:     https://www.darlinghq.org/

Source0: https://github.com/darlinghq/%{name}/archive/%{git_commit}.tar.gz

BuildRequires: git
BuildRequires: make
BuildRequires: cmake
BuildRequires: clang
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(bzip2)
BuildRequires: libicu-devel

%description
%{summary}.

%prep
%setup -q -n %{name}-%{git_commit}

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_lib}/libdmg.so
%{_bindir}/%{name}

%changelog
* Sat Jul 27 2024 M3DZIK <me@medzik.dev> - 0.0.0.179.a36bf0c07b16675b446377890c5f6f74563f84dd-1
- Update to 0.0.0.179.a36bf0c07b16675b446377890c5f6f74563f84dd

* Sat Jul 27 2024 M3DZIK <me@medzik.dev> - 0.0.0-1
- Initial release
