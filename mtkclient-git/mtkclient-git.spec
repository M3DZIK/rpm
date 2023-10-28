# disable debuginfo subpackage
%global debug_package %{nil}

%global git_commit d1ca2d6554d346a9cb6d9581b8299e1b3ce70344

Name:          mtkclient-git
Version:       1.63.r39.gd1ca2d6
Release:       1%{?dist}
Summary:       MTK reverse engineering and flash tool
URL:           https://github.com/bkerler/mtkclient
License:       GPLv3
BuildArch:     noarch

Source0:       https://github.com/bkerler/mtkclient/archive/%{git_commit}.tar.gz
Patch0:        remove-data-files.patch
Patch1:        remove-gui-requirements.patch

BuildRequires: python3-devel
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-setuptools
BuildRequires: python3-wheel

%description
Unofficial MTK reverse engineering and flash tool

%prep
%setup -q -n mtkclient-%{git_commit}
%setup -q -n mtkclient-main
%patch0 -p1
%patch1 -p1

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir="%{buildroot}" dist/*.whl

%files
%license LICENSE
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 1.63.r39.gd1ca2d6
- Initial release
