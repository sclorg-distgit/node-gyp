%{?scl:%scl_package node-gyp}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}

Name:       %{?scl_prefix}node-gyp
Version:    3.2.0
Release:    7%{?dist}
Summary:    Node.js native addon build tool
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/TooTallNate/node-gyp
Source0:    http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
Source1:    addon-rpm.gypi
BuildRoot:  %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

# These patches are Fedora-specific for the moment, although I'd like to find
# a way to support this kind of stuff upstream.
Patch1:     node-gyp-addon-gypi.patch
# use RPM installed headers by default instead of downloading a source tree
# for the currently running node version
#use gyp from scl
Patch2:    node-gyp-use-system-gyp.patch
BuildRequires:  %{?scl_prefix}nodejs-devel

#gyp is the actual build framework node-gyp uses
Requires: %{?scl_prefix}gyp
#this is the standard set of headers expected to build any node native module
Requires: %{?scl_prefix}nodejs-devel %{?scl_prefix}libuv-devel %{?scl_prefix}http-parser-devel
#we also need a C++ compiler to actually build stuff ;-)
Requires: gcc-c++

%description
node-gyp is a cross-platform command-line tool written in Node.js for compiling
native addon modules for Node.js, which takes away the pain of dealing with the
various differences in build platforms. It is the replacement to the node-waf
program which is removed for node v0.8.

%prep
%setup -q -n package

%patch2 -p1
%patch1 -p1
%nodejs_fixdep request 2.x
%nodejs_fixdep nopt 3.x
%nodejs_fixdep minimatch 3.x
%nodejs_fixdep --caret
%nodejs_fixdep glob 5.x
%nodejs_fixdep semver 5.x
%nodejs_fixdep npmlog 2.x

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/node-gyp
cp -pr addon*.gypi bin lib package.json %{buildroot}%{nodejs_sitelib}/node-gyp
cp -p %{SOURCE1} %{buildroot}%{nodejs_sitelib}/node-gyp/addon-rpm.gypi

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/node-gyp/bin/node-gyp.js %{buildroot}%{_bindir}/node-gyp

sed -i 's|argv.push('--no-parallel')|// argv.push('--no-parallel')|' %{buildroot}%{nodejs_sitelib}/node-gyp/lib/configure.js

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/node-gyp
%{_bindir}/node-gyp
%doc README.md LICENSE

%changelog
* Tue Feb 23 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 3.2.0-7
- Fix dependencies

* Wed Feb 17 2016 Tomas Hrcka <thrcka@redhat.com> - 3.2.0-6
- Rebase patches to new collection paths
- Remove --no-parallel argument from default config

* Thu Feb 11 2016 Tomas Hrcka <thrcka@redhat.com> - 3.2.0-3
- Disable dependency on v8314 collection

* Mon Nov 30 2015 Tomas Hrcka <thrcka@redhat.com> - 3.2.0-2
- New upstream release

* Thu Jul 23 2015 Tomas Hrcka <thrcka@redhat.com> - 2.0.2-1
- Rebase to latest upstream stable

* Thu Jan 29 2015 Tomas Hrcka <thrcka@redhat.com> - 1.0.2-3
- Fix dependencies versions of nopt and glob
- Backport Patch1  to new sources

* Thu Jan 08 2015 Tomas Hrcka <thrcka@redhat.com> - 1.0.2-1
- New upstream release

* Tue Mar 04 2014 Tomas Hrcka <thrcka@redhat.com> - 0.12.2-2
- Fix addon-rpm-gypi
- Backport patch to new sources

* Thu Jan 16 2014 Tomas Hrcka <thrcka@redhat.com> - 0.12.2-1
- New upstream release

* Tue Jan 14 2014 Tomas Hrcka <thrcka@redhat.com> - 0.10.6-2.3
- use proper path for gyp since its comming from v8 collection

* Thu Jan 09 2014 Tomas Hrcka <thrcka@redhat.com> - 0.10.6-2.2
<<<<<<< HEAD
- require v8314-v8  

* Thu Dec 05 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.6-2.1
- rebuilt with gyp from v8 scl 
=======
- replace dependency on nodejs010-v8 with v8314-v8

* Thu Dec 05 2013 Tomas Hrcka <thrcka@redhat.com> - 0.10.6-2.1
- rebuilt with gyp from v8 collection
>>>>>>> rhscl-2.1-nodejs010-rhel-6

* Tue Jul 30 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.6-2
- fix semver dep

* Fri Jul 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.6-1
- new upstream release 0.10.6

* Sat Jun 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.1-1
- new upstream release 0.10.1

* Sat Jun 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-3
- restrict to compatible arches

* Fri Apr 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.5-3
- Use proper prefixed paths for gyp

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-2
- add macro for EPEL6 dependency generation

* Fri Apr 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.5-2
- Add support for software collections

* Wed Apr 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-1
- new upstream release 0.9.5

* Wed Mar 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.1-2
- update addon-rpm.gypi
- split out addon-rpm.gypi so it's easier to maintain

* Wed Mar 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.1-1
- new upstream release 0.9.1

* Sat Feb 09 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.4-1
- new upstream release 0.8.4

* Mon Jan 21 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.3-1
- new upstream release 0.8.3
- add missing Requires on http-parser-devel

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-3
- add missing build section

* Sat Jan 05 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-2
- use RPM-installed headers by default
- now patched to use the system gyp instead of relying on a symlink

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-1
- new upstream release 0.8.2
- clean up for submission

* Thu Apr 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.4.1-2
- fix dependencies

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.4.1-1
- New upstream release 0.4.1

* Fri Apr 06 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.11-1
- New upstream release 0.3.11

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.10-1
- New upstream release 0.3.10

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.9-1
- New upstream release 0.3.9

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.8-1
- new upstream release 0.3.8

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.7-1
- new upstream release 0.3.7

* Thu Mar 15 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.5-1
- initial package
