import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)


# -----------------------------
# GROQ CLIENT
# -----------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("✉️ AI Email Generator")
st.write(
    "Generate professional emails in seconds using AI."
)


# -----------------------------
# INPUTS
# -----------------------------

email_type = st.selectbox(
    "Email Type",
    [
        "Job Application",
        "Follow-up",
        "Leave Request",
        "Professional Inquiry",
        "Complaint",
        "Thank You",
        "Cold Email",
        "Custom"
    ]
)


recipient = st.text_input(
    "Recipient",
    placeholder="e.g. Hiring Manager"
)


purpose = st.text_area(
    "What is the purpose of the email?",
    placeholder="Describe what you want to communicate..."
)


key_points = st.text_area(
    "Key Points",
    placeholder="Enter important points you want included..."
)


tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Formal",
        "Friendly",
        "Persuasive",
        "Concise"
    ]
)


length = st.selectbox(
    "Email Length",
    [
        "Short",
        "Medium",
        "Detailed"
    ]
)


# -----------------------------
# GENERATE EMAIL
# -----------------------------

if st.button("✨ Generate Email", use_container_width=True):

    if not purpose.strip():
        st.warning("Please enter the purpose of the email.")
    else:

        prompt = f"""
You are an expert professional email writer.

Generate a high-quality email using the information below.

Email Type:
{email_type}

Recipient:
{recipient}

Purpose:
{purpose}

Key Points:
{key_points}

Tone:
{tone}

Length:
{length}

Requirements:
1. Generate a suitable subject line.
2. Write a professional and natural email.
3. Do not invent information or experience.
4. Keep the email relevant to the purpose.
5. Avoid unnecessary filler.
6. Use appropriate greeting and closing.
7. Return the response in this format:

Subject: [subject]

[Email body]
"""

        with st.spinner("Generating your email..."):

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            """You are an expert professional email writer. Generate a high-quality email based on the following information.

Email Type:
Job Application

Recipient:
Hiring Manager

Purpose:
Apply for a Software QA Engineer position.

Key Points:
I have experience in manual testing, test cases,
bug reporting and API testing.

Tone:
Professional

Length:
Medium

Requirements:
1. Generate a suitable subject line.
2. Write a professional email.
3. Do not invent experience.
4. Keep the language natural.
5. Avoid unnecessary filler.
6. Do not use placeholders unless required.
7. Return the subject and email body clearly."""
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
            )

        email = response.choices[0].message.content

        st.subheader("Generated Email")

        st.text_area(
            "Your Email",
            email,
            height=400
        )
