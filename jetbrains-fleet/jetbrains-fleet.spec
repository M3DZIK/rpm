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
%global __provides_exclude_from %{_javadir}/%{name}/lib/.*
%global __requires_exclude_from %{_javadir}/%{name}/lib/.*

Name:          jetbrains-fleet
Version:       1.33.90
Release:       1%{?dist}
Summary:       Next-generation IDE by JetBrains
License:       Commercial
URL:           https://www.jetbrains.com/%{appname}/

Source0:       https://download-cdn.jetbrains.com/fleet/installers/linux_x64/Fleet-%{version}.tar.gz

Source101:     %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: librsvg2-tools
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem

%description
Next-generation IDE by JetBrains

%prep
%setup -q -n Fleet

%install
# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./{bin,lib} %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p lib/Fleet.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# # Creating additional PNG icons on the fly...
# for size in 16 22 24 32 48 64 128 256; do
#     dest=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
#     install -d ${dest}
#     rsvg-convert -w ${size} -h ${size} bin/%{appname}.svg -o ${dest}/%{name}.png
#     chmod 0644 ${dest}/%{name}.png
#     touch -r bin/%{appname}.svg ${dest}/%{name}.png
# done

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/Fleet %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
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
