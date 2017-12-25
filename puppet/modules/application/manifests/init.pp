# == Class: application
#
# Configuring l-Met application
#
class application {

  exec { 'storage ownership':
     command  => "/bin/chown -R vagrant:vagrant /var/www/sites/project/data",
     require  => Package['httpd'],
  }

  # TODO: This should not go into production
  exec { 'storage write permissions':
     command  => "/bin/chmod -R 777 /var/www/sites/project/data",
     require  => Exec['storage ownership'],
  }  
  

}
