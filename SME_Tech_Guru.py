import streamlit as st
import pandas as pd
import sqlite3
import os

# --- Database Setup ---
DB_NAME = 'faculty_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Drop tables if they exist to ensure clean slate for development/re-initialization
    # In a production scenario with persistent data, you might remove these DROP statements
    cursor.execute("DROP TABLE IF EXISTS cse_faculty;")
    cursor.execute("DROP TABLE IF EXISTS it_faculty;")

    # Create CSE Faculty Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cse_faculty (
            S_No INTEGER PRIMARY KEY,
            Name_of_the_Faculty_Member TEXT,
            Degree_Highest_Degree TEXT,
            University TEXT,
            Year_of_attaining_higher_qualification INTEGER,
            Designation TEXT,
            Date_on_which_designated_as_Professor_Associate_Professor TEXT,
            Date_of_joining_the_Institution TEXT,
            Department TEXT,
            Specialization TEXT,
            Research_Paper_Publication TEXT,
            PhD_Guidance TEXT,
            Faculty_Receiving_PhD_during_the_assessment_Years TEXT,
            Currently_Associated_Y_N TEXT,
            Date_of_Leaving TEXT,
            Nature_of_Association_Regular_Contract TEXT,
            Currently_Teaching_Same_Specialization TEXT
        )
    ''')

    # Create IT Faculty Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS it_faculty (
            S_No INTEGER PRIMARY KEY,
            Name_of_the_Faculty_Member TEXT,
            Degree_Highest_Degree TEXT,
            University TEXT,
            Year_of_attaining_higher_qualification INTEGER,
            Designation TEXT,
            Date_of_joining_the_Institution TEXT,
            Department TEXT,
            Specialization TEXT,
            Research_Paper_Publication TEXT,
            PhD_Guidance TEXT,
            Faculty_Receiving_PhD_during_the_assessment_Years TEXT,
            Currently_Associated_Y_N TEXT,
            Date_of_Leaving TEXT,
            Nature_of_Association_Regular_Contract TEXT,
            Currently_Teaching_Same_Specialization TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(df, table_name):
    conn = sqlite3.connect(DB_NAME)
    # Using 'append' and 'if_exists'='append' ensures data is added if tables exist
    # If 'replace' was used, it would recreate the table every time.
    # We use 'replace' after dropping tables in init_db for fresh start.
    # Here, for subsequent runs, 'append' would be problematic if not careful.
    # The current init_db drops tables, so 'replace' is fine for this specific setup to ensure no duplicate data on re-run.
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

# --- Data Preparation ---
# CSE Department Data
cse_data = {
    'S_No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21],
    'Name_of_the_Faculty_Member': ['Dr. Preetha M', 'Dr. Ravikumar V', 'Dr. Hariharasudhan S', 'Dr. Senthil K', 'Dr. Veeralakshmi P', 'Ms.Umamaheswari B', 'Ms. Bhuvaneswari S', 'Ms. Arunadevi R', 'Ms. Sathya S', 'Ms. Keerthiga A', 'Ms. Sindhu M', 'Ms. Rajalakshmi G', 'Ms. Sowmiya S', 'Ms. Senthurya S', 'Ms. Reena R', 'Ms. Sathya T', 'Ms. Jermin Jersha T C', 'Ms. Sowmya B', 'Ms Aparna R', 'Mr .Senthil Kumar S R'],
    'Degree_Highest_Degree': ['Ph.D.', 'Ph.D.', 'Ph.D.', 'Ph.D.', 'Ph.D.', 'M. Tech.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M. Tech.', 'M.E.', 'M.E.', 'M.E', 'M.E', 'M.E.', 'M.E.', 'M. Tech', 'M.E'],
    'University': ['Anna University', 'Bharath University', 'Bharath University', 'Anna University', 'B.S. Abdur Rahman University', 'SRM University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'Vel Tech Technical University', 'Anna University', 'Anna University', 'Anna University', 'SRM University', 'St Peters University', 'Anna University', 'BSAREC', 'Annamalai University'],
    'Year_of_attaining_higher_qualification': [2017, 2011, 2020, 2019, 2018, 2013, 2015, 2014, 2016, 2021, 2013, 2012, 2023, 2023, 2008, 2013, 2011, 2017, 2013, 2013],
    'Designation': ['Professor', 'Professor', 'Associate Professor', 'Assistant Professor', 'Associate Professor', 'Assistant professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor', 'Assistant Professor'],
    'Date_on_which_designated_as_Professor_Associate_Professor': ['N/A'] * 20, # Explicitly mark empty fields as N/A or similar
    'Date_of_joining_the_Institution': ['01-07-2021', '08-05-2023', '12-06-2023', '08-12-2021', '04-06-2007', '19-12-2018', '20-05-2020', '08-07-2022', '06-07-2022', '01-06-2023', '05-06-2023', '19-06-2023', '11-10-2023', '13-10-2023', '18-08-2007', '06-01-2017', '06-02-2020', '04-12-2017', '04-06-2018', '11-09-2013'],
    'Department': ['CSE'] * 20,
    'Specialization': ['Wireless sensor networks', 'Machine learning, Artificial Intelligence', 'Networks, Internet of things', 'Cloud Computing', 'Network Security', 'Artificial Intelligence', 'Artificial Intelligence and Big Data', 'Machine learning, Wireless networks', 'Machine learning, Artificial intelligence', 'Compiler networks, Cloud computing', 'Cyber security, block chain technology', 'Bio informatics, AR/VR', 'Wireless networks, AR/VR', 'Wireless networks, image processing', 'Cloud Computing, Big Data Analytics', 'Data Base Management System', 'Artificial Intelligence, Network security', 'Data Mining', 'Machine learning', 'Image Processing'],
    'Research_Paper_Publication': ['20', '4', '0', '4', '0', '12', '3', '4', '2', '1', '2', '0', '1', '1', '16', '4', '0', '1', '0', '0'],
    'PhD_Guidance': ['-'] * 20,
    'Faculty_Receiving_PhD_during_the_assessment_Years': ['-'] * 20,
    'Currently_Associated_Y_N': ['Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'No'],
    'Date_of_Leaving': ['N/A', 'N/A', 'N/A', '06-05-2023', '01-12-2021', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Transferred to IT 31.07.23', '26-07-2023', '06-06-2023', 'N/A', '13-05-2022', '10-05-2022'],
    'Nature_of_Association_Regular_Contract': ['Regular'] * 20
}
cse_df = pd.DataFrame(cse_data)

# IT Department Data
it_data = {
    'S_No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    'Name_of_the_Faculty_Member': ['Dr D. Venkata Subramaniam', 'Dr P. Balakumar', 'Dr P. Indira Priya', 'Dr S. Anbu', 'Dr G.Ayyappan', 'MS R.Kalpana', 'MS J. Jayashankari', 'MS M.R .Rajeswari', 'MS D.Deepa', 'MS A.Shantha kumari', 'MS M. Sumana', 'MS M. Sirija', 'MS B. Latha', 'MS S K. Velumathy Kalaivani', 'MS M. Divya bharathi', 'MS T. Vanaja', 'MS P. Allirani', 'MS R. Nishanthi', 'MS R. Reena', 'MS S. Ganga', 'MS K. Revathi', 'MR T. Vignesh'],
    'Degree_Highest_Degree': ['PDF', 'Ph.D.', 'Ph.D.', 'Ph.D.', 'Ph.D.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M. Tech.', 'M. Tech.', 'M.E.', 'M.E.', 'M.E.', 'M.E.', 'M.E', 'M.E.', 'M.E.', 'M.E.'],
    'University': ['B.S. Abdur Rahman Institute Of Science And Technology', 'Bharath University', 'Anna University', 'Bharath University', 'Bharath University', 'Sathyabama University', 'Annamalai University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'MGR University', 'SRM University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'Anna University', 'Sathyabama University', 'Anna University', 'Anna University'],
    'Year_of_attaining_higher_qualification': [2014, 2011, 2014, 2011, 2018, 2012, 2013, 2012, 2014, 2012, 2012, 2019, 2007, 2012, 2019, 2015, 2010, 2012, 2008, 2012, 2014, 2016],
    'Designation': ['Professor', 'Professor', 'Professor', 'Professor', 'Associate Professor', 'Assistant Professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor', 'Assistant professor'],
    'Date_of_joining_the_Institution': ['15.05.2023', '03.05.2023', '01.02.2022', '08.07.2019', '08.02.2021', '05.07.2007', '07.05.2009', '04.04.2012', '09.01.2014', '19.12.2018', '05.06.2019', '23.12.2019', '01.03.2021', '09.05.2022', '02.06.2022', '16.08.2022', '17.08.2022', '01.12.2022', '01.06.2023', '12.06.2023', '26-06-2023', '09.06.2023'],
    'Department': ['IT'] * 22,
    'Specialization': ['Deep Learning', 'Augmented Reality/Virtual Reality', 'Deep Learning', 'Data Structure', 'Robotics', 'Cloud computing Big data analytics', 'Artificial intelligence', 'Big data analytics', 'Cyber Security', 'Data mining', 'Data science', 'Big data Analytics', 'Cryptography and network security', 'Artificial Intelligence', 'Software Testing', 'Cloud computing', 'Cryptography and network security', 'Cyber Security', 'Cloud Computing and Big Data Analytics', 'Artificial Intelligence and Machine learning', 'Cryptography and network security', 'Networks'],
    'Research_Paper_Publication': ['1', '22', '18', '-', '4', '31', '19', '3', '-', '7', '-', '-', '2', '-', '-', '-', '-', '-', '4', '5', '-', '-'],
    'PhD_Guidance': ['N/A', 'N/A', 'N/A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    'Faculty_Receiving_PhD_during_the_assessment_Years': ['N/A', 'N/A', 'N/A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    'Currently_Associated_Y_N': ['Yes', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
    'Date_of_Leaving': ['N/A', 'N/A', '01.05.2023', '04-05-2022', '12.02.2023', '31-07-2023', 'N/A', '11-05-2022', '18-05-2022', 'N/A', '20-05-2022', '31-10-2023', 'N/A', '27-05-2023', '17-08-2023', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    'Nature_of_Association_Regular_Contract': ['Regular'] * 22
}
it_df = pd.DataFrame(it_data)

# Add the 'Currently_Teaching_Same_Specialization' column based on 'Currently_Associated_Y_N'
# If 'Currently_Associated_Y_N' is 'Yes', we'll assume they are potentially teaching their specialization.
cse_df['Currently_Teaching_Same_Specialization'] = cse_df['Currently_Associated_Y_N'].apply(lambda x: 'Yes' if x == 'Yes' else 'No')
it_df['Currently_Teaching_Same_Specialization'] = it_df['Currently_Associated_Y_N'].apply(lambda x: 'Yes' if x == 'Yes' else 'No')

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="SME Tech Guru", page_icon="💡")

# Initialize database and insert data if the DB file doesn't exist
# This prevents re-initializing the DB on every app refresh if it's already there
if not os.path.exists(DB_NAME):
    init_db()
    insert_data(cse_df, 'cse_faculty')
    insert_data(it_df, 'it_faculty')

# --- Branding ---
st.write("## Agile Assembly proudly presents:")
st.title("💡 SME Tech Guru 💡")
st.markdown("### *A Prince Campus Company*") # Motto

st.markdown("""
Welcome, students! This app helps you find the perfect faculty member for your research doubts and project assistance.
Simply enter a technology or research area you're interested in, and we'll show you the experts!
""")

st.markdown("---")

st.markdown('''these are the key word to use:
Deep Learning
Augmented Reality/Virtual Reality
Deep Learning
Data Structure
Robotics
Cloud computing Big data analytics
Artificial intelligence
Big data analytics
Cyber Security
Data mining
Data science
Big data Analytics
Cryptography and network security
Artificial Intelligence
Software Testing
Cloud computing
Cryptography and network security
Cyber Security
Cloud Computing and Big Data Analytics
Artificial Intelligence and Machine learning
Cryptography and network security
Networks
Wireless sensor networks
Machine learning, Artificial Intelligence
Networks, Internet of things
Cloud Computing
Network Security
Artificial Intelligence
Artificial Intelligence and Big Data
Machine learning, Wireless networks
Machine learning, Artificial intelligence
Compiler networks, Cloud computing
Cyber security, block chain technology
Bio informatics, AR/VR
Wireless networks, AR/VR
Wireless networks, image processing
Cloud Computing, Big Data Analytics
Data Base Management System
Artificial Intelligence, Network security
Data Mining
Machine learning
Image Processing''')
# User Input
search_query = st.text_input("Enter the Technology/Specialization (e.g., Machine Learning, Cybersecurity, Networks):", "").lower().strip()
filter_currently_teaching = st.checkbox("Show only faculty currently teaching in their specialization", value=True)

st.markdown("---")

def search_faculty(query, department_table_name, filter_teaching):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Using parameterized queries to prevent SQL injection
    sql_query = f"SELECT * FROM {department_table_name} WHERE LOWER(Specialization) LIKE ?"
    params = [f"%{query}%"]

    if filter_teaching:
        sql_query += " AND Currently_Teaching_Same_Specialization = 'Yes'"

    cursor.execute(sql_query, params)
    results = cursor.fetchall()
    conn.close()

    # Get column names for DataFrame
    column_names = [description[0] for description in cursor.description]
    return pd.DataFrame(results, columns=column_names)

if search_query:
    st.subheader(f"Faculty specializing in: **{search_query.title()}**")

    # Search in CSE Department
    cse_results_df = search_faculty(search_query, 'cse_faculty', filter_currently_teaching)
    if not cse_results_df.empty:
        st.markdown("### 💻 CSE Department Faculty")
        # Display relevant columns for students
        st.dataframe(cse_results_df[[
            'Name_of_the_Faculty_Member',
            'Designation',
            'Specialization',
            'Research_Paper_Publication',
            'PhD_Guidance',
            'Currently_Teaching_Same_Specialization'
        ]].set_index('Name_of_the_Faculty_Member'))
    else:
        st.info("No CSE faculty found for this specialization (or none currently teaching if filtered).")

    st.markdown("---")

    # Search in IT Department
    it_results_df = search_faculty(search_query, 'it_faculty', filter_currently_teaching)
    if not it_results_df.empty:
        st.markdown("### 🌐 IT Department Faculty")
        # Display relevant columns for students
        st.dataframe(it_results_df[[
            'Name_of_the_Faculty_Member',
            'Designation',
            'Specialization',
            'Research_Paper_Publication',
            'PhD_Guidance',
            'Currently_Teaching_Same_Specialization'
        ]].set_index('Name_of_the_Faculty_Member'))
    else:
        st.info("No IT faculty found for this specialization (or none currently teaching if filtered).")
else:
    st.info("Please enter a technology or specialization to find matching faculty.")

st.markdown("---")
st.markdown("Feel free to explore different specializations! ✨")
