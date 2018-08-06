%global debug_package %{nil}

%global gopath      %{_datadir}/gocode
%global goipath     github.com/radanalyticsio/oshinko-cli

%global golang_version 1.10

%gometa

Name:           oshinko-cli
Version:        0.5.4
Release:        0%{?dist}
Summary:        Command line interface for spark cluster management app

License:        ASL 2.0
URL:            https://github.com/radanalyticsio/oshinko-cli
Source0:        https://%{goipath}/archive/v%{version}.tar.gz

Patch0:         01-scripts-build.patch

ExclusiveArch: x86_64

BuildRequires:  golang >= %{golang_version}

%description
The oshinko application manages Apache Spark clusters on OpenShift. The application
consists of a REST server (oshinko-rest) and a web UI and is designed to run in an
OpenShift project.

This repository contains tools to launch the oshinko application along with the source
code for the oshinko REST server in the rest subdirectory. The source code for the web
UI is located in a different repository.

%package -n %{goname}-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{goname}-devel
The oshinko application manages Apache Spark clusters on OpenShift. The application
consists of a REST server (oshinko-rest) and a web UI and is designed to run in an
OpenShift project.

This repository contains tools to launch the oshinko application along with the source
code for the oshinko REST server in the rest subdirectory. The source code for the web
UI is located in a different repository.

This package contains library source intended for building other packages which use 
import path with %{goipath} prefix.

%prep
%gosetup -q -n %{name}-%{version}
%patch0 -p1

%build
%gobuildroot
make build

%install
%goinstall
install -Dpm 0755 _output/oshinko %{buildroot}%{_bindir}/oshinko
install -Dpm 0755 _output/oshinko-cli %{buildroot}%{_bindir}/oshinko-cli

%check
%gochecks

%files
%license LICENSE
%{_bindir}/oshinko
%{_bindir}/oshinko-cli

%files -n %{goname}-devel -f devel.file-list
%license LICENSE
%doc README.md

%changelog
* Thu Jul 26 2018 Ricardo Martinelli de Oliveira <rmartine@redhat.com> - 0-0.5.3
- First package for Fedora