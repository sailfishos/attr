Name:       attr
Summary:    Utilities for managing filesystem extended attributes
Version:    2.5.1
Release:    1
License:    GPLv2+
URL:        https://github.com/sailfishos/attr
Source0:    %{name}-%{version}.tar.bz2
Patch0:     0003-attr-2.4.48-xattr-conf-nfs4-acls.patch
BuildRequires:  gettext
BuildRequires:  libtool >= 1.5
Requires:   libattr = %{version}-%{release}

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{name}-docs

%description doc
Man pages for %{name}.

%package -n libattr-devel
Summary:    Extended attribute static libraries and headers
License:    LGPLv2+
Requires:   %{name} = %{version}-%{release}
Requires:   libattr = %{version}

%description -n libattr-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%package -n libattr
Summary:    Dynamic library for extended attribute support
License:    LGPLv2+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
./autogen.sh
%configure --disable-static

%make_build

%install
%make_install

# get rid of libattr.a and libattr.la
rm -f %{buildroot}%{_libdir}/libattr.{a,la}

rm -f %{buildroot}%{_docdir}/%{name}/COPYING*
rm -f %{buildroot}%{_docdir}/%{name}/PORTING
mv %{buildroot}%{_docdir}/%{name} %{buildroot}%{_docdir}/%{name}-%{version}

%find_lang %{name}
%lang_package

%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license doc/COPYING
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr

%files -n libattr-devel
%defattr(-,root,root,-)
%{_libdir}/libattr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/attr/*

%files -n libattr
%defattr(-,root,root,-)
%license doc/COPYING.LGPL
%{_libdir}/libattr.so.*
%config(noreplace) %{_sysconfdir}/xattr.conf

%files doc
%defattr(-,root,root,-)
%{_mandir}/man*/*%{name}*.*
%{_docdir}/%{name}-%{version}
