%global debug_package %{nil}
%global _build_id_links none

%global _exclude_from %{_datadir}/%{name}/.*
%global __provides_exclude_from %{_exclude_from}
%global __requires_exclude_from %{_exclude_from}

Name:    code-oss
Version: 1.99.1
Release: 1%{?dist}
Summary: The Open Source version of Visual Studio Code (vscode) editor
License: MIT
URL:     https://github.com/microsoft/vscode

Source0: https://github.com/microsoft/vscode/archive/%{version}.tar.gz
Patch0:  product_json.patch

BuildRequires: python3
BuildRequires: npm
BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(krb5)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(libsecret-1)
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
        s|@@ICON@@|code-oss|g
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
sed -i 's|@@APPNAME@@|code-oss|g' resources/completions/{bash/code-oss,zsh/_code-oss}

%build
%ifarch x86_64
_vscode_arch="x64"
%elifarch aarch64
_vscode_arch="arm64"
%endif

npm install --cpu=$_vscode_arch
npm run gulp vscode-linux-$_vscode_arch-min

%install
# Installing application...
install -d %{buildroot}%{_datadir}/%{name}
cp -arf ../VSCode-linux-*/* %{buildroot}%{_datadir}/%{name}

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p resources/linux/code.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -m 0644 -p resources/linux/code-url-handler.desktop %{buildroot}%{_datadir}/applications/%{name}-url-handler.desktop

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p resources/linux/code.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

# Installing icon...
install -d %{buildroot}%{_datadir}/pixmaps
ln -s %{_datadir}/%{name}/resources/app/resources/linux/code.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Install shell completions
install -d %{buildroot}%{_datadir}/bash-completion/completions
install -m 0644 -p resources/completions/bash/code %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -m 0644 -p resources/completions/zsh/_code %{buildroot}%{_datadir}/zsh/site-functions/%{name}

%files
%license LICENSE.txt
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-url-handler.desktop
%{_datadir}/pixmaps/%{name}.png
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/%{name}

%changelog
* Tue Apr 08 2025 M3DZIK <me@medzik.dev> - 1.99.1-1
- Update to 1.99.1

* Fri Apr 04 2025 M3DZIK <me@medzik.dev> - 1.99.0-1
- Update to 1.99.0

* Thu Mar 13 2025 M3DZIK <me@medzik.dev> - 1.98.2-1
- Update to 1.98.2

* Tue Mar 11 2025 M3DZIK <me@medzik.dev> - 1.98.1-1
- Update to 1.98.1

* Wed Mar 05 2025 M3DZIK <me@medzik.dev> - 1.98.0-1
- Update to 1.98.0

* Thu Feb 13 2025 M3DZIK <me@medzik.dev> - 1.97.2-1
- Update to 1.97.2

* Tue Feb 11 2025 M3DZIK <me@medzik.dev> - 1.97.1-1
- Update to 1.97.1

* Thu Feb 06 2025 M3DZIK <me@medzik.dev> - 1.97.0-1
- Update to 1.97.0

* Fri Jan 17 2025 M3DZIK <me@medzik.dev> - 1.96.4-1
- Update to 1.96.4

* Mon Jan 13 2025 M3DZIK <me@medzik.dev> - 1.96.3-1
- Update to 1.96.3

* Fri Dec 20 2024 M3DZIK <me@medzik.dev> - 1.96.2-1
- Update to 1.96.2

* Wed Dec 18 2024 M3DZIK <me@medzik.dev> - 1.96.1-1
- Update to 1.96.1

* Thu Dec 12 2024 M3DZIK <me@medzik.dev> - 1.96.0-1
- Update to 1.96.0

* Fri Nov 15 2024 M3DZIK <me@medzik.dev> - 1.95.3-1
- Update to 1.95.3

* Fri Nov 08 2024 M3DZIK <me@medzik.dev> - 1.95.2-1
- Update to 1.95.2

* Fri Nov 01 2024 M3DZIK <me@medzik.dev> - 1.95.1-1
- Update to 1.95.1

* Tue Oct 29 2024 M3DZIK <me@medzik.dev> - 1.95.0-1
- Update to 1.95.0

* Thu Oct 10 2024 M3DZIK <me@medzik.dev> - 1.94.2-1
- Update to 1.94.2

* Tue Oct 08 2024 M3DZIK <me@medzik.dev> - 1.94.1-1
- Update to 1.94.1

* Thu Oct 03 2024 M3DZIK <me@medzik.dev> - 1.94.0-1
- Update to 1.94.0

* Thu Sep 12 2024 M3DZIK <me@medzik.dev> - 1.93.1-1
- Update to 1.93.1

* Thu Sep 05 2024 M3DZIK <me@medzik.dev> - 1.93.0-1
- Update to 1.93.0

* Thu Aug 15 2024 M3DZIK <me@medzik.dev> - 1.92.2-1
- Update to 1.92.2

* Thu Aug 08 2024 M3DZIK <me@medzik.dev> - 1.92.1-1
- Update to 1.92.1

* Thu Aug 01 2024 M3DZIK <me@medzik.dev> - 1.92.0-1
- Update to 1.92.0

* Sat Jul 27 2024 M3DZIK <me@medzik.dev> - 1.91.1-1
- Initial release
