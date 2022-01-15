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


## Stuff to do
- Add secrets
- monitoring
- fix ingress for frontend
- change frontend to use service address
- user management
- reports 

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