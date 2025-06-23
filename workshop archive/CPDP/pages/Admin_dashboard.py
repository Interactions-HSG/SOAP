import streamlit as st
import pandas as pd
import sqlite3
import os
import json
import plotly.express as px
from database.poll_responses.poll_db import PollDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

# Admin authentication
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Use a default password if no secrets file is found or env variable is not set
        default_password = "workshop2025"  # Fallback if not in secrets or .env
        
        # Try to get password from Streamlit secrets first
        admin_password_env = os.getenv("ADMIN_PASSWORD")
        
        try:
            # Prefer Streamlit secrets if available (for deployed apps)
            correct_password = st.secrets.get("admin_password", admin_password_env or default_password)
        except FileNotFoundError:
            # No secrets file found, use environment variable or default
            correct_password = admin_password_env or default_password
            
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store the password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is not True

# Initialize database connection
@st.cache_resource
def get_db():
    return PollDatabase()

db = get_db()

# Main dashboard
st.title("Workshop Admin Dashboard")
st.write("View all participant responses and engagement data")

# Metrics overview
st.header("Participation Metrics")

# Get all unique users
conn = sqlite3.connect(db.db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT COUNT(DISTINCT user_id) as unique_users FROM users")
unique_users = cursor.fetchone()['unique_users']

cursor.execute("SELECT COUNT(*) as total_responses FROM poll_responses")
total_responses = cursor.fetchone()['total_responses']

cursor.execute("""
    SELECT COUNT(DISTINCT poll_id) as unique_polls 
    FROM poll_responses
""")
unique_polls = cursor.fetchone()['unique_polls']

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Unique Participants", unique_users)
with col2:
    st.metric("Total Responses", total_responses)
with col3:
    st.metric("Unique Polls", unique_polls)

# Poll response analysis
st.header("Poll Response Analysis")

# Get all poll IDs and page names
cursor.execute("""
    SELECT DISTINCT poll_id, page
    FROM poll_responses
    ORDER BY page, poll_id
""")
polls = cursor.fetchall()

# Convert to list of tuples for the selectbox
poll_options = [(row['poll_id'], f"{row['page']} - {row['poll_id']}") for row in polls]

# Display selector for poll
if poll_options:
    selected_poll_tuple = st.selectbox(
        "Select a poll to analyze:",
        options=poll_options,
        format_func=lambda x: x[1]
    )

    if selected_poll_tuple:
        selected_poll = selected_poll_tuple[0]
        
        # Get responses for selected poll
        cursor.execute("""
            SELECT p.*, u.first_seen, u.last_seen
            FROM poll_responses p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.poll_id = ?
            ORDER BY p.timestamp
        """, (selected_poll,))
        
        responses = [dict(row) for row in cursor.fetchall()]
        
        # Display information about the poll
        st.subheader(f"Poll: {selected_poll}")
        st.write(f"Page: {responses[0]['page'] if responses else 'Unknown'}")
        st.write(f"Total responses: {len(responses)}")
        
        # Try to determine if responses are numeric, text, or structured
        if responses:
            try:
                # Try parsing as JSON first
                sample_response = json.loads(responses[0]['response']) if isinstance(responses[0]['response'], str) else responses[0]['response']
                
                if isinstance(sample_response, dict):
                    st.write("Response type: Structured (JSON)")
                    
                    # For structured responses, create a dataframe with all fields flattened
                    df_rows = []
                    for resp in responses:
                        row = {'user_id': resp['user_id'], 'timestamp': resp['timestamp']}
                        response_data = json.loads(resp['response']) if isinstance(resp['response'], str) else resp['response']
                        row.update(response_data)
                        df_rows.append(row)
                    
                    df = pd.DataFrame(df_rows)
                    st.dataframe(df)
                    
                    # Try to create visualizations for numeric fields
                    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
                    if numeric_cols:
                        st.subheader("Visualizations")
                        
                        for col in numeric_cols:
                            if col not in ['user_id', 'timestamp']:
                                fig = px.histogram(df, x=col, title=f"Distribution of {col}")
                                st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    # Simple response type (string, number)
                    df = pd.DataFrame([
                        {
                            'user_id': r['user_id'],
                            'response': json.loads(r['response']) if isinstance(r['response'], str) else r['response'],
                            'timestamp': r['timestamp']
                        } 
                        for r in responses
                    ])
                    
                    # Display as table
                    st.dataframe(df)
                    
                    # If all responses are numeric, show histogram
                    if df['response'].apply(lambda x: isinstance(x, (int, float))).all():
                        st.write("Response type: Numeric")
                        fig = px.histogram(df, x='response', title="Response Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("Response type: Text")
            
            except (json.JSONDecodeError, TypeError, ValueError):
                # Simple text responses
                st.write("Response type: Text")
                # Show raw responses
                for i, resp in enumerate(responses):
                    with st.expander(f"Response {i+1} - {resp['timestamp']}"):
                        st.write(resp['response'])
else:
    st.info("No poll responses found in the database yet.")

# User engagement analysis
st.header("User Engagement Analysis")

# Get all users with their first and last seen times
cursor.execute("""
    SELECT u.user_id, u.first_seen, u.last_seen, COUNT(p.response_id) as response_count
    FROM users u
    LEFT JOIN poll_responses p ON u.user_id = p.user_id
    GROUP BY u.user_id
    ORDER BY response_count DESC
""")
users = [dict(row) for row in cursor.fetchall()]

# Create dataframe for users
user_df = pd.DataFrame(users)
if not user_df.empty:
    # Format timestamps
    user_df['first_seen'] = pd.to_datetime(user_df['first_seen'])
    user_df['last_seen'] = pd.to_datetime(user_df['last_seen'])
    user_df['session_duration'] = (user_df['last_seen'] - user_df['first_seen']).dt.total_seconds() / 60  # in minutes
    
    # Display user data
    st.dataframe(user_df)
    
    # Visualize response count distribution
    fig = px.histogram(
        user_df, 
        x="response_count", 
        title="Distribution of Responses per User"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualize session duration
    fig = px.histogram(
        user_df, 
        x="session_duration", 
        title="Distribution of Session Duration (minutes)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No user data found in the database yet.")

# Export data
st.header("Export Data")
export_format = st.radio("Select export format:", ["CSV", "JSON"])

if st.button("Export All Poll Data"):
    # Get all poll responses
    cursor.execute("""
        SELECT p.*, u.first_seen, u.last_seen
        FROM poll_responses p
        JOIN users u ON p.user_id = u.user_id
        ORDER BY p.timestamp
    """)
    all_responses = [dict(row) for row in cursor.fetchall()]
    
    if all_responses:
        if export_format == "CSV":
            # For CSV, we need to flatten JSON responses
            df_rows = []
            for resp in all_responses:
                row = {
                    'user_id': resp['user_id'],
                    'poll_id': resp['poll_id'],
                    'page': resp['page'],
                    'timestamp': resp['timestamp'],
                    'response': resp['response'],
                    'first_seen': resp['first_seen'],
                    'last_seen': resp['last_seen']
                }
                df_rows.append(row)
                
            df = pd.DataFrame(df_rows)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="workshop_poll_data.csv",
                mime="text/csv"
            )
        else:  # JSON
            # Convert to JSON
            json_str = json.dumps(all_responses, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="workshop_poll_data.json",
                mime="application/json"
            )
    else:
        st.warning("No data available to export yet.")

# Close connection
conn.close()