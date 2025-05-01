### <---------- Imports ---------->
# Import necessary modules for Flask and JSON handling
from flask import request, session, render_template, redirect, url_for
import json

### <---------- Chat Service Class ---------->
class chatService:
    def __init__(self):
        ## Load the dataset when the service is initialized
        self.dataset = self.load_dataset()

    ### <---------- Utility Functions ---------->

    # Load the dataset from a JSON file
    def load_dataset(self):
        try:
            with open("D:/Coding/Python-Projects/QuickBot-Chat/dataset/dataset.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("self.dataset file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding the self.dataset JSON.")
            return {}
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {}

    ### <---------- Response Generation Functions ---------->

    # Return all available categories in the dataset
    def respondcategories(self):
        category_list = [f"{category}<br>" for category in self.dataset.keys()]
        return "\n".join(category_list)

    # Return subcategories for a given category
    def respondsubcategories(self, query_category_c):
        query_category = query_category_c.replace(" ", "").lower()
        for category in self.dataset.keys():
            category_c = category.lower().replace(" ", "")
            if query_category == category_c:
                sub_category = ["Choose from the following SubCategories: "]
                for subcategory in self.dataset[category].keys():
                    sub_category.append(f"{subcategory}<br>")
                sub_category += ["Back <br>", "Stop <br>"]
                return "\n".join(sub_category)
        return "Sorry, I am unable to understand your choosen category. <br> Please rephrase your question, or type BACK to select/change query categories."

    # Return questions for a given subcategory
    def respondquestions(self, query_subcategory):
        query_subcategory = query_subcategory.replace(" ", "").lower()
        for category in self.dataset.keys(): 
            for subcategory in self.dataset[category]:  
                if query_subcategory == subcategory.replace(" ", "").lower():
                    questions = ["Choose from the following questions: "]
                    for question_entry in self.dataset[category][subcategory]:  
                        questions.append(f"{question_entry['question']}<br>")
                    questions += ["Back <br>", "Thank You <br>", "Stop <br>"]
                    return "\n".join(questions)
        return "Sorry, I am unable to understand your choosen subcategory. <br> Please rephrase your question, or type BACK to select/change query categories."

    # Return answer for a matched question under a specific category and subcategory
    def respond(self, query_category, query_subcategory, input_text):
        query_category = query_category.replace(" ", "").lower()
        query_subcategory = query_subcategory.replace(" ", "").lower()
        for category in self.dataset.keys():
            for subcategory in self.dataset[category].keys():
                for entry in self.dataset[category][subcategory]: 
                    if input_text.lower() in entry["question"].lower():
                        return entry["answer"]
        return "Sorry, I don't have an answer for that. <br> Please rephrase your question, or type BACK to select/change query categories."
