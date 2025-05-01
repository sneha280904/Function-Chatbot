## <---------- Imports ---------->

# Import necessary modules for Flask and JSON handling
from flask import request, session, render_template, redirect, url_for
import json


## <---------- Chat Service Class ---------->

class chatService:
    def __init__(self):
        ## Load the dataset when the service is initialized
        self.dataset = self.load_dataset()


    ## <---------- Utility Functions ---------->

    # Load the dataset from a JSON file
    def load_dataset(self):
        try:
            with open("D:/Coding/Python-Projects/QuickBot-Chat/dataset/dataset.json", "r", encoding="utf-8") as file:
                return json.load(file)  ## Load and return the dataset
        except FileNotFoundError:
            print("self.dataset file not found.")  ## File not found error
            return {}
        except json.JSONDecodeError:
            print("Error decoding the self.dataset JSON.")  ## Invalid JSON format
            return {}
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  ## Catch-all for any other issues
            return {}


    ## <---------- Response Generation Functions ---------->

    # Return all available categories in the dataset
    def respondcategories(self):
        category_list = [f"{category}<br>" for category in self.dataset.keys()]  ## Format category list
        return "\n".join(category_list)  ## Return as HTML line-breaked string

    # Return subcategories for a given category
    def respondsubcategories(self, query_category_c):
        query_category = query_category_c.replace(" ", "").lower()  ## Normalize input
        for category in self.dataset.keys():
            category_c = category.lower().replace(" ", "")  ## Normalize dataset category
            if query_category == category_c:
                sub_category = ["Choose from the following SubCategories: "]
                for subcategory in self.dataset[category].keys():
                    sub_category.append(f"{subcategory}<br>")  ## Append each subcategory
                sub_category += ["Back <br>", "Stop <br>"]  ## Navigation options
                return "\n".join(sub_category)
        
        ## If no match is found
        return "Sorry, I am unable to understand your choosen category. <br> Please rephrase your question, or type BACK to select/change query categories."

    # Return questions for a given subcategory
    def respondquestions(self, query_subcategory):
        query_subcategory = query_subcategory.replace(" ", "").lower()  ## Normalize input
        for category in self.dataset.keys(): 
            for subcategory in self.dataset[category]:  
                if query_subcategory == subcategory.replace(" ", "").lower():
                    questions = ["Choose from the following questions: "]
                    for question_entry in self.dataset[category][subcategory]:  
                        questions.append(f"{question_entry['question']}<br>")  ## Append each question
                    questions += ["Back <br>", "Thank You <br>", "Stop <br>"]  ## Navigation options
                    return "\n".join(questions)
        
        ## If no matching subcategory found
        return "Sorry, I am unable to understand your choosen subcategory. <br> Please rephrase your question, or type BACK to select/change query categories."

    # Return answer for a matched question under a specific category and subcategory
    def respond(self, query_category, query_subcategory, input_text):
        query_category = query_category.replace(" ", "").lower()  ## Normalize category
        query_subcategory = query_subcategory.replace(" ", "").lower()  ## Normalize subcategory
        for category in self.dataset.keys():
            for subcategory in self.dataset[category].keys():
                for entry in self.dataset[category][subcategory]: 
                    if input_text.lower() in entry["question"].lower():  ## Match found
                        return entry["answer"]  ## Return the corresponding answer
        
        ## If no question match is found
        return "Sorry, I don't have an answer for that. <br> Please rephrase your question, or type BACK to select/change query categories."
