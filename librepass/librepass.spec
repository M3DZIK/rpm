# disable debuginfo subpackage
%global debug_package %{nil}

%global git_commit c8dd4712bde94a94f96195ec63500d80ade77405

Name:          librepass
Epoch:         1
Version:       1.0.0.alpha1.r100.gc8dd471
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
* Mon Apr 29 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r100.gc8dd471-1
- Update to 1.0.0.alpha1.r100.gc8dd471

* Tue Apr 16 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r99.ge358989-1
- Update to 1.0.0.alpha1.r99.ge358989

* Tue Apr 16 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r98.g37a883d-1
- Update to 1.0.0.alpha1.r98.g37a883d

* Sun Apr 14 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r97.g2f6bf9f-1
- Update to 1.0.0.alpha1.r97.g2f6bf9f

* Fri Apr 12 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r95.g024447e-1
- Update to 1.0.0.alpha1.r95.g024447e

* Thu Apr 11 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r94.ga13e829-1
- Update to 1.0.0.alpha1.r94.ga13e829

* Wed Apr 10 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r93.g0d761cc-1
- Update to 1.0.0.alpha1.r93.g0d761cc

* Tue Apr 09 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r92.g93a55d9-1
- Update to 1.0.0.alpha1.r92.g93a55d9

* Mon Apr 08 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r90.g3f1777d-1
- Update to 1.0.0.alpha1.r90.g3f1777d

* Sun Apr 07 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r89.g49b6114-1
- Update to 1.0.0.alpha1.r89.g49b6114

* Fri Apr 05 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r88.g594c223-1
- Update to 1.0.0.alpha1.r88.g594c223

* Thu Apr 04 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r87.gf1ea7f5-1
- Update to 1.0.0.alpha1.r87.gf1ea7f5

* Sun Mar 31 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r86.g9cffcbe-1
- Update to 1.0.0.alpha1.r86.g9cffcbe

* Tue Mar 26 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r85.gfdfcbc4-1
- Update to 1.0.0.alpha1.r85.gfdfcbc4

* Sun Mar 24 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r84.g06c7370-1
- Update to 1.0.0.alpha1.r84.g06c7370

* Fri Mar 15 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r81.g151c4c1-1
- Update to 1.0.0.alpha1.r81.g151c4c1

* Thu Mar 14 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r77.g34307f3-1
- Update to 1.0.0.alpha1.r77.g34307f3

* Sun Feb 11 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r76.g0b9c7da-1
- Update to 1.0.0.alpha1.r76.g0b9c7da

* Sat Feb 03 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r75.g1b363bb-1
- Update to 1.0.0.alpha1.r75.g1b363bb

* Fri Jan 26 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r74.g1dee19d-1
- Update to 1.0.0.alpha1.r74.g1dee19d

* Mon Jan 15 2024 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r73.g407ca07-1
- Update to 1.0.0.alpha1.r73.g407ca07

* Fri Dec 29 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r69.g41e86bf-1
- Update to 1.0.0.alpha1.r69.g41e86bf

* Mon Dec 18 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r68.gff76e40-1
- Update to 1.0.0.alpha1.r68.gff76e40

* Sat Dec 16 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r67.g02b48fb-1
- Update to 1.0.0.alpha1.r67.g02b48fb

* Fri Dec 15 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r66.g5bf44b8-1
- Update to 1.0.0.alpha1.r66.g5bf44b8

* Thu Dec 14 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r65.g5bda734-1
- Update to 1.0.0.alpha1.r65.g5bda734

* Sun Dec 10 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r63.ge4ee6d6-1
- Update to 1.0.0.alpha1.r63.ge4ee6d6

* Fri Dec 08 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r62.g6372909-1
- Update to 1.0.0.alpha1.r62.g6372909

* Tue Dec 05 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r61.g5a47b4b-1
- Update to 1.0.0.alpha1.r61.g5a47b4b

* Sun Dec 03 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r58.g3107c8c-1
- Update to 1.0.0.alpha1.r58.g3107c8c

* Sat Dec 02 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r57.ge7db90c-1
- Update to 1.0.0.alpha1.r57.ge7db90c

* Fri Dec 01 2023 M3DZIK <me@medzik.dev> - 1:1.0.0.alpha1.r56.gefa51f9-1
- Update to 1.0.0.alpha1.r56.gefa51f9

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
