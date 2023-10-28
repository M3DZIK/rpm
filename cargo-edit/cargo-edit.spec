%global crate cargo-edit

Name:           cargo-edit
Version:        0.12.2
Release:        3%{?dist}
Summary:        Cargo commands for modifying dependencies in a `Cargo.toml` file.

License:        Apache-2.0 OR MIT
URL:            https://crates.io/crates/cargo-edit
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 23
BuildRequires:  openssl-devel
BuildRequires:  libgit2-devel

%description
A utility for managing cargo dependencies from the command line.

%files
%license LICENSE
%doc README.md
%{_bindir}/cargo-add
%{_bindir}/cargo-rm
%{_bindir}/cargo-set-version
%{_bindir}/cargo-upgrade

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep
sed -i '/\"vendored-libgit2\"/d' Cargo.toml

%build
cargo build --release

%install
%cargo_install

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 0.12.2
- Initial release
