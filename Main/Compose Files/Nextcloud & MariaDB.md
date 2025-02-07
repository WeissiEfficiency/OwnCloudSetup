´´´services:
  mariadb:
    image: mariadb:latest
    container_name: nextcloud_mariadb
    restart: always
    env_file:
      - .env.mariadb
    volumes:
      - mariadb_data:/var/lib/mysql
    networks:
      - internal
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 30s
      timeout: 10s
      retries: 5

  nextcloud:
    image: nextcloud:latest
    container_name: nextcloud_app
    restart: always
    depends_on:
      mariadb:
        condition: service_healthy
    env_file:
      - .env.nextcloud
    volumes:
      - nextcloud_data:/var/www/html
    networks:
      - internal
    labels:
      # Traefik labels for automatic routing and certificate management:
      - "traefik.enable=true"
      - "traefik.http.routers.nextcloud.rule=Host(`${NEXTCLOUD_DOMAIN}`)"
      - "traefik.http.routers.nextcloud.entrypoints=websecure"
      - "traefik.http.routers.nextcloud.tls.certresolver=myresolver"

volumes:
  mariadb_data:
    driver: local
  nextcloud_data:
    driver: local

networks:
  internal:
    external: true
  macvlan_net:
    external: true
    ´´´
