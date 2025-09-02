# setting some global constants
%global appname rubymine

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

Name:    rubymine
Version: 2025.2.1
Release: 1%{?dist}
Summary: Ruby and Rails IDE with the full stack of essential developer tools
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
Requires:      %{name}-jbr = %{version}-%{release}

%description
RubyMine is an IDE that helps you be more productive in every aspect of Ruby/Rails projects development.

%package jbr
Summary:  JetBrains Runtime
Requires: %{name} = %{version}-%{release}

%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

%description jbr
JetBrains Runtime - a patched Java Runtime Environment (JRE).

%prep
%ifarch x86_64
download_file="RubyMine-%{version}.tar.gz"
%else
download_file="RubyMine-%{version}-aarch64.tar.gz"
%endif

wget -q "https://download-cf.jetbrains.com/ruby/$download_file"
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
* Mon Jun 23 2025 M3DZIK <me@medzik.dev> - 2025.1.3-1
- Update to 2025.1.3

* Fri Jun 06 2025 M3DZIK <me@medzik.dev> - 2025.1.2-1
- Update to 2025.1.2

* Thu May 08 2025 M3DZIK <me@medzik.dev> - 2025.1.1-1
- Update to 2025.1.1

* Wed Apr 16 2025 M3DZIK <me@medzik.dev> - 2025.1-1
- Update to 2025.1

* Fri Mar 14 2025 M3DZIK <me@medzik.dev> - 2024.3.5-1
- Update to 2024.3.5

* Fri Feb 28 2025 M3DZIK <me@medzik.dev> - 2024.3.4-1
- Update to 2024.3.4

* Tue Feb 18 2025 M3DZIK <me@medzik.dev> - 2024.3.3-1
- Update to 2024.3.3

* Fri Jan 24 2025 M3DZIK <me@medzik.dev> - 2024.3.2.1-1
- Update to 2024.3.2.1

* Fri Jan 17 2025 M3DZIK <me@medzik.dev> - 2024.3.2-1
- Update to 2024.3.2

* Fri Dec 20 2024 M3DZIK <me@medzik.dev> - 2024.3.1.1-1
- Update to 2024.3.1.1

* Wed Dec 11 2024 M3DZIK <me@medzik.dev> - 2024.3.1-1
- Update to 2024.3.1

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 2024.3-1
- Update to 2024.3

* Fri Oct 25 2024 M3DZIK <me@medzik.dev> - 2024.2.4-1
- Update to 2024.2.4

* Thu Sep 26 2024 M3DZIK <me@medzik.dev> - 2024.2.3-1
- Update to 2024.2.3

* Thu Sep 19 2024 M3DZIK <me@medzik.dev> - 2024.2.2-1
- Update to 2024.2.2

* Fri Aug 30 2024 M3DZIK <me@medzik.dev> - 2024.2.1-1
- Update to 2024.2.1

* Wed Aug 21 2024 M3DZIK <me@medzik.dev> - 2024.2.0.1-1
- Update to 2024.2.0.1

* Mon Aug 12 2024 M3DZIK <me@medzik.dev> - 2024.2-1
- Update to 2024.2

* Fri Aug 09 2024 M3DZIK <me@medzik.dev> - 2024.1.6-1
- Update to 2024.1.6

* Tue Aug 06 2024 M3DZIK <me@medzik.dev> - 2024.1.5-1
- Update to 2024.1.5

* Fri Jun 21 2024 M3DZIK <me@medzik.dev> - 2024.1.4-1
- Update to 2024.1.4

* Mon Jun 10 2024 M3DZIK <me@medzik.dev> - 2024.1.3-1
- Update to 2024.1.3

* Thu May 23 2024 M3DZIK <me@medzik.dev> - 2024.1.2-1
- Update to 2024.1.2

* Thu Apr 25 2024 M3DZIK <me@medzik.dev> - 2024.1.1-1
- Update to 2024.1.1

* Thu Apr 04 2024 M3DZIK <me@medzik.dev> - 2024.1-1
- Update to 2024.1

* Mon Mar 25 2024 M3DZIK <me@medzik.dev> - 2023.3.6-1
- Update to 2023.3.6

* Tue Mar 12 2024 M3DZIK <me@medzik.dev> - 2023.3.5-1
- Update to 2023.3.5

* Tue Feb 20 2024 M3DZIK <me@medzik.dev> - 2023.3.4-1
- Update to 2023.3.4

* Thu Dec 21 2023 M3DZIK <me@medzik.dev> - 2023.3.2-1
- Update to 2023.3.2

* Wed Dec 13 2023 M3DZIK <me@medzik.dev> - 2023.3.1-1
- Update to 2023.3.1

* Thu Dec 07 2023 M3DZIK <me@medzik.dev> - 2023.3-1
- Update to 2023.3

* Fri Nov 10 2023 M3DZIK <me@medzik.dev> - 2023.2.5-1
- Update to 2023.2.5

* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 2023.2.4
- Update to 2023.2.4

* Tue Oct 10 2023 M3DZIK <me@medzik.dev> - 2023.2.3
- Update to 2023.2.3

* Fri Sep 15 2023 M3DZIK <me@medzik.dev> - 2023.2.2
- Initial release
