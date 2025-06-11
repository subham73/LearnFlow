<!-- ---
title: LearnFlow
emoji: 📚
colorFrom: red
colorTo: red
sdk: gradio
sdk_version: 5.33.1
app_file: app.py
pinned: true
license: mit
short_description: Imagine having a smart educational guide right at your side.
tags: [agent-demo-track]
--- -->

![LearnFlow Banner](assets\Slide2.JPG)
## 🎥 [Watch the LearnFlow Usecase Video](https://youtu.be/2UTir0MX0kU)

# 📑 LearnFlow Agent

### Your Smart Educational Guide for Personalized Learning Paths 🧠📚
## 🎯 What is LearnFlow Agent?

**LearnFlow Agent** is an intelligent, conversational tool that helps you figure out *what to learn next* — tailored precisely to your **age**, **background**, and **interests**.
Powered by advanced language models and a sleek Gradio interface, it delivers a **personalized study roadmap**, helpful explanations, beginner resources, and even custom questions to test your understanding.

## 🚀 Key Objectives

LearnFlow Agent is built to **empower learners** by:

* 🎓 **Creating Personalized Learning Plans**
  Customized to match your educational background and interests.
* 🧭 **Clarifying Why It Matters**
  Get a clear reason behind every suggested topic and how it helps *you*.
* 📚 **Recommending Actionable Resources**
  Handpicked beginner-friendly content like courses, videos, and books.
* 🧩 **Ensuring You Understand**
  Test yourself with grasp-check questions based on your learning path.

## 🔑 What You Get
### 🗺️ **Personalized Study Workflow**
Generates a structured roadmap (`study_workflow`) with 3–5 main topics and their subtopics, progressing from beginner ➝ advanced.
### 🧠 **Meaningful Reasoning + Outcomes**
Clearly explains:
* Why this learning path fits *you*
* What you’ll be able to do after completing it
### 📘 **Beginner-Friendly Resources**
Includes 2–3 handpicked materials (YouTube, MOOCs, docs) to help you get started confidently.
### ❓ **Grasp Check Questions**
Provides 5–10 custom questions to assess your comprehension along the way.
### 📊 **Visual Mermaid Diagram**
Automatically turns your learning roadmap into an interactive diagram for visual learners.

## 🔌 Integrations & Stack

| Component                  | Description                                                             |
| -------------------------- | ----------------------------------------------------------------------- |
| 🧠 **Language Model**      | Uses models like `Meta-Llama-3.1-405B-Instruct` to generate responses   |
| 🧱 **Pydantic Validation** | Enforces JSON structure for consistency using `StudyPlan`, `GraspCheck` |
| 💡 **Gradio Interface**    | Simple, modern UI for input/output, diagrams, and feedback              |
| 📈 **MermaidJS**           | Converts study workflows into clear visual diagrams                     |

## 🔁 How It Works

### 1️⃣ User Input
You enter your **age**, **background**, and **interests** via a friendly Gradio form.

### 2️⃣ Study Plan Generation
A powerful LLM processes your input and returns:
* A detailed **study\_workflow**
* A tailored **reason** and **expected outcome**
* Curated **resources**

### 3️⃣ Visual Diagram
The study plan is rendered as a clean **Mermaid diagram** to help you visualize your learning journey.

### 4️⃣ Feedback Loop
Want changes? Provide feedback and get an updated plan instantly.

### 5️⃣ Resources & Comprehension
Alongside your study path, receive:

* 📚 Beginner resources
* ❓ Smart grasp-check questions to reinforce your learning

## 💡 Example Outputs
* 📖 **Study Workflow:** `"Python Basics ➝ NumPy ➝ Pandas ➝ Visualization"`
* 💬 **Reason:** “This path introduces you to practical tools for data analysis using your interest in numbers.”
* 🎯 **Outcome:** “By the end, you'll be able to clean, analyze, and visualize real datasets using Python.”
* 📘 **Resources:** CS50, freeCodeCamp, Kaggle
* ✅ **Questions:** What is a DataFrame? What does `axis=1` mean in Pandas?

## 👤 Who Is This For?
Whether you're:

* A **student** exploring tech,
* A **career switcher** entering data or programming,
* A **hobbyist** wanting structure in your learning journey…

**LearnFlow Agent** is here to guide you with confidence and clarity. 🌟

## 🧪 Future Features (Coming Soon!)
* 🌍 Multi-language support
* 🧑‍🏫 Tutor Mode with progress tracking
* 🔗 Resource bookmark sync
* 🧠 AI-powered concept explanation on hover

## 🛠️ Tech Stack
* `Python` + `Gradio` + `Pydantic`
* `OpenAI` + `SambaNova`
* `MermaidJS` for diagrams
## 📎 License
MIT License
## 🙌 Contribute
Have ideas? Found a bug? PRs and feedback are welcome. Let's build better learning tools together. 🤝


