Name:          cargo-audit
Version:       0.18.3
Release:       1%{?dist}
Summary:       Audit Cargo.lock for crates with security vulnerabilities
License:       Apache-2.0 OR MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/rustsec/rustsec/archive/cargo-audit/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: openssl-devel

%description
Audit Cargo.lock for crates with security vulnerabilities

%prep
%setup -q -n rustsec-cargo-audit-v%{version}

%build
cargo build --release --features fix

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.18.3
- Initial release
