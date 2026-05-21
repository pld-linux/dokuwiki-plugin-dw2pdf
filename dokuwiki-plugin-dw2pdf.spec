%define		subver		2026-01-08
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		dw2pdf
%define		php_min_version 7.0.0
Summary:	Export DokuWiki content to PDF
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/splitbrain/dokuwiki-plugin-%{plugin}/archive/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	01be71898470e9add771f4c6d001566f
URL:		https://www.dokuwiki.org/plugin:dw2pdf
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20101107
Requires:	php(core) >= %{php_min_version}
Conflicts:	dokuwiki-plugin-html2pdf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_rpmconfigdir}/dokuwiki-find-lang.sh %{buildroot}

# bundled mpdf via composer vendor/ tree
%define		_noautopear	pear
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
The goal of this plugin was to provide a simple, ready to go PDF
converter that almost faithfully replicates the screen view of your
wiki pages (i.e. doesn't convert them to a print-document format like
the latex plugin).

%prep
%setup -qc
mv dokuwiki-plugin-%{plugin}-*/* .
mv dokuwiki-plugin-%{plugin}-*/.[!.]* . 2>/dev/null || :

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

# drop CI/test/dev files
rm -rf .github _test .gitignore

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/README
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/*.css
%{plugindir}/*.svg
%{plugindir}/*.png
%{plugindir}/composer.json
%{plugindir}/composer.lock
%{plugindir}/deleted.files
%{plugindir}/conf
%{plugindir}/syntax
%{plugindir}/tpl
%{plugindir}/vendor
