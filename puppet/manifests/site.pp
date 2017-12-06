# create a new run stage to ensure certain modules are included first
stage { 'pre':
  before => Stage['main']
}

# add the baseconfig module to the new 'pre' run stage
class { 'baseconfig':
  stage => 'pre'
}

# set defaults for file ownership/permissions
File {
  owner => 'root',
  group => 'root',
  mode  => '0644',
}

# all boxes get the base config
include baseconfig

# include modules
include httpd
include python


#database setup
class {'::mongodb::globals':
  manage_package_repo => true,
  repo_location => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/3.4/x86_64/',
}->
class {'::mongodb::server':
  port    => 27017,
  verbose => true,
  bind_ip => ['0.0.0.0'],
  service_enable => true,
  service_ensure => running,
}->
class {'::mongodb::client':}

include database
