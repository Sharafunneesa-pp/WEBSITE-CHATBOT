AI Prompt Engineering - Sales Representative Chatbot

Objective

To create a chatbot that can:

Crawl and extract relevant data using BeautifulSoup from a specified website.

Generate effective prompts for personalized recommendations.

Use upselling and cross-selling techniques to drive sales.

Respond accurately to policy-related inquiries.

Store chat logs in a database for review and analysis.

Installation

Clone the repository:

git clone https://github.com/your-repo/nutrinova-chatbot.git

Navigate to the project directory:

cd nutrinova-chatbot

Install dependencies:

pip install -r requirements.txt

How to Run

Start the web crawler:

python crawler.py

Ensure the target website URL is correctly set in the configuration file.

Launch the chatbot application:

python chatbot.py

The chatbot will be accessible locally at http://localhost:5000 or another specified port.

Configure the database:

Set up the database schema using the provided script:

python setup_db.py

Features

Web Crawling:

Extracts data like product names, descriptions, health benefits, and policy documents.

Prompt Engineering:

Generates personalized recommendations.

Supports upselling and cross-selling strategies.

Database Logging:

Stores conversation logs for review and analysis.

Technologies Used

Programming Language: Python

Libraries: BeautifulSoup, Flask, SQLAlchemy

Database: MySQL, PostgreSQL, or SQLite

Contribution

Fork the repository.

Create a new branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Add new feature"

Push to the branch:

git push origin feature-name

Create a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

