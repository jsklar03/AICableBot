import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import openai
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Function to scrape information from a given URL
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant information from the HTML, modify based on the structure of the website
    extracted_info = soup.get_text()
    return extracted_info

# Function to fine-tune the model using scraped data
def fine_tune_model(scraped_data):
    fine_tuning_data = f"Fine-tune the model with information from cable providers:\n{scraped_data}"
    fine_tuning_result = openai.FineTune.create(
        model="text-davinci-002",
        data=fine_tuning_data,
        n=1,
        stop=None
    )
    return fine_tuning_result['id']

# Function to get a response from the fine-tuned model
def get_chat_response(user_input, chat_history=[]):
    chat_history.append({"role": "user", "content": user_input})
    response = openai.Completion.create(
        model=fine_tuned_model,
        messages=chat_history
    )
    chat_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply, chat_history

# Function to handle user input and display responses
def handle_user_input():
    user_input = user_input_entry.get()
    if user_input.lower() == 'exit':
        root.destroy()
    else:
        assistant_reply, chat_history = get_chat_response(user_input, chat_history_text)
        chat_history_text.insert(tk.END, f"User: {user_input}\n")
        chat_history_text.insert(tk.END, f"Assistant: {assistant_reply}\n\n")
        user_input_entry.delete(0, tk.END)

# Function to start the Tkinter main loop
def start_gui():
    global fine_tuned_model
    cable_provider_url = "https://www.xfinity.com/support/internet/"
    scraped_data = scrape_website(cable_provider_url)
    fine_tune_model(scraped_data)

    fine_tuned_model = f"text-davinci-002-finetuned-{fine_tuning_id}"

    root.mainloop()

# Create the main Tkinter window
root = tk.Tk()
root.title("Cable TV Support Chatbot")

# Create a scrolled text widget for chat history
chat_history_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
chat_history_text.pack(padx=10, pady=10)

# Create an entry widget for user input
user_input_entry = tk.Entry(root, width=50)
user_input_entry.pack(padx=10, pady=10)

# Create a button to send user input
send_button = tk.Button(root, text="Send", command=handle_user_input)
send_button.pack(padx=10, pady=10)

# Create a thread to start the Tkinter main loop
gui_thread = Thread(target=start_gui)
gui_thread.start()
