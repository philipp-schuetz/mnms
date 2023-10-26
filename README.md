# mnms - Mint Nacht Management System
## setup
- clone this repository with `git clone -b stable https://github.com/philipp-schuetz/mnms`
- set environment variables in `docker-compose.yml`
  - PUBLIC_API_PATH: public api url
  - ADMIN_PASSWORD: set password for account `admin`
  - AUTH_SECRET_KEY: generate new key with `openssl rand -hex 32`
- notice: password hashing is not enabled for this project
- build and start the containers with `docker compose up --build`
- add your data data directly through the api or use `setup.py`
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
