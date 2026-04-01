from groq import Groq


def evaluate_answer(client_key, question, answer, role):
    """
    Provides a deep-dive critique of the candidate's response.
    """
    client = Groq(api_key=client_key)

    prompt = f"""
    You are an Elite Technical Interviewer. Evaluate the candidate's response for a {role} role.

    Question: {question}
    Answer: {answer}

    Provide your evaluation in strict Markdown with these sections:
    ### 🎯 Technical Score: [X/10]

    ### 📝 Content Analysis
    Check for technical accuracy, use of keywords, and logical flow.

    ### 🗣️ Communication Feedback
    Analyze clarity and professional tone.

    ### 💡 Areas of Improvement
    Identify missing concepts or weak points.

    ### 🌟 Model Answer
    Provide a concise example of a high-quality response.
    """

    try:
        # Pehle ye tha: model="llama3-70b-8192"
        # Ab ye dalo:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Latest and Fast
            messages=[{"role": "system", "content": "You are a professional career coach."},
                      {"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Critique currently unavailable: {str(e)}"