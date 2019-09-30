%global dnf_conflict 2.8.8

Name:           librepo
Version:        1.9.1
Release:        1
Summary:        Repodata downloading library
License:        LGPLv2.1
URL:            https://github.com/rpm-software-management/librepo
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake gcc doxygen pkgconfig(glib-2.0)
BuildRequires:  check-devel gpgme-devel libattr-devel
BuildRequires:  libcurl-devel >= 7.19.0
BuildRequires:  pkgconfig(libxml-2.0) pkgconfig(libcrypto) pkgconfig(openssl)

%description
A library providing C and Python (libcURL like) API to downloading packages
and linux repository metadata in rpm-md format.

%package devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-gpg python3-devel python3-flask
BuildRequires:  python3-nose python3-sphinx python3-pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      platform-python-%{name} < %{version}-%{release}
Conflicts:      python3-dnf < %{dnf_conflict}

%description -n python3-%{name}
Python 3 bindings for the librepo library.

%prep
%autosetup -p1

mkdir build-py3

%build
cd build-py3
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python3} ..
  %make_build
cd ..

%check
cd build-py3
  make ARGS="-V" test
cd ..

%install
cd build-py3
  %make_install
cd ..

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%{python3_sitearch}/%{name}/

%changelog
* Fri Aug 17 2018 openEuler Buildteam <buildteam@openeuler.org> - 1.9.1-1
- Package init
