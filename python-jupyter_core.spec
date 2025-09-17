#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

Summary:	Core common functionality of Jupyter projects
Summary(pl.UTF-8):	Główna, wspólna funkcjonalność projektów Jupyter
Name:		python-jupyter_core
Version:	4.6.3
Release:	9
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jupyter_core/
Source0:	https://files.pythonhosted.org/packages/source/j/jupyter_core/jupyter_core-%{version}.tar.gz
# Source0-md5:	aaed36bf01888c9e810462e6226db70a
Patch0:		%{name}-tests.patch
Patch1:		%{name}-completions.patch
Patch2:		sphinx8.patch
URL:		https://pypi.org/project/jupyter_core/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-traitlets >= 4.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-traitlets >= 4.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-traitlets >= 4.0
BuildRequires:	sphinx-pdg-3 >= 8
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains base application classes and configuration
inherited by other projects. It doesn't do much on its own.

%description -l pl.UTF-8
Ten pakiet zawiera klasy bazowe aplikacji oraz konfigurację
dziedziczoną przez inne obiekty. Samodzielnie robi niewiele.

%package -n python3-jupyter_core
Summary:	Core common functionality of Jupyter projects
Summary(pl.UTF-8):	Główna, wspólna funkcjonalność projektów Jupyter
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-jupyter_core
This package contains base application classes and configuration
inherited by other projects. It doesn't do much on its own.

%description -n python3-jupyter_core -l pl.UTF-8
Ten pakiet zawiera klasy bazowe aplikacji oraz konfigurację
dziedziczoną przez inne obiekty. Samodzielnie robi niewiele.

%package apidocs
Summary:	API documentation for Python jupyter_core module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jupyter_core
Group:		Documentation

%description apidocs
API documentation for Python jupyter_core module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jupyter_core.

%package -n bash-completion-jupyter
Summary:	Bash completion for jupyter commands
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów poleceń jupyter
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
#Requires:	python-jupyter_core or python3-jupyter_core

%description -n bash-completion-jupyter
Bash completion for jupyter commands.

%description -n bash-completion-jupyter -l pl.UTF-8
Bashowe dopełnianie parametrów poleceń jupyter.

%package -n zsh-completion-jupyter
Summary:	Zsh completion for jupyter commands
Summary(pl.UTF-8):	Dopełnianie parametrów w zsh dla poleceń jupyter
Group:		Applications/Shells
#Requires:	python-jupyter_core or python3-jupyter_core
Requires:	zsh

%description -n zsh-completion-jupyter
Zsh completion for jupyter commands.

%description -n zsh-completion-jupyter -l pl.UTF-8
Dopełnianie parametrów w zsh dla poleceń jupyter.

%prep
%setup -q -n jupyter_core-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest jupyter_core/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest jupyter_core/tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for f in $RPM_BUILD_ROOT%{_bindir}/jupyter* ; do
	%{__mv} "$f" "${f}-2"
done

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/jupyter_core/tests
%endif

%if %{with python3}
%py3_install

for f in $RPM_BUILD_ROOT%{_bindir}/jupyte*[!2] ; do
	%{__mv} "$f" "${f}-3"
done

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/jupyter_core/tests
%endif

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{zsh_compdir}}
cp -p examples/completions-zsh $RPM_BUILD_ROOT%{zsh_compdir}/_jupyter
cp -p examples/jupyter-completion.bash $RPM_BUILD_ROOT%{bash_compdir}/jupyter

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-2
%attr(755,root,root) %{_bindir}/jupyter-migrate-2
%attr(755,root,root) %{_bindir}/jupyter-troubleshoot-2
%{py_sitescriptdir}/jupyter.py[co]
%{py_sitescriptdir}/jupyter_core
%{py_sitescriptdir}/jupyter_core-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jupyter_core
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-3
%attr(755,root,root) %{_bindir}/jupyter-migrate-3
%attr(755,root,root) %{_bindir}/jupyter-troubleshoot-3
%{py3_sitescriptdir}/jupyter.py
%{py3_sitescriptdir}/__pycache__/jupyter.cpython-*.py[co]
%{py3_sitescriptdir}/jupyter_core
%{py3_sitescriptdir}/jupyter_core-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

%files -n bash-completion-jupyter
%defattr(644,root,root,755)
%{bash_compdir}/jupyter

%files -n zsh-completion-jupyter
%defattr(644,root,root,755)
%{zsh_compdir}/_jupyter
