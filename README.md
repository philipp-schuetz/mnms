# mnms - Mint Nacht Management System
## setup
- clone this repository with `git clone https://github.com/philipp-schuetz/mnms`
- set environment variables in `docker-compose.yml`
  - PUBLIC_API_PATH: public API URL
  - ADMIN_PASSWORD: set password for account `admin`
  - AUTH_SECRET_KEY: generate a new key with `openssl rand -hex 32`
  - CACHING_ENABLED: enable (1) or disable (0) database caching, improves performance
- notice: Password hashing is not enabled for this project.
- build and start the containers with `docker compose up --build`
- add your data directly through the API or use `setup.py`
  - if you use `setup.py` set the API URL and admin password at the top of the file
- minimum amount of data required:
  - 8 stations
  - 1 class
  - 2 groups per class
  - 1 user per group
  - 1 participant per group

## demo
- [Frontend](https://mnms.philippschuetz.com)
- [Backend](https://mnms-api.philippschuetz.com)
- [Backend Docs](https://mnms-api.philippschuetz.com/docs)
