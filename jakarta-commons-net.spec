%define base_name	net
%define short_name	commons-%{base_name}
%define	section		free
%define build_tests	0
%define gcj_support	1

Summary:	Jakarta Commons Net Package
Name:		jakarta-%{short_name}
Version:	3.1
Release:	1
License:	Apache License
Group:		Development/Java
Url:		http://jakarta.apache.org/commons/%{base_name}/
Source0:	http://www.apache.org/dist/jakarta/commons/net/source/commons-net-3.1-src.tar.gz
Patch0:		%{name}-crosslink.patch
%if !%{gcj_support}
Buildarch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
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
%rename		%{short_name}

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
%setup -qn %{short_name}-%{version}
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
sed -i -e 's/compile,test/compile/' build.xml
%ant \
	-Dnoget=true \
	-Dfinal.name=commons-net-%{version} \
	-Dj2se.api=%{_javadocdir}/java \
	dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


