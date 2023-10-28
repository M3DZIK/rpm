Name:          cargo-outdated
Version:       0.18.3
Release:       1%{?dist}
Summary:       Cargo subcommand for displaying when dependencies are out of date
License:       MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/kbknapp/cargo-outdated/archive/v%{version}.tar.gz

BuildRequires: cargo

%description
Cargo subcommand for displaying when dependencies are out of date.

%prep
%setup -q -n {name}-%{version}

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.18.3
- Initial release
