# disable debuginfo subpackage
%global debug_package %{nil}

%global git_commit e283e622d644b91130826c887a4dd8cbb936549d

Name:          librepass
Epoch:         1
Version:       1.0.0.alpha1.r55.ge283e62
Release:       1%{?dist}
Summary:       LibrePass Desktop Application
License:       GPLv3
URL:           https://librepass.medzik.dev

Source0:       https://github.com/LibrePass/LibrePass-Desktop/archive/%{git_commit}.tar.gz

Source101:     %{name}.metainfo.xml

BuildRequires: maven
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: librsvg2-tools
BuildRequires: /usr/bin/rpm2cpio
BuildRequires: /usr/bin/cpio

Requires:      jre-17

%description
Official LibrePass Desktop Application

%prep
%setup -q -n LibrePass-Desktop-%{git_commit}

%build
mvn package -P rpm

%install
# Unpack the rpm package
# shellcheck disable=SC2144
if [ -f ./target/rpm/librepass/RPMS/*.rpm ]; then
  rpm2cpio ./target/rpm/librepass/RPMS/*.rpm | cpio -idmv
else
  rpm2cpio ./target/rpm/librepass/RPMS/*/*.rpm | cpio -idmv
fi

# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./usr/lib/librepass/* %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p .%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Creating additional PNG icons on the fly...
for size in 16 22 24 32 48 64 128 256; do
    dest=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    install -d ${dest}
    rsvg-convert -w ${size} -h ${size} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg -o ${dest}/%{name}.png
    chmod 0644 ${dest}/%{name}.png
    touch -r %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg ${dest}/%{name}.png
done

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE101} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

# Installing launcher...
install -d %{buildroot}%{_bindir}
cp -af ./usr/bin/librepass %{buildroot}%{_bindir}/%{name}
sed -i 's;/usr/lib/librepass;%{_javadir}/%{name};' %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p .%{_datadir}/applications/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.metainfo.xml

%changelog
* Sun Nov 26 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r55.ge283e62-1
- Update to 1.0.0.alpha1.r55.ge283e62

* Sat Nov 25 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r53.g669df65-1
- Update to 1.0.0.alpha1.r53.g669df65

* Thu Nov 23 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r50.gdfc8374-1
- Update to 1.0.0.alpha1.r50.gdfc8374

* Fri Nov 17 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r49.g82aec20-1
- Update to 1.0.0.alpha1.r49.g82aec20

* Wed Nov 15 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r48.g02e8e6e-1
- Update to 1.0.0.alpha1.r48.g02e8e6e

* Tue Nov 14 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r47.g5c79aa9-1
- Update to 1.0.0.alpha1.r47.g5c79aa9

* Mon Nov 13 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r44.g56afa6d-1
- Update to 1.0.0.alpha1.r44.g56afa6d

* Sat Nov 11 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r43.g8545b34-1
- Update to 1.0.0.alpha1.r43.g8545b34

* Mon Nov 06 2023 M3DZIK <me@medzik.dev> - 1.0.0.alpha1.r40.g296bdba
- Update to 1.0.0.alpha1.r40.g296bdba

* Wed Nov 01 2023 M3DZIK <me@medzik.dev> - 1.0.0.alpha1.r39.g1aa6cf8
- Update to 1.0.0.alpha1.r39.g1aa6cf8

* Mon Oct 30 2023 M3DZIK <me@medzik.dev> - 1.0.0.alpha1.r37.g3e6e687
- Update to 1.0.0.alpha1.r37.g3e6e687

* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 1.0.0.alpha1.r33.g2588940
- Update to 1.0.0.alpha1.r33.g2588940

* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 1.0.0.alpha1.r32.gfb4f737
- Update to 1.0.0.alpha1.r32.gfb4f737

* Sun Oct 22 2023 M3DZIK <me@medzik.dev> - 1.0.0+alpha2
- Update to v1.0.0-alpha2

* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 1.0.0+alpha1
- Initial release
