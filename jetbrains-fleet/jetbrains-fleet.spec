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
%global _exclude_from %{_datadir}/%{name}/lib/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    jetbrains-fleet
Version: 1.48.236
Release: 1%{?dist}
Summary: Next-generation IDE by JetBrains
License: Commercial
URL:     https://www.jetbrains.com/%{appname}/

Source0: %{name}.desktop

BuildRequires: desktop-file-utils
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

%install
# Installing application...
install -d %{buildroot}%{_datadir}/%{name}
cp -arf ./{bin,lib} %{buildroot}%{_datadir}/%{name}/
chmod -R 775 "%{buildroot}%{_datadir}/%{name}/lib/app/code-cache"

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p lib/Fleet.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/Fleet %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE0} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Wed Apr 30 2025 M3DZIK <me@medzik.dev> - 1.48.236-1
- Update to 1.48.236

* Fri Mar 21 2025 M3DZIK <me@medzik.dev> - 1.47.158-1
- Update to 1.47.158

* Wed Feb 19 2025 M3DZIK <me@medzik.dev> - 1.46.97-1
- Update to 1.46.97

* Fri Jan 24 2025 M3DZIK <me@medzik.dev> - 1.45.163-1
- Update to 1.45.163

* Thu Dec 26 2024 M3DZIK <me@medzik.dev> - 1.44.151-1
- Update to 1.44.151

* Thu Dec 19 2024 M3DZIK <me@medzik.dev> - 1.44.148-1
- Update to 1.44.148

* Wed Dec 18 2024 M3DZIK <me@medzik.dev> - 1.44.143-1
- Update to 1.44.143

* Mon Dec 02 2024 M3DZIK <me@medzik.dev> - 1.43.148-1
- Update to 1.43.148

* Wed Nov 27 2024 M3DZIK <me@medzik.dev> - 1.43.142-1
- Update to 1.43.142

* Wed Nov 13 2024 M3DZIK <me@medzik.dev> - 1.42.88-1
- Update to 1.42.88

* Tue Nov 12 2024 M3DZIK <me@medzik.dev> - 1.42.87-1
- Update to 1.42.87

* Thu Oct 31 2024 M3DZIK <me@medzik.dev> - 1.42.84-1
- Update to 1.42.84

* Wed Oct 09 2024 M3DZIK <me@medzik.dev> - 1.41.101-1
- Update to 1.41.101

* Thu Sep 19 2024 M3DZIK <me@medzik.dev> - 1.40.87-1
- Update to 1.40.87

* Thu Sep 12 2024 M3DZIK <me@medzik.dev> - 1.40.86-1
- Update to 1.40.86

* Fri Sep 06 2024 M3DZIK <me@medzik.dev> - 1.40.83-1
- Update to 1.40.83

* Mon Aug 26 2024 M3DZIK <me@medzik.dev> - 1.39.118-1
- Update to 1.39.118

* Tue Aug 20 2024 M3DZIK <me@medzik.dev> - 1.39.114-1
- Update to 1.39.114

* Fri Aug 02 2024 M3DZIK <me@medzik.dev> - 1.38.89-2
- Fix run issue

* Wed Jul 31 2024 M3DZIK <me@medzik.dev> - 1.38.89-1
- Update to 1.38.89

* Sun Jul 28 2024 M3DZIK <me@medzik.dev> - 1.38.82-2
- Rebuild

* Thu Jul 25 2024 M3DZIK <me@medzik.dev> - 1.38.82-1
- Update to 1.38.82

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
