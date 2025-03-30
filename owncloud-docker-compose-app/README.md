# OwnCloud Docker Compose Setup

This project provides a Docker Compose configuration for setting up OwnCloud, a powerful open-source file sync and share solution. The configuration utilizes secrets defined in a `.env` file for sensitive information such as database credentials and admin passwords.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Project Structure

```
owncloud-docker-compose-app
├── docker-compose.yml
├── .env
└── README.md
```

## Setup Instructions

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```
   git clone <repository-url>
   cd owncloud-docker-compose-app
   ```

2. **Configure the `.env` File**

   Create a `.env` file in the project root directory if it doesn't exist. Populate it with the necessary environment variables:

   ```
   DB_PASSWORD=your_database_password
   ADMIN_PASSWORD=your_admin_password
   ```

   Make sure to replace `your_database_password` and `your_admin_password` with secure values.

3. **Start the OwnCloud Application**

   Run the following command to start the OwnCloud application using Docker Compose:

   ```
   docker-compose up -d
   ```

   This command will start all the services defined in the `docker-compose.yml` file in detached mode.

4. **Access OwnCloud**

   Once the services are up and running, you can access OwnCloud by navigating to `http://localhost:8080` in your web browser.

5. **Stopping the Application**

   To stop the OwnCloud application, run:

   ```
   docker-compose down
   ```

## Additional Information

- For more details on configuring OwnCloud, refer to the [OwnCloud documentation](https://doc.owncloud.com/).
- Ensure that your Docker and Docker Compose versions are up to date for the best compatibility.