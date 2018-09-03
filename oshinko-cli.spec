%if 0%{?rhel} == 7
%define debug_package %{nil}
%endif

%global goipath     github.com/radanalyticsio/oshinko-cli
%global gopath      %{_datadir}/gocode

%global golang_version 1.10
%global GIT_COMMIT 7acbd8382
%global TAG %{VERSION}-%{GIT_COMMIT}
%global SPARK_IMAGE "radanalyticsio/openshift-spark:2.3-latest"

Version:        0.5.4   

%if 0%{?fedora} >= 28
%gometa
%endif

Name:           oshinko-cli
Release:        1%{?dist}
Summary:        Command line interface for spark cluster management app

License:        ASL 2.0

%if 0%{?fedora} >= 28
URL:            %{gourl}
%else
URL:            https://%{goipath}
%endif
Source0:        https://%{goipath}/archive/v%{version}/%{name}-v%{version}.tar.gz

Patch0:         01-scripts-build-sh.patch

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif

%if 0%{?fedora} >= 28
BuildRequires:  golang >= %{golang_version}
%else
BuildRequires:  golang >= 1.9
%endif

%description
The oshinko application manages Apache Spark clusters on OpenShift. The
application consists of a REST server (oshinko-rest) and a web UI and is
designed to run in an OpenShift project.

This repository contains tools to launch the oshinko application along with
the source code for the oshinko REST server in the rest subdirectory. The
source code for the web UI is located in a different repository.

%prep
%if 0%{?rhel} == 7
%setup -q -n %{name}-%{version}
%else
%gosetup -q -n %{name}-%{version}
%endif
%if 0%{?rhel} == 7
%patch0 -p1
%endif

%build
%if 0%{?rhel} == 7
goipath="${goipath:-%{goipath}}"
GO_BUILD_PATH="${GO_BUILD_PATH:-${PWD}/_build}"
if [[ ! -e  ""$GO_BUILD_PATH"/src/${goipath}" ]] ; then
  install -m 0755 -vd "$(dirname "$GO_BUILD_PATH"/src/${goipath})"
  ln -fs "${sourcedir:-$PWD}"   ""$GO_BUILD_PATH"/src/${goipath}"
fi
cd ""$GO_BUILD_PATH"/src/${goipath}"
install -m 0755 -vd _bin
export PATH="${PWD}/_bin${PATH:+:${PATH}}"
export GOPATH=""$GO_BUILD_PATH":/usr/share/gocode"
export LDFLAGS="${LDFLAGS:-}"
%else
%gobuildroot
%endif

export LDFLAGS="$LDFLAGS -X %{goipath}/version.gitTag=%{TAG} -X %{goipath}/version.appName=oshinko -X %{goipath}/version.sparkImage=%{SPARK_IMAGE}"

%if 0%{?rhel} == 7
make build
%else
%gobuild -o _output/oshinko ./cmd/oshinko
%endif

%install
install -Dpm 0755 _output/oshinko %{buildroot}%{_bindir}/oshinko

%check
%if 0%{?fedora} >= 28
%gochecks
%endif

%files
%license LICENSE
%{_bindir}/oshinko
%doc README.md

%changelog
* Thu Jul 26 2018 Ricardo Martinelli de Oliveira <rmartine@redhat.com> - 0.5.4-1
- First package for Fedora