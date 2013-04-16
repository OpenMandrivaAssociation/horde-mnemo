%define module	mnemo
%define name	horde-%{module}
%define version	2.2.2
%define release:	6

%define _requires_exceptions pear(Horde.*)

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	The Horde notes and memo application
License:	GPL
Group: 		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch:      %{module}-h3-2.2-fix-constant-loading.patch
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
BuildArch:	noarch

%description
Mnemo is the Horde note manager application.

%prep
%setup -q -n %{module}-h3-%{version}
%patch -p 1

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

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
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR notepads %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
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
%if %mdkversion < 201010
%_post_webapp
%endif


%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.2-4mdv2011.0
+ Revision: 565288
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-3mdv2010.1
+ Revision: 493350
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-1mdv2010.0
+ Revision: 445895
- new version
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.2.1-2mdv2010.0
+ Revision: 437884
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.1-1mdv2009.1
+ Revision: 354888
- update to new version 2.2.1

* Tue Nov 18 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-3mdv2009.1
+ Revision: 304337
- fix constant loading

* Tue Jun 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-2mdv2009.0
+ Revision: 223589
- add missing js and notepads directories (fix #41534)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-1mdv2009.0
+ Revision: 213377
- new version
  drop patch0
  don't recompress sources
  don't duplicate spec-helper work

* Wed Jan 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.2-1mdv2008.1
+ Revision: 153803
- update to new version 2.1.2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 21 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.1-3mdv2008.1
+ Revision: 136619
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Dec 18 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.1-2mdv2007.0
+ Revision: 98620
- but don't forget to add used ones
- drop unused source
- new version
  use herein document for horde configuration

  + Andreas Hasenack <andreas@mandriva.com>
    - Import horde-mnemo

* Sat Aug 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-2mdv2007.0
- Rebuild

* Tue Mar 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-1mdk
- new version

* Fri Feb 10 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.3-2mdk
- fix automatic dependencies

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.3-1mdk
- new version
- %%mkrel

* Fri Jul 01 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-3mdk 
- better fix encoding
- fix requires

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.1-2mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.1-1mdk 
- new version
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-2mdk 
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-1mdk 
- new version
- top-level is now /var/www/horde/mnemo
- config is now in /etc/horde/mnemo
- other non-accessible files are now in /usr/share/horde/mnemo
- drop old obsoletes
- rediff patch0
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Thu Aug 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.1.2-1mdk 
- new version

* Mon Jul 19 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.1.1-3mdk 
- apache config file in /etc/httpd/webapps.d
- pluggable horde configuration

* Fri May 07 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.1.1-2mdk
- new naming scheme

* Wed Apr 07 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.1.1-1mdk
- First Mandrakelinux release

