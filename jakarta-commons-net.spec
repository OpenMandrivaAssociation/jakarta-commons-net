%define base_name	net
%define short_name	commons-%{base_name}
%define	section		free
%define build_tests	0
%define gcj_support	1

Name:		jakarta-%{short_name}
Version:	1.4.1
Release:	%mkrel 5.0.0
Epoch:		0
Summary:	Jakarta Commons Net Package
License:	Apache License
Group:		Development/Java
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
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	oro >= 0:2.0.7
%if %{build_tests}
BuildRequires:	junit >= 0:3.8.1
%endif
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
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
