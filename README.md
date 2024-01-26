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

### Setup

- Login to dev/prod parametrized
- Get data system id for dev, test and production? or use intermediate login redirection like on Havistin?
- Database sorting/collation settings
- Generic exception handling?
- Automate database setup - does OpenShift need this?

### Features

- Slug for challenges?

#### Pages

- My participations
    - open
    - closed
    - link to edit
    - link to results
- Participation creation page
- Participation edit page
- Challenge result page
    - list of species
    - list of those with >= 100 species
    - how many % have passed 100 species
    - chart?
- Admin page
    - button to add a challenge
    - open challenges
    - draft challenges
    - closed challenges
    - edit link to each
    - statistics of each
        - number of participants
        - number of those with >= 100 species
        - number of active participants (added species last 7 days)
- Challenge creation page
- Challenge edit page
