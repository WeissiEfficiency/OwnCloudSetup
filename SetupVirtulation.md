##How to set up virtualisation

```Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All```

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

Create Username and Password

```
apt-get update
```

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



---

##Portainer

``` 

```
