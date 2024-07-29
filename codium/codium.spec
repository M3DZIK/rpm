%global debug_package %{nil}
%global _build_id_links none

%global _lib %{_prefix}/lib

%global __requires_exclude libffmpeg.so
%global __provides_exclude_from %{_lib}/%{name}/.*.so

Name:    codium
Version: 1.91.1.24193
Release: 1%{?dist}
Summary: Free/Libre Open Source Software Binaries of VS Code
License: MIT
URL:     https://vscodium.com

Source0: https://github.com/VSCodium/vscodium/archive/%{version}.tar.gz

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

cd vscode

# Patch appdata and desktop file
sed -i 's|/usr/share/@@NAME@@/@@NAME@@|@@NAME@@|g
        s|@@NAME_SHORT@@|VSCodium|g
        s|@@NAME_LONG@@|VSCodium|g
        s|@@NAME@@|codium|g
        s|@@ICON@@|com.vscodium.codium|g
        s|@@EXEC@@|codium|g
        s|@@LICENSE@@|MIT|g
        s|@@URLPROTOCOL@@|vscode|g
        s|inode/directory;||' resources/linux/code{.appdata.xml,.desktop,-url-handler.desktop}

desktop-file-edit --set-key StartupWMClass --set-value VSCodium resources/linux/code.desktop

desktop-file-edit --set-key MimeType --set-value x-scheme-handler/codium resources/linux/code-url-handler.desktop

# Add completions for codium
cp resources/completions/bash/code resources/completions/bash/%{name}
cp resources/completions/zsh/_code resources/completions/zsh/_%{name}

# Patch completions with correct names
sed -i 's|@@APPNAME@@|%{name}|g' resources/completions/{bash/%{name},zsh/_%{name}}

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
install -d %{buildroot}%{_lib}/%{name}
cp -arf VSCode-linux-*/* %{buildroot}%{_lib}/%{name}

# Replace statically included binary with system copy
ln -sf %{_bindir}/rg %{buildroot}%{_lib}/%{name}/resources/app/node_modules.asar.unpacked/@vscode/ripgrep/bin/rg

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_lib}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p vscode/resources/linux/code.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p vscode/resources/linux/code.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

# Installing icon...
install -d %{_datadir}/pixmaps
install -m 0644 -p VSCode-linux-*/resources/app/resources/linux/code.png %{_datadir}/pixmaps/%{name}.png

# Install shell completions
install -d %{buildroot}%{_datadir}/bash-completion/completions
install -m 0644 -p vscode/resources/completions/bash/codium %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -m 0644 -p vscode/resources/completions/zsh/_codium %{buildroot}%{_datadir}/zsh/site-functions/%{name}

%files
%license LICENSE
%{_lib}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/%{name}

%changelog
* Sun Jul 27 2024 M3DZIK <me@medzik.dev> - 1.91.1.24193-1
- Initial release
