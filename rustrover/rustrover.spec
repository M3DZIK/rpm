# setting some global constants
%global appname rustrover

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

Name:    rustrover
Version:       2024.1.6
Release:       1%{?dist}
Summary: A powerhouse IDE for Rust developers
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
Recommends:    %{name}-jbr

%description
Trust RustRover to take care of the routine while you focus on the important things. Knowing your code through
and through, it can boost your productivity with smart and relevant code completion, instant navigation and
reliable refactorings.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="RustRover-%{version}.tar.gz"
%else
download_file="RustRover-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/%{appname}/$download_file"
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
ln -s %{_javadir}/%{name}/bin/%{appname}.sh %{buildroot}%{_bindir}/%{name}

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
* Wed Jul 24 2024 M3DZIK <me@medzik.dev> - 2024.1.6-1
- Update to 2024.1.6

* Mon Jun 22 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Initial release
