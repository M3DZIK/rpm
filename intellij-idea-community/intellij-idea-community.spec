# setting some global constants
%global appname idea
%global build_ver 251.23774.435
%global idea_name ideaIC

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
%global __brp_check_rpaths %{nil}
# there are some python 2 and python 3 scripts so there is no way out to bytecompile them ^_^
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global _exclude_from %{_datadir}/%{name}/bin/.*|%{_datadir}/%{name}/lib/.*|%{_datadir}/%{name}/plugins/.*|%{_datadir}/%{name}/jbr/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    intellij-idea-community
Version: 2025.1
Release: 1%{?dist}
Summary: Capable and Ergonomic Java IDE - Community Edition
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
IntelliJ IDEA Community is a free and open-source edition of IntelliJ IDEA, the commercial Java IDE by JetBrains.
IntelliJ IDEA Community provides all the tools you need for Java, Groovy, Kotlin, Scala, and Android.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
git clone https://github.com/JetBrains/intellij-community -b idea/%{build_ver} --depth 1
cd intellij-community
git clone git://git.jetbrains.org/idea/android.git android -b idea/%{build_ver} --depth 1

%build
# Building
cd intellij-community
./installers.cmd -Dintellij.build.target.os=linux
cd ..

artifact_version=$(echo "%{build_ver}" | sed -E 's|idea/||; s|.[0-9]+$||')

idea_target_dir="./intellij-community/out/idea-ce/artifacts"
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
* Wed Apr 16 2025 M3DZIK <me@medzik.dev> - 2025.1-1
- Update to 2025.1 (251.23774.435)

* Tue Mar 18 2025 M3DZIK <me@medzik.dev> - 2024.3.5-1
- Update to 2024.3.5 (243.26053.27)

* Wed Mar 05 2025 M3DZIK <me@medzik.dev> - 2024.3.4.1-1
- Update to 2024.3.4.1 (243.25659.59)

* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.4-1
- Update to 2024.3.4 (243.25659.39)

* Thu Feb 13 2025 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3 (243.24978.46)

* Wed Jan 29 2025 M3DZIK <me@medzik.dev> - 2024.3.2.2-1
- Update to 2024.3.2.2 (243.23654.189)

* Fri Jan 24 2025 M3DZIK <me@medzik.dev> - 2024.3.2.1-1
- Update to 2024.3.2.1 (243.23654.153)

* Fri Jan 17 2025 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2 (243.23654.117)

* Thu Dec 19 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1 (243.22562.218)

* Mon Dec 09 2024 M3DZIK <me@medzik.dev> - 2024.3.1-1
- Update to 2024.3.1 (243.22562.145)

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3 (243.21565.193)

* Wed Oct 23 2024 M3DZIK <me@medzik.dev> - 2024.2.4-1
- Update to 2024.2.4 (242.23726.103)

* Wed Sep 25 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3 (242.23339.11)

* Thu Sep 19 2024 M3DZIK <me@medzik.dev> - 2024.2.2-1
- Update to 2024.2.2 (242.22855.74)

* Thu Aug 29 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1 (242.21829.142)

* Tue Aug 20 2024 M3DZIK <me@medzik.dev> - 2024.2.0.2-1
- Update to 2024.2.0.2 (242.20224.419)

* Wed Aug 14 2024 M3DZIK <me@medzik.dev> - 2024.2.0.1-1
- Update to 2024.2.0.1 (242.20224.387)

* Wed Aug 07 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2 (242.20224.300)

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5 (241.18968.26)

* Fri Jun 26 2024 M3DZIK <me@medzik.dev> - 2024.1.4-3
- Bump from sources

* Fri Jun 21 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Update to 2024.1.4 (241.18034.62)

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.3-1
- Update to 2024.1.3 (241.17890.1)

* Thu May 23 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Update to 2024.1.2 (241.17011.79)

* Tue Apr 30 2024 M3DZIK <me@medzik.dev> - 2024.1.1-1
- Update to 2024.1.1 (241.15989.150)

* Thu Apr 04 2024 M3DZIK <me@medzik.dev> - 2024.1-1
- Update to 2024.1 (241.14494.240)

* Thu Mar 21 2024 M3DZIK <me@medzik.dev> - 2023.3.6-1
- Update to 2023.3.6 (233.15026.9)

* Wed Mar 13 2024 M3DZIK <me@medzik.dev> - 2023.3.5-1
- Update to 2023.3.5 (233.14808.21)

* Wed Feb 14 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4 (233.14475.28)

* Fri Jan 26 2024 M3DZIK <me@medzik.dev> - 2023.3.3-1
- Update to 2023.3.3 (233.14015.106)

* Thu Dec 21 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2 (233.13135.103)

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1 (233.11799.300)

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3 (233.11799.241)

* Fri Nov 10 2023 M3DZIK <me@medzik.dev> - 2023.2.5-1
- Update to 2023.2.5 (232.10227.8)

* Thu Oct 26 2023 M3DZIK <me@medzik.dev> - 2023.2.4
- Update to 2023.2.4 (232.10203.10)

* Thu Oct 12 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3 (232.10072.27)

* Thu Sep 14 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Update to 2023.2.2 (232.9921.47)

* Thu Aug 31 2023 M3DZIK <me@medzik.dev> - 2023.2.1
- Initial release
