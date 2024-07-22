# disable debuginfo subpackage
%global debug_package %{nil}

%global dartlibdir /opt/dark-sdk

Name:    dart
Version: 3.4.4
Release: 1%{?dist}
Summary: The dart programming language SDK
License: BSD-3

Source0: https://github.com/dart-lang/sdk/archive/refs/tags/%{version}.tar.gz

BuildRequires: python3
BuildRequires: git

%description
%{summary}

%prep
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git --depth 1

%setup -q -n sdk-%{version}

%{buildroot}/depot_tools/fetch dart --no-history

%build
cd sdk

%ifarch x86_64
arch=x64
%elifarch aarch64
arch=arm64
%endif

./tools/build.py --mode release --arch $arch create_sdk

%install
%ifarch x86_64
out_dir=out/ReleaseX64
%elifarch aarch64
out_dir=out/ReleaseARM64
%endif

install -d %{buildroot}%{dartlibdir}
cp -arf ./${out_dir}/dart-sdk %{buildroot}%{dartlibdir}/

# Set up symbolic links for the executables
install -d %{buildroot}%{_bindir}
for f in dart dartaotruntime; do
    ln -s %{dartlibdir}/bin/$f %{buildroot}%{_bindir}/$f
done

%files
%license LICENSE
%{dartlibdir}
%{_bindir}/%{name}

%changelog
* Mon Jul 22 2024 M3DZIK <me@medzik.dev> - 3.4.4-1
- Initial release
