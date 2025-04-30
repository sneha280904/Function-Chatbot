# from flask import Flask, request, jsonify, render_template, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from validation import validation
# import json
# import re

# <------------- Flask App and Database Setup ------------- >
# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# Configure MySQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sarita&2007@localhost:3306/chatbotdata'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
# db = SQLAlchemy(app)

# # <------------- Database Model ------------- >
# class User(db.Model):
#     __tablename__ = 'userDetail'
#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     phoneNo = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     query_description = db.Column(db.String(100))

# Create tables
# with app.app_context():
#     try:
#         db.create_all()
#     except Exception as e:
#         print(f"Error creating database tables: {str(e)}")

# # <------------- Utility Functions ------------- >
# def load_dataset():
#     try:
#         with open("D:\\Coding\\Python-Projects\\QuickBot-Chat\\dataset.json", "r", encoding="utf-8") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print("Dataset file not found.")
#         return {}
#     except json.JSONDecodeError:
#         print("Error decoding the dataset JSON.")
#         return {}
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         return {}

# dataset = load_dataset()

# # <------------- Response Generation Functions ------------- >
# def respondcategories():
#     category_list = [f"{category}<br>" for category in dataset.keys()]
#     return "\n".join(category_list)

# def respondsubcategories(query_category_c):
#     query_category = query_category_c.replace(" ", "").lower()
#     for category in dataset.keys():
#         category_c = category.lower().replace(" ", "")
#         if query_category == category_c:
#             sub_category = ["Choose from the following SubCategories: "]
#             for subcategory in dataset[category].keys():
#                 sub_category.append(f"{subcategory}<br>")
#             sub_category += ["Back <br>", "Stop <br>"]
#             return "\n".join(sub_category)
#     return "Sorry, I am unable to understand your choosen category. <br> Please rephrase your question, or type BACK to select/change query categories."

# def respondquestions(query_subcategory):
#     query_subcategory = query_subcategory.replace(" ", "").lower()
#     for category in dataset.keys(): 
#         for subcategory in dataset[category]:  
#             if query_subcategory == subcategory.replace(" ", "").lower():
#                 questions = ["Choose from the following questions: "]
#                 for question_entry in dataset[category][subcategory]:  
#                     questions.append(f"{question_entry['question']}<br>")
#                 questions += ["Back <br>", "Thank You <br>", "Stop <br>"]
#                 return "\n".join(questions)
#     return "Sorry, I am unable to understand your choosen subcategory. <br> Please rephrase your question, or type BACK to select/change query categories."

# def respond(query_category, query_subcategory, input_text):
#     query_category = query_category.replace(" ", "").lower()
#     query_subcategory = query_subcategory.replace(" ", "").lower()
#     for category in dataset.keys():
#         for subcategory in dataset[category].keys():
#             for entry in dataset[category][subcategory]: 
#                 if input_text.lower() in entry["question"].lower():
#                     return entry["answer"]
#     return "Sorry, I don't have an answer for that. <br> Please rephrase your question, or type BACK to select/change query categories."

# # <------------- Validation Functions ------------- >
# import re
# import phonenumbers
# import dns.resolver

# # Set of known disposable email domains
# blocklist = {"mailinator.com", "tempmail.com", "10minutemail.com"}  # Extend as needed

# def validate_phone_number(phone, region='IN'):
#     """
#     Validates Indian phone number using regex and phonenumbers library.
#     """
#     try:
#         phone_regex = r'^[6-9]\d{9}$'
#         parsed = phonenumbers.parse(phone, region)
#         return re.match(phone_regex, phone) and phonenumbers.is_possible_number(parsed) and phonenumbers.is_valid_number(parsed)
#     except:
#         return False

# def validate_email(email):
#     """
#     Validates email using regex, checks against disposable domains, and MX record existence.
#     """
#     try:
#         email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#         domain = email.split('@')[-1].lower()
#         if not re.match(email_regex, email) or domain in blocklist:
#             return False
#         return len(dns.resolver.resolve(domain, 'MX')) > 0
#     except:
#         return False


# # <------------- Routes ------------- >
# @app.route("/", methods=["GET"])
# def index():
#     session["chat_history"] = [{"sender": "bot", "text": "Type HELLO"}]
#     session["step"] = "greet"
#     session["query_category"] = ""
#     session["query_subcategory"] = ""
#     return render_template("chat.html", chat_history=session["chat_history"])

# @app.route("/chat", methods=["POST"])
# def chatbot():
#     input_text = request.form["message"].strip()
#     query_category = ""
#     query_subcategory = ""
#     if not input_text:
#         return redirect(url_for("index"))

#     if "chat_history" not in session:
#         session["chat_history"] = []
#         session["step"] = "greet"

#     response = ""

#     # ------------- >
#     # Chatbot Conversation Flow
#     # ------------- >
#     if session["step"] == "greet":
#         response = "Hello! What is your name?"
#         session["step"] = "ask_name"

#     elif session["step"] == "ask_name":
#         session["name"] = input_text
#         response = f"Nice to meet you, {input_text}! Please enter your email."
#         session["step"] = "ask_email"

#     elif session["step"] == "ask_email":
#         if validate_email(input_text):
#             session["email"] = input_text
#             response = "Thanks! Now, enter your phone number."
#             session["step"] = "ask_phone"
#         else:
#             response = "Please enter a valid email address."

#     elif session["step"] == "ask_phone":
#         if validate_phone_number(input_text):
#             session["phoneNo"] = input_text
#             response = respondcategories()
#             session["step"] = "ask_query_category"
#         else:
#             response = "Please enter a valid phone number."

#     elif session["step"] == "ask_query_category":
#         session["query_category"] = input_text
#         input_text = input_text.replace(" ", "")
#         new_user = User(
#             name=session["name"],
#             email=session["email"],
#             phoneNo=session["phoneNo"],
#             query_description=session["query_category"]
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         response = respondsubcategories(input_text)
#         session["step"] = "ask_query_subcategory"

#     elif session["step"] == "ask_query_category_again":
#         session["query_category"] = input_text
#         input_text = input_text.replace(" ", "")
#         response = respondsubcategories(input_text)
#         session["step"] = "ask_query_subcategory"

#     elif session["step"] == "ask_query_subcategory":
#         session["query_subcategory"] = input_text
#         input_text = input_text.replace(" ", "")
#         if input_text.lower() == "back":
#             session["step"] = "ask_query_category_again"
#             session["query_subcategory"] = ""
#             session["query_category"] = ""
#             response = respondcategories()
#         elif input_text.lower() == 'stop':
#             session['step'] = "completed"
#             response = "Are you satisfied with the response? Type Yes or No"
#         else:
#             response = respondquestions(input_text)
#             session["step"] = "ask_query"

#     elif session["step"] == "ask_query":
#         session["query"] = input_text
#         query_category = session["query_category"]
#         query_subcategory = session["query_subcategory"]
#         if input_text.lower().replace(" ", "") == "back":
#             session["step"] = "ask_query_subcategory"
#             response = respondsubcategories(query_category)
#         elif input_text.lower().replace(" ", "") == 'thankyou':
#             response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."
#             session["step"] = "more"
#         elif input_text.lower().replace(" ", "") == 'stop':
#             session['step'] = "completed"
#             response = "Are you satisfied with the response? Type Yes or No"
#         else:
#             response = respond(query_category, query_subcategory, input_text)
#             session["step"] = "ask_query"

#     elif session["step"] == "more":
#         session["again"] = input_text
#         if input_text.lower().replace(" ", "") == "more":
#             session["step"] = "ask_query_category_again"
#             response = respondcategories()
#         elif input_text.lower().replace(" ", "") == "stop":
#             response = "Are you satisfied with the response? Type Yes or No"
#         else: 
#             response = "Thank you! If you have more questions, type MORE and feel free to ask or type STOP to end conversation."

#     elif session["step"] == "completed":
#         session["again"] = input_text
#         if input_text.lower().replace(" ", "") == "yes":
#             response = "Thank you! If you have more questions, type MORE and feel free to ask. :)"
#         elif input_text.lower().replace(" ", "") == "no":
#             response = "Sorry for that :("
#         else: 
#             session["step"] = "ask_query_category_again"
#             response = respondcategories()

#     else:
#         response = "Error!"

#     # ------------- >
#     # Store Chat History
#     # ------------- >
#     session["chat_history"].append({"sender": "user", "text": input_text})
#     session["chat_history"].append({"sender": "bot", "text": response})
#     session.modified = True
#     return render_template("chat.html", chat_history=session["chat_history"])

# <------------- Run App ------------- >
# if __name__ == "__main__":
#     app.run(debug=True)
