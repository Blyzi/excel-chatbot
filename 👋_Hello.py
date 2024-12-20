import streamlit as st

# Streamlit App Title
st.title("📊 Excel Question-Answering Chatbot 🤖")

# Introduction
st.markdown("""
Welcome to the **ultimate Excel data wizard! 🧙‍♂️** 
This app is here to turn your Excel files into a smart, chatty assistant. Whether you're digging for data 🕵️‍♀️ or crunching numbers 🧮, 
we've got you covered. Let's explore what makes this chatbot awesome! 🚀
""")

# Solution Structure
st.header("✨ How It Works")
st.markdown("""
Our app is split into two magical pages:
1. **📂 Upload Your File**  
   Drop your Excel files (**.xls**, **.xlsx**, or **.csv**) here, and our bot will comb through the data like a pro. 🧹  
   - Automatically finds tables 🗄️, even in tricky spots.  
   - Handles sheets with multiple tables seamlessly. 🌟  

2. **🤔 Ask Questions**  
   Head over to the question page, type in your query, and watch the magic happen! 🪄  
   - **For Data Retrieval**: Get instant answers like *“What is the phone number of Henri?”* 📞  
   - **For Calculations**: Ask things like *“What is the total compensation for the HR department?”* 💼
""")

# Key Features
st.header("🔥 Features You'll Love")
st.markdown("""
- **Dynamic Table Detective** 🕵️‍♂️: Finds tables wherever they are hiding in your Excel sheets!  
- **Super Smart Queries** 🧠: Handles everything from basic lookups to complex calculations.  
- **Streaming Responses** 🚀: See your answers as they’re generated, fast and smooth.  
- **Performance Champ** 🏅: Handles big files (up to 50,000 rows) and delivers answers in under 30 seconds.  
""")

# Technologies
st.header("🛠️ Powered By...")
st.markdown("""
- **Streamlit** 🎨: For a slick, interactive interface.  
- **LangChain SQL Chain** 🧑‍💻: Makes your natural language queries shine by converting them into SQL magic.  
- **SQLite** 🗄️: Stores and queries your Excel data dynamically.  
- **pandas/OpenPyXL** 📜: For Excel file parsing like a champ.  
""")

# Example Workflow
st.header("📚 Example Workflow")
st.markdown("""
1. **Upload File**: 🖱️ Drag and drop your file.  
2. **Ask Questions**:  
   - *“What is the phone number of Henri?”*  
     Response: *“The phone number of Henri is +33 6 58 83 38 63.”*  
   - *“What is the total compensation for the HR department?”*  
     Response: *“The total compensation for HR is 154,300.”*  
3. **Sit Back & Relax**: Let the chatbot handle the hard stuff. 🛋️
""")

# Footer
st.markdown("""
---  
**Ready to unleash the power of your Excel files? 🚀 Let's go! 🎉**
""")