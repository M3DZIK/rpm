%global debug_package %{nil}
%global _build_id_links none

%global _git_tag master

%global _lib %{_prefix}/lib

Name:    darling-dmg
Version: 0.0.0
Release: 1%{?dist}
Summary: FUSE module for .dmg files (containing an HFS+ filesystem) 
License: GPL-3
URL:     https://www.darlinghq.org/

Source0: https://github.com/darlinghq/%{name}/archive/%{_git_tag}.tar.gz

BuildRequires: git
BuildRequires: make
BuildRequires: cmake
BuildRequires: clang
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(fuse)
BuildRequires: libicu-devel

%description
%{summary}.

%prep
%setup -q -n %{name}-%{_git_tag}

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
* Sat Jul 27 2024 M3DZIK <me@medzik.dev> - 0.0.0-1
- Initial release
