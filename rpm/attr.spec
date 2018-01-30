Name:       attr
Summary:    Utilities for managing filesystem extended attributes
# Currently not updated to version 2.4.48 as acl upstream has not 
# released version that is build compatible with attr 2.4.48.
# After that is there we can update this further.
Version:    2.4.47
Release:    1
Group:      System/Base
License:    GPLv2+
URL:        http://savannah.nongnu.org/projects/attr
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  gettext
BuildRequires:  libtool >= 1.5
Requires:   libattr = %{version}-%{release}

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr-devel
Summary:    Extended attribute static libraries and headers
License:    LGPLv2+
Group:      Development/Libraries
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
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
make distclean
make configure
%configure --disable-static \
    --libexecdir=%{_libdir}


make %{?_smp_mflags}  LIBTOOL="libtool --tag=CC"

%install
rm -rf %{buildroot}

make install-dev DESTDIR=%{buildroot}
make install-lib DESTDIR=%{buildroot}

# get rid of libattr.a and libattr.la
rm -f %{buildroot}%{_libdir}/libattr.{a,la}

# fix permissions
chmod 0755 %{buildroot}/%{_libdir}/libattr.so.*.*.*

rm -rf %{buildroot}%{_docdir}

%find_lang %{name}
%docs_package
%lang_package

%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc doc/COPYING
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr

%files -n libattr-devel
%defattr(-,root,root,-)
%{_libdir}/libattr.so
%{_includedir}/attr/*

%files -n libattr
%defattr(-,root,root,-)
%doc doc/COPYING.LGPL
%{_libdir}/libattr.so.*
