# TODO
# - system mpdf
%define		plugin		dw2pdf
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	Export DokuWiki content to PDF
Name:		dokuwiki-plugin-%{plugin}
Version:	20120123
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://github.com/splitbrain/dokuwiki-plugin-%{plugin}/tarball/master#/%{plugin}-%{version}.tgz
# Source0-md5:	9a95f566ba0553e488f27ea58552b0f3
URL:		http://www.dokuwiki.org/plugin:dw2pdf
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20101107
Requires:	php-common >= 4:%{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# no pear deps
%define		_noautopear	pear

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
The goal of this plugin was to provide a simple, ready to go PDF
converter that almost faithfully replicates the screen view of your
wiki pages (i.e. doesn't convert them to a print-document format like
the latex plugin).

%prep
%setup -qc
mv *-%{plugin}-*/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
#	exit 1
fi

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
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/mpdf
%{plugindir}/tpl
