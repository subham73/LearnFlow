import os
import json
from openai import OpenAI
from typing import List, Dict, Union
from pydantic import BaseModel, ValidationError

# === OpenAI Client Initialization ===
client = OpenAI(
    api_key=os.getenv("SAMBANOVA_KEY"),
    base_url="https://api.sambanova.ai/v1",
)
# === Sample Data for Testing ===
sample_studyflow = {'Machine Learning Fundamentals': ['Introduction to Machine Learning', 'Types of Machine Learning', 'Model Evaluation Metrics', 'Overfitting and Underfitting'], 'Deep Learning with Python': ['Introduction to Neural Networks', 'Convolutional Neural Networks (CNNs)', 'Recurrent Neural Networks (RNNs)', 'Transfer Learning'], 'Large Language Models': ['Introduction to Natural Language Processing (NLP)', 'Language Model Architectures', 'Transformers and Attention Mechanisms', 'Fine-Tuning Pre-Trained Models'], 'Pattern Recognition': ['Introduction to Pattern Recognition', 'Supervised and Unsupervised Learning', 'Clustering Algorithms', 'Dimensionality Reduction Techniques'], 'Model Deployment': ['Introduction to Model Deployment', 'Model Serving and Monitoring', 'Containerization with Docker', 'Cloud Deployment Options']}
sample_reason = "Given your background in computer science engineering and interests in machine learning, large language models, and pattern recognition, this plan dives into the fundamentals of machine learning and deep learning, with a focus on practical applications in Python."
sample_outcome = "After completing this plan, you will be able to design, train, and deploy machine learning models, including large language models, and apply pattern recognition techniques to real-world problems. You will also understand how to evaluate and fine-tune your models for optimal performance."
sample_resource = ['Machine Learning Crash Course - YouTube by Google Developers', 'Deep Learning with Python - Book by François Chollet', 'Natural Language Processing with Python - Book by Steven Bird, Ewan Klein, and Edward Loper']

_cached_data = {
    "reason": sample_reason,
    "expected_outcome": None,
    "resources": None
}
# === Connector to Frontend ===
def driver(age: int, background: str, interest: str, feedback: Union[str, None] = None):
    _, study_plan_response = get_learning_suggestion(client, age, background, interest, feedback)  
    
    # Save the response in the cache  
    _cached_data["reason"] = study_plan_response.reason
    _cached_data["expected_outcome"] = study_plan_response.expected_outcome
    _cached_data["resources"] = study_plan_response.resources

    study_workflow_diagram = get_studyflow_diagram(study_plan_response.study_workflow)
    # if feedback:
    #     feedback_interpretation = interpret_feedback(feedback)
    #     print(f"Feedback interpretation: {feedback_interpretation}")

    return study_workflow_diagram, study_plan_response.reason, study_plan_response.expected_outcome

def driver_resource():
    reason= _cached_data["reason"]
    expected_outcome = _cached_data["expected_outcome"]
    resources = _cached_data["resources"]

    questions = build_grasp_check(reason, expected_outcome, resources)

    # both are lists, so print it like they points and question 
    formated_resources = "\n".join([f"- {resource}" for resource in resources])
    formated_questions = "\n".join([f"{question}" for i, question in enumerate(questions)])
   
    return formated_resources, formated_questions

# === Pydantic Models for Structured Output ===
class StudyPlan(BaseModel):
    study_workflow: Dict[str, List[str]]
    reason: str
    expected_outcome: str
    resources: List[str]

class ClarificationRequest(BaseModel):
    follow_up_question: str

class GraspCheck(BaseModel):
    questions: List[str]

# === System Prompt ===
SYSTEM_PROMPT = """
You are a smart educational guide agent.
You help people figure out what to learn next based on their age, background, and interests.
Be adaptive: if input is too vague, ask for clarification. If it's clear, give them:
1. A study_workflow - a roadmap of topics and subtopics.
2. A reason why it's the right path for the user.
3. An expected outcome after finishing this learning path.
4. Beginner-friendly resources.
Use simple and clear language.
Always respond in strict JSON.
"""

# === User Prompt Generator ===
def build_user_prompt(age, background, interest, feedback=None):
    feedback_note = f"\n- Additional Feedback from User: {feedback}" if feedback else ""
    return f"""
    You are an expert curriculum advisor.

    ### User Profile
    - Age: {age}
    - Educational Background: {background}
    - Interests: {interest}{feedback_note}

    ### Your Task:
    Generate a structured learning plan in **strict JSON format only**, without any extra text or markdown.

    Your output must include:
    1. **study_workflow**: a Python-style dictionary (JSON-safe)  
    - Keys: main topics relevant to the user's profile  
    - Values: 2–5 subtopics per main topic, written as a list of strings ordered from beginner to advanced  

    2. **reason**: 3-4 clear sentence explaining "why" this path fits the user's background and interests. Avoid overly technical or overly vague language. Match the tone to their background. 
    3. **expected_outcome**: 3–4 sentences describing what the user will *be able to do* by the end. Be specific, realistic, and motivating. Avoid overly technical or overly vague language. Match the tone to their background. 
    4. **resources**: list of 3–4 beginner-friendly materials

    ### VERY IMPORTANT:
    - Talk directly to the user, not in third person.
    - Do NOT return more than 5 main topics
    - Do NOT return more than 5 subtopics per main topic
    - Do NOT return more than 3 resources
    - Do NOT include explanations outside the JSON
    - Do NOT use markdown code blocks like ```json
    - Only output valid JSON

    ### Output Example:
    {{
        "study_workflow": {{
        "Start with Python": ["Variables and Data Types", "Loops", "Functions", "Error Handling"],
        "Data Structures": ["Lists", "Dictionaries", "Tuples", "Sets"],
        "NumPy": ["Arrays", "Array Operations", "Broadcasting"],
        "Pandas": ["Series and DataFrames", "Filtering and Sorting", "Basic Data Cleaning"],
        "Matplotlib": ["Line Charts", "Bar Charts", "Histograms"]
        }},
        "reason": "Since you are new to programming and interested in data-related topics, this plan starts with Python basics and gradually introduces tools used in real data analysis projects.",
        "expected_outcome": "After completing this plan, you will understand the fundamentals of Python and be able to explore and analyze real-world datasets using tools like Pandas and Matplotlib. You wil be able to write small scripts to automate tasks, clean data, and create visual summaries.",
        "resources": [
            "Python for Beginners - YouTube by freeCodeCamp",
            "CS50’s Introduction to Computer Science",
            "Kaggle: Python Course"
        ]
    }}

    ### If the user profile is too vague to proceed:
    Return this JSON instead:
    {{
    "follow_up_question": "Ask a specific question to clarify what the user needs"
    }}
    """

# === GPT Driver ===
def get_learning_suggestion(client, age, background, interest, feedback=None):
    user_prompt = build_user_prompt(age, background, interest, feedback)

    try:
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-405B-Instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        raw_response = completion.choices[0].message.content.strip()
        print("🔍 Raw LLM Response:", raw_response)

        # Validate against expected schemas
        try:
            response_json = json.loads(raw_response)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON from model")

        if "follow_up_question" in response_json:
            follow_up = ClarificationRequest(**response_json)
            return "clarify", follow_up.follow_up_question

        study_plan = StudyPlan(**response_json)
        return "complete", study_plan

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return "error", str(e)

# === Feedback Interpreter Layer ===
def interpret_feedback(feedback_text):
    """ You can use a small model or rule-based classifier to tag feedback. """
    keywords = {
        "too advanced": "make it easier",
        "too basic": "increase complexity",
        "add resources": "expand resources",
        "missing outcome": "add outcome"
    }
    interpreted = [keywords[k] for k in keywords if k in feedback_text.lower()]
    return ", ".join(interpreted) if interpreted else feedback_text

def build_grasp_check(reason: str, outcome: str, resources: List[str]) -> List[str]:
    """
    Make an LLM request to generate 5–10 comprehension-check questions
    based on the user's reason, desired outcome, and resources.
    """
    # Create a prompt that instructs the model to write 5–10 questions.
    prompt = f"""
    You are a helpful AI tutor. The user is learning because:
    {reason}

    Their desired outcome is:
    {outcome}

    They have these resources:
    {resources}

    Please generate 5 to 10 short questions that the user could answer
    after studying these materials, to check their overal understanding.
    Return only the list of questions.

    """

    # Make your LLM (OpenAI, SambaNova, etc.) request here:
    # (Change this to your actual function call and model parameters.)
    completion = client.chat.completions.create(
        model="Meta-Llama-3.1-405B-Instruct",
        messages=[
            {"role": "system", "content": "You are a question setter whoes objective is to test learners overall understanding of the topic, not specifics "},
            {"role": "user", "content": prompt},
        ],

    )

    # Get the raw text from the response
    response = completion.choices[0].message.content.strip()
    print("🔍 Grasp Check Questions:", response)  # Debug print

    try:
        # If the LLM returned JSON: parse it
        # e.g. questions_list = json.loads(response_text)
        # Or if it returned newline-separated text:
        questions_list = [line.strip("- ").strip() for line in response.splitlines() if line.strip()]

        # Validate with Pydantic
        validated = GraspCheck(questions=questions_list)
        return validated.questions

    except (ValidationError, json.JSONDecodeError) as e:
        print("Error parsing or validating questions:", e)
        return []

# === Studyflow Preparation ===
def convert_studyflow_to_mermaid_text(studyflow):
  """
  Convert a structured learning workflow dictionary to step titles and details for 
  Mermaid diagram generation.
  """
  step_titles = []
  step_details = []

  for topic, subtopics in studyflow.items():
      step_titles.append(topic)
      step_details.append(", ".join(subtopics))

  step_titles = ", ".join(step_titles)
  step_details = " | ".join(step_details)

  # return ", ".join(step_titles), " | ".join(step_details)
  print(step_titles, step_details)
  return step_titles, step_details


def get_studyflow_diagram(studyflow):
  """
  Expected inputs:
  - step_titles: A comma-separated string (e.g., "Learn Python, Learn NumPy, Learn Pandas")
  - step_details: A string with each step's details separated by |,
    and details for a specific step separated by commas.
    (e.g., "Variables, Loops, Functions | Arrays, Vector Math | DataFrames, Analysis")
  """
  step_titles, step_details = convert_studyflow_to_mermaid_text(studyflow)
  # Process input strings into lists.
  titles = [title.strip() for title in step_titles.split(",")]
  details_list = [details.strip() for details in step_details.split("|")]
  
  # Define a list of colors to be used for the nodes.
  # You can add as many colors as you like.
  colors = ["#f9c74f", "#90be6d", "#f9844a", "#577590", "#277da1", "#ff595e", "#ffd166"]
  
  mermaid_code = "graph TD;\n"
  previous_step = None

  for i, title in enumerate(titles):
      if i >= len(details_list):
          break
      
      # Split the details for the current step and strip each one.
      details = [detail.strip() for detail in details_list[i].split(",")]
      # Create bullet points using HTML line breaks.
      bullet_points = "<br/>".join([f"• {detail}" for detail in details])
      # Combine title and bullet points in one node.
      node_text = f"<b><u>{title}</u></b><br/>{bullet_points}"
      main_node = f"A{i}[\"{node_text}\"]"
      mermaid_code += f"    {main_node}\n"
      
      # Apply a custom color for this node.
      # Using modulo (%) ensures that if there are more nodes than colors,
      # the list will cycle through.
      color = colors[i % len(colors)]
      mermaid_code += f"    style A{i} fill:{color},stroke:#333,stroke-width:1.5px;\n"
      
      # Link this main node with the previous one to create a sequential flow.
      if previous_step:
          mermaid_code += f"    {previous_step} --> A{i}\n"
      previous_step = f"A{i}"
  
  return f"```mermaid\n{mermaid_code}\n```"