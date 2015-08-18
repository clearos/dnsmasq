# dnsmasq

Forked version of dnsmasq with ClearOS changes applied

* git clone git+ssh://git@github.com/clearos/dnsmasq.git
* cd dnsmasq
* git checkout master
* git remote add upstream git://pkgs.fedoraproject.org/dnsmasq.git
* git pull upstream master
* git checkout clear7
* git merge --no-commit master
* git commit
