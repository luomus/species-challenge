# 100 Species Challenge Web Service

## Development setup

- Clone this repository
- Optionally change development database password to `docker-entrypoint-initdb.d/init_db.sql`
- Set up environment variables to `.env.` and `playwright.example` Use example files as templates.
- Build Docker image `docker build -t species-challenge:latest .`
- Startup with `docker-compose up build playwright; docker-compose down;`
- Set up database using `species_challenge_dev.sql`, e.g. via phpMyAdmin

Site will be visible http://localhost:8081

phpMyAdmin admin UI will be at http://localhost:8080 

## Running tests

- Run the app with `docker-compose up; docker-compose down;`
- Login to playwright container with `docker exec -ti species-challenge-playwright-1 bash`
- Run tests with `python -m pytest -v`. Add `-s` option to the end to see print outputs.

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

- Check http://localhost:8081/osallistuminen/4/6
    - it has e.g. ahvenvita, whic is not part of species list MX.67601
        - why does it save it? this is how it should be; save taxa that are not on the basic list
        - why does it show it on the list? should show at the end
        - should we version the species lists? work with 
        - how to show names of additional species? fetch from participation table, api or json?

### Setup

- Clarify Docker build commands
- Database sorting/collation settings utf8mb4_swedish_ci
- Generic exception handling
- Set target to 100 species on challenge.py & admin.py

### Features

- Plan with the team:
    - Login
        - Get data system id for dev, test and production? or use intermediate login redirection like on Havistin?
        - Login dev/prod parametrized through /login
    - Prod deployment
        - Automate database setup - does OpenShift need this?
    - Admin role
        - Set by custom value from Laji.fi?
- Test:
    - Automated testing with Playwright
    - Giving malicious login token
    - Thorough testing by multiple people
- First production version:
    - Health check
        - Fetch unique participation taxa from database (try)
        - Check that files for all taxa exist
    - All 3 lists
    - Adjust additional species API call: only finnish, only species, colloquial names, match type?
    - Handling higher taxa
    - Mobile navi & testing, including autocomplete
    - Setting challenge start and end dates
    - Disable selecting date beyond start/end page
    - Proper login
    - Fade out flash messages (without page moving upwards)
    - Logos
    - Styling with the team
    - Privacy policy
    - Warning when navigating away without saving changes
- Later:
    - Accessibility
    - Own data dump download
    - Admin ability to edit any participations
    - Challenge sort order (int) for the front page
    - Chart of species accumulation
    - Activity stats, e.g. users active during last 7 days, new participations
    - Exclude existing species from the autocomplete? Could exclude all top N species, what to do then?
- Nice:
    - Admin to see user email
    - Min and max dates instead of year to database
        - Database structure change, content change and sql dump update
        - Challenge form update, with date fields
        - Challenge year validation replacement with min & max validation
        - Test
        - Use these when creating date fields on participation form
            - Existing fields / Python
            - Empty fields / Python
            - Additional species fields / js

#### Pages

- My participations ✅
    - open ✅
    - closed ✅
    - link to edit ✅
    - link to results ✅
- Participation creation page ✅
- Participation edit page ✅
- Challenge result page ✅
    - list of species ✅
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
