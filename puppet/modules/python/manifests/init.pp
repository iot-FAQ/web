# == Class: python
#
# Installs Python2 and necessary modules. Sets config files.
#
class python {
  package { ['python2-pip',
			 'python-devel',
			 'gcc',
			 'cpp'
             ]:
    ensure => present;
  }
  
   exec { 'update PIP':
     command  => "/usr/bin/pip install --upgrade pip",
     require  => Package['python2-pip'],
   }

  exec { 'install Pyramid':
     command  => "/usr/bin/pip install pyramid",
     require  => Package['python2-pip'],
   }
 
   exec { 'install Paster':
     command  => "/usr/bin/pip install paster",
     require  => Package['python2-pip'],
   }
 
    exec { 'install Chameleon':
     command  => "/usr/bin/pip install chameleon",
     require  => Package['python2-pip'],
   }
   
   exec { 'install magic':
     command  => "/usr/bin/pip install python_magic",
     require  => Package['python2-pip'],
   }
 
    exec { 'setup l_met package':
     command  => "/bin/pip install -e /var/www/sites/project/source/",
     require  => Package['python2-pip'],
   }
 
 
 

}