Name:          cargo-audit
Version:       0.12.2
Release:       1%{?dist}
Summary:       Audit Cargo.lock for crates with security vulnerabilities
License:       Apache-2.0 OR MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/killercup/cargo-edit/archive/cargo-audit/v%{version}.tar.gz

BuildRequires: cargo

%description
Audit Cargo.lock for crates with security vulnerabilities

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release --features fix

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.12.2
- Initial release
