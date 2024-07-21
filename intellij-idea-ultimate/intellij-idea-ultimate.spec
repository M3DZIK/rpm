# setting some global constants
%global appname idea
%global build_ver 241.18034.62
%global idea_name idea-IU

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
%global __provides_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*
%global __requires_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*

Name:          intellij-idea-ultimate
Version:       2024.1.4
Release:       2%{?dist}
Summary:       Capable and Ergonomic Java IDE - Ultimate Edition
License:       Commercial
URL:           https://www.jetbrains.com/%{appname}/

Source0:   source-info.txt

Source101: intellij-idea-ultimate.desktop
Source102: %{name}.metainfo.xml

BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: librsvg2-tools
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem
BuildRequires: wget
BuildRequires: tar

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem

%description
IntelliJ IDEA Ultimate is a fully-fledged commercial IDE for the JVM platform. IntelliJ IDEA provides all the
tools you need for productive enterprise, Web, and mobile development. IntelliJ IDEA supports Java, Groovy,
Kotlin, Scala, Android, JavaScript, SQL and lots of other languages and frameworks.

%package doc
Summary:       Documentation for IntelliJ IDEA Ultimate
BuildArch:     noarch

%description doc
This package contains documentation for IntelliJ IDEA Ultimate

%prep
%ifarch x86_64
wget https://download.jetbrains.com/idea/ideaIU-%{version}.tar.gz
tar xvf %{idea_name}-%{version}.tar.gz
%else
wget https://download.jetbrains.com/idea/ideaIU-%{version}-aarch64.tar.gz
tar xvf %{idea_name}-%{version}-aarch64.tar.gz
%endif

cd %{idea_name}-%{build_ver}

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix bin
%else
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
cd %{idea_name}-%{build_ver}

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

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE102} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.metainfo.xml

%files doc
%doc help/
%doc *.txt

%changelog
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
