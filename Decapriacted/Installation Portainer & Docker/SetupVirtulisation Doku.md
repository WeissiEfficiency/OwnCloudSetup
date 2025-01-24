##How to set up virtualisation

Update Windows (Security KB5041571)

```
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

Nested Virt
```
Set-VMProcessor -VMName <VMName> -ExposeVirtualizationExtensions $true
```

---

##WSL

Enable WSL

```
wsl --install
```

```  
wsl --unregister Ubuntu
 ```

```
wsl -l
 ```

Check if Ubuntu got deleted to get the right distro

```  
wsl -l -online
  ```

``` 
wsl install <right Distro>
```

Set Verion to 2, got more features
```
wsl --set-default-version 2
```

Create Username and Password

```
apt-get update
```

[WSL Doku](https://learn.microsoft.com/de-de/windows/wsl/about)

---

##Docker (ubuntu v24.04)

"IF NEEDED" Check for old Docker Engine

```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Install Docker Engine Env.

```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Install Docker Enginge
``` 
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 
```

Run for test
``` 
sudo docker run hello-world
```

Docker is installed

[Docker Doku Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

---

##Portainer


Persisitant volume for Protainer
```
docker volume create portainer_data
```

Install Portainer Container with Ports 8000 and 9443
```
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

>https://localhost:9443
 
