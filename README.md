# 📊 Excel Question-Answering Chatbot 🤖

Welcome to the **Excel Question-Answering Chatbot**, your all-in-one tool for retrieving and analyzing data from Excel files. This project combines natural language processing with database querying to provide lightning-fast answers to your data questions. Whether you're retrieving a phone number or calculating total compensation, this chatbot has you covered. 🚀

---

## 🌟 Features

### 🗄️ **Dynamic Table Detection**

- Automatically identifies tables in Excel files, even in non-standard layouts or when multiple tables exist on a single sheet.

### 🧠 **Smart Query Handling**

- Supports two main question types:
  1. **Direct Retrieval**: Extract specific data, like “What is the phone number of Henri?”
  2. **Data Calculations**: Perform computations, such as “What is the total compensation for the HR department?”

### 🚀 **Fast and Efficient**

- Processes large datasets quickly, thanks to optimized querying and data handling.

### 🎨 **User-Friendly Interface**

- Built with **Streamlit**, offering a clean and interactive experience for file uploads and querying.

### 📂 **File Format Support**

- Handles **.xls**, **.xlsx**, and **.csv** files effortlessly.

### 💬 **Real-Time Responses**

- Streaming responses ensure answers are displayed as they’re generated.

---

## 🛠️ Technologies Used

- **Streamlit**: For building the user interface.
- **LangChain Chain**: For building the thinking process of the chatbot.
- **Ollama**: For hosting the nomic-embed-text model.
- **SQLite**: A lightweight database for dynamic querying.
- **pandas/OpenPyXL**: For parsing Excel files and transforming them into queryable datasets.
- **Poetry**: Simplifies dependency management and environment setup.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12**
- **Poetry** for dependency management
- **Ollama** with the nomic-embed-text model
- **Mistral API Key** for the text generation

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Blyzi/excel-chatbot.git
   cd excel-chatbot
   ```

2. **Install Dependencies**  
   Use Poetry to install all required packages:

   ```bash
   poetry install
   ```

3. **Run the Application**

   ```bash
   poetry run streamlit run 👋_Hello.py
   ```

---

## 💻 How to Use

### 1. Upload Your File 📂

- Navigate to the **Upload File** page and drag your Excel file into the uploader.
- The app will automatically detect and process all tables in the file.

### 2. Ask Questions 🤔

- Switch to the **Ask Questions** page and enter your query in natural language.
- Examples:
  - “What is the phone number of Henri?”
  - “What is the total average compensation for the company?”

---

**Happy querying! 🧙‍♂️✨**
