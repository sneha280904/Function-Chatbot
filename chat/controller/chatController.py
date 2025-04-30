### <---------- Imports ---------->
# Import Flask modules for API responses and request handling
from flask import  request, session, render_template

# Import for safely rendering HTML
from markupsafe import Markup 

# Import for handling datetime and timezone
from datetime import datetime, timezone 

# Import chat service to handle core chatbot logic
from chat.service.chatService import chatService

# Import validation to validate email and phone number
from validation import validation

# Import database instance and models
from database.database.database import db
from database.model.model import User

## <---------- Chat Service Initialization ---------->
# Create an instance of chatService
chatService = chatService()

## <---------- Chat Controller Class ---------->
class chatController:

    ## <---------- Main Chatbot Controller Function ---------->
    @staticmethod
    def chatbotController(input_text, query_category, query_subcategory, response):
        
        ## <---------- Step: Greeting the User ---------->
        if session["step"] == "greet":
            session["DateTime"] = datetime.now().isoformat()  # Store the current datetime
            response = "Hello! What is your name?"  # Prompt user for name
            session["step"] = "ask_name"  # Move to next step

        ## <---------- Step: Asking for Name ---------->
        elif session["step"] == "ask_name":
            session["name"] = input_text  # Store user name
            response = f"Nice to meet you, {input_text}! Please enter your email."  # Prompt for email
            session["step"] = "ask_email"  # Move to next step

        ## <---------- Step: Asking for Email ---------->
        elif session["step"] == "ask_email":
            if validation.validateEmail(input_text):  # Validate email format
                session["email"] = input_text  # Store email
                response = "Thanks! Now, enter your phone number."  # Prompt for phone
                session["step"] = "ask_phone"  # Move to next step
            else:
                response = "Please enter a valid email address."  # Error message

        ## <---------- Step: Asking for Phone Number ---------->
        elif session["step"] == "ask_phone":
            if validation.validatePhoneNumber(input_text):  # Validate phone number
                session["phoneNo"] = input_text  # Store phone number
                response = chatService.respondcategories()  # Ask for category
                session["step"] = "ask_query_category"  # Move to next step
            else:
                response = "Please enter a valid phone number."  # Error message

        ## <---------- Step: Asking for Query Category ---------->
        elif session["step"] == "ask_query_category":
            session["query_category"] = input_text  # Store category
            input_text = input_text.replace(" ", "")  # Normalize input
            new_user = User(
                name=session["name"],
                email=session["email"],
                phoneNo=session["phoneNo"],
                query_description=session["query_category"],
                # DateTime = session["DateTime"]
                DateTime=datetime.now(timezone.utc)  # Store UTC time
            )
            db.session.add(new_user)  # Save user to DB
            db.session.commit()
            response = chatService.respondsubcategories(input_text)  # Ask for subcategory
            session["step"] = "ask_query_subcategory"  # Move to next step

        ## <---------- Step: Re-asking for Query Category ---------->
        elif session["step"] == "ask_query_category_again":
            session["query_category"] = input_text  # Store new category
            input_text = input_text.replace(" ", "")  # Normalize input
            response = chatService.respondsubcategories(input_text)  # Ask for subcategory
            session["step"] = "ask_query_subcategory"  # Move to next step

        ## <---------- Step: Asking for Query Subcategory ---------->
        elif session["step"] == "ask_query_subcategory":
            session["query_subcategory"] = input_text  # Store subcategory
            input_text = input_text.replace(" ", "")  # Normalize input
            if input_text.lower() == "back":  # Handle 'back'
                session["step"] = "ask_query_category_again"
                session["query_subcategory"] = ""
                session["query_category"] = ""
                response = chatService.respondcategories()
            elif input_text.lower() == 'stop':  # Handle 'stop'
                session['step'] = "completed"
                response = "Are you satisfied with the response? Type Yes or No"
            else:
                response = chatService.respondquestions(input_text)  # Ask question
                session["step"] = "ask_query"  # Move to next step

        ## <---------- Step: Asking Actual Query ---------->
        elif session["step"] == "ask_query":
            session["query"] = input_text  # Store query
            query_category = session["query_category"]
            query_subcategory = session["query_subcategory"]
            if input_text.lower().replace(" ", "") == "back":  # Handle 'back'
                session["step"] = "ask_query_subcategory"
                response = chatService.respondsubcategories(query_category)
            elif input_text.lower().replace(" ", "") == 'thankyou':  # Handle 'thankyou'
                response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."
                session["step"] = "more"
            elif input_text.lower().replace(" ", "") == 'stop':  # Handle 'stop'
                session['step'] = "completed"
                response = "Are you satisfied with the response? Type Yes or No"
            else:
                response = chatService.respond(query_category, query_subcategory, input_text)  # Get response
                session["step"] = "ask_query"  # Stay on same step

        ## <---------- Step: More Queries Flow ---------->
        elif session["step"] == "more":
            session["again"] = input_text  # Store answer
            if input_text.lower().replace(" ", "") == "more":  # Handle 'more'
                session["step"] = "ask_query_category_again"
                response = chatService.respondcategories()
            elif input_text.lower().replace(" ", "") == "stop":  # Handle 'stop'
                response = "Are you satisfied with the response? Type Yes or No"
            else: 
                response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."

        ## <---------- Step: Conversation Completed ---------->
        elif session["step"] == "completed":
            session["again"] = input_text  # Store answer
            if input_text.lower().replace(" ", "") == "yes":  # Handle 'yes'
                response = "Thank you! If you have more questions, type MORE and feel free to ask. :)"
            elif input_text.lower().replace(" ", "") == "no":  # Handle 'no'
                response = "Sorry for that :("
            else: 
                session["step"] = "ask_query_category_again"  # Restart flow
                response = chatService.respondcategories()

        ## <---------- Step: Error Handling ---------->
        else:
            response = "Error!"

        ## <---------- Store Chat History ---------->
        session["chat_history"].append({"sender": "user", "text": input_text})  # Save user message
        session["chat_history"].append({"sender": "bot", "text": response})  # Save bot reply
        session.modified = True  # Mark session as modified
        return render_template("chat.html", chat_history=session["chat_history"])  # Render chat
