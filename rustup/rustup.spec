# disable debuginfo subpackage
%global debug_package %{nil}

Name:          rustup
Version:       1.26.0
Release:       1%{?dist}
Summary:       The Rust toolchain installer
License:       MIT
URL:           https://github.com/rust-lang/rustup

Source0:       https://github.com/rust-lang/rustup/archive/%{version}.tar.gz

BuildRequires: cargo

Requires: curl
Requires: xz
Requires: zstd

%description
The Rust toolchain installer

%prep
%setup -q -n %{name}-%{version}

%build
cargo build --release --features no-self-update

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./target/release/%{name} %{buildroot}%{_bindir}

for link in "cargo rustc rustdoc rust-gdb rust-lldb rustfmt cargo-fmt cargo-clippy clippy-driver cargo-miri"; do
  ln -s /usr/bin/rustup "%{buildroot}%{_bindir}/${link}"
done

# Generate completion files
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
%{buildroot}%{_bindir}/%{name} completions bash > %{buildroot}%{_datadir}/bash-completion/completions/rustup
%{buildroot}%{_bindir}/%{name} completions bash cargo > %{buildroot}%{_datadir}/bash-completion/completions/cargo
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
%{buildroot}%{_bindir}/%{name} completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/rustup.fish
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
%{buildroot}%{_bindir}/%{name} completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_rustup
%{buildroot}%{_bindir}/%{name} completions zsh cargo > %{buildroot}%{_datadir}/zsh/site-functions/_cargo

%files
%license LICENSE-MIT LICENSE-APACHE
%{_bindir}/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/fish/vendor_completions.d/*
%{_datadir}/zsh/site-functions/*

%changelog
* Sun Oct 29 2023 M3DZIK <me@medzik.dev> - 1.26.0
- Initial release
