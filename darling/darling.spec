%global debug_package %{nil}
%global _build_id_links none
%global __brp_mangle_shebangs %{nil}

%global git_commit a36bf0c07b16675b446377890c5f6f74563f84dd

Name:    darling
Version: 0.0.0.179.a36bf0c07b16675b446377890c5f6f74563f84dd
Release: 1%{?dist}
Summary: Darwin/macOS emulation layer for Linux
License: GPL-3
URL:     https://www.darlinghq.org/

Source0: https://github.com/darlinghq/darling/archive/%{git_commit}.tar.gz

BuildRequires: git
BuildRequires: git-lfs
BuildRequires: make
BuildRequires: cmake
BuildRequires: clang
BuildRequires: bison
BuildRequires: dbus-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: glibc-devel(x86-32)
BuildRequires: fuse-devel
BuildRequires: systemd-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: cairo-devel
BuildRequires: freetype-devel
BuildRequires: freetype-devel(x86-32)
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo-devel(x86-32)
BuildRequires: fontconfig-devel
BuildRequires: fontconfig-devel(x86-32)
BuildRequires: libglvnd-devel
BuildRequires: libglvnd-devel(x86-32)
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGL-devel(x86-32)
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libEGL-devel(x86-32)
BuildRequires: mesa-libGLU-devel
BuildRequires: mesa-libGLU-devel(x86-32)
BuildRequires: vulkan-loader-devel
BuildRequires: vulkan-headers
BuildRequires: glslang-devel
BuildRequires: glslc
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: libbsd-devel
BuildRequires: libXcursor-devel
BuildRequires: libXrandr-devel
BuildRequires: giflib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libxkbfile-devel
BuildRequires: openssl-devel
BuildRequires: llvm-devel
BuildRequires: libcap-devel
BuildRequires: libavcodec-free-devel
BuildRequires: libavformat-free-devel

%description
%{summary}

%prep
%setup -q -n darling-%{git_commit}

cd ..
rm -rf darling-%{git_commit}
git clone --depth 1 --recursive -b %{git_commit} https://github.com/darlinghq/darling.git darling-%{git_commit}

%build
CFLAGS="" CXXFLAGS="" CPPFLAGS="" LDFLAGS="" cmake -S . -B redhat-linux-build -DCMAKE_INSTALL_PREFIX=/usr
%cmake_build

%install
%cmake_install

sed -i 's@/usr/local@/usr@g' %{buildroot}%{_prefix}/lib/binfmt.d/%{name}.conf

%files
%license LICENSE
%{_prefix}/lib/binfmt.d/%{name}.conf
%{_libexecdir}/%{name}
%{_bindir}/%{name}*

%changelog
* Fri Jul 26 2024 M3DZIK <me@medzik.dev> - 0.0.0-1
- Initial release
