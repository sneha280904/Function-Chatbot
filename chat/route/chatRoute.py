from flask import render_template, session, Blueprint, request, redirect, url_for

from chat.controller.chatController import chatController

# Create an instance of chatService
chatController = chatController()

### <---------- Blueprint Initialization ---------->
# Create a new Blueprint for chat-related routes
chat_bp = Blueprint("chat", __name__)

# <------------- Routes ------------- >

@chat_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["message"].strip()
        query_category = ""
        query_subcategory = ""
        if not input_text:
            return redirect(url_for("index"))

        if "chat_history" not in session:
            session["chat_history"] = []
            session["step"] = "greet"

        response = ""

        return chatController.chatbotController(input_text, query_category, query_subcategory, response)

    session["chat_history"] = [{"sender": "bot", "text": "Type HELLO"}]
    session["step"] = "greet"
    session["query_category"] = ""
    session["query_subcategory"] = ""
    return render_template("chat.html", chat_history=session["chat_history"])

# @chat_bp.route("/", methods=["POST"])
# def chatbot():
#         input_text = request.form["message"].strip()
#         query_category = ""
#         query_subcategory = ""
#         if not input_text:
#             return redirect(url_for("index"))

#         if "chat_history" not in session:
#             session["chat_history"] = []
#             session["step"] = "greet"

#         response = ""

#         return chatController.chatbotController(input_text, query_category, query_subcategory, response)

        
        

