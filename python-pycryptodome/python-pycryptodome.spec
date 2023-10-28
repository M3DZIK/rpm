# Created by pyp2rpm-3.3.10
%global pypi_name pycryptodome
%global pypi_version 3.19.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Cryptographic library for Python

License:        BSD, Public Domain
URL:            https://www.pycryptodome.org
Source0:        %{pypi_source}

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
PyCryptodome PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.It supports Python 2.7, Python 3.5 and newer, and
PyPy. You can install it with :: pip install pycryptodomeAll modules are
installed under the Crypto package.Check the pycryptodomex_ project for the
equivalent library that works under the Cryptodome package. PyCryptodome is a
fork of PyCrypto.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
PyCryptodome PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.It supports Python 2.7, Python 3.5 and newer, and
PyPy. You can install it with :: pip install pycryptodomeAll modules are
installed under the Crypto package.Check the pycryptodomex_ project for the
equivalent library that works under the Cryptodome package. PyCryptodome is a
fork of PyCrypto.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%license Doc/LEGAL/copy/LICENSE.libtom Doc/LEGAL/copy/LICENSE.orig Doc/LEGAL/copy/LICENSE.python-2.2 Doc/src/license.rst LICENSE.rst
%doc README.rst
%{python3_sitearch}/Crypto
%{python3_sitearch}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sat Oct 28 2023 M3DZIK <me@medzik.dev> - 3.19.0-1
- Initial package.
