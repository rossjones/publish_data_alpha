# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Allow local machines to view the VM
  config.vm.network "private_network", ip: "192.168.99.99"

  config.vm.provider :virtualbox do |vb|
    config.vm.box = "ubuntu/trusty64"
    vb.gui = false

    vb.customize ["modifyvm", :id, "--name", "v2_dev"]
    vb.customize ["modifyvm", :id, "--memory", "4096"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end


end
