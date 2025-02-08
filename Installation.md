Erstellen pref Subnets

```
sudo docker network create --driver bridge --subnet 10.0.1.0/24 --internal backend
sudo docker network create --driver bridge  frontend
sudo docker network create --driver bridge  frontend_rp

```

Install Portainer

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


Cloudflare Tunnel docker compose

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


Cloudflare Tunnel .env

```.env
TUNNEL_TOKEN= hier Tunnel Token einsetzen
```


Traefik docker compose

```docker-compose.yaml

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    networks:
      - backend
      - frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik.yml:/etc/traefik/traefik.yml
      - ./letsencrypt:/letsencrypt
    environment:
      - CF_API_EMAIL=${CLOUDFLARE_EMAIL}
      - CLOUDFLARE_DNS_API_TOKEN=${CLOUDFLARE_API_TOKEN}

networks:
  backend:
    external: true
  frontend:
    external: true

```


Traefik yml

```Traefik.yaml

api:
  dashboard: true
  insecure: true  # Securely expose this in production

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

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false

certificatesResolvers:
  cloudflare:
    acme:
      email: ${CF_API_EMAIL}
      storage: /letsencrypt/acme.json
      dnsChallenge:
        provider: cloudflare
```


Traefik .env

```

CLOUDFLARE_EMAIL=your@email.com
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token

```


Nextcloud + Maria DB docker compose

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
      - "traefik.enable=true"
      - "traefik.http.routers.nextcloud.rule=Host(`${NEXTCLOUD_DOMAIN}`)"
      - "traefik.http.routers.nextcloud.entrypoints=websecure"
      - "traefik.http.routers.nextcloud.tls.certresolver=cloudflare"
      - "traefik.http.services.nextcloud.loadbalancer.server.port=80"

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
  frontend
    external: true

```

Nextcloud & Maria DB .env

```.env

MYSQL_ROOT_PASSWORD=secure_root_password
MYSQL_DATABASE=nextcloud
MYSQL_USER=nextcloud
MYSQL_PASSWORD=secure_db_password
NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD=secure_admin_password
NEXTCLOUD_DOMAIN=nextcloud.weissi.org

```
