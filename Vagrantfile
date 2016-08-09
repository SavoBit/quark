# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

vagrant_slaves = ENV.fetch('MESOS_SLAVES', 1).to_i
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "prasincs/mesos"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/vagrant"


  config.vm.define "master" do |master|
    master.vm.network "private_network", ip: "10.10.4.2"
    master.vm.hostname = "master"

    master.vm.provision "shell", inline: <<-SHELL
      sudo apt-get install mesos=0.25.0-0.2.70.ubuntu1404
      sed -i.bak '9,10d' /etc/network/interfaces && sudo ifdown eth1 && sudo ifup eth1
      echo "10.10.4.2" > /etc/mesos-master/ip
      rm -f /etc/init/zookeeper.override
      service zookeeper restart
      rm -f /etc/init/mesos-master.override
      service mesos-master restart
      rm -f /etc/init/marathon.override
      service marathon restart
    SHELL
  end



  vagrant_slaves.times do |n|
    config.vm.define "slave_#{n}" do |slave|
      slave.vm.network "private_network", ip: "10.10.4.1#{n}"
      slave.vm.hostname = "slave-#{n}"
      slave.vm.provision "shell", inline: <<-SHELL
       sudo apt-get install mesos=0.25.0-0.2.70.ubuntu1404
        sed -i.bak '9,10d' /etc/network/interfaces && sudo ifdown eth1 && sudo ifup eth1
        echo "zk://10.10.4.2:2181/mesos" > /etc/mesos/zk
        echo "10.10.4.1#{n}" > /etc/mesos-slave/ip
        echo "mesos,docker" > /etc/mesos-slave/containerizers
        rm -f /etc/init/mesos-slave.override
        service mesos-slave restart
      SHELL
    end
  end


  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
     sudo apt-get update
     sudo apt-get install -yy software-properties-common python-software-properties
     sudo add-apt-repository ppa:webupd8team/java
     sudo apt-get update
     echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
     echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
     sudo apt-get install -yy oracle-java8-installer
     sudo apt-get install -yy htop sysstat
     cd /vagrant && ./setup_dev_env.sh
SHELL
end
