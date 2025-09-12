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

Name:    android-studio-canary
Version: 2025.1.4.5
Release: 1%{?dist}
Summary: Integrated development environment for Google's Android platform - Canary Channel
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
* Sat Jun 21 2025 M3DZIK <me@medzik.dev> - 2025.1.2.6-1
- Update to 2025.1.2.6

* Fri Jun 13 2025 M3DZIK <me@medzik.dev> - 2025.1.2.5-1
- Update to 2025.1.2.5

* Fri Jun 06 2025 M3DZIK <me@medzik.dev> - 2025.1.2.4-1
- Update to 2025.1.2.4

* Fri May 30 2025 M3DZIK <me@medzik.dev> - 2025.1.2.3-1
- Update to 2025.1.2.3

* Sat May 24 2025 M3DZIK <me@medzik.dev> - 2025.1.2.2-1
- Update to 2025.1.2.2

* Tue May 20 2025 M3DZIK <me@medzik.dev> - 2025.1.2.1-1
- Update to 2025.1.2.1

* Fri May 09 2025 M3DZIK <me@medzik.dev> - 2025.1.1.10-1
- Update to 2025.1.1.10

* Fri May 02 2025 M3DZIK <me@medzik.dev> - 2025.1.1.9-1
- Update to 2025.1.1.9

* Mon Apr 28 2025 M3DZIK <me@medzik.dev> - 2025.1.1.8-1
- Update to 2025.1.1.8

* Fri Apr 18 2025 M3DZIK <me@medzik.dev> - 2025.1.1.7-1
- Update to 2025.1.1.7

* Thu Apr 10 2025 M3DZIK <me@medzik.dev> - 2025.1.1.6-1
- Update to 2025.1.1.6

* Wed Apr 09 2025 M3DZIK <me@medzik.dev> - 2025.1.1.5-1
- Update to 2025.1.1.5

* Fri Apr 04 2025 M3DZIK <me@medzik.dev> - 2025.1.1.4-1
- Update to 2025.1.1.4

* Thu Mar 27 2025 M3DZIK <me@medzik.dev> - 2025.1.1.3-1
- Update to 2025.1.1.3

* Fri Mar 21 2025 M3DZIK <me@medzik.dev> - 2025.1.1.2-1
- Update to 2025.1.1.2

* Thu Mar 20 2025 M3DZIK <me@medzik.dev> - 2025.1.1.1-1
- Update to 2025.1.1.1

* Wed Mar 19 2025 M3DZIK <me@medzik.dev> - 2024.3.2.9-1
- Update to 2024.3.2.9

* Sat Mar 08 2025 M3DZIK <me@medzik.dev> - 2024.3.2.8-1
- Update to 2024.3.2.8

* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.2.7-1
- Update to 2024.3.2.7

* Fri Feb 21 2025 M3DZIK <me@medzik.dev> - 2024.3.2.6-1
- Update to 2024.3.2.6

* Fri Feb 14 2025 M3DZIK <me@medzik.dev> - 2024.3.2.5-1
- Update to 2024.3.2.5

* Fri Feb 07 2025 M3DZIK <me@medzik.dev> - 2024.3.2.4-1
- Update to 2024.3.2.4

* Mon Feb 03 2025 M3DZIK <me@medzik.dev> - 2024.3.2.3-1
- Update to 2024.3.2.3

* Fri Jan 24 2025 M3DZIK <me@medzik.dev> - 2024.3.2.2-1
- Update to 2024.3.2.2

* Tue Jan 21 2025 M3DZIK <me@medzik.dev> - 2024.3.2.1-1
- Update to 2024.3.2.1

* Sat Jan 11 2025 M3DZIK <me@medzik.dev> - 2024.3.1.9-1
- Update to 2024.3.1.9

* Mon Jan 06 2025 M3DZIK <me@medzik.dev> - 2024.3.1.8-1
- Update to 2024.3.1.8

* Tue Dec 24 2024 M3DZIK <me@medzik.dev> - 2024.3.1.7-1
- Update to 2024.3.1.7

* Tue Dec 17 2024 M3DZIK <me@medzik.dev> - 2024.3.1.6-1
- Update to 2024.3.1.6

* Thu Dec 12 2024 M3DZIK <me@medzik.dev> - 2024.3.1.5-1
- Update to 2024.3.1.5

* Tue Dec 03 2024 M3DZIK <me@medzik.dev> - 2024.3.1.4-1
- Update to 2024.3.1.4

* Fri Nov 22 2024 M3DZIK <me@medzik.dev> - 2024.3.1.3-1
- Update to 2024.3.1.3

* Fri Nov 15 2024 M3DZIK <me@medzik.dev> - 2024.3.1.2-1
- Update to 2024.3.1.2

* Tue Nov 12 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1

* Fri Nov 01 2024 M3DZIK <me@medzik.dev> - 2024.2.2.9-1
- Update to 2024.2.2.9

* Sat Oct 26 2024 M3DZIK <me@medzik.dev> - 2024.2.2.8-1
- Update to 2024.2.2.8

* Fri Oct 18 2024 M3DZIK <me@medzik.dev> - 2024.2.2.7-1
- Update to 2024.2.2.7

* Tue Oct 15 2024 M3DZIK <me@medzik.dev> - 2024.2.2.6-1
- Update to 2024.2.2.6

* Fri Oct 04 2024 M3DZIK <me@medzik.dev> - 2024.2.2.5-1
- Update to 2024.2.2.5

* Fri Sep 27 2024 M3DZIK <me@medzik.dev> - 2024.2.2.4-1
- Update to 2024.2.2.4

* Tue Sep 24 2024 M3DZIK <me@medzik.dev> - 2024.2.2.3-1
- Update to 2024.2.2.3

* Fri Sep 13 2024 M3DZIK <me@medzik.dev> - 2024.2.2.2-1
- Update to 2024.2.2.2

* Tue Sep 10 2024 M3DZIK <me@medzik.dev> - 2024.2.2.1-1
- Update to 2024.2.2.1

* Fri Sep 06 2024 M3DZIK <me@medzik.dev> - 2024.2.1.6-1
- Update to 2024.2.1.6

* Fri Aug 30 2024 M3DZIK <me@medzik.dev> - 2024.2.1.5-1
- Update to 2024.2.1.5

* Wed Aug 28 2024 M3DZIK <me@medzik.dev> - 2024.2.1.4-1
- Update to 2024.2.1.4

* Fri Aug 16 2024 M3DZIK <me@medzik.dev> - 2024.2.1.3-1
- Update to 2024.2.1.3

* Tue Aug 13 2024 M3DZIK <me@medzik.dev> - 2024.2.1.2-1
- Update to 2024.2.1.2

* Wed Aug 07 2024 M3DZIK <me@medzik.dev> - 2024.2.1.1-1
- Update to 2024.2.1.1

* Fri Jul 26 2024 M3DZIK <me@medzik.dev> - 2024.1.3.3-1
- Update to 2024.1.3.3

* Mon Jul 22 2024 M3DZIK <me@medzik.dev> - 2024.1.3.2-1
- Update to 2024.1.3.2

* Tue Jul 16 2024 M3DZIK <me@medzik.dev> - 2024.1.3.1-1
- Update to 2024.1.3.1

* Wed Jul 10 2024 M3DZIK <me@medzik.dev> - 2024.1.2.9-1
- Update to 2024.1.2.9

* Fri Jun 28 2024 M3DZIK <me@medzik.dev> - 2024.1.2.8-1
- Update to 2024.1.2.8

* Thu Jun 20 2024 M3DZIK <me@medzik.dev> - 2024.1.2.7-1
- Update to 2024.1.2.7

* Tue Jun 18 2024 M3DZIK <me@medzik.dev> - 2024.1.2.6-1
- Update to 2024.1.2.6

* Fri Jun 07 2024 M3DZIK <me@medzik.dev> - 2024.1.2.5-1
- Update to 2024.1.2.5

* Fri May 31 2024 M3DZIK <me@medzik.dev> - 2024.1.2.4-1
- Update to 2024.1.2.4

* Fri May 24 2024 M3DZIK <me@medzik.dev> - 2024.1.2.3-1
- Update to 2024.1.2.3

* Fri May 17 2024 M3DZIK <me@medzik.dev> - 2024.1.2.2-1
- Update to 2024.1.2.2

* Tue May 14 2024 M3DZIK <me@medzik.dev> - 2024.1.2.1-1
- Update to 2024.1.2.1

* Fri May 10 2024 M3DZIK <me@medzik.dev> - 2024.1.1.7-1
- Update to 2024.1.1.7

* Fri May 03 2024 M3DZIK <me@medzik.dev> - 2024.1.1.6-1
- Update to 2024.1.1.6

* Tue Apr 30 2024 M3DZIK <me@medzik.dev> - 2024.1.1.5-1
- Update to 2024.1.1.5

* Fri Apr 19 2024 M3DZIK <me@medzik.dev> - 2024.1.1.4-1
- Update to 2024.1.1.4

* Thu Apr 11 2024 M3DZIK <me@medzik.dev> - 2024.1.1.3-1
- Update to 2024.1.1.3

* Mon Apr 08 2024 M3DZIK <me@medzik.dev> - 2024.1.1.2-1
- Update to 2024.1.1.2

* Tue Apr 02 2024 M3DZIK <me@medzik.dev> - 2024.1.1.1-1
- Update to 2024.1.1.1

* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 2023.3.2.2-1
- Update to 2023.3.2.2

* Wed Mar 20 2024 M3DZIK <me@medzik.dev> - 2023.3.2.1-1
- Update to 2023.3.2.1

* Fri Mar 08 2024 M3DZIK <me@medzik.dev> - 2023.3.1.13-1
- Update to 2023.3.1.13

* Fri Mar 01 2024 M3DZIK <me@medzik.dev> - 2023.3.1.12-1
- Update to 2023.3.1.12

* Fri Feb 23 2024 M3DZIK <me@medzik.dev> - 2023.3.1.11-1
- Update to 2023.3.1.11

* Sat Feb 17 2024 M3DZIK <me@medzik.dev> - 2023.3.1.10-1
- Update to 2023.3.1.10

* Fri Feb 09 2024 M3DZIK <me@medzik.dev> - 2023.3.1.9-1
- Update to 2023.3.1.9

* Tue Feb 06 2024 M3DZIK <me@medzik.dev> - 2023.3.1.8-1
- Update to 2023.3.1.8

* Sat Jan 27 2024 M3DZIK <me@medzik.dev> - 2023.3.1.7-1
- Update to 2023.3.1.7

* Thu Jan 25 2024 M3DZIK <me@medzik.dev> - 2023.3.1.6-1
- Update to 2023.3.1.6

* Tue Jan 23 2024 M3DZIK <me@medzik.dev> - 2023.3.1.5-1
- Update to 2023.3.1.5

* Sat Jan 13 2024 M3DZIK <me@medzik.dev> - 2023.3.1.4-1
- Update to 2023.3.1.4

* Fri Jan 05 2024 M3DZIK <me@medzik.dev> - 2023.3.1.3-1
- Update to 2023.3.1.3

* Wed Jan 03 2024 M3DZIK <me@medzik.dev> - 2023.3.1.2-1
- Update to 2023.3.1.2

* Fri Dec 29 2023 M3DZIK <me@medzik.dev> - 2023.3.1.1-1
- Update to 2023.3.1.1

* Wed Dec 27 2023 M3DZIK <me@medzik.dev> - 2023.2.1.19-1
- Update to 2023.2.1.19

* Thu Dec 14 2023 M3DZIK <me@medzik.dev> - 2023.2.1.18-1
- Update to 2023.2.1.18

* Fri Dec 08 2023 M3DZIK <me@medzik.dev> - 2023.2.1.17-1
- Update to 2023.2.1.17

* Fri Dec 01 2023 M3DZIK <me@medzik.dev> - 2023.2.1.16-1
- Update to 2023.2.1.16

* Wed Nov 29 2023 M3DZIK <me@medzik.dev> - 2023.2.1.15-1
- Update to 2023.2.1.15

* Fri Nov 17 2023 M3DZIK <me@medzik.dev> - 2023.2.1.14-1
- Update to 2023.2.1.14

* Fri Nov 10 2023 M3DZIK <me@medzik.dev> - 2023.2.1.13-1
- Update to 2023.2.1.13

* Fri Nov 03 2023 M3DZIK <me@medzik.dev> - 2023.2.1.12
- Update to 2023.2.1.12

* Fri Oct 27 2023 M3DZIK <me@medzik.dev> - 2023.2.1.11
- Update to 2023.2.1.11

* Tue Oct 24 2023 M3DZIK <me@medzik.dev> - 2023.2.1.10
- Update to 2023.2.1.10

* Fri Oct 20 2023 M3DZIK <me@medzik.dev> - 2023.2.1.9
- Update to 2023.2.1.9

* Fri Oct 06 2023 M3DZIK <me@medzik.dev> - 2023.2.1.7
- Update to 2023.2.1.7

* Fri Sep 29 2023 M3DZIK <me@medzik.dev> - 2023.2.1.6
- Update to 2023.2.1.6

* Fri Sep 22 2023 M3DZIK <me@medzik.dev> - 2023.2.1.5
- Update to 2023.2.1.5

* Sat Sep 16 2023 M3DZIK <me@medzik.dev> - 2023.2.1.4
- Update to 2023.2.1.4

* Fri Sep 08 2023 M3DZIK <me@medzik.dev> - 2023.2.1.3
- Update to 2023.2.1.3

* Thu Sep 07 2023 M3DZIK <me@medzik.dev> - 2023.2.1.2
- Update to 2023.2.1.2

* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 2023.2.1.1
- Initial release
