VAGRANT_VM_PROVIDER = "virtualbox"

Vagrant.configure("2") do |config|


  config.vm.define "node" do |node1|
    node1.vm.box = "centos/7"
    node1.vm.hostname = "node1"
    node1.vm.network :private_network, ip: "192.168.10.2"
    #node1.vm.provision "file", source: "/Users/mac/.ssh/id_rsa.pub", destination: "/home/vagrant/.ssh/me.pub"
    #node1.vm.provision "shell", inline: "cat /home/vagrant/.ssh/me.pub >> /home/vagrant/.ssh/authorized_keys"
    #node1.vm.provision "shell", inline: "yum install  -y java-1.8.0- openjdk.x86_64"

  end

end
