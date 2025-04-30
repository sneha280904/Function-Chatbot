### <---------- Imports ---------->
# Import necessary modules from Flask and database
from flask import render_template
from database.database.database import db
from database.model.model import User
# from database.model.model import Query

# Import datetime for date manipulation
# from datetime import datetime, timezone

### <---------- DashService Class ---------->
class dashService:
    # <---------- Constructor ---------->
    def __init__(self):
        print("DashService initialized.")

    # <---------- Main Method to Fetch Data ---------->
    def dashService(self, start_date, end_date):
        # Print the start and end dates for debugging
        print("Start date service: ", start_date)
        print("End date service: ", end_date)

        # <---------- To fetch the join content (uncomment it) ---------->

        # # Subquery: Select the minimum id (earliest entry) for each sessionId
        # subquery = db.session.query(
        #     db.func.min(Query.id).label('min_id')
        # ).group_by(Query.sessionId).subquery()

        # # Now fetch only Detail + Query where Query.id is in the min_id list
        # results = db.session.query(Detail, Query).join(
        #     Query, Detail.sessionId == Query.sessionId
        # ).filter(
        #     Detail.inquiry_time >= start_date,
        #     Detail.inquiry_time <= end_date,
        #     Query.id.in_(subquery)
        # ).all()

        # <---------- To fetch the Detail table content only ---------->
        # Querying the Detail table for entries within the given date range
        results = db.session.query(User).filter(
            User.DateTime >= start_date,
            User.DateTime <= end_date,
        ).all()

        # Print the fetched results for debugging
        print("Result: ", results)

        # Return the fetched results
        return results
