
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv


from career_guidance_system import CareerGuidanceSystem
from career_chatbot import display_chat_interface

# Load environment variables from the .env file
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Siet Career Guider",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #4285F4;}
    .sub-header {font-size: 1.2rem; margin-bottom: 2rem; color: #9E9E9E;}
    .stApp {background-color: #121212; color: #E0E0E0;}
    [data-testid="stSidebar"] {background-color: #1E1E1E; border-right: 1px solid #333;}
    h1, h2, h3, h4, h5, h6 {color: #90CAF9 !important;}
    .stButton > button {background-color: #303F9F; color: white; border: none; font-weight: bold;}
    .stButton > button:hover {background-color: #5C6BC0;}
    .career-section {background-color: #1A237E; color: white; border-radius: 8px; padding: 20px; margin-bottom: 20px;}
    .market-section {background-color: #0D47A1; color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;}
    .roadmap-section {background-color: #1B5E20; color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;}
    .insights-section {background-color: #4A148C; color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# Initialize csiet career guider from environment variables
if "career_system" not in st.session_state:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    google_serper_api_key = os.environ.get("GOOGLE_SERPER_API_KEY")
    if google_api_key:
        st.session_state.career_system = CareerGuidanceSystem(
            google_api_key=google_api_key, 
            google_serper_api_key=google_serper_api_key
        )
    else:
        st.session_state.career_system = None

# Initialize other session state variables
if "selected_career" not in st.session_state:
    st.session_state.selected_career = None
if "selected_category" not in st.session_state:  
    st.session_state.selected_category = None  
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "career_analysis" not in st.session_state:
    st.session_state.career_analysis = None
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.markdown("<div class='main-header'>🚀 AI-Powered SIET Career Guider</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Explore career options, analyze job markets, and create personalized learning paths with AI</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Configuration")
    if st.session_state.career_system:
        st.success("Siet Career Guider initialized successfully!")
        if os.environ.get("GOOGLE_SERPER_API_KEY"):
            st.info("Web search capabilities enabled!")
    else:
        st.error("Siet Career Guider not initialized. Please configure your .env file.")

    st.markdown("### 👤 Your Profile")
    user_name = st.text_input("Name", value=st.session_state.user_profile.get("name", ""))
    education_level = st.selectbox("Education Level", ["High School", "Some College", "Bachelor's Degree", "Master's Degree", "PhD", "Other"], index=2)
    experience = st.selectbox("Experience Level", ["Student/No experience", "0-2 years", "3-5 years", "5-10 years", "10+ years"], index=0)
    
    if user_name:
        st.session_state.user_profile = {"name": user_name, "education": education_level, "experience": experience}
    
    st.markdown("### 🧠 Skills Assessment")
    st.markdown("Rate your skills from 1 (beginner) to 10 (expert):")
    technical_score = st.slider("Technical Skills", 1, 10, 5)
    creative_score = st.slider("Creative Skills", 1, 10, 5)
    analytical_score = st.slider("Analytical Skills", 1, 10, 5)
    communication_score = st.slider("Communication Skills", 1, 10, 5)
    
    if "skills" not in st.session_state.user_profile:
        st.session_state.user_profile["skills"] = {}
    
    st.session_state.user_profile["skills"] = {
        "technical": technical_score, "creative": creative_score,
        "analytical": analytical_score, "communication": communication_score
    }
    
    if all(score > 0 for score in [technical_score, creative_score, analytical_score, communication_score]):
        st.markdown("### Your Skills Profile")
        fig = go.Figure()
        categories = ['Technical', 'Creative', 'Analytical', 'Communication']
        values = [technical_score, creative_score, analytical_score, communication_score]
        fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Your Skills'))
        fig.update_layout(template="plotly_dark", paper_bgcolor="#212121", plot_bgcolor="#212121", font=dict(color="#E0E0E0"),
                          polar=dict(radialaxis=dict(visible=True, range=[0, 10], gridcolor="#424242")),
                          height=300, margin=dict(l=10, r=10, b=10, t=30))
        st.plotly_chart(fig, use_container_width=True)

# Create tabs for main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Discover Careers", "📊 Market Analysis", "📚 Learning Roadmap", "💡 Career Insights", "💬 Chat Assistant"
])

# Tab 1: Discover Careers
with tab1:
    st.markdown("## Discover Your Ideal Career Path")
    if not st.session_state.career_system:
        st.warning("Please configure the application using a .env file to get started.")
    else:
        if st.session_state.user_profile and "name" in st.session_state.user_profile:
            st.markdown(f"""
            <div style="background-color: #212121; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #4285F4;">
                <h3 style="color: #82B1FF; margin-top: 0;">👋 Hello, {st.session_state.user_profile['name']}!</h3>
                <p style="font-size: 16px; line-height: 1.6;">
                    Based on your profile as a <span style="background-color: #303F9F; color: white; padding: 2px 5px; border-radius: 3px;">{st.session_state.user_profile['education']}</span> 
                    graduate with <span style="background-color: #303F9F; color: white; padding: 2px 5px; border-radius: 3px;">{st.session_state.user_profile['experience']}</span> of experience, 
                    we'll help you find the perfect career path.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Select a Career Category")
        career_options = st.session_state.career_system.get_career_options()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💻 Technology", help="Careers in software, data, cybersecurity, and more", key="tech_button", use_container_width=True):
                st.session_state.selected_category = "Technology"
                st.session_state.career_analysis = None
                st.session_state.messages = [] 
        with col2:
            if st.button("🏥 Healthcare", help="Medical and health-related careers", key="health_button", use_container_width=True):
                st.session_state.selected_category = "Healthcare"
                st.session_state.career_analysis = None
                st.session_state.messages = [] 
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("💼 Business", help="Finance, marketing, management careers", key="business_button", use_container_width=True):
                st.session_state.selected_category = "Business"
                st.session_state.career_analysis = None
                st.session_state.messages = [] 
        with col4:
            if st.button("🎨 Creative", help="Design, content creation, and artistic careers", key="creative_button", use_container_width=True):
                st.session_state.selected_category = "Creative"
                st.session_state.career_analysis = None
                st.session_state.messages = [] 
        
        if st.session_state.selected_category:
            st.markdown(f"### {st.session_state.selected_category} Careers")
            selected_careers = career_options[st.session_state.selected_category]
            career_cols = st.columns(2)
            
            for i, career in enumerate(selected_careers):
                with career_cols[i % 2]:
                    if st.button(career, key=f"career_{i}", use_container_width=True):
                        st.session_state.selected_career = career
                        st.session_state.career_analysis = None
                        st.session_state.messages = []
            
            if st.session_state.selected_career:
                st.markdown(f"""
                <div style="background-color: #212121; border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #4285F4;">
                    <h3 style="color: #82B1FF; margin-top: 0;">🎯 Selected Career: {st.session_state.selected_career}</h3>
                    <p style="font-size: 16px; line-height: 1.6;">
                        Let's analyze this career path to help you understand the opportunities, requirements, and job market.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.career_analysis is None:
                    if st.session_state.career_system:
                        if os.environ.get("GOOGLE_SERPER_API_KEY"):
                            st.success("Our AI career advisors are ready to provide detailed analysis with up-to-date information!")
                        else:
                            st.success("Our AI career advisors are ready to provide detailed analysis!")
                    
                    if st.button("🔍 Analyze This Career Path", type="primary", use_container_width=True):
                        with st.spinner(f"Analyzing {st.session_state.selected_career} career path... This may take a few minutes."):
                            try:
                                if st.session_state.career_system:
                                    career_analysis = st.session_state.career_system.comprehensive_career_analysis(
                                        st.session_state.selected_career,
                                        st.session_state.user_profile
                                    )
                                    st.session_state.career_analysis = career_analysis
                                    st.success("Analysis complete!")
                                    st.session_state.show_chat = True
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error during analysis: {str(e)}")
                
                if st.session_state.career_analysis:
                    research = st.session_state.career_analysis.get("research", "")
                    if isinstance(research, str) and research:
                        st.markdown(f"""
                        <div class="career-section">
                            <h3 style="color: #82B1FF; margin-top: 0;">Overview of {st.session_state.selected_career}</h3>
                            <div style="font-size: 16px; line-height: 1.6;">{research}</div>
                        </div>
                        """, unsafe_allow_html=True)

# Tab 2: Market Analysis
with tab2:
    st.markdown("## Job Market Analysis")
    if not st.session_state.career_system:
        st.warning("Please configure the application using a .env file to get started.")
    elif not st.session_state.selected_career:
        st.info("Please select a career in the 'Discover Careers' tab first.")
    else:
        st.markdown(f"### Market Analysis for: {st.session_state.selected_career}")
        if st.session_state.career_analysis and st.session_state.career_analysis.get("market_analysis"):
            market_analysis = st.session_state.career_analysis["market_analysis"]
            st.markdown(f"""
            <div class="market-section">
                <h4 style="margin-top: 0;">📊 Market Analysis</h4>
                <div style="font-size: 16px; line-height: 1.6;">{market_analysis}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Job Growth Projection")
            years = list(range(2025, 2030))
            growth_rate = np.random.uniform(0.05, 0.15)
            starting_jobs = np.random.randint(80000, 200000)
            jobs = [int(starting_jobs * (1 + growth_rate) ** i) for i in range(5)]
            cagr = (jobs[-1]/jobs[0])**(1/4) - 1
            job_fig = px.line(x=years, y=jobs, labels={"x": "Year", "y": "Projected Jobs"}, title=f"Projected Job Growth for {st.session_state.selected_career}")
            job_fig.update_layout(template="plotly_dark", paper_bgcolor="#212121", plot_bgcolor="#212121", font=dict(color="#E0E0E0"), title_font=dict(color="#82B1FF"), xaxis=dict(gridcolor="#424242"), yaxis=dict(gridcolor="#424242"))
            job_fig.update_traces(mode="lines+markers", line=dict(width=3, color="#2196F3"), marker=dict(size=10))
            job_fig.add_annotation(x=years[2], y=jobs[2], text=f"CAGR: {cagr:.1%}", showarrow=True, arrowhead=1, arrowsize=1, arrowwidth=2, arrowcolor="#FF5722", font=dict(size=14, color="#FF5722"), bgcolor="#212121", bordercolor="#FF5722", borderwidth=2, borderpad=4, ax=-50, ay=-40)
            st.plotly_chart(job_fig, use_container_width=True)
            
            st.markdown("### Salary Analysis")
            experience_levels = ["Entry Level", "Mid Level", "Senior", "Expert"]
            base_salary = np.random.randint(60000, 90000)
            salaries = [base_salary]
            for i in range(1, 4):
                salaries.append(int(salaries[-1] * (1 + np.random.uniform(0.2, 0.4))))
            salary_fig = px.bar(x=experience_levels, y=salaries, labels={"x": "Experience Level", "y": "Annual Salary ($)"}, title=f"Salary by Experience Level - {st.session_state.selected_career}")
            salary_fig.update_layout(template="plotly_dark", paper_bgcolor="#212121", plot_bgcolor="#212121", font=dict(color="#E0E0E0"), title_font=dict(color="#82B1FF"), xaxis=dict(gridcolor="#424242"), yaxis=dict(gridcolor="#424242"))
            salary_fig.update_traces(marker=dict(color=["#64B5F6", "#42A5F5", "#2196F3", "#1976D2"]))
            st.plotly_chart(salary_fig, use_container_width=True)
        else:
            st.info("Run the full analysis on the 'Discover Careers' tab to see market data.")

# Tab 3: Learning Roadmap
with tab3:
    st.markdown("## Personalized Learning Roadmap")
    if not st.session_state.career_system:
        st.warning("Please configure the application using a .env file to get started.")
    elif not st.session_state.selected_career:
        st.info("Please select a career in the 'Discover Careers' tab first.")
    else:
        st.markdown(f"### Learning Roadmap for: {st.session_state.selected_career}")
        experience_options = {"Student/No experience": "beginner", "0-2 years": "beginner", "3-5 years": "intermediate", "5-10 years": "advanced", "10+ years": "expert"}
        user_experience = st.session_state.user_profile.get("experience", "Student/No experience")
        experience_level = experience_options.get(user_experience, "beginner")
        
        st.markdown(f"""
        <div style="background-color:#1A237E; color:#E0E0E0; border-radius:8px; padding:15px; margin-bottom:20px;">
            <h4 style="margin-top:0; color:#82B1FF;">Your Current Level: {experience_level.title()}</h4>
            <p>This roadmap is tailored for someone at your experience level.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.career_analysis and st.session_state.career_analysis.get("learning_roadmap"):
            roadmap = st.session_state.career_analysis["learning_roadmap"]
            st.markdown(f"""
            <div class="roadmap-section">
                <h4 style="margin-top: 0;">📚 Learning Roadmap</h4>
                <div style="font-size: 16px; line-height: 1.6;">{roadmap}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Run the full analysis on the 'Discover Careers' tab to generate a learning roadmap.")

# Tab 4: Career Insights
with tab4:
    st.markdown("## Advanced Career Insights")
    if not st.session_state.career_system:
        st.warning("Please configure the application using a .env file to get started.")
    elif not st.session_state.selected_career:
        st.info("Please select a career in the 'Discover Careers' tab first.")
    else:
        if st.session_state.career_analysis and st.session_state.career_analysis.get("industry_insights"):
            insights_text = st.session_state.career_analysis["industry_insights"]
            st.markdown(f"""
            <div class="insights-section">
                <h4 style="margin-top: 0;">💡 Industry Insights</h4>
                <div style="font-size: 16px; line-height: 1.6;">{insights_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Run the full analysis on the 'Discover Careers' tab to see industry insights.")

# Tab 5: Chat Assistant
with tab5:
    st.markdown("## Career Chat Assistant")
    if not st.session_state.career_system:
        st.warning("Please configure the application using a .env file to get started.")
    elif not st.session_state.selected_career:
        st.info("Please select a career in the 'Discover Careers' tab first.")
    elif not st.session_state.career_analysis:
        st.info("Please run an analysis on the 'Discover Careers' tab to activate the chat assistant.")
    else:
        career_data = st.session_state.career_analysis
        career_system = st.session_state.career_system
        display_chat_interface(career_data, career_system)

# Add information about the AI system
with st.expander("ℹ️ About Siet Career Guider"):
    st.markdown("""
    Siet Career Guider uses advanced AI technologies to provide personalized career insights.
    - **LangChain**: For structured interaction with AI language models
    - **Web Search**: The system can search the internet for up-to-date information
    - **Streamlit**: Powers the interactive web interface
    """)