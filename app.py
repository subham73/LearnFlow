import gradio as gr
from utils import driver, driver_resource

# -----------------------------
# Callback for initial suggestion
# -----------------------------
def on_submit(age, background, interest):
    # Get LLM-generated study plan, reason, and resources
    diagram, reason, outcome = driver(age, background, interest)

    return (
        gr.update(value=diagram, visible=True),      # studyflow_diagram
        gr.update(value=reason, visible=True),       # topic_reason
        gr.update(value=outcome, visible=True),      # topic_outcome
        gr.update(visible=False),                    # hide submit
        gr.update(visible=True),                     # show feedback section
        gr.update(visible=True),                     # show revised submission button
        gr.update(visible=True),                     # show original section
        gr.update(visible=False),                    # hide revised section
        gr.update(visible=True),                     # show resource button
    )

# -----------------------------
# Callback for revised suggestion based on feedback
# -----------------------------
def on_feedback(age, background, interest, userFeedback):
    # Optionally send feedback to model
    diagram, reason, outcome = driver(age, background, interest, userFeedback)

    return (
        gr.update(value=diagram, visible=True),      # revisedStudyflow_diagram
        gr.update(value=reason, visible=True),       # revisedTopic_reason
        gr.update(value=outcome, visible=True),      # revisedTopic_outcome
        gr.update(visible=False),                    # hide submitWithFeedback
        gr.update(visible=False),                    # hide original section
        gr.update(visible=True),                     # show revised section
    )

# -----------------------------
# Helpers for dummy resource button
# -----------------------------
# def getResouces():
#     return "Here are some resources to help you get started with your learning path."

def getResouces():
    resources, questions = driver_resource()
    return resources, questions

def on_Resource():
    resources, questions = driver_resource()
    return (
        resources,
        questions,
        gr.update(visible=True),    # Show resource section
        gr.update(visible=False),   # Hide resource button
        gr.update(visible=False),   # Hide feedback button
    )

# -----------------------------
# UI with Gradio Blocks
# -----------------------------
with gr.Blocks(css="""
    #scrollable-md {
        max-height: 350px;
        border: 1px solid #999;
        overflow-y: auto;
    }
    #original_section{
        background-color: transparent !important;           
    }
               
""") as demo:
    gr.Markdown("# 📚 LearnFlow")
    gr.Markdown("""🔹 **🗺️ Personalized Study Workflow**  🔹 **🧠 Meaningful Reasoning & Outcomes**  🔹 **📘 Beginner-Friendly Resources**  🔹 **❓ Grasp Check Questions** """)

    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group(elem_id="input-section", visible=True):
                age = gr.Number(label="👶 Your Age", value=18)
                background = gr.Textbox(label="🎓 Your Educational Background")
                interest = gr.Textbox(label="💡 Your Interests")

            submit = gr.Button("🚀 Suggest What to Learn", visible=True, elem_classes="gr-button")

            with gr.Group(elem_id="feedback-section", visible=False) as feedback_section:
                userFeedback = gr.Textbox(label="ℹ️ Help us know what you’re looking for")
                submitWithFeeback = gr.Button("🔂 Update the flow with feedback", elem_classes="gr-button")

            resource_button = gr.Button("📘 Click to get Resource", visible=False, elem_classes="gr-button")

        with gr.Column(scale=2):
            # REVISED Section (initially hidden)
            with gr.Group(visible=False) as revised_section:
                gr.Markdown("### 🔄 Revised Recommendation")
                with gr.Row():
                    revisedStudyflow_diagram = gr.Markdown(
                        value="<p>No recommendation yet.</p>",
                        label="🔗 The flow you are looking for",
                        elem_id="scrollable-md",
                        visible=False
                    )
                    with gr.Column():
                        revisedTopic_reason = gr.Textbox(label="🧐 Why this topic", lines=5, max_lines=5, visible=False)
                        revisedTopic_outcome = gr.Textbox(label="💪 Outcome of this topic", lines=5, max_lines=5, visible=False)

            # ORIGINAL Section (initially visible)
            with gr.Group(visible=True) as original_section:
                gr.Markdown("### 🔎 Recommendation")
                with gr.Row():
                    studyflow_diagram = gr.Markdown(
                        value="<p>No recommendation yet.</p>",
                        label="🔗 The flow you are looking for",
                        elem_id="scrollable-md",
                        visible=False
                    )
                    with gr.Column():
                        topic_reason = gr.Textbox(label="🧐 Why this topic", lines=5, max_lines=5, visible=False)
                        topic_outcome = gr.Textbox(label="💪 Outcome of this topic", lines=5, max_lines=5, visible=False)

            # RESOURCES Section (initially hidden)
            with gr.Group(elem_id="resource-section", visible=False) as resource_section:
                gr.Markdown("### 📘 Learning Resources")
                learningResource = gr.Textbox(label="Resources to help you get started")
                graspCheck = gr.Textbox(label="Grasp Check Questions")

    # ----------- Events ------------

    submit.click(
        fn=on_submit,
        inputs=[age, background, interest],
        outputs=[
            studyflow_diagram,
            topic_reason,
            topic_outcome,
            submit,
            feedback_section,
            submitWithFeeback,
            original_section,
            revised_section,
            resource_button,
        ],
        queue=True
    )

    submitWithFeeback.click(
        fn=on_feedback,
        inputs=[age, background, interest, userFeedback],
        outputs=[
            revisedStudyflow_diagram,
            revisedTopic_reason,
            revisedTopic_outcome,
            submitWithFeeback,
            original_section,
            revised_section,
        ],
        queue=True
    )

    resource_button.click(
        fn=on_Resource,
        inputs=[],
        outputs=[
            learningResource, 
            graspCheck, 
            resource_section, 
            resource_button, 
            submitWithFeeback
        ],
        queue=True
    )

# Launch the app
demo.launch()
