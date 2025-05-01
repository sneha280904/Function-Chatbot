### <---------- Imports ---------->

# Import necessary modules from Flask and database
from flask import render_template
from database.database.database import db
from database.model.model import User
# from database.model.model import Query  # Uncomment if Query model is needed later

# Import datetime for date manipulation
# from datetime import datetime, timezone  # Uncomment if timezone-aware datetime is needed


### <---------- DashService Class ---------->

class dashService:

    ### <---------- Constructor ---------->
    def __init__(self):
        print("DashService initialized.")  ## Confirmation message on service initialization

    ### <---------- Main Method to Fetch Data ---------->
    def dashService(self, start_date, end_date):
        ## Print the start and end dates for debugging
        print("Start date service: ", start_date)
        print("End date service: ", end_date)

        ### <---------- Fetching User Table Content Only ---------->
        ## Querying the User table for entries within the given date range
        results = db.session.query(User).filter(
            User.DateTime >= start_date,
            User.DateTime <= end_date,
        ).all()

        ## Print the fetched results for debugging
        print("Result: ", results)

        ## Return the fetched results to the controller
        return results
