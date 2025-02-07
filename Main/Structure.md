/home/weissi/
├── nextcloud
│   ├── docker-compose.yml
│   ├── .env.nextcloud      # Nextcloud-specific variables (e.g. domain, trusted domains)
│   ├── .env.mariadb        # MariaDB secrets (root password, database name, user, password)
│   ├── nextcloud_data/      # Persistent volume for Nextcloud files
│   └── mariadb_data/        # Persistent volume for MariaDB data
├── traefik
│   ├── docker-compose.yml
│   ├── traefik.yml         # (Optional) Traefik static configuration file
│   ├── .env.traefik        # Traefik settings (ACME email, etc.)
│   └── letsencrypt/         # Volume to store ACME certificates and data
└── cloudflare
    ├── docker-compose.yml
    ├── .env.cloudflared      # Cloudflare Tunnel credentials and configuration variables
    └── cloudflared/          # Volume for cloudflared configuration files (tunnel JSON, etc.)
