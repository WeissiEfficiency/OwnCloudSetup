``
sudo docker network create -d ipvlan \
  --subnet=192.168.0.0/24 \
  --gateway=192.168.0.1 \
  -o parent=eth0 \
  macvlan_net
  ``

``
sudo docker network create \
  --driver bridge \
  --subnet 10.0.1.0/24 \
  --internal \
  internal_net
  ``
