%global debug_package %{nil}
%global _build_id_links none

%global _exclude_from %{_datadir}/%{name}/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    codium
Version: 1.97.2.25045
Release: 1%{?dist}
Summary: Free/Libre Open Source Software Binaries of VS Code
License: MIT
URL:     https://vscodium.com

Source0: https://github.com/VSCodium/vscodium/archive/%{version}.tar.gz

Source100: %{name}.desktop
Source101: %{name}-uri-handler.desktop
Source102: %{name}.appdata.xml

Provides: vscodium = %{version}-%{release}

BuildRequires: python3
BuildRequires: npm
BuildRequires: yarnpkg
BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(krb5)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: desktop-file-utils
BuildRequires: zip
BuildRequires: jq
BuildRequires: git

%description
VSCodium is a community-driven, freely-licensed binary distribution of Microsoft's editor VS Code.

%prep
%setup -q -n vscodium-%{version}

%ifarch x86_64
_vscode_arch="x64"
%elifarch aarch64
_vscode_arch="arm64"
%endif

# Export necessary environment variables
export SHOULD_BUILD="yes"
export SHOULD_BUILD_REH="no"
export CI_BUILD="no"
export OS_NAME="linux"
export VSCODE_ARCH="${_vscode_arch}"
export VSCODE_QUALITY="stable"
export RELEASE_VERSION="%{version}"
export DISABLE_UPDATE="yes"

./get_repo.sh

%build
%ifarch x86_64
_vscode_arch="x64"
%elifarch aarch64
_vscode_arch="arm64"
%endif

# Export necessary environment variables
export SHOULD_BUILD="yes"
export SHOULD_BUILD_REH="no"
export CI_BUILD="no"
export OS_NAME="linux"
export VSCODE_ARCH="${_vscode_arch}"
export VSCODE_QUALITY="stable"
export RELEASE_VERSION="%{version}"
export DISABLE_UPDATE="yes"

./build.sh

%install
# Installing application...
install -d %{buildroot}%{_datadir}/%{name}
cp -arf VSCode-linux-*/* %{buildroot}%{_datadir}/%{name}

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE100} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}-uri-handler.desktop

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE102} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

# Installing icon...
install -d %{buildroot}%{_datadir}/pixmaps
ln -s %{_datadir}/%{name}/resources/app/resources/linux/code.png %{buildroot}%{_datadir}/pixmaps/vs%{name}.png

# Install shell completions
install -d %{buildroot}%{_datadir}/bash-completion/completions
ln -s %{_datadir}/%{name}/resources/completions/bash/codium %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -d %{buildroot}%{_datadir}/zsh/site-functions
ln -s %{_datadir}/%{name}/resources/completions/zsh/_codium %{buildroot}%{_datadir}/zsh/site-functions/%{name}

%files
%license LICENSE
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-uri-handler.desktop
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/pixmaps/vs%{name}.png
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/%{name}

%changelog
* Fri Feb 14 2025 M3DZIK <me@medzik.dev> - 1.97.2.25045-1
- Update to 1.97.2.25045

* Thu Feb 13 2025 M3DZIK <me@medzik.dev> - 1.97.1.25044-1
- Update to 1.97.1.25044

* Fri Feb 07 2025 M3DZIK <me@medzik.dev> - 1.97.0.25037-1
- Update to 1.97.0.25037

* Sun Jan 26 2025 M3DZIK <me@medzik.dev> - 1.96.4.25026-1
- Update to 1.96.4.25026

* Fri Jan 17 2025 M3DZIK <me@medzik.dev> - 1.96.4.25017-1
- Update to 1.96.4.25017

* Mon Jan 13 2025 M3DZIK <me@medzik.dev> - 1.96.3.25013-1
- Update to 1.96.3.25013

* Fri Dec 20 2024 M3DZIK <me@medzik.dev> - 1.96.2.24355-1
- Update to 1.96.2.24355

* Wed Dec 18 2024 M3DZIK <me@medzik.dev> - 1.96.1.24353-1
- Update to 1.96.1.24353

* Wed Dec 18 2024 M3DZIK <me@medzik.dev> - 1.96.0.24352-1
- Update to 1.96.0.24352

* Thu Dec 12 2024 M3DZIK <me@medzik.dev> - 1.96.0.24347-1
- Update to 1.96.0.24347

* Sat Nov 16 2024 M3DZIK <me@medzik.dev> - 1.95.3.24321-1
- Update to 1.95.3.24321

* Fri Nov 08 2024 M3DZIK <me@medzik.dev> - 1.95.2.24313-1
- Update to 1.95.2.24313

* Sat Nov 02 2024 M3DZIK <me@medzik.dev> - 1.95.1.24307-1
- Update to 1.95.1.24307

* Sun Oct 13 2024 M3DZIK <me@medzik.dev> - 1.94.2.24286-1
- Update to 1.94.2.24286

* Thu Oct 10 2024 M3DZIK <me@medzik.dev> - 1.94.2.24284-1
- Update to 1.94.2.24284

* Thu Oct 10 2024 M3DZIK <me@medzik.dev> - 1.94.1.24283-1
- Update to 1.94.1.24283

* Tue Oct 08 2024 M3DZIK <me@medzik.dev> - 1.94.0.24282-1
- Update to 1.94.0.24282

* Mon Oct 07 2024 M3DZIK <me@medzik.dev> - 1.94.0.24281-1
- Update to 1.94.0.24281

* Thu Sep 12 2024 M3DZIK <me@medzik.dev> - 1.93.1.24256-1
- Update to 1.93.1.24256

* Mon Sep 09 2024 M3DZIK <me@medzik.dev> - 1.93.0.24253-1
- Update to 1.93.0.24253

* Thu Aug 15 2024 M3DZIK <me@medzik.dev> - 1.92.2.24228-1
- Update to 1.92.2.24228

* Mon Aug 12 2024 M3DZIK <me@medzik.dev> - 1.92.1.24225-1
- Update to 1.92.1.24225

* Sun Jul 27 2024 M3DZIK <me@medzik.dev> - 1.91.1.24193-1
- Initial release
