%global srcname aws-cli
%global appname awscli

Name:           %{appname}-2
Version:        2.4.19
Release:        2%{?dist}
Summary:        Universal Command Line Environment for AWS, Version 2

License:        ASL 2.0 and MIT
URL:            https://github.com/aws/aws-cli
Source0:        %{url}/archive/%{version}/%{appname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(jsonschema)
BuildRequires:  python3dist(mock)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-xdist)

Recommends:     groff
Obsoletes:      awscli <= 1
Obsoletes:      python3-botocore <= 1


%description

This package provides version 2 of the unified command line
interface to Amazon Web Services.


%prep
%autosetup -n %{srcname}-%{version}
find awscli/examples/ -type f -name '*.rst' -executable -exec chmod -x '{}' +

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files awscli


%check
# Remove failing tests ("python" expected as an executable)
rm -rf tests/unit/customizations/emr/test_emr_utils.py tests/functional/kinesis/test_remove_operations.py tests/functional/lex/test_remove_operations.py
PATH="%{buildroot}%{_bindir}:$PATH" PYTHONPATH="${PYTHONPATH:-%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}}" PYTHONDONTWRITEBYTECODE=1 %{python3} scripts/ci/run-tests


%files -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst

%{_bindir}/aws
%{_bindir}/aws.cmd
%{_bindir}/aws_bash_completer
%{_bindir}/aws_completer
%{_bindir}/aws_zsh_completer.sh


%changelog
* Tue Feb 22 2022 David Duncan <davdunc@amazon.com> - 2.4.19-2
- Updated for package review

* Tue Feb 22 2022 Kyle Knapp <kyleknap@amazon.com> - 2.4.19-1
- Import version 2.4.19

* Fri Feb 04 2022 Kyle Knapp <kyleknap@amazon.com> - 2.4.12-3
- Remove unneeded dependencies/macros and add check for tests

* Wed Feb 02 2022 David Duncan <davdunc@amazon.com> - 2.4.12-2
- Prepare for package review

* Tue Jan 25 2022 Kyle Knapp <kyleknap@amazon.com> - 2.4.12-1
- Update to 2.4.12 and switch to using pyproject macros

* Fri Mar 13 2020 David Duncan <davdunc@amazon.com> - 2.0.3-2
- Modify python3-botocore dependency to python3-botocore-2

* Fri Mar 13 2020 David Duncan <davdunc@amazon.com> - 2.0.3-1
- Initial Commit for awscli version 2
