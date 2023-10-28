Name:          cargo-edit
Version:       0.12.2
Release:       1%{?dist}
Summary:       Cargo commands for modifying dependencies in `Cargo.toml` file
License:       Apache-2.0 OR MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/killercup/cargo-edit/archive/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: openssl-devel

%description
A utility for managing cargo dependencies from the command line.

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
install -m 755 -p ./target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 0.12.2
- Initial release
