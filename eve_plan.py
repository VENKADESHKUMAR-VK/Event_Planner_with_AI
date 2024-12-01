import streamlit as st
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCmMnH1xctvxZ9h6AUeaQJDd0-1tg3VbDg")

# Function to generate suggestions
def generate_suggestions(event_type, audience_size, budget, location, special_requests):
    try:
        prompt = (
            f"You are an event planning assistant. Help me plan an event with the following details:\n"
            f"Event type: {event_type}\n"
            f"Audience size: {audience_size}\n"
            f"Budget: {budget}\n"
            f"Location: {location}\n"
            f"Special requests: {special_requests}\n"
            f"Please provide venue suggestions, catering ideas, activities, and a schedule for the event."
        )
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            generated_text = candidate.content.parts[0].text
            return generated_text
        else:
            return "No suggestions generated. Check the API response for more details."
    except Exception as e:
        return f"Error generating suggestions: {e}"

# Streamlit UI
def main():
    # Apply custom CSS
    st.markdown("""
        <style>
        body {
            background-color: #f5f5f5;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add a header banner
    st.markdown("<div class='header'><h1>🎉 Event Planner Assistant</h1></div>", unsafe_allow_html=True)
    st.write("Plan your event effortlessly with AI-powered suggestions!")

    # Structured input layout
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            event_type = st.text_input("📝 Event Type", placeholder="e.g., Birthday Party, Wedding")
            location = st.text_input("📍 Location", placeholder="e.g., Chennai, New York")

        with col2:
            audience_size = st.number_input("👥 Audience Size", min_value=1, step=1, value=50)
            budget = st.text_input("💰 Budget", placeholder="e.g., $5000, ₹200000")

        special_requests = st.text_area("🛠 Special Requests", placeholder="e.g., Vegetarian catering, Outdoor seating")

    # Generate button
    if st.button("🚀 Generate Suggestions"):
        if event_type and budget and location:
            with st.spinner("Generating suggestions..."):
                suggestions = generate_suggestions(event_type, audience_size, budget, location, special_requests)
            st.success("✨ Here are the suggestions for your event:")
            st.write(suggestions)
        else:
            st.error("⚠️ Please fill in all required fields (Event Type, Budget, Location).")

# Run the app
if __name__ == "__main__":
    main()
