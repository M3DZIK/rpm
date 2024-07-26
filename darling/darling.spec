%global debug_package %{nil}
%global _build_id_links none

%global _git_tag master

Name:    darling
Version: 0.0.0
Release: 1%{?dist}
Summary: Darwin/macOS emulation layer for Linux
License: GPL-3
URL:     https://www.darlinghq.org/

Source0: https://github.com/darlinghq/darling/archive/%{_git_tag}.tar.gz

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
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: libbsd-devel
BuildRequires: libXcursor-devel
BuildRequires: libXrandr-devel
BuildRequires: giflib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libxkbfile-devel
BuildRequires: openssl-devel
BuildRequires: llvm
BuildRequires: libcap-devel
BuildRequires: libavcodec-free-devel
BuildRequires: libavformat-free-devel

%description
%{summary}

%prep
git clone --depth 1 --recursive -b %{_git_tag} https://github.com/darlinghq/darling.git %{_builddir}/%{name}

%build
cd %{_builddir}/%{name}

mkdir build && cd build
CFLAGS="" CXXFLAGS="" CPPFLAGS="" LDFLAGS="" cmake ..
make -j$(nproc)

%install
cd %{_builddir}/%{name}/build

cmake --install . --prefix %{buildroot}%{_prefix}

sed -i 's@/usr/local@/usr@g' %{buildroot}%{_prefix}/lib/binfmt.d/%{name}.conf

%files
%license %{name}/LICENSE
%{_prefix}/lib/binfmt.d/%{name}.conf
%{_libexecdir}/%{name}
%{_bindir}/%{name}*

%changelog
* Fri Jul 26 2024 M3DZIK <me@medzik.dev> - 0.0.0-1
- Initial release
