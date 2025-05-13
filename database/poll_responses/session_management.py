import streamlit as st
import uuid
from .poll_db import PollDatabase

def get_db():
    """Get a fresh database connection for the current thread."""
    return PollDatabase()

def initialize_session():
    """Initialize or retrieve a user session ID for tracking poll responses."""
    # Create a session state for storing the user ID
    if 'user_id' not in st.session_state:
        # Generate a new user ID if not already set
        st.session_state.user_id = str(uuid.uuid4())
    
    # Update the user's last seen timestamp
    db = get_db()
    db.add_or_update_user(st.session_state.user_id)
    
    return st.session_state.user_id

def save_poll_response(poll_id, page, response_data):
    """Save a poll response to the database with the current user ID."""
    # Ensure session is initialized
    if 'user_id' not in st.session_state:
        initialize_session()
    
    # Save the response to the database
    db = get_db()
    db.save_response(
        st.session_state.user_id,
        poll_id,
        page,
        response_data
    )
    
    # Also store in session state to show consistent values in UI
    if 'poll_responses' not in st.session_state:
        st.session_state.poll_responses = {}
    
    # Store response by poll_id for easy retrieval
    st.session_state.poll_responses[poll_id] = response_data
    
    return True

def get_user_responses():
    """Get all responses for the current user."""
    # Ensure session is initialized
    if 'user_id' not in st.session_state:
        initialize_session()
    
    db = get_db()
    return db.get_user_responses(st.session_state.user_id)

def get_response_for_poll(poll_id):
    """Get the user's response for a specific poll."""
    # Check if we have it in session state first (faster)
    if 'poll_responses' in st.session_state and poll_id in st.session_state.poll_responses:
        return st.session_state.poll_responses[poll_id]
    
    # Otherwise retrieve from database
    responses = get_user_responses()
    for response in responses:
        if response['poll_id'] == poll_id:
            # Store in session state for faster retrieval next time
            if 'poll_responses' not in st.session_state:
                st.session_state.poll_responses = {}
            st.session_state.poll_responses[poll_id] = response['response']
            return response['response']
    
    return None