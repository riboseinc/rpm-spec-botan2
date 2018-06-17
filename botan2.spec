%global major_version 2

Name:           botan2
Version:        2.6.0
Release:        1%{?dist}
Summary:        Crypto and TLS for C++11

License:        BSD
URL:            https://botan.randombit.net/
Source0:        https://botan.randombit.net/releases/Botan-%{version}.tgz
Patch0:         01-remove-rpath-gcc.patch
Patch1:         02-sphinx-concurrency.patch

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  %{_bindir}/sphinx-build
BuildRequires:  %{_bindir}/rst2man
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

%description
Botan is a BSD-licensed crypto library written in C++. It provides a
wide variety of basic cryptographic algorithms, X.509 certificates and
CRLs, PKCS \#10 certificate requests, a filter/pipe message processing
system, and a wide variety of other features, all written in portable
C++. The API reference, tutorial, and examples may help impart the
flavor of the library. This is the current stable release branch 2.x
of Botan.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{summary}

This package contains HTML documentation for %{name}.


%package -n python%{python3_pkgversion}-%{name}
Summary:        Python3 bindings for %{name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
%{summary}

This package contains the Python3 binding for %{name}.


%prep
%setup -q -n Botan-%{version}
%patch0 -p0
%patch1 -p0


%build
export CXXFLAGS="${CXXFLAGS:-%{optflags}}"

# we have the necessary prerequisites, so enable optional modules
%global enable_modules bzip2,zlib,openssl

%{__python3} ./configure.py \
        --prefix=%{_prefix} \
        --libdir=%{_lib} \
        --docdir=%{_docdir} \
        --cc=gcc \
        --os=linux \
        --cpu=%{_arch} \
        --enable-modules=%{enable_modules} \
        --with-python-version=%{python3_version} \
        --with-sphinx \
        --with-rst2man \
        --distribution-info="$(cat /etc/os-release | grep -Po '(?<=^NAME=).*' | sed -e 's/\"//g')" \
        --disable-static-library \
        --with-debug-info

%make_build

%install
make install DESTDIR=%{buildroot}

sed -e '1{/^#!/d}' -i %{buildroot}%{python3_sitearch}/botan2.py

# doc installation fixups
mv %{buildroot}%{_docdir}/botan-%{version} %{buildroot}%{_pkgdocdir}
rm -r %{buildroot}%{_pkgdocdir}/manual/{.doctrees,.buildinfo}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license license.txt
%dir %{_pkgdocdir}
%{_pkgdocdir}/*.txt
%{_libdir}/libbotan-%{major_version}.so.*
%{_bindir}/botan
%{_mandir}/man1/botan.1.gz


%files devel
%license license.txt
%{_includedir}/*
%{_libdir}/libbotan-%{major_version}.so
%{_libdir}/pkgconfig/botan-%{major_version}.pc


%files doc
%license license.txt
%dir %{_pkgdocdir}
%{_pkgdocdir}/manual


%files -n python%{python3_pkgversion}-%{name}
%license license.txt
%{python3_sitearch}/%{name}.py
%{python3_sitearch}/__pycache__/*


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./botan-test


%changelog
* Sat Jun 16 2018 Daniel Wyatt <daniel.wyatt@ribose.com> - 2.6.0-1
- Adapted for CentOS/RHEL.
- Add patch to disable sphinx concurrency if not supported.
- Use %%python3_pkgversion macro.
- Add make build requirement.
- Revert %%ldconfig_scriptlets.
- Support quoted NAME in /etc/os-release.

* Thu Apr 12 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.6.0-1
- New upstream release

* Sun Apr 01 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-10
- Add patch to fix test suite failure due to expired test certificate

* Mon Mar 19 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-9
- Update empty patch file with the real patch contents.

* Sat Mar 17 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-8
- Add patch to fix test suite failures on ppc64le (see gh#1498).
- Add patch to fix test suite if SIMD instructions are not available (see gh#1495).

* Thu Mar 15 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-7
- Add patch to the Python module, supporting loading via
  libbotan-2.so.X.

* Thu Mar 15 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-6
- Set CXXFLAGS before calling configure.py.
- Patch for building on armv7hl (see gh#1495).
- Make dependency on rst2man explicit.
- Don't use Python2 at all.
- Remove shebang from botan2.py.
- Don't build a static library.
- Switch to %%ldconfig_scriptlets.

* Tue Mar 13 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.4.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Mar 06 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-4
- Exclude ppc64le arch, fix linter warnings

* Tue Mar 06 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-3
- Fix macro expansion in changelog section

* Sat Jan 13 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-2
- Remove INSTALL_ variables, not used anymore

* Thu Jan 11 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-1
- New upstream version; add new man page for botan command line utility

* Fri Dec 15 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.3.0-1
- New upstream version

* Thu Sep 07 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-4
- Backport upstream fix for broken GOST on i686

* Wed Sep 06 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-3
- Fix %%check section after rpath removal, generate debug symbols

* Thu Aug 31 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-2
- Fix issues that came up in review, see RH Bugzilla #1487067

* Sat Aug 12 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-1
- New package. No need for compat-openssl10-devel anymore with 2.2.0 release
