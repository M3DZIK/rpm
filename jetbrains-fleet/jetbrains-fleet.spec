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
%global _exclude_from %{_javadir}/%{name}/lib/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    jetbrains-fleet
Version: 1.37.84
Release: 2%{?dist}
Summary: Next-generation IDE by JetBrains
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

%description
%{summary}.

%prep
%ifarch x86_64
download_file="Fleet-%{version}.tar.gz"
download_arch="x64"
%else
download_file="Fleet-%{version}-aarch64.tar.gz"
download_arch="aarch64"
%endif

wget -q "https://download-cf.jetbrains.com/fleet/installers/linux_$download_arch/$download_file"
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
cp -arf ./{bin,lib} %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p lib/Fleet.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/Fleet %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Wed Jul 03 2024 M3DZIK <me@medzik.dev> - 1.37.84-1
- Update to 1.37.84

* Thu Jun 13 2024 M3DZIK <me@medzik.dev> - 1.36.104-1
- Update to 1.36.104

* Tue Jun 11 2024 M3DZIK <me@medzik.dev> - 1.36.103-1
- Update to 1.36.103

* Thu May 23 2024 M3DZIK <me@medzik.dev> - 1.35.115-1
- Update to 1.35.115

* Wed May 22 2024 M3DZIK <me@medzik.dev> - 1.35.110-1
- Update to 1.35.110

* Thu May 02 2024 M3DZIK <me@medzik.dev> - 1.34.94-1
- Update to 1.34.94

* Wed Apr 10 2024 M3DZIK <me@medzik.dev> - 1.33.90-1
- Update to 1.33.90

* Mon Apr 08 2024 M3DZIK <me@medzik.dev> - 1.33.88-1
- Update to 1.33.88

* Tue Mar 26 2024 M3DZIK <me@medzik.dev> - 1.32.122-1
- Update to 1.32.122

* Fri Mar 22 2024 M3DZIK <me@medzik.dev> - 1.32.118-1
- Update to 1.32.118

* Sat Mar 09 2024 M3DZIK <me@medzik.dev> - 1.31.107-1
- Update to 1.31.107

* Tue Mar 05 2024 M3DZIK <me@medzik.dev> - 1.31.102-1
- Update to 1.31.102

* Fri Mar 01 2024 M3DZIK <me@medzik.dev> - 1.31.99-1
- Update to 1.31.99

* Mon Feb 19 2024 M3DZIK <me@medzik.dev> - 1.30.83
- Initial release
