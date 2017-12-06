# == Class: baseconfig
#
# Performs initial configuration tasks for all Vagrant boxes.
#
class baseconfig {
  exec { 'yum update -y':
    command => '/usr/bin/yum update -y';
  }
  
  package { ['bash-completion',
             'net-tools',
             'mc',
             'telnet',
             'vim-enhanced',
             'lsof',
             'mlocate',
             'elinks'
             ]:
    ensure => present;
  }

  exec { 'turn off SELINUX':
    command => '/sbin/setenforce 0 || :';
  }
  
  exec { 'disable SELINUX':
    command => '/bin/sed -i \'s/SELINUX=\\(enforcing\\|permissive\\)/SELINUX=disabled/g\' /etc/selinux/config'
  }

}
