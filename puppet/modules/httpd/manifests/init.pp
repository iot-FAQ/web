# == Class: apache
#
# Installs packages for HTTPD, enables modules, and sets config files.
#
class httpd {
  package { ['httpd', 'mod_ssl', 'mod_wsgi' ]:
    ensure => present;
  }

  service { 'httpd':
    ensure  => running,
    require => Package['httpd'];
  }
  
  file {'vhost-dev':
      require => Package['httpd'],
	  ensure => present,
	  path   => '/etc/httpd/conf.d/vhost-dev.conf',
	  owner  => 'root',
	  group  => 'root',
	  mode   => '0644',
	  source => 'puppet:///modules/httpd/vhost-dev.conf',
  }
  
  exec {'reload apache' :
  	command => '/bin/systemctl reload httpd',
  	require => [ Package['httpd'], File['vhost-dev'] ]
  }
  
  exec { 'apache chown':
     command  => "/bin/chown -R apache:apache /var/www/sites/project",
     require  => Package['httpd'],
 }

  exec { 'storage ownership fix':
     command  => "/bin/chown -R vagrant:vagrant /var/www/sites/project/data",
     require  => Exec['apache chown'],
  }


}
