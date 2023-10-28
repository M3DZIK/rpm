Name:          cargo-edit
Version:       0.12.2
Release:       3%{?dist}
Summary:       Cargo commands for modifying dependencies in a `Cargo.toml` file
License:       Apache-2.0 OR MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/killercup/cargo-edit/archive/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: openssl-devel
BuildRequires: libgit2-devel

%description
A utility for managing cargo dependencies from the command line.

%prep
%setup -q -n %{name}-%{version}
sed -i '/\"vendored-libgit2\"/d' Cargo.toml

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/cargo-{add,rm,set-version,upgrade} %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/cargo-add
%{_bindir}/cargo-rm
%{_bindir}/cargo-set-version
%{_bindir}/cargo-upgrade

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 0.12.2
- Initial release
