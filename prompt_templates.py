"""
Prompt Engineering Templates for Professional AI Prompts
Contains system prompts and construction logic for high-quality outputs
"""

from typing import List, Dict, Optional


class PromptTemplates:
    """Manages prompt engineering templates and construction logic"""
    
    # System prompts for different complexity levels
    SYSTEM_PROMPTS = {
        "Simple": """You are a helpful AI assistant that generates clear, concise prompts for various tasks.
Your prompts should be easy to understand and follow.
Focus on simplicity and clarity.""",
        
        "Standard": """You are an expert prompt engineer with deep knowledge of AI interaction patterns.
You create well-structured prompts that maximize AI performance and output quality.
Your prompts include clear context, specific instructions, and desired outcomes.""",
        
        "Professional": """You are a Senior Prompt Engineer with expertise in AI systems, natural language processing, and human-AI interaction design.
You specialize in crafting enterprise-grade prompts that:
- Maximize AI response accuracy and relevance
- Include comprehensive context and constraints
- Define clear output structures and quality metrics
- Account for edge cases and ambiguity
- Follow best practices for different AI models

Your prompts are detailed, actionable, and optimized for production use.""",
        
        "Enterprise": """You are a Principal AI Architect with extensive experience in building AI-powered enterprise solutions.
You design sophisticated prompt systems that:
- Integrate with complex business workflows
- Scale across multiple use cases and departments
- Maintain consistency and compliance requirements
- Include multi-layered context and role definitions
- Define comprehensive quality gates and evaluation criteria
- Support iterative refinement and A/B testing

Your prompts are strategic assets that drive measurable business outcomes."""
    }
    
    # Tone-specific instructions
    TONE_INSTRUCTIONS = {
        "Professional": "Use formal, business-appropriate language with technical precision.",
        "Casual": "Use conversational, friendly language while maintaining clarity.",
        "Technical": "Use precise technical terminology with detailed specifications.",
        "Creative": "Use imaginative language with engaging narrative elements.",
        "Friendly": "Use warm, approachable language that builds rapport.",
        "Authoritative": "Use confident, decisive language that establishes expertise."
    }
    
    # Length guidelines
    LENGTH_GUIDELINES = {
        "Concise": "Keep the prompt brief and focused (50-100 words).",
        "Balanced": "Provide moderate detail (150-250 words).",
        "Detailed": "Include comprehensive detail (300-500 words).",
        "Comprehensive": "Be extremely thorough (500+ words) with all context."
    }
    
    # Output format templates
    OUTPUT_FORMATTERS = {
        "Markdown": "Format output with proper Markdown headers, lists, and emphasis.",
        "JSON": "Provide structured JSON output with clear key-value pairs.",
        "XML": "Use XML tags for structured data representation.",
        "Plain Text": "Use clean, readable plain text formatting.",
        "Code Block": "Wrap code in appropriate syntax-highlighted code blocks."
    }
    
    def get_system_prompt(self, complexity: str = "Professional", 
                         tone: str = "Professional") -> str:
        """Get the appropriate system prompt based on complexity and tone"""
        base_prompt = self.SYSTEM_PROMPTS.get(
            complexity, 
            self.SYSTEM_PROMPTS["Professional"]
        )
        
        tone_instruction = self.TONE_INSTRUCTIONS.get(
            tone, 
            self.TONE_INSTRUCTIONS["Professional"]
        )
        
        return f"{base_prompt}\n\n{tone_instruction}"
    
    def construct_prompt(self, user_input: str, 
                        length: str = "Detailed",
                        language: str = "English",
                        output_format: List[str] = None) -> str:
        """Construct a complete prompt from user requirements"""
        if output_format is None:
            output_format = ["Markdown"]
        
        length_guideline = self.LENGTH_GUIDELINES.get(
            length, 
            self.LENGTH_GUIDELINES["Detailed"]
        )
        
        format_instructions = " ".join([
            self.OUTPUT_FORMATTERS.get(fmt, self.OUTPUT_FORMATTERS["Markdown"])
            for fmt in output_format
        ])
        
        prompt = f"""{user_input}

## Response Guidelines
- **Language**: Respond in {language}
- **Length**: {length_guideline}
- **Format**: {format_instructions}

## Quality Standards
1. Be specific and actionable
2. Provide clear reasoning and context
3. Include relevant examples where helpful
4. Address potential edge cases
5. Maintain consistency throughout"""
        
        return prompt
    
    def generate_enhanced_prompt(self, raw_requirement: str,
                                role: str = None,
                                context: str = None,
                                constraints: List[str] = None,
                                examples: List[str] = None,
                                output_structure: str = None) -> str:
        """Generate an enhanced prompt with all professional elements"""
        
        components = []
        
        # Role Definition
        if role:
            components.append(f"## Role Definition\nYou are an expert {role} with deep knowledge and experience.")
        
        # Context
        if context:
            components.append(f"## Context\n{context}")
        
        # Core Task
        components.append(f"## Core Task\n{raw_requirement}")
        
        # Constraints
        if constraints:
            constraints_text = "\n".join([f"- {c}" for c in constraints])
            components.append(f"## Constraints\n{constraints_text}")
        
        # Examples
        if examples:
            examples_text = "\n".join([f"**Example {i+1}**: {e}" for i, e in enumerate(examples)])
            components.append(f"## Examples\n{examples_text}")
        
        # Output Structure
        if output_structure:
            components.append(f"## Output Structure\n{output_structure}")
        
        return "\n\n".join(components)
    
    def get_prompt_audit_checklist(self) -> Dict[str, List[str]]:
        """Get a checklist for auditing prompt quality"""
        return {
            "Clarity": [
                "Is the objective clearly stated?",
                "Are there any ambiguous terms?",
                "Is the scope well-defined?"
            ],
            "Completeness": [
                "Is sufficient context provided?",
                "Are all necessary constraints included?",
                "Is the desired output format specified?"
            ],
            "Actionability": [
                "Can the AI immediately begin working?",
                "Are there clear steps or instructions?",
                "Is the success criteria defined?"
            ],
            "Optimization": [
                "Is the prompt neither too short nor too long?",
                "Are there any redundant sections?",
                "Is the formatting optimal for readability?"
            ]
        }
    
    def generate_prompt_for_model(self, requirement: str, 
                                  model: str = "GPT-4") -> str:
        """Generate an optimized prompt for a specific AI model"""
        
        model_specific_guidance = {
            "GPT-4": "GPT-4 excels at complex reasoning and following detailed instructions. Include step-by-step guidance.",
            "GPT-3.5-Turbo": "GPT-3.5-Turbo is fast but benefits from clearer, more direct prompts. Avoid excessive complexity.",
            "Claude-3-Haiku": "Claude-3-Haiku is fast and good at following instructions. Use natural language.",
            "Claude-3-Sonnet": "Claude-3-Sonnet balances capability and speed. Standard detailed prompts work well."
        }
        
        guidance = model_specific_guidance.get(
            model, 
            "Use standard prompt engineering best practices."
        )
        
        return f"""{requirement}

## Model-Specific Optimization
{guidance}

## Additional Instructions
Please provide your best possible response following the requirements above.
Consider the model you're working with and optimize your output accordingly."""
    
    def get_few_shot_examples(self, task_type: str) -> List[Dict]:
        """Get few-shot examples for common task types"""
        
        examples = {
            "code_generation": [
                {
                    "input": "Create a Python function to calculate Fibonacci numbers",
                    "output": "```python\ndef fibonacci(n):\n    if n <= 0:\n        return []\n    elif n == 1:\n        return [0]\n    \n    fib序列 = [0, 1]\n    while len(fib序列) < n:\n        fib序列.append(fib序列[-1] + fib序列[-2])\n    \n    return fib序列\n```"
                }
            ],
            "content_writing": [
                {
                    "input": "Write a product description for wireless headphones",
                    "output": "**Premium Wireless Headphones**\n\nExperience crystal-clear audio with our latest wireless headphones..."
                }
            ],
            "data_analysis": [
                {
                    "input": "Analyze this sales data for trends",
                    "output": "## Sales Data Analysis\n\n### Key Findings\n1. **Growth Trend**: 15% QoQ increase\n2. **Top Product**: Product A (40% of sales)\n3. **Recommendation**: Focus marketing on Product A"
                }
            ]
        }
        
        return examples.get(task_type, [])