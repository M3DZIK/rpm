# disable debuginfo subpackage
%global debug_package %{nil}

Name:          cargo-bloat
Version:       0.11.1
Release:       1%{?dist}
Summary:       Find out what takes most of the space in your executable.
License:       MIT
URL:           https://crates.io/crates/%{name}

Source0:       https://github.com/RazrFalcon/cargo-bloat/archive/v%{version}.tar.gz

BuildRequires: cargo

%description
Find out what takes most of the space in your executable.

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.11.1
- Update to 0.11.1

* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 0.9.3
- Initial release
