%global __os_install_post %{nil}
%global debug_package %{nil}
%global _build_id_links none
%global __brp_mangle_shebangs %{nil}

# explicitly ignore all the bogus dependencies that the auto-scanner finds in `/usr/libexec/darling`
#
# note that we *don't* want to simply use `__requires_exclude_from` to exclude `/usr/libexec/darling` from scanning,
# since we *do* want our Mach-O scanner to scan that tree (and there's no way to only exclude paths for some dependency generators; it's all or nothing).
%global __requires_exclude ^(/bin/sed|/bin/sh|/usr/bin/perl|/usr/bin/python2.7|/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7|/usr/bin/python|/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/bin/ruby|/usr/bin/env|/usr/bin/ruby)$

%global git_commit 203af1f604727e13032df1870e3491572e7d6704

Name:    darling
Version: 0.0.0.4224.203af1
Release: 4%{?dist}
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
git clone --recursive https://github.com/darlinghq/darling.git darling-%{git_commit}
cd darling-%{git_commit}

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
* Sun Aug 04 2024 M3DZIK <me@medzik.dev> - 0.0.0.4224.203af1-4
- Exclude requires from internal darling files

* Sun Jul 28 2024 M3DZIK <me@medzik.dev> - 0.0.0.4224.203af1-1
- Initial release
