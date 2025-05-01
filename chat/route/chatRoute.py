## <---------- Imports ---------->

# Import necessary Flask modules
from flask import render_template, session, Blueprint, request, redirect, url_for

# Import the chatbot controller to handle logic
from chat.controller.chatController import chatController


## <---------- Controller Initialization ---------->

# Create an instance of chatController
chatController = chatController()


## <---------- Blueprint Initialization ---------->

# Create a new Blueprint for chat-related routes
chat_bp = Blueprint("chat", __name__)


## <---------- Routes ---------->

# Define the main chat route
@chat_bp.route("/", methods=["GET", "POST"])
def index():
    
    ## Handle POST requests when the user sends a message
    if request.method == "POST":
        input_text = request.form["message"].strip()  ## Get and clean user input
        query_category = ""  ## Initialize query category
        query_subcategory = ""  ## Initialize query subcategory
        
        ## If message is empty, redirect to the same page
        if not input_text:
            return redirect(url_for("index"))

        ## Initialize session chat history and step if not already present
        if "chat_history" not in session:
            session["chat_history"] = []  ## Start a new chat history list
            session["step"] = "greet"  ## Start at greeting step

        response = ""  ## Initialize response

        ## Call the chatbot controller to handle the logic
        return chatController.chatbotController(input_text, query_category, query_subcategory, response)

    ## Set initial session variables for a new chat session
    session["chat_history"] = [{"sender": "bot", "text": "Type HELLO"}]  ## Initial bot message
    session["step"] = "greet"  ## Initial step
    session["query_category"] = ""  ## Clear category
    session["query_subcategory"] = ""  ## Clear subcategory
    
    ## Render the chat interface
    return render_template("chat.html", chat_history=session["chat_history"])
