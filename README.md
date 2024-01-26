# 100 Species Challenge Web Service

## Development setup

- Clone this repository
- Optionally change development database password to `docker-entrypoint-initdb.d/init_db.sql`
- Set up environment variables to `.env.` Use `example.env` as a template.
- Build Docker image `docker build -t species-challenge:latest .`
- Startup with `docker-compose up; docker-compose down;`
- Set up database using `species_challenge_dev.sql`, e.g. via phpMyAdmin

Site will be visible http://localhost:8081

phpMyAdmin admin UI will be at http://localhost:8080 

## Notes

Login to dev at
https://login.laji.fi/login?target=KE.781&redirectMethod=GET&locale=fi&next=sc_dev

## Todo

- Database sorting/collation settings
- Generic exception handling?
- Automate database setup - does OpenShift need this?
