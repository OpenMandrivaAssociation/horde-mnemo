%define module	mnemo
%define name	horde-%{module}
%define version	2.1.1
%define release	%mkrel 2

%define _requires_exceptions pear(Horde.*)

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	The Horde notes and memo application
License:	GPL
Group: 		System/Servers
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.bz2
Patch0:		%{module}-2.0-path.patch
URL:		http://www.horde.org/%{module}
Requires(post):	rpm-helper
Requires:	horde >= 3.0
BuildArch:	noarch

%description
Mnemo is the Horde note manager application.

%prep
%setup -q -n %{module}-h3-%{version}
%patch

# fix encoding
for file in `find . -type f`; do
    perl -pi -e 'BEGIN {exit unless -T $ARGV[0];} tr/\r//d;' $file
done

%build

%install
rm -rf %{buildroot}

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Mnemo Horde configuration file
//
 
$this->applications['mnemo'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/mnemo',
    'webroot'     => $this->applications['horde']['webroot'] . '/mnemo',
    'name'        => _("Notes"),
    'status'      => 'active',
    'provides'    => 'notes',
    'menu_parent' => 'organizing'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_var}/www/horde/%{module}
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR *.php %{buildroot}%{_var}/www/horde/%{module}
cp -pR themes %{buildroot}%{_var}/www/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

# use symlinks to recreate original structure
pushd %{buildroot}%{_var}/www/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
ln -s ../../../..%{_datadir}/horde/%{module}/lib .
ln -s ../../../..%{_datadir}/horde/%{module}/locale .
ln -s ../../../..%{_datadir}/horde/%{module}/templates .
popd
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_var}/www/horde/%{module}


