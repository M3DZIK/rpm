%global debug_package %{nil}

Name:    cargo-edit
Version: 0.12.3
Release: 1%{?dist}
Summary: Managing cargo dependencies from the command line
License: Apache-2.0 or MIT
URL:     https://github.com/killercup/cargo-edit

Source0: https://github.com/killercup/cargo-edit/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: openssl-devel
%if 0%{?fedora} >= 41
BuildRequires: openssl-devel-engine
%endif
BuildRequires: libgit2-devel

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release --no-default-features --features 'add rm set-version upgrade'

%install
install -d %{buildroot}%{_bindir}
cp -af ./target/release/cargo-{add,rm,set-version,upgrade} %{buildroot}%{_bindir}/

%files
%license LICENSE
%{_bindir}/cargo-{add,rm,set-version,upgrade}

%changelog
* Sun Aug 25 2024 M3DZIK <me@medzik.dev> - 0.12.3-1
- Initial release
