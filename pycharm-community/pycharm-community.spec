# setting some global constants
%global appname pycharm
%global build_ver 243.25659.43
%global idea_name pycharmPC

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

Name:    pycharm-community
Version: 2024.3.4
Release: 1%{?dist}
Summary: Intelligent Python IDE - Community
License: Apache-2.0
URL:     https://www.jetbrains.com/%{appname}/

Source0: %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem
BuildRequires: wget
BuildRequires: tar
BuildRequires: git
BuildRequires: p7zip
BuildRequires: java-17-openjdk-devel

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem
Requires:      %{name}-jbr = %{version}-%{release}

%description
PyCharm is designed by programmers, for programmers, to provide all the tools you need for productive Python development.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
git clone https://github.com/JetBrains/intellij-community -b pycharm/%{build_ver} --depth 1
cd intellij-community
git clone git://git.jetbrains.org/idea/android.git android -b pycharm/%{build_ver} --depth 1

%build
# Building
cd intellij-community
./python/installers.cmd -Dintellij.build.use.compiled.classes=false -Dintellij.build.target.os=linux -Dbuild.number="%{build_ver}"
cd ..

artifact_version=$(echo "%{build_ver}" | sed -E 's|pycharm/||; s|.[0-9]+$||')

idea_target_dir="./intellij-community/out/pycharm-ce/artifacts"
%ifarch x86_64
target_file_name="%{idea_name}-${artifact_version}.*.tar.gz"
%else
target_file_name="%{idea_name}-${artifact_version}.*-aarch64.tar.gz"
%endif

target_file_pattern="${idea_target_dir}/${target_file_name}"

%ifarch x86_64
# Exclude aarch64 from search
target_file=$(ls ${target_file_pattern} 2>/dev/null | grep -v 'aarch64' | head -n 1)
%else
target_file=$(ls ${target_file_pattern} 2>/dev/null | head -n 1)
%endif

mkdir -p "unpacked"
tar xf "${target_file}" -C "unpacked"
mkdir -p "target"

mv "unpacked"/*/* target

cd target

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix .
%else
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
cd target

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
%license target/license/*
%{_datadir}/%{name}/{bin,lib,plugins,modules,build.txt,product-info.json}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files jbr
%{_datadir}/%{name}/jbr

%changelog
* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.4-1
- Update to 2024.3.4 (243.25659.43)

* Fri Feb 14 2025 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3 (243.24978.54)

* Tue Jan 28 2025 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2 (243.23654.177)

* Thu Dec 19 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1 (243.22562.220)

* Thu Dec 12 2024 M3DZIK <me@medzik.dev> - 2024.3.1-1
- Update to 2024.3.1 (243.22562.180)

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3 (243.21565.199)

* Wed Oct 23 2024 M3DZIK <me@medzik.dev> - 2024.2.4-1
- Update to 2024.2.4 (242.23726.102)

* Fri Sep 27 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3 (242.23339.19)

* Fri Sep 20 2024 M3DZIK <me@medzik.dev> - 2024.2.2-1
- Update to 2024.2.2 (242.22855.92)

* Thu Aug 29 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1 (242.21829.153)

* Fri Aug 23 2024 M3DZIK <me@medzik.dev> - 2024.2.0.1-1
- Update to 2024.2.0.1 (242.20224.428)

* Mon Aug 12 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2 (242.20224.347)

* Fri Aug 09 2024 M3DZIK <me@medzik.dev> - 2024.1.6-1
- Update to 2024.1.6 (241.19072.16)

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5 (241.18968.29)

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
