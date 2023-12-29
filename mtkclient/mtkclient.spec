# disable debuginfo subpackage
%global debug_package %{nil}

Name:          mtkclient
Version:       1.63
Release:       2%{?dist}
Summary:       MTK reverse engineering and flash tool
URL:           https://github.com/bkerler/mtkclient
License:       GPLv3
BuildArch:     noarch

Source0:       https://github.com/bkerler/mtkclient/archive/%{version}.tar.gz
Patch0:        remove-requirements.patch

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

%description
Unofficial MTK reverse engineering and flash tool

%generate_buildrequires
%pyproject_buildrequires

%prep
%setup -q -n mtkclient-%{version}
%patch 0 -p1

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files '*' +auto

%files -f %{pyproject_files}
%license LICENSE

%changelog
* Thu Dec 21 2023 M3DZIK <me@medzik.dev> - 1.63.r46.g2f4eb98-1
- Update to 1.63.r46.g2f4eb98

* Fri Dec 15 2023 M3DZIK <me@medzik.dev> - 1.63.r45.g48f7be9-1
- Update to 1.63.r45.g48f7be9

* Sat Dec 02 2023 M3DZIK <me@medzik.dev> - 1.63.r42.ga9f2223-1
- Update to 1.63.r42.ga9f2223

* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 1.63.r39.gd1ca2d6
- Initial release
