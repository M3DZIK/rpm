# disable debuginfo subpackage
%global debug_package %{nil}

Name:          apktool
Version:       2.10.0
Release:       1%{?dist}
Summary:       A tool for reverse engineering Android apk files
License:       Apache-2.0 
BuildArch:     noarch
ExclusiveArch: %{java_arches} noarch

Source0:       https://github.com/iBotPeaches/Apktool/archive/v%{version}.tar.gz
Source1:       apktool.sh

# https://apktool.org/docs/build/
# With R8 required JDK > 11
BuildRequires: java-11-openjdk-devel

Requires:      jre >= 1.8.0

%description
%{summary}.

%prep
%setup -q -n Apktool-%{version}

%build
./gradlew --no-daemon build shadowJar proguard

%install
install -d %{buildroot}%{_datadir}/%{name}
cp -af ./brut.apktool/apktool-cli/build/libs/apktool-%{version}*.jar %{buildroot}%{_datadir}/%{name}/apktool.jar

sed -i "s,%apktooljar%,%{_datadir}/%{name}/apktool.jar,g" %{SOURCE1}

install -d %{buildroot}%{_bindir}
install -m 0644 -p %{SOURCE1} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE.md
%{_datadir}/%{name}
%{_bindir}/%{name}

%changelog
* Fri Sep 27 2024 M3DZIK <me@medzik.dev> - 2.10.0-1
- Initial release
