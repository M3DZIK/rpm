# setting some global constants
%global appname pycharm

%global _name pycharm-community

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
%global _exclude_from %{_datadir}/%{_name}/bin/.*|%{_datadir}/%{_name}/lib/.*|%{_datadir}/%{_name}/plugins/.*|%{_datadir}/%{_name}/jbr/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    %{_name}-bin
Version: 2025.1.2
Release: 1%{?dist}
Summary: Intelligent Python IDE - Community
License: Apache-2.0
URL:     https://www.jetbrains.com/%{appname}/

Provides: pycharm-community

Source0: %{_name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem
BuildRequires: wget
BuildRequires: tar

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem
Requires:      %{_name}-jbr = %{version}-%{release}

%description
PyCharm is designed by programmers, for programmers, to provide all the tools you need for productive Python development.

%package jbr
Summary:  JetBrains Runtime
Requires: %{_name} = %{version}-%{release}

Conflicts: %{_name}-jbr

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="%{_name}-%{version}.tar.gz"
%else
download_file="%{_name}-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/python/$download_file"
mkdir "${download_file}.out"
tar xf "$download_file" -C "${download_file}.out"
mv "${download_file}.out"/*/* .

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix .
%else
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
# Installing application...
install -d %{buildroot}%{_datadir}/%{_name}
cp -arf ./{bin,jbr,lib,plugins,modules,build.txt,product-info.json} %{buildroot}%{_datadir}/%{_name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/%{_name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{_name}.svg

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{_name}/bin/%{appname} %{buildroot}%{_bindir}/%{_name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{_name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{_name}.desktop

%files
%license license/*
%{_datadir}/%{_name}/{bin,lib,plugins,modules,build.txt,product-info.json}
%{_bindir}/%{_name}
%{_datadir}/applications/%{_name}.desktop
%{_datadir}/pixmaps/%{_name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{_name}.svg

%files jbr
%{_datadir}/%{_name}/jbr

%changelog
* Wed Jun 11 2025 M3DZIK <me@medzik.dev> - 2025.1.2-1
- Update to 2025.1.2

* Thu May 15 2025 M3DZIK <me@medzik.dev> - 2025.1.1.1-1
- Update to 2025.1.1.1

* Thu May 08 2025 M3DZIK <me@medzik.dev> - 2025.1.1-1
- Update to 2025.1.1

* Wed Apr 16 2025 M3DZIK <me@medzik.dev> - 2025.1-1
- Update to 2025.1

* Wed Mar 19 2025 M3DZIK <me@medzik.dev> - 2024.3.5-1
- Update to 2024.3.5

* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.4-1
- Update to 2024.3.4

* Fri Feb 14 2025 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3

* Tue Jan 28 2025 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2

* Thu Dec 19 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1

* Thu Dec 12 2024 M3DZIK <me@medzik.dev> - 2024.3.1-1
- Update to 2024.3.1

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3

* Wed Oct 23 2024 M3DZIK <me@medzik.dev> - 2024.2.4-1
- Update to 2024.2.4

* Fri Sep 27 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3

* Fri Sep 20 2024 M3DZIK <me@medzik.dev> - 2024.2.2-1
- Update to 2024.2.2

* Thu Aug 29 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1

* Fri Aug 23 2024 M3DZIK <me@medzik.dev> - 2024.2.0.1-1
- Update to 2024.2.0.1

* Mon Aug 12 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2

* Fri Aug 09 2024 M3DZIK <me@medzik.dev> - 2024.1.6-1
- Update to 2024.1.6

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5

* Sat Jun 27 2024 M3DZIK <me@medzik.dev> - 2024.1.4-2
- Fix vmoptions file

* Fri Jun 26 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Migrated from `pycharm-community`
