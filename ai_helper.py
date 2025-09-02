import ollama
import json

# ==============================
# AI Helper Function (Ollama)
# ==============================
def get_ai_answer(question, profile):
    """
    AI-based short answers for job forms.
    - Always answer briefly (one word or number).
    - Never say 'I don't know', 'N/A', or 'I have not worked'.
    - For tech stack: always say 'Yes' if mentioned in profile, otherwise still say 'Yes'.
    - Never say 0 for years of experience always get from profile, otherwise say 1.
    - For relocation: always 'Yes'.
    """

    try:
        rules = (
            "Answer briefly in one word or a number. "
            "Never say 'I don't know', 'N/A', or 'I have not worked'. "
            "If asked about skills, always answer 'Yes'. "
            "If asked about relocation, always answer 'Yes'. "
            "If asked about years of experience, infer from profile. "
            "If the question is about rating yourself in skills/experience, always answer with the highest range (8-10, Expert, Advanced). "
            "Never choose 'Beginner' or 'No Experience'. "
            "Never give 0 or 0 years in experience instead say 1."
            "If the question is vague or unclear, pick 'Intermediate' or 'Advanced'. "
            "Output only the direct answer, nothing else."
        )

        response = ollama.chat(model="llama3", messages=[
            {"role": "system", "content": f"You are filling job forms. Profile: {json.dumps(profile)}"},
            {"role": "system", "content": rules},
            {"role": "user", "content": question}
        ])

        return response["message"]["content"].strip()

    except Exception as e:
        print("AI Error:", e)
        return "Yes"

