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

Name:    android-studio
Version: 2024.1.2.13
Release: 1%{?dist}
Summary: Integrated development environment for Google's Android platform
License: Apache-2.0
URL:     https://developer.android.com/%{appname}/

Source0:   https://dl.google.com/android/studio/ide-zips/%{version}/android-studio-%{version}-linux.tar.gz

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
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/com.google.AndroidStudio.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/com.google.AndroidStudio.svg

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/%{appname}.sh %{buildroot}%{_bindir}/%{name}

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
%{_datadir}/pixmaps/com.google.AndroidStudio.png
%{_datadir}/icons/hicolor/scalable/apps/com.google.AndroidStudio.svg

%files jbr
%{_datadir}/%{name}/jbr

%changelog
* Thu Sep 19 2024 M3DZIK <me@medzik.dev> - 2024.1.2.13-1
- Update to 2024.1.2.13

* Thu Aug 29 2024 M3DZIK <me@medzik.dev> - 2024.1.2.12-1
- Update to 2024.1.2.12

* Fri Aug 09 2024 M3DZIK <me@medzik.dev> - 2024.1.1.13-1
- Update to 2024.1.1.13

* Fri Jul 12 2024 M3DZIK <me@medzik.dev> - 2024.1.1.12-1
- Update to 2024.1.1.12

* Thu Jun 13 2024 M3DZIK <me@medzik.dev> - 2024.1.1.11-1
- Update to 2024.1.1.11

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2023.3.1.20-1
- Update to 2023.3.1.20

* Mon May 20 2024 M3DZIK <me@medzik.dev> - 2023.3.1.19-1
- Update to 2023.3.1.19

* Tue Apr 30 2024 M3DZIK <me@medzik.dev> - 2023.3.1.18-1
- Update to 2023.3.1.18

* Wed Apr 10 2024 M3DZIK <me@medzik.dev> - 2023.2.1.25-1
- Update to 2023.2.1.25

* Mon Mar 18 2024 M3DZIK <me@medzik.dev> - 2023.2.1.24-1
- Update to 2023.2.1.24

* Fri Mar 01 2024 M3DZIK <me@medzik.dev> - 2023.2.1.23-1
- Update to 2023.2.1.23

* Wed Jan 24 2024 M3DZIK <me@medzik.dev> - 2023.1.1.28-1
- Update to 2023.1.1.28

* Thu Jan 04 2024 M3DZIK <me@medzik.dev> - 2023.1.1.27-1
- Update to 2023.1.1.27

* Fri Dec 01 2023 M3DZIK <me@medzik.dev> - 2023.1.1.26-1
- Update to 2023.1.1.26

* Fri Nov 17 2023 M3DZIK <me@medzik.dev> - 2022.3.1.22-1
- Update to 2022.3.1.22

* Wed Nov 08 2023 M3DZIK <me@medzik.dev> - 2022.3.1.21
- Update to 2022.3.1.21

* Fri Sep 29 2023 M3DZIK <me@medzik.dev> - 2022.3.1.20
- Update to 2022.3.1.20

* Thu Aug 31 2023 M3DZIK <me@medzik.dev> - 2022.3.1.19
- Initial release
