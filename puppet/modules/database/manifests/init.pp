# == Class: mongodb
#
# Installs MongoDB and necessary modules. Sets config files.
#

class database {

  package { ['mongodb-org-tools']:
    ensure => present,
    require  => Class['mongodb::server'],
  }
}



