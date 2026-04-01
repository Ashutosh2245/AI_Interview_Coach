import random
import logging
from groq import Groq

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.fallback_questions = {
            "software engineer": [
                "How do you handle technical debt in a fast-paced environment?",
                "Explain the difference between microservices and monolithic architecture.",
                "How do you ensure your code is scalable and maintainable?",
                "Describe a time you had to debug a critical production issue.",
                "What is your approach to writing unit tests?"
            ],
            "data science": [
                "How do you deal with imbalanced datasets in classification?",
                "Explain the bias-variance tradeoff in detail.",
                "What is the significance of p-values in hypothesis testing?",
                "How do you choose between a Random Forest and an XGBoost model?",
                "Describe a data project where you had to perform extensive feature engineering."
            ]
        }

    def generate(self, role, resume_text=""):
        logger.info(f"Generating questions for role: {role}")
        role_lower = role.lower()

        try:
            prompt = f"""
            You are a Senior Technical Recruiter at a Top Tech Firm.
            Generate 5 sophisticated, non-generic interview questions for a {role} position.

            Candidate Resume Context:
            {resume_text[:2000]}

            Constraints:
            1. Mix technical depth with behavioral scenarios.
            2. Do not number the questions.
            3. Separate each question with a pipe symbol '|'.
            4. Focus on specific skills mentioned in the resume if available.
            """

            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "system", "content": "You are a professional interviewer."},
                          {"role": "user", "content": prompt}],
                temperature=0.7
            )

            raw_content = response.choices[0].message.content
            questions = [q.strip() for q in raw_content.split('|') if len(q) > 15]

            if len(questions) < 5:
                raise ValueError("Insufficient questions generated")

            return questions[:5]

        except Exception as e:
            logger.error(f"AI Question Generation failed: {e}")
            # Intelligent fallback based on keywords
            for key in self.fallback_questions:
                if key in role_lower:
                    return random.sample(self.fallback_questions[key], 5)

            return random.sample(self.fallback_questions["software engineer"], 5)


def get_questions(role, resume_text="", client_key=""):
    gen = QuestionGenerator(client_key)
    return gen.generate(role, resume_text)