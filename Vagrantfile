VAGRANT_VM_PROVIDER = "virtualbox"

Vagrant.configure("2") do |config|


  config.vm.define "node" do |node1|
    node1.vm.box = "centos/7"
    node1.vm.hostname = "node1"
    node1.vm.network :private_network, ip: "192.168.10.2"
    #node1.vm.provision "file", source: "/Users/mac/.ssh/id_rsa.pub", destination: "/home/vagrant/.ssh/me.pub"
    #node1.vm.provision "shell", inline: "cat /home/vagrant/.ssh/me.pub >> /home/vagrant/.ssh/authorized_keys"

    node1.vm.provision "shell", inline: "yum install  -y https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm"
    node1.vm.provision "shell", inline: "yum install -y python36.x86_64 python34-pip.noarch"
    node1.vm.provision "shell", inline: "pip3 install --upgrade pip", privileged: "True"
    node1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--cpus", 1]
    end

  end

end
