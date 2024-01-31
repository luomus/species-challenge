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

To have many types of challenges, you would need to:

- define types
- when loading participation edit form, load the challenge data to see the type
    - router calls a helper, passes this data also to method
- on router, select template based on the type
    - template includes additional fields (no rendering same field differently, that would create complexity)
- on method, select type-specific validator (using a function that passes the validator) to validate participation data
- this way form template and validator make sure the data is always ok.
- data structure need to be defined in three places
    - database: new fields
    - form: new fields and UI
    - validator: field values


## Todo

### Decidions to do

- Should challenge have a description, or is a link to an external website enough?
    - No: simpler
    - Yes: description could also include a logo, if it allows html.
- Should challenge have a start and end date?
    - No, if there is description which can include this. 
    - Yes, if we want to validate that observation dates are within this limit.
- Do we need a login info page, or is it enough to just link to login page?
- Subheadings to species list? e.g. Lehtisammalet
- Non-species to the list? E.g. voikukat
    - Yes.

### Next

- Species names to json, when we get list from the project.
- List of species observed in the challenge

### Setup

- Login to dev/prod parametrized through /login
- Get data system id for dev, test and production? or use intermediate login redirection like on Havistin?
- Database sorting/collation settings utf8mb4_swedish_ci
- Generic exception handling
- Automate database setup - does OpenShift need this?
- Set target to 100 species on challenge.py & admin.py

### Features

- Plan:
    - Admin role set by custom value from Laji.fi?
- Test:
    - Automated testing
    - Giving malicious login token
- Features:
    - Admin ability to edit any participations
    - Challenge sort order (int) on front page
    - Mobile navi
    - Setting challenge start and end dates
    - Disable selecting date beyon start/end page
    - Add species names to participation JSON (fi + sci?)
    - Ability to add additional species

#### Pages

- My participations ✅
    - open ✅
    - closed ✅
    - link to edit ✅
    - link to results ❌
- Participation creation page ✅
- Participation edit page ✅
- Challenge result page ✅
    - list of species ❌
    - list of those with >= 100 species / all participants ✅
    - how many % have passed 100 species ✅
- Admin page ✅
    - button to add a challenge ✅
    - open challenges ✅
    - draft challenges ✅
    - closed challenges ✅
    - edit link to each ✅
    - statistics page of each ✅
        - number of participants ✅
        - number of those with >= 100 species ✅
        - number of active participants (edited participation during last 7 days) ❌
- Challenge creation page ✅
- Challenge edit page ✅
