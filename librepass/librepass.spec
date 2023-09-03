%global tag 1.0.0-alpha1

Name:          librepass
Version:       1.0.0+alpha1
Release:       1%{?dist}
Summary:       LibrePass Desktop Application
License:       GPL-3.0
URL:           https://librepass.medzik.dev

Source0:       https://github.com/LibrePass/LibrePass-Desktop/archive/v%{tag}.tar.gz

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
%setup -q -n LibrePass-Desktop-%{tag}

%build
# Build and package
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
cp -arf ./usr/{bin,lib} %{buildroot}%{_javadir}/%{name}/

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
ln -s %{_javadir}/%{name}/bin/%{name} %{buildroot}%{_bindir}/%{name}

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
* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 1.0.0+alpha1
- Initial release
