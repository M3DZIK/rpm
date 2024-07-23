%global debug_package %{nil}
%global _build_id_links none

%global common_libdir %{_prefix}/lib
%global dartlibdir %{common_libdir}/dart-sdk

Name:    dart
Version: 3.4.4
Release: 2%{?dist}
Summary: The dart programming language SDK
License: BSD-3
URL:     https://dart.dev

Source0: https://github.com/dart-lang/sdk/archive/refs/tags/%{version}.tar.gz

BuildRequires: python3
BuildRequires: git

%description
%{summary}

%prep
git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git %{_builddir}/depot_tools

%setup -q -n sdk-%{version}

%{_builddir}/depot_tools/fetch --no-history dart

%build
cd sdk

%ifarch x86_64
arch=x64
%elifarch aarch64
arch=arm64
%endif

./tools/build.py --mode release --arch $arch create_sdk

%install
install -d %{buildroot}%{dartlibdir}
cp -arf ./sdk/out/*/dart-sdk/* %{buildroot}%{dartlibdir}/

# Set up symbolic links for the executables
install -d %{buildroot}%{_bindir}
for f in dart dartaotruntime; do
    ln -s %{dartlibdir}/bin/$f %{buildroot}%{_bindir}/$f
done

%files
%license LICENSE
%{dartlibdir}
%{_bindir}/%{name}
%{_bindir}/%{name}aotruntime

%changelog
* Mon Jul 22 2024 M3DZIK <me@medzik.dev> - 3.4.4-1
- Initial release
