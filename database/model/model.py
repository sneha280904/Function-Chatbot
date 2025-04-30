### <---------- Imports ---------->
# Import necessary modules from SQLAlchemy and datetime
from database.database.database import db
from datetime import datetime, timezone

### <---------- Detail Table Definition ---------->
# Represents the userDetails table in the database
class User(db.Model):
    __tablename__ = 'QuickBotChatUserDetailssss'  # Table name in the database

    # <---------- Columns of the userDetails Table ---------->
    userId = db.Column(db.Integer, primary_key=True)  # Primary key for userId

    # URL = db.Column(db.String(50))  # URL column (max length 50)
    # sessionId = db.Column(db.String(50), nullable=False)  # Session ID (mandatory)
    
    name = db.Column(db.String(100))  # User name (max length 100)
    email = db.Column(db.String(100))  # User email (max length 100)
    phoneNo = db.Column(db.String(20))  # User phone number (max length 20)

    query_description = db.Column(db.String(1000))  # User very first query category (max length 1000)

    DateTime = db.Column(
        db.DateTime, 
        # default=datetime.utcnow,  # Uncomment for default to UTC now
        default=lambda: datetime.now(timezone.utc),  # Default to current UTC time
        nullable=False  # This field cannot be null
    )

    # <---------- Commented out fields (for future use) ---------->
    # These are commented out for now but could be used for queries
    # phoneNo = db.Column(db.String(20), nullable=False)

    # query1 = db.Column(db.String(100))
    # query2 = db.Column(db.String(100))
    # query3 = db.Column(db.String(100))
    # query4 = db.Column(db.String(100))
    # query5 = db.Column(db.String(100))
    # query6 = db.Column(db.String(100))
    # query7 = db.Column(db.String(100))
    # query8 = db.Column(db.String(100))
    # query9 = db.Column(db.String(100))
    # query10 = db.Column(db.String(100))

# ### <---------- Query Table Definition ---------->
# # Represents the userQuery table in the database
# class Query(db.Model):
#     __tablename__ = 'userQuery'  # Table name in the database

#     # <---------- Columns of the Query Table ---------->
#     queryId = db.Column(db.Integer, primary_key=True)  # Primary key for queryId
#     sessionId = db.Column(db.String(50), nullable=False)  # Session ID (mandatory)
#     query = db.Column(db.String(100))  # The query text (max length 100)
#     response = db.Column(db.String(10000))  # The response text (max length 10000)
#     DataTime = db.Column(
#         db.DateTime, 
#         default=lambda: datetime.now(timezone.utc),  # Default to current UTC time
#         nullable=False  # This field cannot be null
#     )
