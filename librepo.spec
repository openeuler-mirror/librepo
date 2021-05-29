%global libcurl_version 7.28.0
%global dnf_conflict 2.8.8

%bcond_without python3
%bcond_without pythontests
%bcond_with python2
%bcond_with zchunk

Name:                    librepo
Version:                 1.12.0
Release:                 3
Summary:                 Repodata downloading library                 
License:                 LGPLv2+
URL:                     https://github.com/rpm-software-management/librepo
Source0:                 %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:                  backport-CVE-2020-14352-Validate-path-read-from-repomd.xml.patch
Patch1:                  backport-Fix-memory-leaks.patch
Patch2:                  backport-Fix-lr_fastestmirror_prepare-Resource-leaks.patch
Patch3:                  backport-Fix-lr_get_curl_handle-Check-curl_easy-handle-before.patch
Patch4:                  backport-lr_get_curl_handle-Strict-check-of-curl_easy_setopt-.patch
Patch5:                  backport-Remove-may-be-used-uninitialized-compiler-warnings.patch

BuildRequires:           cmake check-devel doxygen pkgconfig(glib-2.0) gcc
BuildRequires:           libcurl-devel >= %{libcurl_version} pkgconfig(libxml-2.0)
BuildRequires:           pkgconfig(openssl) gpgme-devel libattr-devel pkgconfig(libcrypto)
Requires:                libcurl >= %{libcurl_version}

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package                 devel
Summary:                 Repodata downloading library
Requires:                %{name} = %{version}-%{release}

%description devel
Development files for librepo.

%if %{with python2}
%package -n              python2-librepo
Summary:                 Python bindings for the librepo library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:           python2-sphinx python2-devel python2-flask python2-nose
BuildRequires:           python2-requests python2-pyxattr python2-gpg
Requires:                %{name} = %{version}-%{release}
Conflicts:               python2-dnf < %{dnf_conflict}

%description -n python2-%{name}
Python 2 bindings for the librepo library.
%endif

%package -n              python3-librepo
Summary:                 Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:           python3-devel python3-gpg python3-flask python3-nose
BuildRequires:           python3-pyxattr python3-requests python3-sphinx
Requires:                %{name} = %{version}-%{release}
Obsoletes:               platform-python-%{name} < %{version}-%{release}
Conflicts:               python3-dnf < %{dnf_conflict}

%description -n         python3-%{name}
Python 3 bindings for the librepo library.

%prep
%autosetup -p1

mkdir build-py2
mkdir build-py3

%build
%if %{with python2}
pushd build-py2
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python2} %{!?with_zchunk:-DWITH_ZCHUNK=OFF} -DENABLE_PYTHON_TESTS=%{?with_pythontests:ON}%{!?with_pythontests:OFF} ..
  %make_build
popd
%endif

%if %{with python3}
pushd build-py3
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python3} %{!?with_zchunk:-DWITH_ZCHUNK=OFF} -DENABLE_PYTHON_TESTS=%{?with_pythontests:ON}%{!?with_pythontests:OFF} ..
  %make_build
popd
%endif

%check
%if %{with python2}
pushd build-py2
  #ctest -VV
  make ARGS="-V" test
popd
%endif

%if %{with python3}
pushd build-py3
  #ctest -VV
  make ARGS="-V" test
popd
%endif

%install
%if %{with python2}
pushd build-py2
  %make_install
popd
%endif

%if %{with python3}
pushd build-py3
  %make_install
popd
%endif

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if %{with python2}
%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%endif

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%endif

%changelog
* Sat May 29 2021 fuanan <fuanan3@huawei.com> - 1.12.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:[add] backport patches from upstream
       Fix:memory leaks
       Fix:lr_fastestmirror_prepare:Resource leaks
       Fix:lr_get_curl_handle:Check curl_easy handle before use
       lr_get_curl_handle:Strict check of curl_easy_setopt return code
       Remove "may be used uninitialized" compiler warnings

* Mon Jan 25 2021 fuanan <fuanan3@huawei.com> - 1.12.0-2
- fix CVE-2020-14352

* Tue Aug 04 2020 shanzhikun <shanzhikun@huawei.com> - 1.12.0-1
- upgrade librepo to 1.12.0.

* Tue Jan 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.11.0-2
- Pakcage init
