# setting some global constants
%global appname gateway
%global build_ver 251.26094.128
%global idea_name JetBrainsGateway

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
# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global _exclude_from %{_datadir}/%{name}/bin/.*|%{_datadir}/%{name}/lib/.*|%{_datadir}/%{name}/plugins/.*|%{_datadir}/%{name}/jbr/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    jetbrains-gateway
Version: 2025.1.2
Release: 1%{?dist}
Summary: Your single entry point to all remote development environments
License: Commercial
URL:     https://www.jetbrains.com/remote-development/gateway/

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
Your single entry point to all remote development environments

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="%{idea_name}-%{version}.tar.gz"
%else
download_file="%{idea_name}-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/idea/gateway/$download_file"
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
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_datadir}/%{name}/{bin,lib,plugins,build.txt,product-info.json}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files jbr
%{_datadir}/%{name}/jbr

%changelog
* Wed Jun 04 2025 M3DZIK <me@medzik.dev> - 2025.1.2-1
- Update to 2025.1.2 (251.26094.128)

* Thu May 15 2025 M3DZIK <me@medzik.dev> - 2025.1.1.1-1
- Update to 2025.1.1.1 (251.25410.160)

* Tue May 13 2025 M3DZIK <me@medzik.dev> - 2025.1.1-1
- Update to 2025.1.1 (251.25410.139)

* Thu Apr 17 2025 M3DZIK <me@medzik.dev> - 2025.1-1
- Update to 2025.1 (251.23774.441)

* Thu Feb 13 2025 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3 (243.24978.56)

* Tue Jan 21 2025 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2 (243.23654.132)

* Tue Dec 24 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1 (243.22562.252)

* Tue Dec 10 2024 M3DZIK <me@medzik.dev> - 2024.3.1-1
- Update to 2024.3.1 (243.22562.160)

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3 (243.21565.196)

* Tue Oct 01 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3 (242.23339.42)

* Fri Sep 06 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1 (242.21829.203)

* Thu Aug 15 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2 (242.20224.368)

* Thu Aug 08 2024 M3DZIK <me@medzik.dev> - 2024.1.2-3
- Fix desktop file

* Sun Jul 21 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Initial version
