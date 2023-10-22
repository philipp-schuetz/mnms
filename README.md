# mnms - Mint Nacht Management System
## setup
- clone this repository with `git clone -b stable https://github.com/philipp-schuetz/mnms`
- set PUBLIC_API_PATH inside `docker-compose.yml` to the actual url of the api
- build and start the containers with `docker compose build` and `docker compose up`
- add your data data directly with the api, `setup.py` or continue with the example data already provided in `setup.py`
- minimum amount of data required:
  - 8 stations
  - 1 class
  - 2 groups per class
  - 1 participant per group

## demo
- [Frontend](https://mnms.philippschuetz.com)
- [Backend](https://mnms-api.philippschuetz.com)
- [Backend Docs](https://mnms-api.philippschuetz.com/docs)

#todo: reformat nicely
generate a secret key with openssl rand -hex 32 and put in the the environ. var in the docker-compose.yml

password hashing is not enabled in this project, because it doesnt make any sense in this case, we only use pins with numbers
