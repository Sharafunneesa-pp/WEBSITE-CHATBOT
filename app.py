# import os
# import logging
# from flask import Flask, request, render_template, jsonify
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import PyPDFLoader
# import openai
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv
# import json
# from langchain.schema import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Load environment variables from a .env file
# load_dotenv()

# # Fetch OpenAI API key from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Set the OpenAI API key for usage
# openai.api_key = OPENAI_API_KEY

# # Initialize the Flask application
# app = Flask(__name__)

# # Initialize global variables for conversation history
# conversation_history = []

# # Setup logging for error handling and debugging purposes
# logging.basicConfig(level=logging.ERROR)

# # Function to load JSON files from a folder and extract text from 'structured_info' key
# def get_json_text_from_folder(json_folder):
#     documents = []
#     try:
#         # Loop through each file in the folder and process only JSON files
#         for json_file in os.listdir(json_folder):
#             if json_file.endswith(".json"):  # Only process JSON files
#                 json_path = os.path.join(json_folder, json_file)

#                 # Load JSON data
#                 with open(json_path, 'r', encoding='utf-8') as f:
#                     json_data = json.load(f)
                
#                 # Extract product information from 'products' key
#                 products = json_data.get('products', [])
                
#                 for product in products:
#                     structured_info = product.get('structured_info', '')
                    
#                     # Split text if it is large
#                     for chunk in get_text_chunks(structured_info):
#                         document = Document(page_content=chunk, metadata={'source': json_file, 'product_url': product.get('url', '')})
#                         documents.append(document)
#     except Exception as e:
#         logging.error(f"Error in get_json_text_from_folder: {str(e)}")
#     return documents

# # Function to split large chunks of text into smaller parts for easier processing
# def get_text_chunks(text):
#     try:
#         # Use LangChain's RecursiveCharacterTextSplitter to split text into smaller chunks
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         return text_splitter.split_text(text)
#     except Exception as e:
#         logging.error(f"Error in get_text_chunks: {str(e)}")
#         return []

# # Function to create a vector store using FAISS and OpenAI embeddings from the documents
# def create_vector_store(json_folder):
#     try:
#         # Load documents from the JSON folder
#         documents = get_json_text_from_folder(json_folder)

#         # Use OpenAI embeddings to represent text data as vectors
#         embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)  # Use the API key from environment

#         # Use FAISS to create a vector store from the documents
#         vector_store = FAISS.from_documents(documents, embedding=embeddings)

#         # Save the vector store locally for future use
#         vector_store.save_local("faiss_index")

#         return vector_store
#     except Exception as e:
#         logging.error(f"Error in create_vector_store: {str(e)}")
#         return None

# def get_conversational_chain():
#     try:
#         # Define a prompt template to combine context and chat history with the user's question
#         prompt_template = """
#         You are John, a sales representative and health advisor for Nutrinova. 
#         You speak only English and provide expert advice on health supplements. 
#         Your user may inquire about different health concerns, such as joint health, memory enhancement, or immunity support. 
#         Your goal is to recommend Nutrinova products based on the user's health needs. 
#         You should upsell products with current offers or cross-sell complementary items to enhance the user's health journey. 
#         Additionally, respond accurately to policy-related inquiries about returns, privacy policies, and more. 
#         When making recommendations, provide clear and factual responses. 
#         Use all of the context from the current conversation to ensure the recommendations and responses are relevant. 
#         Please keep your responses concise and user-friendly, avoiding unnecessary verbosity.


#         Context: {context}
#         Chat History: {chat_history}
#         Human: {question}
#         AI: 
#         """
        
#         # Initialize the OpenAI model for question answering with specific parameters
#         model = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.0, max_tokens=50)

#         # Create a PromptTemplate object with the defined prompt
#         prompt = PromptTemplate(template=prompt_template, input_variables=["context", "chat_history", "question"])

#         # Load the QA chain using the prompt and the OpenAI model
#         return load_qa_chain(model, chain_type="stuff", prompt=prompt)
#     except Exception as e:
#         logging.error(f"Error in get_conversational_chain: {str(e)}")
#         return None

# # Function to process user input, fetch relevant documents, and generate a response
# def user_input(user_question, chat_history):
#     try:
#         # Load FAISS vector store with OpenAI embeddings for document retrieval
#         embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
#         new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

#         # Build a combined query from the entire conversation history
#         recent_context = "\n".join([f"Human: {chat['question']}\nAI: {chat['answer']}" for chat in chat_history[-5:]])  # Limit to last 5 exchanges
#         combined_query = f"{recent_context}\nHuman: {user_question}"

#         # Perform similarity search in the FAISS vector store
#         docs = new_db.similarity_search(combined_query, k=7)

#         # Aggregate the content of the most relevant documents
#         context = "\n".join([doc.page_content for doc in docs])

#         # Retrieve the conversational chain (question-answering logic)
#         chain = get_conversational_chain()

#         if chain is None:
#             return "Sorry, something went wrong with the AI model."

#         # Generate a response based on the documents and context
#         response = chain.invoke(
#             {
#                 "input_documents": docs,
#                 "question": combined_query,
#                 "chat_history": recent_context,
#                 "context": context,
#             },
#             return_only_outputs=True
#         )

#         # Return the generated response, or a default message if the response is empty
#         return response["output_text"].strip() if response.get("output_text") else "I'm sorry, I don't have that information."
    
#     except Exception as e:
#         logging.error(f"Error in user_input: {str(e)}")
#         return "Sorry, something went wrong with your request."


# @app.route('/')
# def home():
#     try:
#         return render_template('chat.html')  # Render the HTML page (rag.html should be created in templates)
#     except Exception as e:
#         logging.error(f"Error loading home page: {str(e)}")
#         return "Sorry, something went wrong while loading the page."


# # Route to handle chat interactions
# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         # Retrieve user input and chat history from the form data
#         user_message = request.form['user_input']
#         chat_history = request.form.get('chat_history', [])

#         # If chat_history is a string, convert it to a Python object (list of dicts)
#         if isinstance(chat_history, str):
#             chat_history = json.loads(chat_history)

#         # Print the chat history for debugging purposes
#         print(f"Chat History: {json.dumps(chat_history, indent=2)}")

#         # Get the bot's response based on user input and chat history
#         bot_message = user_input(user_message, chat_history)

#         # Append the new user question and bot response to the chat history
#         chat_history.append({"question": user_message, "answer": bot_message})

#         # Return the response as JSON, excluding the sources field
#         response_data = {
#             "response": bot_message,
#             "chat_history": chat_history
#         }

#         # Return the response as JSON
#         return jsonify(response_data)
#     except Exception as e:
#         logging.error(f"Error in /chat route: {str(e)}")
#         return jsonify({"response": "Sorry, an error occurred while processing your message."})

# # Main entry point for the application
# if __name__ == '__main__':
#     try:
#         # Define the path to the folder containing PDF files or JSON files
#         pdf_folder_path = os.path.join(os.getcwd(), 'data')  # Assuming the 'data' folder exists
#         # Create the FAISS vector store using the JSON folder data
#         vector_store = create_vector_store(pdf_folder_path)

#         if vector_store is None:
#             raise Exception("Failed to create vector store.")

#         # Start the Flask web application
#         app.run(debug=True)
#     except Exception as e:
#         logging.error(f"Error starting the application: {str(e)}")

