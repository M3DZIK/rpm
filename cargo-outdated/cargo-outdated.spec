# disable debuginfo subpackage
%global debug_package %{nil}

Name:          cargo-outdated
Version:       0.14.0
Release:       1%{?dist}
Summary:       Cargo subcommand for displaying when dependencies are out of date
License:       MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/kbknapp/cargo-outdated/archive/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: libgit2-devel

%description
Cargo subcommand for displaying when dependencies are out of date.

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

%files
%license LICENSE-MIT
%{_bindir}/%{name}

%changelog
* Fri Nov 03 2023 M3DZIK <me@medzik.dev> - 0.14.0
- Update to 0.14.0

* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.13.1
- Initial release
