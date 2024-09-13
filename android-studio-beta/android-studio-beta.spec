# setting some global constants
%global appname studio

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

Name:    android-studio-beta
Version: 2024.2.1.7
Release: 1%{?dist}
Summary: Integrated development environment for Google's Android platform - Beta Channel
License: Apache-2.0
URL:     https://developer.android.com/%{appname}/

Source0: https://dl.google.com/android/studio/ide-zips/%{version}/android-studio-%{version}-linux.tar.gz

Source101: %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem
Requires:      %{name}-jbr = %{version}-%{release}

%description
Official Integrated Development Environment (IDE) for developing
applications. The IDE is based on IntelliJ IDEA, and provides
features on top of its powerful code editor and developer tools
to enhance the productivity of the Android application developers

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%setup -q -n android-studio

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix bin
%else
find bin -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
# Installing application...
install -d %{buildroot}%{_datadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,build.txt,product-info.json} %{buildroot}%{_datadir}/%{name}/

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
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files jbr
%{_datadir}/%{name}/jbr

%changelog
* Fri Sep 13 2024 M3DZIK <me@medzik.dev> - 2024.2.1.7-1
- Update to 2024.2.1.7

* Tue Sep 10 2024 M3DZIK <me@medzik.dev> - 2024.2.1.6-1
- Update to 2024.2.1.6

* Fri Sep 06 2024 M3DZIK <me@medzik.dev> - 2024.2.1.5-1
- Update to 2024.2.1.5

* Wed Aug 07 2024 M3DZIK <me@medzik.dev> - 2024.1.2.11-1
- Update to 2024.1.2.11

* Thu Jul 25 2024 M3DZIK <me@medzik.dev> - 2024.1.2.10-1
- Update to 2024.1.2.10

* Tue Jul 16 2024 M3DZIK <me@medzik.dev> - 2024.1.2.9-1
- Update to 2024.1.2.9

* Wed Jul 10 2024 M3DZIK <me@medzik.dev> - 2024.1.2.8-1
- Update to 2024.1.2.8

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.1.10-1
- Update to 2024.1.1.10

* Fri May 31 2024 M3DZIK <me@medzik.dev> - 2024.1.1.9-1
- Update to 2024.1.1.9

* Wed May 15 2024 M3DZIK <me@medzik.dev> - 2024.1.1.8-1
- Update to 2024.1.1.8

* Tue May 14 2024 M3DZIK <me@medzik.dev> - 2024.1.1.7-1
- Update to 2024.1.1.7

* Fri May 10 2024 M3DZIK <me@medzik.dev> - 2024.1.1.6-1
- Update to 2024.1.1.6

* Mon Apr 08 2024 M3DZIK <me@medzik.dev> - 2023.3.1.17-1
- Update to 2023.3.1.17

* Fri Apr 05 2024 M3DZIK <me@medzik.dev> - 2023.3.1.16-1
- Update to 2023.3.1.16

* Thu Mar 28 2024 M3DZIK <me@medzik.dev> - 2023.3.1.15-1
- Update to 2023.3.1.15

* Thu Mar 21 2024 M3DZIK <me@medzik.dev> - 2023.3.1.14-1
- Update to 2023.3.1.14

* Wed Feb 14 2024 M3DZIK <me@medzik.dev> - 2023.2.1.22-1
- Update to 2023.2.1.22

* Tue Feb 06 2024 M3DZIK <me@medzik.dev> - 2023.2.1.21-1
- Update to 2023.2.1.21

* Thu Jan 11 2024 M3DZIK <me@medzik.dev> - 2023.2.1.20-1
- Update to 2023.2.1.20

* Fri Dec 29 2023 M3DZIK <me@medzik.dev> - 2023.2.1.19-1
- Update to 2023.2.1.19

* Wed Dec 27 2023 M3DZIK <me@medzik.dev> - 2023.2.1.18-1
- Update to 2023.2.1.18

* Fri Nov 10 2023 M3DZIK <me@medzik.dev> - 2023.1.1.25-1
- Update to 2023.1.1.25

* Tue Oct 31 2023 M3DZIK <me@medzik.dev> - 2023.1.1.24
- Update to 2023.1.1.24

* Wed Oct 18 2023 M3DZIK <me@medzik.dev> - 2023.1.1.23
- Update to 2023.1.1.23

* Thu Sep 28 2023 M3DZIK <me@medzik.dev> - 2023.1.1.22
- Update to 2023.1.1.22

* Fri Sep 22 2023 M3DZIK <me@medzik.dev> - 2023.1.1.21
- Update to 2023.1.1.21

* Thu Sep 14 2023 M3DZIK <me@medzik.dev> - 2023.1.1.20
- Update to 2023.1.1.20

* Fri Sep 08 2023 M3DZIK <me@medzik.dev> - 2023.1.1.19
- Update to 2023.1.1.19

* Thu Sep 07 2023 M3DZIK <me@medzik.dev> - 2023.1.1.18
- Update to 2023.1.1.18

* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 2023.1.1.17
- Initial release
