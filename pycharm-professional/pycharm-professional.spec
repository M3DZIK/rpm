# setting some global constants
%global appname pycharm

# disable debuginfo subpackage
%global debug_package %{nil}
# Disable build-id symlinks to avoid conflicts
%global _build_id_links none
# don't strip bundled binaries because pycharm checks length (!!!) of binary fsnotif
# and if you strip debug stuff from it, it will complain
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# disable rpath checks
%define __brp_check_rpaths %{nil}
# there are some python 2 and python 3 scripts so there is no way out to bytecompile them ^_^
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global __provides_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*
%global __requires_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*

Name:          pycharm-professional
Version:       2024.1.4
Release:       1%{?dist}
Summary:       Intelligent Python IDE - Professional
License:       Commercial
URL:           https://www.jetbrains.com/%{appname}/

Source0:       source-info.txt

Source101:     %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem

%description
PyCharm is designed by programmers, for programmers, to provide all the tools you need for productive Python development.

%prep
%ifarch x86_64
wget -q https://download.jetbrains.com/python/%{name}-%{version}.tar.gz
tar xf %{name}-%{version}.tar.gz
%else
wget -q https://download.jetbrains.com/python/%{name}-%{version}-aarch64.tar.gz
tar xf %{name}-%{version}-aarch64.tar.gz
%endif

cd %{appname}-%{version}

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix .
%else
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
cd %{name}-%{version}

# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,build.txt,product-info.json} %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/%{appname}.sh %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license %{name}-%{version}/license/*
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Tue Jun 25 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Update to 2024.1.4

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.3-1
- Update to 2024.1.3

* Wed May 29 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Update to 2024.1.2

* Tue Apr 30 2024 M3DZIK <me@medzik.dev> - 2024.1.1-1
- Update to 2024.1.1

* Thu Apr 04 2024 M3DZIK <me@medzik.dev> - 2024.1-1
- Update to 2024.1

* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 2023.3.5-1
- Update to 2023.3.5

* Tue Feb 27 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4

* Tue Feb 20 2024 M3DZIK <me@medzik.dev> - 2023.3.3-1
- Update to 2023.3.3

* Fri Dec 22 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3

* Wed Nov 15 2023 M3DZIK <me@medzik.dev> - 2023.2.5-1
- Update to 2023.2.5

* Tue Nov 07 2023 M3DZIK <me@medzik.dev> - 2023.2.4
- Update to 2023.2.4

* Sun Oct 15 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3

* Wed Oct 04 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Update to 2023.2.2

* Sat Sep 02 2023 M3DZIK <me@medzik.dev> - 2023.2.1
- Initial release
