%global debug_package %{nil}

Name:    cargo-bloat
Version: 0.12.1
Release: 1%{?dist}
Summary: Find out what takes most of the space in your executable
License: MIT
URL:     https://github.com/RazrFalcon/cargo-bloat

Source0: https://github.com/RazrFalcon/cargo-bloat/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
cp -af ./target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Aug 25 2024 M3DZIK <me@medzik.dev> - 0.12.1-1
- Initial release
