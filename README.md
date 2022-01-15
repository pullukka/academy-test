###

Original challenge:
https://github.com/solita/dev-academy-2022-exercise



### Fullstack version

Contains Pyhton backend and react frontend draft.
Developed with kubernetes 


### Frontend version
Tried React and managed to get CSV upload to working

### Backend version
Created with python

## How to deploy
- Build containers with build.sh
- Deploy needed kubernetes services 
- Use portforward (or fix ingress :D)
- Create database and user from dump
- Place DB SSL certs if needed and fix line ssl_conf = {'ssl_ca': os.path.dirname(os.path.abspath(__file__))+F"/{CONF.DATABASE_CA}"----- } from db.py

## Stuff to do
- Add secrets
- monitoring
- fix ingress for frontend
- change frontend to use service address
- user management
- reports
- Tests

Backend:
Provide more endpoints for frontend.
Add prometheud monitoring


Fronted:
Validate input
Validate input size
Validate input None

Add all other frontend stuff :D!

## Database
hosted on Azure MariaDB or local vm

farm_stats.sql includes DB schema

Create user:

GRANT ALL PRIVILEGES ON *.* TO `admin`@`%` IDENTIFIED BY PASSWORD '*54E7B1D5CBA63EEA95CC2D56CCFE440910DA1226';