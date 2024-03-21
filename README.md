# 100 Species Challenge Web Service

A web app designed for organizing and participating in wildlife observation challenges, specifically targeting the identification of 100 species. In these challenges, participants aim to observe a hundred different species of plants, fungi, or insects over the course of a year.

Backend application built with Flask. Database on MariaDB. Depends on FinBIF Laji-auth authentication service (Laji.fi). Funded by [Kone Foundation, 2023](https://koneensaatio.fi/en/grants-and-residencies/sata-lajia-haaste-2/).

![alt text](./app/static/screencapture.png)

## Development setup

- Clone this repository
- Optionally change development database password to `docker-entrypoint-initdb.d/init_db.sql`
- Set up environment variables to `.env.` and `playwright.example` Use example files as templates.
- Build Docker image `docker build -t species-challenge:latest .`
- Startup with `docker-compose up build playwright; docker-compose down;`
- Set up database using `sql/species_challenge_dev.sql`, e.g. via phpMyAdmin

Site will be visible http://localhost:8081

phpMyAdmin admin UI will be at http://localhost:8080 

## Running tests

- Run the app with `docker-compose up; docker-compose down;`
- Login to playwright container with `docker exec -ti species-challenge-playwright-1 bash`
- Run tests with `python -m pytest -v`. Add `-s` option to the end to see print outputs.

## OpenShift setup

Note that in order to create MariaDB database on Rahti, PHPMyAdmin data dump does not work. You need to create the dump on the command line:

    mariadb-dump --user=USERNAME --password --lock-tables --databases DATABASENAME > ./species-challenge.sql


## Notes

- Setting up new challenge
    - Provide list of basic taxa to `app/data/`, e.g. `plantae_2024.json` or use one of the existing ones.
    - Provide list of all allowed taxa to `app/data/` (for backend) and `statix/taxa/` (for frontend autocomplete), e.g. `plantae_2024_all.json`. This should contain all taxa that the basic list above contains, icnluding non-species.
- The UI prevents setting dates that are outside the challenge dates, and dates in the future. This relies on min & max attributes on the date field and browser validation and error messages.
    - If a challenge for 2025 is published in 2024, users have to clear dates which they might have added by clicking the species name. Better solution wpould be to edit the Javascript so that it wont add today's date if it's outside the allowed range.


#### Future: To have a new challenge type, you would need to:

- Define new types to data/challenge_vocabulary.json
- When loading participation edit form, load the challenge data to see the type
    - Router calls a helper, passes this data also to method
- On router, select template based on the type
    - Template includes additional fields (no rendering same field differently, that would create complexity)
- On method, select type-specific validator (using a function that passes the validator) to validate participation data
- This way form template and validator make sure the data is always ok.
- SQL inset & update queries need to be duplicated or automated.
- So data structure need to be defined in four places
    - Database: new fields
    - Form: new fields and UI
    - Validator: field values
    - Database query: fields and values


## Todo

### Next

* Page titles
* Trim whitespace from MX codes, both on read and write
* Use API for autocomplete? Would allow sorting results based on abundance, so e.g. "pihlaja" would return pihalaja and note rare species. But could lead to conflicts with existing data, if taxonomy changes?

### Setup

- Version numbering?
- More robust error handling and restart? Try with triggering syntax error.
- Clarify Docker build commands
- Database sorting/collation settings utf8mb4_swedish_ci?
- Backup monitoring

### Features todo

- Test:
    - Automated testing with Playwright
        - Admin editing challenges
        - Logout
    - Giving malicious login token
    - Giving incorrect numeric challenge & participation id's -> redirect with flash
- Later:
    - Handling higher taxa (is uses adds rikkavoikukka, don't add voikukat to taxon_count)
    - Remove button (dull red X?) to participation form taxon list
    - Move observed species list away from challenge main page to separate page, preparing for tables that have >200 observers and species 
    - Prevent editing species of closed / draft challenge participations
    - Accessibility
    - Own data dump download
    - Admin ability to edit any participations
    - Challenge sort order (int) for the front page
    - My participation species accumulation chart
    - Activity stats, e.g. users active during last 7 days, new participations
    - Exclude existing species from the autocomplete? Could exclude all top N species, what to do then?
- Nice:
    - Min and max dates instead of year to database
        - Database structure change, content change and sql dump update
        - Challenge form update, with date fields
        - Challenge year validation replacement with min & max validation
        - Test
        - Use these when creating date fields on participation form
            - Existing fields / Python
            - Empty fields / Python
            - Additional species fields / js
