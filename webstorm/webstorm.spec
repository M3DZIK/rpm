# setting some global constants
%global appname webstorm
%global build_ver 242.20224.342

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
%global _exclude_from %{_javadir}/%{name}/bin/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*|%{_javadir}/%{name}/jbr/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    webstorm
Version: 2024.2
Release: 1%{?dist}
Summary: The smartest JavaScript IDE
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
Recommends:    %{name}-jbr = %{version}-%{release}

%description
WebStorm is an IDE for JavaScript and related technologies.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="WebStorm-%{version}.tar.gz"
%else
download_file="WebStorm-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/%{name}/$download_file"
mkdir "${download_file}.out"
tar xf "$download_file" -C "${download_file}.out"
mv "${download_file}.out"/*/* .

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix .
%else
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

# Deleting unnecessary files...
size_before=$(du -s . | awk '{print $1}')
# First it removes directories, because it sometimes throws an error
find . -type d -iname '*darwin*' -exec rm -rv {} +
find . -iname '*darwin*' -exec rm -rv {} +
find . -type d -iname '*macos*' -exec rm -rv {} +
find . -iname '*macos*' -exec rm -rv {} +
find . -type d -iname '*windows*' -exec rm -rv {} +
find . -iname '*windows*' -exec rm -rv {} +
%ifarch x86_64
find . -type d -name '*arm64*' -exec rm -rv {} +
find . -name '*arm64*' -exec rm -rv {} +
find . -type d -name '*aarch64*' -exec rm -rv {} +
find . -name '*aarch64*' -exec rm -rv {} +
%else
find . -type d -name '*amd64*' -exec rm -rv {} +
find . -name '*amd64*' -exec rm -rv {} +
find . -type d -name '*x86_64*' -exec rm -rv {} +
find . -name '*x86_64*' -exec rm -rv {} +
%endif
size_after=$(du -s . | awk '{print $1}')
size_diff=$(( size_before - size_after ))
echo "Space freed: $size_diff bytes"

%install
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
ln -s %{_javadir}/%{name}/bin/%{appname} %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}/{bin,lib,plugins,build.txt,product-info.json}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files jbr
%{_javadir}/%{name}/jbr

%changelog
* Mon Aug 12 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2 (242.20224.342)

* Fri Jun 21 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5 (241.18034.50)

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Update to 2024.1.4 (241.17890.13)

* Thu May 23 2024 M3DZIK <me@medzik.dev> - 2024.1.3-1
- Update to 2024.1.3 (241.17011.90)

* Fri Apr 26 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Update to 2024.1.2 (241.15989.105)

* Wed Apr 17 2024 M3DZIK <me@medzik.dev> - 2024.1.1-1
- Update to 2024.1.1 (241.15989.47)

* Thu Apr 04 2024 M3DZIK <me@medzik.dev> - 2024.1-1
- Update to 2024.1 (241.14494.235)

* Mon Mar 25 2024 M3DZIK <me@medzik.dev> - 2023.3.6-1
- Update to 2023.3.6 (233.15026.13)

* Sat Mar 16 2024 M3DZIK <me@medzik.dev> - 2023.3.5-1
- Update to 2023.3.5 (233.14808.24)

* Tue Feb 20 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4 (233.14475.40)

* Fri Dec 22 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2 (233.13135.92)

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1 (233.11799.293)

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3 (233.11799.229)

* Tue Nov 14 2023 M3DZIK <me@medzik.dev> - 2023.2.5-1
- Update to 2023.2.5 (232.10227.9)

* Fri Oct 27 2023 M3DZIK <me@medzik.dev> - 2023.2.4
- Update to 2023.2.4 (232.10203.14)

* Fri Oct 13 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3 (232.10072.28)

* Sat Sep 16 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Update to 2023.2.2 (232.9921.42)

* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 2023.2.1
- Initial release
