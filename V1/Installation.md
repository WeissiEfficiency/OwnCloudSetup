Make directories

```
cd /home/weissi
sudo mkdir -p docker/cloudflare
sudo mkdir docker/nextcloud
sudo mkdir -p docker/traefik/config
sudo mkdir docker/traefik/data
sudo mkdir docker/portainer

```


Erstellen pref Subnets

```
sudo docker network create --driver bridge --subnet 10.0.1.0/24 --internal backend
sudo docker network create --driver bridge  frontend
sudo docker network create --driver bridge  frontend_rp
```

---

Install Portainer

```
sudo vim  /home/weissi/docker/portainer/docker-compose.yml
```

```docker-compose.yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"  # Web-UI über HTTPS
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Zugriff auf Docker-API
      - portainer_data:/data  # Persistente Daten
    networks:
      - backend  # Internes Netzwerk
      - frontend # Externes Netzwerk

volumes:
  portainer_data:

networks:
  backend:
    external: true
  frontend:
    external: true
```

```
cd /home/weissi/docker/portainer
sudo docker compose up -d
```

---

Cloudflare Tunnel docker compose

Cloudflare Tunnel .env

```
sudo vim  /home/weissi/docker/cloudflare/docker-compose.yml
```

```docker-compose.yaml
networks:
  frontend:
    external: true

services:
  cloudflared:
    container_name: cloudflare_tunnel
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
    command: tunnel --no-autoupdate run
    networks:
      - frontend
```

```
sudo vim  /home/weissi/docker/cloudflare/.env
```

```.env
TUNNEL_TOKEN= hier Tunnel Token einsetzen
```

```
cd /home/weissi/docker/cloudflare
sudo docker compose up -d
```

---

Traefik docker compose

Traefik config traefik.yml

Traefik .env


```
sudo vim /home/weissi/docker/traefik/docker-compose.yml
```

```docker-compose.yaml

services:
  traefik:
    image: traefik:latest
    container_name: traefik
    restart: unless-stopped
    networks:
      - backend
      - frontend
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./config/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./data/certs/:/var/traefik/certs/:rw
    environment:
      - CF_DNS_API_TOKEN=${CF_DNS_API_TOKEN}

networks:
  backend:
    external: true
  frontend:
    external: true

```

```
sudo vim /home/weissi/docker/traefik/config/traefik.yml
```

```Traefik.yaml
global:
  checkNewVersion: false
  sendAnonymousUsage: false
log:
  level: DEBUG
api:
  dashboard: true
#  insecure: true  # Securely expose this in production
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
websecure:
    address: ":443"
certificatesResolvers:
  cloudflare:
    acme:
      email: "stefanweissopuss@gmail.com"
      storage: var/traefik/certs/cloudflare-acme.json
      caServer: 'https://acme-v02.api.letsencrypt.org/directory'
      keyType: EC256
      dnsChallenge:
        provider: cloudflare
        resolver:
          - "1.1.1.1:53"
          - "8.8.8.8:53"
providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

```
sudo vim /home/weissi/docker/traefik/.env
```

```.env
CF_DNS_API_TOKEN=your_cloudflare_DNS_api_token
```


```
cd /home/weissi/docker/traefik
sudo docker compose up -d
```


---

Nextcloud + Maria DB docker compose

Nextcloud + Maria DB .env

```
sudo vim /home/weissi/docker/nextcloud/docker-compose.yml
```

```docker-compose.yaml

services:
  nextcloud:
    image: nextcloud:latest
    container_name: nextcloud
    restart: unless-stopped
    networks:
      - backend
      - frontend
    environment:
      - NEXTCLOUD_DB_HOST=mariadb
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - NEXTCLOUD_ADMIN_USER=${NEXTCLOUD_ADMIN_USER}
      - NEXTCLOUD_ADMIN_PASSWORD=${NEXTCLOUD_ADMIN_PASSWORD}
    volumes:
      - ./nextcloud:/var/www/html
      - ./data:/var/www/html/data
    labels:
      - traefik.enable=true
      - traefik.http.routers.nextcloud-http.rule=Host(`nextcloud.weissi.org`)
      - traefik.http.routers.nextcloud-http.entrypoint=web
      - traefik.http.routers.nextcloud-https.tls=true
      - traefik.http.routers.nextcloud-https.tls.certresolver=cloudflare
      - traefik.http.routers.nextcloud-https.entrypoints=websecure
      - traefik.http.routers.nextcloud-https.rule=Host(`nextcloud.weissi.org`)


  mariadb:
    image: mariadb:latest
    container_name: mariadb
    restart: unless-stopped
    networks:
      - backend
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    volumes:
      - ./db:/var/lib/mysql
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW

networks:
  backend:
    external: true
  frontend:
    external: true

```

```
sudo vim /home/weissi/docker/nextcloud/.env
```

```.env

MYSQL_ROOT_PASSWORD=secure_root_password
MYSQL_DATABASE=nextcloud
MYSQL_USER=nextcloud
MYSQL_PASSWORD=secure_db_password
NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD=secure_admin_password
NEXTCLOUD_DOMAIN=nextcloud.weissi.org

```


```
cd /home/weissi/docker/nextcloud
sudo docker compose up -d
```



---

# Pending:
Health Checks
Umstellung der Directories
Zusweisung und Segmentierung

