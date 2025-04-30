### <---------- Imports ---------->
# Import Flask modules for API responses and request handling
from flask import  request, session, render_template, redirect, url_for
from markupsafe import Markup 

from datetime import datetime, timezone

# # Store current datetime in ISO format
# session["DateTime"] = datetime.now().isoformat()

# Import chat service to handle core chatbot logic
from chat.service.chatService import chatService

# Import validation to validate email and phone number
from validation import validation

# Import database instance and models
from database.database.database import db
from database.model.model import User

# Create an instance of chatService
chatService = chatService()

class chatController:
    
    @staticmethod
    def chatbotController(input_text, query_category, query_subcategory, response):
        # Chatbot Conversation Flow
        if session["step"] == "greet":
            session["DateTime"] = datetime.now().isoformat()
            response = "Hello! What is your name?"
            session["step"] = "ask_name"

        elif session["step"] == "ask_name":
            session["name"] = input_text
            response = f"Nice to meet you, {input_text}! Please enter your email."
            session["step"] = "ask_email"

        elif session["step"] == "ask_email":
            if validation.validateEmail(input_text):
                session["email"] = input_text
                response = "Thanks! Now, enter your phone number."
                session["step"] = "ask_phone"
            else:
                response = "Please enter a valid email address."

        elif session["step"] == "ask_phone":
            if validation.validatePhoneNumber(input_text):
                session["phoneNo"] = input_text
                response = chatService.respondcategories()
                session["step"] = "ask_query_category"
            else:
                response = "Please enter a valid phone number."

        elif session["step"] == "ask_query_category":
            session["query_category"] = input_text
            input_text = input_text.replace(" ", "")
            new_user = User(
                name=session["name"],
                email=session["email"],
                phoneNo=session["phoneNo"],
                query_description=session["query_category"],
                # DateTime = session["DateTime"]
                DateTime=datetime.now(timezone.utc)
            )
            db.session.add(new_user)
            db.session.commit()
            response = chatService.respondsubcategories(input_text)
            session["step"] = "ask_query_subcategory"

        elif session["step"] == "ask_query_category_again":
            session["query_category"] = input_text
            input_text = input_text.replace(" ", "")
            response = chatService.respondsubcategories(input_text)
            session["step"] = "ask_query_subcategory"

        elif session["step"] == "ask_query_subcategory":
            session["query_subcategory"] = input_text
            input_text = input_text.replace(" ", "")
            if input_text.lower() == "back":
                session["step"] = "ask_query_category_again"
                session["query_subcategory"] = ""
                session["query_category"] = ""
                response = chatService.respondcategories()
            elif input_text.lower() == 'stop':
                session['step'] = "completed"
                response = "Are you satisfied with the response? Type Yes or No"
            else:
                response = chatService.respondquestions(input_text)
                session["step"] = "ask_query"

        elif session["step"] == "ask_query":
            session["query"] = input_text
            query_category = session["query_category"]
            query_subcategory = session["query_subcategory"]
            if input_text.lower().replace(" ", "") == "back":
                session["step"] = "ask_query_subcategory"
                response = chatService.respondsubcategories(query_category)
            elif input_text.lower().replace(" ", "") == 'thankyou':
                response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."
                session["step"] = "more"
            elif input_text.lower().replace(" ", "") == 'stop':
                session['step'] = "completed"
                response = "Are you satisfied with the response? Type Yes or No"
            else:
                response = chatService.respond(query_category, query_subcategory, input_text)
                session["step"] = "ask_query"

        elif session["step"] == "more":
            session["again"] = input_text
            if input_text.lower().replace(" ", "") == "more":
                session["step"] = "ask_query_category_again"
                response = chatService.respondcategories()
            elif input_text.lower().replace(" ", "") == "stop":
                response = "Are you satisfied with the response? Type Yes or No"
            else: 
                response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."

        elif session["step"] == "completed":
            session["again"] = input_text
            if input_text.lower().replace(" ", "") == "yes":
                response = "Thank you! If you have more questions, type MORE and feel free to ask. :)"
            elif input_text.lower().replace(" ", "") == "no":
                response = "Sorry for that :("
            else: 
                session["step"] = "ask_query_category_again"
                response = chatService.respondcategories()

        else:
            response = "Error!"

        # ------------- >
        # Store Chat History
        # ------------- >
        session["chat_history"].append({"sender": "user", "text": input_text})
        session["chat_history"].append({"sender": "bot", "text": response})
        session.modified = True
        return render_template("chat.html", chat_history=session["chat_history"])
    



