# disable debuginfo subpackage
%global debug_package %{nil}

Name:          zls
Version:       0.11.0
Release:       1%{?dist}
Summary:       The zig language server for all your Zig editor tooling needs, from autocomplete to goto-def! 
License:       MIT
URL:           https://github.com/zigtools/zls

Source0:       https://github.com/zigtools/zls/archive/%{version}.tar.gz

BuildRequires: zig

%description
The Zig Language Server (zls) is a tool that implements Microsoft's Language Server Protocol for Zig in Zig

%prep
%setup -q -n %{name}-%{version}

%build
zig build -Doptimize=ReleaseSafe

%install
install -d %{buildroot}%{_bindir}
cp -af -p ./zig-out/bin/zls %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Fri Dec 29 2023 M3DZIK <me@medzik.dev> - 0.11.0
- Initial release
