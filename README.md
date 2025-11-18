To do:
- Combine current wave and wind pipelines into one set of functions ✅
- Find a good tide source and create a distinct pipeline for that ✅
- Add in some logging and debug tests ✅
- Add in some unit tests (assertion errors) ✅

- Solve for no next tide 'Could not termine next or prev tide' 🐞
- Circular import issue 🐞
- Add logic to account for all this to rate the spots and order them ✅
- Write our input Data to a SQL Database instead of a Pandas DF for persistence? - Put on hold for forecasting tool ❌

- Finish logic to rate ALL the spots not just one
- Add in wave power sweetspot adjustment
- Add in logic to store this data as a dictionary for the purpose of viewing on frontend including comments e.g. maxxing out
- Rearrange the code to be more akin to DataCamp production code guidelines
- Add a super simple frontend to house this using JavaScript
- Build some logic around storing Historical Data on Frontend?