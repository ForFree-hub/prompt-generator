"""
Professional Prompt Generator - Free with Groq API
"""

import streamlit as st
import uuid
from datetime import datetime
from groq import Groq
from history_manager import HistoryManager

st.set_page_config(page_title="PromptGen Pro", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .prompt-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px; padding: 20px; margin: 10px 0;
        border: 1px solid #475569;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 8px; padding: 12px 24px;
        font-weight: 600;
    }
    .main-header {
        font-size: 2.5rem; font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)


class PromptGeneratorApp:
    def __init__(self):
        self.history_manager = HistoryManager()
        self.client = None
        self.initialize_session_state()
    
    def initialize_session_state(self):
        if 'generated_prompts' not in st.session_state:
            st.session_state.generated_prompts = []
        if 'current_prompt' not in st.session_state:
            st.session_state.current_prompt = None
    
    def render_header(self):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('<h1 class="main-header">⚡ PromptGen Pro</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Free AI Prompt Generator with Groq API</p>', unsafe_allow_html=True)
        with col2:
            st.markdown("###")
            if st.button("🗑️ Clear History"):
                self.history_manager.clear_history()
                st.rerun()
    
    def render_sidebar(self):
        with st.sidebar:
            st.header("🎛️ Configuration")
            
            # API Key Input
            st.subheader("🔑 Groq API Key")
            st.info("Get free key: https://console.groq.com/")
            api_key = st.text_input("Enter Groq API Key", type="password")
            
            if api_key:
                st.session_state.groq_api_key = api_key
                self.client = Groq(api_key=api_key)
                st.success("✅ API Key configured!")
            
            st.divider()
            
            # Model Selection - UPDATED WITH NEW MODELS!
            st.subheader("🤖 Model (All Free!)")
            model = st.selectbox(
                "Choose a model:",
                options=[
                    "llama-3.1-8b-instant",    # ✅ NEW! Fast & good
                    "llama-3.1-70b-instant",   # More powerful
                    "mixtral-8x7b-32768",       # Great for prompts
                    "gemma2-9b-it"             # Lightweight
                ],
                index=0
            )
            
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            
            st.divider()
            
            # Complexity
            st.subheader("📝 Complexity")
            complexity = st.select_slider(
                "Prompt Complexity",
                options=["Simple", "Standard", "Professional", "Enterprise"],
                value="Professional"
            )
            
            # Output Format
            st.subheader("📋 Output Format")
            output_format = st.multiselect(
                "Desired Output Formats",
                options=["Markdown", "JSON", "XML", "Plain Text", "Code Block"],
                default=["Markdown", "Code Block"]
            )
            
            return {
                'model': model,
                'temperature': temperature,
                'complexity': complexity,
                'output_format': output_format
            }
    
    def render_main_content(self, config):
        st.subheader("📥 Input Your Requirements")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_input = st.text_area(
                "Describe what you want to achieve:",
                placeholder="Example: Write a professional farewell message for an employee leaving after 5 years...",
                height=120
            )
        
        with col2:
            st.markdown("###")
            st.markdown("**💡 Tips:**")
            st.markdown("- Be specific about audience")
            st.markdown("- Define desired format")
            st.markdown("- Mention constraints")
        
        # Advanced Options
        with st.expander("🔧 Advanced Options", expanded=False):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                tone = st.selectbox("Tone", ["Professional", "Casual", "Technical", "Creative", "Friendly"], index=0)
            with col_b:
                length = st.selectbox("Length", ["Concise", "Balanced", "Detailed", "Comprehensive"], index=2)
            with col_c:
                language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
        
        st.markdown("###")
        
        if st.button("⚡ Generate Professional Prompt", use_container_width=True):
            if user_input.strip():
                if not self.client:
                    st.error("❌ Please enter your Groq API key in the sidebar first!")
                else:
                    with st.spinner("🔮 Generating prompt..."):
                        try:
                            generated_prompt = self.generate_prompt(
                                user_input=user_input,
                                config=config,
                                tone=tone,
                                length=length,
                                language=language
                            )
                            
                            prompt_id = str(uuid.uuid4())
                            prompt_data = {
                                'id': prompt_id,
                                'timestamp': datetime.now().isoformat(),
                                'user_input': user_input,
                                'generated_prompt': generated_prompt,
                                'config': config
                            }
                            
                            st.session_state.generated_prompts.insert(0, prompt_data)
                            st.session_state.current_prompt = generated_prompt
                            self.history_manager.save_prompt(prompt_data)
                            
                            st.success("✅ Prompt generated successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter your requirements first!")
        
        if st.session_state.current_prompt:
            self.render_generated_prompt(st.session_state.current_prompt)
    
    def generate_prompt(self, user_input, config, tone, length, language):
        """Generate prompt using Groq API"""
        
        system_prompt = """You are a Senior Prompt Engineer with expertise in AI systems, natural language processing, and human-AI interaction design. You specialize in crafting enterprise-grade prompts that:
- Maximize AI response accuracy and relevance
- Include comprehensive context and constraints
- Define clear output structures and quality metrics
- Account for edge cases and ambiguity
- Follow best practices for different AI models

Your prompts are detailed, actionable, and optimized for production use."""
        
        user_prompt = f"""Task: Generate a professional AI prompt based on the following requirements.

## User Requirements
{user_input}

## Requirements
- **Tone**: {tone}
- **Complexity**: {config['complexity']}
- **Length**: {length}
- **Language**: {language}
- **Output Format**: {', '.join(config['output_format'])}

## Instructions
1. Create a well-structured, production-ready prompt
2. Include clear instructions, constraints, and expected output format
3. Optimize for clarity, specificity, and actionability
4. Add relevant context and consider edge cases
5. Format the output as specified

Please generate the professional prompt now:"""

        try:
            response = self.client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config['temperature'],
                max_tokens=2000
            )
            
            generated = response.choices[0].message.content
            return generated
            
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")
    
    def render_generated_prompt(self, prompt):
        st.markdown("---")
        st.subheader("✨ Generated Professional Prompt")
        
        st.markdown(f"""
        <div class="prompt-card">
            <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">{prompt}</pre>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download",
                data=prompt,
                file_name="generated_prompt.txt",
                mime="text/plain"
            )
        
        with col2:
            if st.button("🔄 Regenerate"):
                st.rerun()
        
        with col3:
            if st.button("💾 Save to Favorites"):
                self.history_manager.save_favorite(prompt)
                st.success("Saved!")
    
    def render_history_section(self):
        st.markdown("---")
        st.subheader("📚 Prompt History")
        
        history = self.history_manager.get_history()
        
        if history:
            for idx, item in enumerate(history):
                with st.expander(f"📝 {item['user_input'][:50]}...", expanded=False):
                    st.markdown(f"**Generated:** {item['generated_prompt'][:200]}...")
                    st.markdown(f"**Date:** {item['timestamp']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Reuse", key=f"reuse_{idx}"):
                            st.session_state.current_prompt = item['generated_prompt']
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{idx}"):
                            self.history_manager.delete_prompt(item['id'])
                            st.rerun()
        else:
            st.info("📭 No history yet!")
    
    def run(self):
        self.render_header()
        config = self.render_sidebar()
        self.render_main_content(config)
        self.render_history_section()
        
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #64748b;'>🤖 Powered by PromptGen Pro + Groq API</div>",
            unsafe_allow_html=True
        )


def main():
    app = PromptGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()