Erstellen pref Subnets

```
sudo docker network create --driver bridge --subnet 10.0.1.0/24 --internal backend
sudo docker network create --driver bridge frontend
```


Cloudflare Tunnel yaml

```
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

```
TUNNEL_TOKEN= hier Tunnel Token einsetzen
```
