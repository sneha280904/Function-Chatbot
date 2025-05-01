### <---------- Imports ---------->

# Import necessary modules from Flask
from flask import request, render_template

# Import datetime for date manipulation
from datetime import datetime

# Import the dashboard service to fetch data
from dashboard.service.dashService import dashService


### <---------- Initialize Service ---------->

# Create an instance of the dashService class
dashService = dashService()


### <---------- DashController Class ---------->

class dashController:

    ### <---------- Dash Controller Method ---------->
    @staticmethod
    def dashController():
        # Fetch the start and end dates from the submitted HTML form
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Convert input string dates to Python datetime objects for processing
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Debug: Print the start and end dates received
        print("Start date: ", start_date)
        print("End date: ", end_date)

        # Call the dashService to process data between the given dates
        results = dashService.dashService(start_date, end_date)
        
        # Debug: Print the results returned from the service layer
        print("Results in controller: ", results)

        # Render the 'dashboard.html' page with the result data and original dates
        return render_template(
            'dashboard.html', 
            results=results, 
            start_date=start_date, 
            end_date=end_date
        )
