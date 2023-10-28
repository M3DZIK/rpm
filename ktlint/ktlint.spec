# disable debuginfo subpackage
%global debug_package %{nil}

Name:          ktlint
Version:       1.0.1
Release:       2%{?dist}
Summary:       An anti-bikeshedding Kotlin linter with built-in formatter
License:       MIT
BuildArch:     noarch
ExclusiveArch: %{java_arches} noarch

Source0:       https://github.com/pinterest/ktlint/archive/%{version}.tar.gz

BuildRequires: java-latest-openjdk-devel

Requires:      jre >= 11

%description
An anti-bikeshedding Kotlin linter with built-in formatter

%prep
%setup -q -n ktlint-%{version}

%build
./gradlew --no-configuration-cache --no-scan --no-daemon --console plain -Pktlint.publication.signing.enable=false shadowJarExecutable

%install
install -d %{buildroot}%{_bindir}
cp -af ./ktlint-cli/build/run/ktlint %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 1.0.1
- Initial release