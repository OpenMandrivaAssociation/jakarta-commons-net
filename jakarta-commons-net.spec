%define base_name	net
%define short_name	commons-%{base_name}
%define	section		free
%define build_tests	0
%define gcj_support	1

Name:		jakarta-%{short_name}
Version:	1.4.1
Release:	%mkrel 5.0.7
Epoch:		0
Summary:	Jakarta Commons Net Package
License:	Apache License
Group:		Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-%{version}-src.tar.bz2
Patch0:		%{name}-crosslink.patch
Url:		http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:	ant
%if %{build_tests}
BuildRequires:	ant-junit
%endif
BuildRequires:	java-devel
BuildRequires:	java-javadoc
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	oro >= 0:2.0.7
%if %{build_tests}
BuildRequires:	junit >= 0:3.8.1
%endif
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
Obsoletes:	%{short_name} < %{epoch}:%{version}-%{release}
Provides:	%{short_name} = %{epoch}:%{version}-%{release}

%description
This is an Internet protocol suite Java library originally developed by
ORO, Inc.  This version supports Finger, Whois, TFTP, Telnet, POP3, FTP,
NNTP, SMTP, and some miscellaneous protocols like Time and Echo as well
as BSD R command support. The purpose of the library is to provide
fundamental protocol access, not higher-level abstractions. 

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}
%patch0 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
mkdir -p target/lib
ln -s %{_javadir}/oro.jar target/lib
%if %{build_tests}
ln -s %{_javadir}/junit.jar target/lib
%endif

export CLASSPATH=$(build-classpath oro)
%if %{build_tests}
export CLASSPATH=$CLASSPATH:$(build-classpath junit)
%endif
%{__perl} -pi -e 's/compile,test/compile/' build.xml
%{ant} -Dnoget=true -Dfinal.name=commons-net-%{version} \
  -Dj2se.api=%{_javadocdir}/java dist

%install
%{__rm} -rf %{buildroot}

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-5.0.5mdv2011.0
+ Revision: 665807
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-5.0.4mdv2011.0
+ Revision: 606061
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-5.0.3mdv2010.1
+ Revision: 523004
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.4.1-5.0.2mdv2010.0
+ Revision: 425443
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.4.1-5.0.1mdv2009.0
+ Revision: 167949
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.1-5.0.1mdv2008.1
+ Revision: 120917
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Fri Sep 21 2007 David Walluck <walluck@mandriva.org> 0:1.4.1-5.0.0mdv2008.0
+ Revision: 92015
- rebuild as archs seem to be out of sync
- add epochs to BuildRequires
- version Obsoletes/Provides
- remove buildroot in %%install
- create javadoc symlink
- remove javadoc scriptlets

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.1-5mdv2008.0
+ Revision: 87415
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.4.1-4mdv2008.0
+ Revision: 82875
- rebuild


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.4.1-3mdv2007.1
+ Revision: 143926
- rebuild for 2007.1
- Import jakarta-commons-net

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.4-2mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.4.1-1mdk
- 1.4.1
- rediff crosslink patch
- BuildRequires: ant, java-devel

* Mon May 16 2005 David Walluck <walluck@mandriva.org> 0:1.2.2-3.1mdk
- release

* Sat Nov 13 2004 Ville Skyttä <scop at jpackage.org> - 0:1.2.2-3jpp
- BuildRequire ant-junit, thanks to Nicolas Mailhot for the catch.
- Crosslink with local J2SE API docs, remove extra api/ from javadoc dir.

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.2.2-2jpp
- Rebuild with ant-1.6.2

* Mon Jun 28 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.2.2-1jpp
- Update to 1.2.2

