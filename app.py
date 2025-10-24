"""
Main Gradio application for the AI Lead Qualification Bot.
"""

import os
import json
import uuid
import gradio as gr
from typing import Dict, List, Any, Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, continue without it
    pass

from config.settings import app_config, validate_config
from models.llm_pipeline import get_llm_pipeline
from models.vector_store import initialize_vector_store_from_files
from models.predictive_model import train_model_from_data
from utils.crm_integration import get_crm_manager
from utils.logging import get_logger

logger = get_logger(__name__)

class LeadQualificationBot:
    """Main application class for the AI Lead Qualification Bot."""
    
    def __init__(self):
        """Initialize the bot application."""
        self.llm_pipeline = get_llm_pipeline()
        self.crm_manager = get_crm_manager()
        self.conversations = {}
        
        # Initialize components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components."""
        try:
            # Validate configuration
            if not validate_config():
                logger.error("Configuration validation failed")
                return
            
            # Initialize vector store with documents
            initialize_vector_store_from_files(app_config.data_dir)
            
            # Train predictive model if training data exists
            training_data_path = os.path.join(app_config.data_dir, "training_data", "crm_data.csv")
            if os.path.exists(training_data_path):
                logger.info("Training predictive model with existing data...")
                train_model_from_data(training_data_path)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
    
    def start_conversation(self) -> str:
        """Start a new conversation."""
        conversation_id = str(uuid.uuid4())
        greeting = self.llm_pipeline.start_conversation(conversation_id)
        self.conversations[conversation_id] = {
            'messages': [],
            'structured_output': None
        }
        return greeting, conversation_id
    
    def process_message(self, message: str, conversation_id: str, history: List[List[str]]) -> tuple:
        """Process a user message and return the response."""
        if not conversation_id or conversation_id == "None":
            # Start new conversation
            greeting, conversation_id = self.start_conversation()
            history = [[greeting, None]]
        
        try:
            # Process message through LLM pipeline
            result = self.llm_pipeline.process_message(conversation_id, message)
            
            # Update conversation history
            if conversation_id in self.conversations:
                self.conversations[conversation_id]['messages'].append({
                    'user': message,
                    'bot': result['response']
                })
                self.conversations[conversation_id]['structured_output'] = result['structured_output']
            
            # Add to Gradio history
            history.append([message, result['response']])
            
            return history, conversation_id, self._format_structured_output(result['structured_output'])
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            history.append([message, error_response])
            return history, conversation_id, "Error occurred during processing"
    
    def _format_structured_output(self, structured_output: Dict[str, Any]) -> str:
        """Format structured output for display."""
        if not structured_output:
            return "No structured output available"
        
        try:
            # Format the JSON output nicely
            formatted_json = json.dumps(structured_output, indent=2)
            
            # Create a summary
            lead = structured_output.get('lead', {})
            intent = structured_output.get('intent', 'unknown')
            score = structured_output.get('score', 0)
            recommendation = structured_output.get('recommended_action', 'unknown')
            explanation = structured_output.get('explain', 'No explanation available')
            
            summary = f"""
**Lead Information:**
- Name: {lead.get('name', 'Not provided')}
- Company: {lead.get('company', 'Not provided')}
- Role: {lead.get('role', 'Not provided')}
- Industry: {lead.get('industry', 'Not provided')}

**Qualification Results:**
- Intent: {intent}
- Score: {score}/100
- Recommendation: {recommendation}
- Explanation: {explanation}

**Top Signals:**
{chr(10).join([f"- {signal}" for signal in structured_output.get('top_signals', [])])}

**CRM Tags:**
{chr(10).join([f"- {tag}" for tag in structured_output.get('crm_tags', [])])}

**Full JSON Output:**
```json
{formatted_json}
```
"""
            return summary
            
        except Exception as e:
            logger.error(f"Error formatting structured output: {e}")
            return f"Error formatting output: {str(e)}"
    
    def export_lead(self, conversation_id: str) -> str:
        """Export lead data to CRM systems."""
        if not conversation_id or conversation_id == "None":
            return "No conversation to export"
        
        if conversation_id not in self.conversations:
            return "Conversation not found"
        
        try:
            structured_output = self.conversations[conversation_id]['structured_output']
            if not structured_output:
                return "No structured output available for export"
            
            # Prepare lead data for CRM
            lead_data = {
                'name': structured_output['lead'].get('name'),
                'email': structured_output['lead'].get('email'),
                'company': structured_output['lead'].get('company'),
                'role': structured_output['lead'].get('role'),
                'industry': structured_output['lead'].get('industry'),
                'intent': structured_output['intent'],
                'score': structured_output['score'],
                'tags': structured_output['crm_tags']
            }
            
            # Create lead in all CRMs
            results = self.crm_manager.create_lead_in_all_crms(lead_data)
            
            # Format results
            export_summary = "**CRM Export Results:**\n\n"
            for crm_name, result in results.items():
                if result.get('success'):
                    export_summary += f"✅ **{crm_name.title()}**: {result.get('message')}\n"
                    export_summary += f"   Lead ID: {result.get('lead_id')}\n"
                else:
                    export_summary += f"❌ **{crm_name.title()}**: {result.get('message')}\n"
                    export_summary += f"   Error: {result.get('error', 'Unknown error')}\n"
                export_summary += "\n"
            
            return export_summary
            
        except Exception as e:
            logger.error(f"Error exporting lead: {e}")
            return f"Error exporting lead: {str(e)}"
    
    def get_conversation_summary(self, conversation_id: str) -> str:
        """Get a summary of the current conversation."""
        if not conversation_id or conversation_id == "None":
            return "No active conversation"
        
        try:
            summary = self.llm_pipeline.get_conversation_summary(conversation_id)
            if not summary:
                return "Conversation not found"
            
            return f"""
**Conversation Summary:**
- Conversation ID: {summary.get('conversation_id')}
- Message Count: {summary.get('message_count', 0)}
- Current Intent: {summary.get('current_intent', 'unknown')}
- Current Score: {summary.get('current_score', 0)}
- Collected Fields: {', '.join(summary.get('collected_fields', []))}

**Lead Information:**
{json.dumps(summary.get('lead_info', {}), indent=2)}
"""
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return f"Error getting summary: {str(e)}"

def create_gradio_interface():
    """Create the Gradio interface."""
    bot = LeadQualificationBot()
    
    with gr.Blocks(
        title="AI Lead Qualification Bot",
        theme=gr.themes.Soft(),
        css="""
body {
    background: linear-gradient(135deg, #1b1f3b, #3d2c8d);
    font-family: 'Inter', sans-serif;
}

.gradio-container {
    max-width: 1200px !important;
    padding: 20px;
    color: white;
}

#chatbox .message {
    animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    padding: 15px;
}

.output-container {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    overflow-y: auto;
    max-height: 400px;
    backdrop-filter: blur(10px);
}

button {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    border: none !important;
    color: white !important;
    font-weight: bold;
    transition: transform 0.2s ease;
}

button:hover {
    transform: scale(1.05);
}

#structured-output {
    transition: all 0.3s ease-in-out;
}

#structured-output:hover {
    box-shadow: 0 0 20px rgba(255,255,255,0.2);
}
"""

    ) as interface:
        
        gr.Markdown("""
        # 🤖 AI Lead Qualification Bot
        
        Welcome to the AI-powered lead qualification system! This bot helps you:
        
        - **Engage** with inbound leads through natural conversations
        - **Collect** qualification information automatically
        - **Score** leads based on intent and behavior signals
        - **Recommend** next actions for your sales team
        - **Export** qualified leads to your CRM systems
        
        Start a conversation below to begin qualifying leads!
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Chat interface
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=500,
                    show_label=True,
                    container=True,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your message",
                        placeholder="Tell me about your role and what you're looking to accomplish...",
                        lines=2,
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Row():
                    new_conversation_btn = gr.Button("New Conversation", variant="secondary")
                    export_btn = gr.Button("Export to CRM", variant="secondary")
                    summary_btn = gr.Button("Show Summary", variant="secondary")
            
            with gr.Column(scale=1):
                # Conversation ID
                conversation_id = gr.Textbox(
                    label="Conversation ID",
                    value="None",
                    interactive=False
                )
                
                # Structured output
                structured_output = gr.Markdown(
                    label="Lead Qualification Results",
                    value="Start a conversation to see qualification results here...",
                    elem_classes=["output-container"]
                )
                
                # System status
                gr.Markdown("""
                ### System Status
                - ✅ LLM Pipeline: Ready
                - ✅ Vector Store: Ready
                - ✅ Predictive Model: Ready
                - ✅ CRM Integration: Ready
                """)
        
        # Event handlers
        def handle_send(message, conv_id, history):
            return bot.process_message(message, conv_id, history)
        
        def handle_new_conversation():
            greeting, new_conv_id = bot.start_conversation()
            return [[greeting, None]], new_conv_id, "New conversation started!"
        
        def handle_export(conv_id):
            return bot.export_lead(conv_id)
        
        def handle_summary(conv_id):
            return bot.get_conversation_summary(conv_id)
        
        # Connect events
        send_btn.click(
            handle_send,
            inputs=[msg, conversation_id, chatbot],
            outputs=[chatbot, conversation_id, structured_output]
        )
        
        msg.submit(
            handle_send,
            inputs=[msg, conversation_id, chatbot],
            outputs=[chatbot, conversation_id, structured_output]
        )
        
        new_conversation_btn.click(
            handle_new_conversation,
            outputs=[chatbot, conversation_id, structured_output]
        )
        
        export_btn.click(
            handle_export,
            inputs=[conversation_id],
            outputs=[structured_output]
        )
        
        summary_btn.click(
            handle_summary,
            inputs=[conversation_id],
            outputs=[structured_output]
        )
        
        # Initialize with a greeting
        greeting, initial_conv_id = bot.start_conversation()
        chatbot.value = [[greeting, None]]
        conversation_id.value = initial_conv_id
    
    return interface

def main():
    """Main function to run the application."""
    try:
        # Create and launch the interface
        interface = create_gradio_interface()
        
        logger.info(f"Starting AI Lead Qualification Bot on port {app_config.gradio_port}")
        
        interface.launch(
            server_name="0.0.0.0",
            server_port=app_config.gradio_port,
            share=app_config.gradio_share,
            debug=app_config.gradio_debug,
            show_error=True
        )
        
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        raise

if __name__ == "__main__":
    main()
