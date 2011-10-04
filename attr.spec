#
# Please submit bugfixes or comments via http://bugs.meego.com/
#

Name:           attr
Version:        2.4.46
Release:        1
Summary:        Utilities for managing filesystem extended attributes
Source:         http://download.savannah.gnu.org/releases-noredirect/attr/attr-%{version}.src.tar.gz
# make it ready for rpmbuild
Patch0:         attr-2.4.32-build.patch
# silence compile-time warnings
Patch1:         attr-2.4.44-warnings.patch
# getfattr: return non-zero exit code on failure (#660619)
Patch2:         attr-2.4.44-bz660619.patch
# walk_tree: do not follow symlink to directory with -h (#660613)
Patch3:         attr-2.4.44-bz660613.patch
# fix typos in attr(1) man page (#669095)
Patch4:         attr-2.4.44-bz669095.patch

License:        GPLv2+
Url:            http://acl.bestbits.at/
Group:          System/Base
BuildRequires:  gettext
BuildRequires:  libtool >= 1.5
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr
License:        LGPLv2+
Summary:        Dynamic library for extended attribute support
Group:          System/Libraries

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%package -n libattr-devel
License:        LGPLv2+
Summary:        Extended attribute static libraries and headers
Group:          Development/Libraries
Requires:       libattr = %{version}

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# attr abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir} --disable-gettext
make %{?_smp_mflags}  LIBTOOL="libtool --tag=CC"

%install
%make_install
make install-dev DESTDIR=%{buildroot}
make install-lib DESTDIR=%{buildroot}

# get rid of libattr.a and libattr.la
rm -f %{buildroot}/%{_lib}/libattr.a
rm -f %{buildroot}/%{_lib}/libattr.la
rm -f %{buildroot}%{_libdir}/libattr.a
rm -f %{buildroot}%{_libdir}/libattr.la

# fix links to shared libs and permissions
rm -f %{buildroot}/%{_libdir}/libattr.so
ln -sf ../../%{_lib}/libattr.so %{buildroot}/%{_libdir}/libattr.so
chmod 0755 %{buildroot}/%{_lib}/libattr.so.*.*.*
rm -rf %{buildroot}%{_docdir}

%clean
rm -rf %{buildroot}

%docs_package


%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc doc/COPYING
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr

%files -n libattr-devel
%defattr(-,root,root)
/%{_lib}/libattr.so
%{_includedir}/attr
%{_libdir}/libattr.*

%files -n libattr
%defattr(-,root,root,-)
/%{_lib}/libattr.so.*

