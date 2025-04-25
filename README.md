# Chatbot

This repository contains the codebase for a rule-based chatbot developed by Dhiyotech Pvt. Ltd. The chatbot operates strictly based on predefined functions and a specific dataset, ensuring consistent and predictable interactions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The chatbot is designed to provide responses based on a fixed set of rules and a structured dataset. It is ideal for applications where controlled and consistent interactions are required.

## Features

- Rule-based response generation
- Utilizes a structured SQL dataset
- Modular codebase for easy maintenance
- Simple web interface using Flask

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/himanshudhiyotech/chatbot.git
   cd chatbot
   git checkout Development-Sneha
   ```


2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```


3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Set up the database:**

   Ensure you have a MySQL server running. Create a database and import the provided `chatbotdata.sql` file:

   ```bash
   mysql -u your_username -p
   CREATE DATABASE chatbot_db;
   USE chatbot_db;
   SOURCE chatbotdata.sql;
   ```


2. **Configure database connection:**

   Update the database connection details in `app.py` to match your MySQL configuration.

3. **Run the application:**

   ```bash
   python app.py
   ```


4. **Access the chatbot:**

   Open your web browser and navigate to `http://localhost:5000` to interact with the chatbot.

## Dataset

- **`chatbotdata.sql`**: Contains the SQL script to set up the chatbot's database with predefined intents and responses.
- **`dataset.json`**: Provides a JSON representation of the chatbot's intents and responses, useful for understanding the data structure or for potential integration with other platforms.

## Project Structure


```plaintext
├── app.py                         # Main application file containing Flask routes and chatbot logic
├── chatbotdata.sql                # SQL script to set up the chatbot database
├── dataset.json                   # JSON representation of intents and responses
├── requirements.txt               # Python dependencies
├── templates/
│   └── index.html                 # HTML template for the chatbot interface
├── Talent Spiral Chatbot Dataset Documentation.docx  # Documentation detailing the dataset
└── README.md                      # Project documentation
```


## Contributing

Contributions are welcome! Please fork the repository and create a new branch for your feature or bugfix. Once done, submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE).
