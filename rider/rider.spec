# setting some global constants
%global appname rider

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
%global __provides_exclude_from %{_javadir}/%{name}/bin/.*|%{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*
%global __requires_exclude_from %{_javadir}/%{name}/bin/.*|%{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*

Name:          rider
Version:       2023.3.4
Release:       1%{?dist}
Summary:       Fast & powerful, cross platform .NET IDE
License:       Commercial
URL:           https://www.jetbrains.com/%{appname}/

Source0:       https://download.jetbrains.com/rider/JetBrains.Rider-%{version}.tar.gz

Source101:     %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: librsvg2-tools
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem

%description
Rider supports .NET Framework, the new cross-platform .NET Core, and Mono based projects.

%package doc
Summary:       Documentation for Rider
BuildArch:     noarch

%description doc
This package contains documentation for Rider

%prep
%setup -q -n 'JetBrains Rider-%{version}'

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix plugins
%else
find plugins -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,build.txt,product-info.json} %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Creating additional PNG icons on the fly...
for size in 16 22 24 32 48 64 128 256; do
    dest=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    install -d ${dest}
    rsvg-convert -w ${size} -h ${size} bin/%{appname}.svg -o ${dest}/%{name}.png
    chmod 0644 ${dest}/%{name}.png
    touch -r bin/%{appname}.svg ${dest}/%{name}.png
done

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/%{appname}.sh %{buildroot}%{_bindir}/%{name}

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
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files doc
%doc *.txt

%changelog
* Wed Mar 13 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4

* Tue Feb 20 2024 M3DZIK <me@medzik.dev> - 2023.3.3-1
- Update to 2023.3.3

* Thu Dec 21 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3

* Sat Nov 04 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3

* Wed Sep 27 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Update to 2023.2.2

* Fri Sep 15 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Initial release
