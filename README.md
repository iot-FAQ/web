# I-Met

## Setup Instructions
### Dev Environment setup with Vagrant
#### Pre-requisites
* Windows users: Install Git client to download the source code. Git can be downloaded from https://git-scm.com/downloads
* Make sure that VirtualBox is installed on the host machine. If not, then download and install the latest version from https://www.virtualbox.org/
* Download and install Oracle VM VirtualBox Extension Pack from https://www.virtualbox.org/wiki/Downloads. Other you will get an error from Vagrant that in cannot mount the source folder because of unknown filesystem.
* Install Vagrant. Vagrant is powerful DEV environment management tool that can be downloaded from https://www.vagrantup.com/downloads.html
* Windows users: Install ```rsync``` for Windows to make to make Vagrant able to sync files with VM. It can be found here: https://www.itefix.net/content/cwrsync-free-edition. Make sure that ```rsync.exe``` and the corresponding DLL files are within Windows PATH.
* Make sure that Apache HTTPD, MongoDB and MySQL are stopped on host (local) machine. Otherwise Vagrant will fail to start the development environment

#### Installation and Setup
* Download the source code and go to the source code root (where you see ```Vagrantfile``` present) and run the commands below
* Add Vagrant CentOS 7 Linux VM
```
vagrant box add centos/7
```
* Install Vagrant Guest Additions plugin:
```
vagrant plugin install vagrant-vbguest
```
* Power up Dev VM (make sure you run this in project root):
```
vagrant up --provider virtualbox
```
* Provision Dev VM configuration:
```
vagrant provision
```
The web site becomes available at http://localhost:8080/ once the provisioning is completed.

### Using the Dev VM
Once provisioned, virtual machine runs headless and serves "l-Met" website. Source folder is automatically mounted to the correspoding directory on the WEB Server so there's not to copy sources to the VM
* You may need to reload the VM if ```Vagrantfile``` was modified:
```
vagrant reload
```
* NOTE: There's no need to reload or restart the VM in case modify the source. You simply work with it like you are doing this on your local machine. However, there's a need to reload Apache HTTPD on the VM when changing the source code

### Working on the VM
* Entering VM's shell:
```
vagrant ssh
```
You'll get this when successful (example):
```
macbook222:I-Met rpavlyuk$ vagrant ssh
Last login: Fri Dec  8 15:15:09 2017 from 10.0.2.2
[vagrant@localhost ~]$
```
* You need to reload Apache HTTPD whenever you make a change to the source code:
```
sudo systemctl reload httpd
```
* Monitoring log file of the application (use CTRL+C to abort):
```
sudo tail -f /var/log/httpd/error_log
```
