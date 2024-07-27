%global debug_package %{nil}
%global _build_id_links none

%global _lib %{_prefix}/lib

Name:    code-oss
Version: 1.91.1
Release: 1%{?dist}
Summary: The Open Source version of Visual Studio Code (vscode) editor
License: MIT
URL:     https://github.com/microsoft/vscode

Source0: https://github.com/microsoft/vscode/archive/%{version}.tar.gz
Patch0:  product_json.patch

BuildRequires: npm
BuildRequires: yarnpkg
BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(krb5)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: desktop-file-utils
BuildRequires: zip
BuildRequires: git

%description
%{summary}.

%prep
%setup -q -n vscode-%{version}

# Must be git repository
cd ..
rm -rf vscode-%{version}
git clone --depth 1 -b %{version} https://github.com/microsoft/vscode.git vscode-%{version}
cd vscode-%{version}

%patch 0

# Patch appdata and desktop file
sed -i 's|/usr/share/@@NAME@@/@@NAME@@|@@NAME@@|g
        s|@@NAME_SHORT@@|Code|g
        s|@@NAME_LONG@@|Code - OSS|g
        s|@@NAME@@|code-oss|g
        s|@@ICON@@|com.visualstudio.code.oss|g
        s|@@EXEC@@|code-oss|g
        s|@@LICENSE@@|MIT|g
        s|@@URLPROTOCOL@@|vscode|g
        s|inode/directory;||' resources/linux/code{.appdata.xml,.desktop,-url-handler.desktop}

desktop-file-edit --set-key StartupWMClass --set-value code-oss resources/linux/code.desktop

cp resources/linux/{code,code-oss}-url-handler.desktop
desktop-file-edit --set-key MimeType --set-value x-scheme-handler/code-oss resources/linux/code-oss-url-handler.desktop

# Add completions for code-oss
cp resources/completions/bash/code resources/completions/bash/code-oss
cp resources/completions/zsh/_code resources/completions/zsh/_code-oss

# Patch completions with correct names
sed -i 's|@@APPNAME@@|code|g' resources/completions/{bash/code,zsh/_code}
sed -i 's|@@APPNAME@@|code-oss|g' resources/completions/{bash/code-oss,zsh/_code-oss}

%build
%ifarch x86_64
_vscode_arch="x64"
%elifarch aarch64
_vscode_arch="arm64"
%endif

yarn install --arch=$_vscode_arch
yarn gulp vscode-linux-$_vscode_arch-min

# Replace statically included binary with system copy
ln -sf /usr/bin/rg usr/lib/code/node_modules.asar.unpacked/@vscode/ripgrep/bin/rg

%install
# Installing application...
install -d %{buildroot}%{_lib}/%{name}
cp -arf VSCode-linux-*/resources/app/* %{buildroot}%{_lib}/%{name}

# Replace statically included binary with system copy
ln -sf /usr/bin/rg %{buildroot}%{_lib}/%{name}/node_modules.asar.unpacked/@vscode/ripgrep/bin/rg

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sat Jul 27 2024 M3DZIK <me@medzik.dev> - 1.91.1-1
- Initial release
