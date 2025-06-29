import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini

# Page Config
st.set_page_config(
    page_title="SWASTH — Your AI Wellness Partner 💪",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #0077cc;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #005fa3;
        color: white;
    }
    .success-box, .warning-box {
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    .success-box {
        background-color: #e6fffa;
        border: 1px solid #81e6d9;
    }
    .warning-box {
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🎯 Why this plan works")
            st.info(plan_content.get("why_this_plan_works", "Information not available"))
            st.markdown("### 🍽️ Meal Plan")
            st.write(plan_content.get("meal_plan", "Plan not available"))
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🎯 Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.write(plan_content.get("routine", "Routine not available"))
        with col2:
            st.markdown("### 💡 Pro Tips")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)

def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    st.markdown("""
        <h1 style='font-family: "Segoe UI", sans-serif; font-size: 2.5rem; color: #0077cc;'>
        🏋️‍♂️ SWASTH 💪 — Your AI Wellness Partner
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: 
        <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: black;'>
        Get personalized dietary and fitness plans tailored to your goals and preferences.<br>
        Powered by Gemini AI and built with 💕 by Devansh Sengar.
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("🔑 Gemini API Setup Instructions")
        st.subheader("Steps: Get Your API Key")
        st.markdown("""
        - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        - Sign in with your Google account
        - Click "Create API Key"
        - Copy the key and paste it below
        """, unsafe_allow_html=True)

        gemini_api_key = st.text_input("🔐 Paste your Gemini API Key below", type="password")

        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API Key to proceed")
        else:
            st.success("✅ API key accepted!")

        # Always show GitHub credit at the bottom
        st.markdown("---")
        st.markdown("""
            <div style='font-size: 0.85rem; color: gray;'>
                🔗 <a href="https://github.com/devanshsengar04" target="_blank" style="text-decoration: none; color: gray;">
                GitHub: @devanshsengar04
                </a><br>
                © 2025 <strong>Swasth</strong> by Devansh Sengar
            </div>
        """, unsafe_allow_html=True)

        if not gemini_api_key:
            return

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-2.5-flash-preview-05-20", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

        st.header("👤 Your Health Profile")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
            dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            fitness_goals = st.selectbox("Fitness Goals", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"])

        if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
            with st.spinner("Creating your perfect health and fitness routine..."):
                try:
                    dietary_agent = Agent(
                        name="Dietary Expert",
                        role="Provides personalized dietary recommendations",
                        model=gemini_model,
                        instructions=[
                            "Consider the user's input, including dietary restrictions and preferences.",
                            "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                            "Provide a brief explanation of why the plan is suited to the user's goals.",
                            "Focus on clarity, coherence, and quality of the recommendations.",
                        ]
                    )

                    fitness_agent = Agent(
                        name="Fitness Expert",
                        role="Provides personalized fitness recommendations",
                        model=gemini_model,
                        instructions=[
                            "Provide exercises tailored to the user's goals.",
                            "Include warm-up, main workout, and cool-down exercises.",
                            "Explain the benefits of each recommended exercise.",
                            "Ensure the plan is actionable and detailed.",
                        ]
                    )

                    user_profile = f"""
                    Age: {age}
                    Weight: {weight}kg
                    Height: {height}cm
                    Sex: {sex}
                    Activity Level: {activity_level}
                    Dietary Preferences: {dietary_preferences}
                    Fitness Goals: {fitness_goals}
                    """

                    dietary_plan_response = dietary_agent.run(user_profile)
                    dietary_plan = {
                        "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hydration: Drink plenty of water throughout the day
                        - Electrolytes: Monitor sodium, potassium, and magnesium levels
                        - Fiber: Ensure adequate intake through vegetables and fruits
                        - Listen to your body: Adjust portion sizes as needed
                        """
                    }

                    fitness_plan_response = fitness_agent.run(user_profile)
                    fitness_plan = {
                        "goals": "Build strength, improve endurance, and maintain overall fitness",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Track your progress regularly
                        - Allow proper rest between workouts
                        - Focus on proper form
                        - Stay consistent with your routine
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []

                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

        if st.session_state.plans_generated:
            st.header("❓ Ask a Question About Your Plan")
            question_input = st.text_input("Type your question here")

            if st.button("Get Answer"):
                if question_input:
                    with st.spinner("Getting insights..."):
                        dietary_plan = st.session_state.dietary_plan
                        fitness_plan = st.session_state.fitness_plan

                        context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                        full_context = f"{context}\nUser Question: {question_input}"

                        try:
                            agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                            run_response = agent.run(full_context)

                            answer = run_response.content if hasattr(run_response, 'content') else "Sorry, I couldn't generate a response."
                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(f"❌ An error occurred while getting the answer: {e}")

            if st.session_state.qa_pairs:
                st.header("💬 Q&A History")
                for question, answer in st.session_state.qa_pairs:
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {answer}")

if __name__ == "__main__":
    main()
