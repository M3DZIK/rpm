# setting some global constants
%global appname rider

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
%global _exclude_from %{_datadir}/%{name}/bin/.*|%{_datadir}/%{name}/lib/.*|%{_datadir}/%{name}/plugins/.*|%{_datadir}/%{name}/jbr/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    rider
Version: 2025.1.2
Release: 1%{?dist}
Summary: Fast & powerful, cross platform .NET IDE
License: Commercial
URL:     https://www.jetbrains.com/%{appname}/

Source0: %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem
BuildRequires: wget
BuildRequires: tar

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem
Requires:      %{name}-jbr = %{version}-%{release}

%description
Rider supports .NET Framework, the new cross-platform .NET Core, and Mono based projects.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="JetBrains.Rider-%{version}.tar.gz"
%else
download_file="JetBrains.Rider-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/rider/$download_file"
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
install -d %{buildroot}%{_datadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,modules,build.txt,product-info.json} %{buildroot}%{_datadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/%{appname} %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_datadir}/%{name}/{bin,lib,plugins,modules,build.txt,product-info.json}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files jbr
%{_datadir}/%{name}/jbr

%changelog
* Thu May 08 2025 M3DZIK <me@medzik.dev> - 2025.1.2-1
- Update to 2025.1.2

* Mon Apr 28 2025 M3DZIK <me@medzik.dev> - 2025.1.1-1
- Update to 2025.1.1

* Wed Apr 16 2025 M3DZIK <me@medzik.dev> - 2025.1-1
- Update to 2025.1

* Thu Apr 03 2025 M3DZIK <me@medzik.dev> - 2024.3.7-1
- Update to 2024.3.7

* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.6-1
- Update to 2024.3.6

* Fri Feb 07 2025 M3DZIK <me@medzik.dev> - 2024.3.5-1
- Update to 2024.3.5

* Thu Jan 23 2025 M3DZIK <me@medzik.dev> - 2024.3.4-1
- Update to 2024.3.4

* Tue Dec 24 2024 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3

* Wed Dec 11 2024 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3

* Thu Oct 24 2024 M3DZIK <me@medzik.dev> - 2024.2.7-1
- Update to 2024.2.7

* Thu Oct 10 2024 M3DZIK <me@medzik.dev> - 2024.2.6-1
- Update to 2024.2.6

* Fri Sep 20 2024 M3DZIK <me@medzik.dev> - 2024.2.5-1
- Update to 2024.2.5

* Mon Sep 09 2024 M3DZIK <me@medzik.dev> - 2024.2.4-1
- Update to 2024.2.4

* Fri Aug 30 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3

* Mon Aug 26 2024 M3DZIK <me@medzik.dev> - 2024.2.2-1
- Update to 2024.2.2

* Tue Aug 20 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1

* Thu Aug 15 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2

* Wed Aug 14 2024 M3DZIK <me@medzik.dev> - 2024.1.6-1
- Update to 2024.1.6

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5

* Tue Jun 25 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Update to 2024.1.4

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.3-1
- Update to 2024.1.3

* Tue May 07 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Update to 2024.1.2

* Wed Apr 17 2024 M3DZIK <me@medzik.dev> - 2024.1.1-1
- Update to 2024.1.1

* Tue Apr 09 2024 M3DZIK <me@medzik.dev> - 2024.1-1
- Update to 2024.1

* Wed Mar 13 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4

* Tue Feb 20 2024 M3DZIK <me@medzik.dev> - 2023.3.3-1
- Update to 2023.3.3

* Thu Dec 21 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3

* Sat Nov 04 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3

* Wed Sep 27 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Update to 2023.2.2

* Fri Sep 15 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Initial release
