# AI Lead Qualification Bot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

An intelligent lead qualification system that automates prospect evaluation through conversational AI and predictive analytics.

## Overview

This system combines natural language processing with machine learning to:

- Conduct automated qualification conversations with prospects
- Generate real-time lead scores based on conversation analysis
- Extract key buying signals and intent indicators
- Integrate seamlessly with existing CRM workflows
- Provide structured data output for sales teams

**Key Benefits:**
- Reduces manual qualification time
- Improves lead scoring accuracy
- Standardizes qualification processes
- Scales prospect engagement

## Core Features

### Conversational Intelligence
- **Natural Language Processing**: Powered by Mistral-7B for human-like interactions
- **Context Retention**: Maintains conversation history for coherent multi-turn dialogues
- **Adaptive Questioning**: Dynamically adjusts questions based on prospect responses

### Predictive Analytics
- **Real-time Scoring**: Generates lead scores (0-100) during conversations
- **Intent Classification**: Categorizes prospects by purchase readiness
- **Signal Detection**: Identifies key buying indicators and pain points

### Knowledge Integration
- **Document Retrieval**: RAG-based system for accessing product information
- **Competitive Intelligence**: Integrated battlecards for handling objections
- **Case Study Access**: Relevant success stories for prospect engagement

### CRM Connectivity
- **Multi-platform Support**: HubSpot and Salesforce integrations
- **Automated Data Entry**: Creates and updates lead records automatically
- **Custom Tagging**: Applies relevant tags based on conversation insights

## Example Usage

### Conversation Flow
```
Prospect: "Hi, I'm looking for a CRM solution for my team of 25 people. 
          We're currently using spreadsheets but need something more robust."

Bot: "I understand you're looking to upgrade from spreadsheets to a proper CRM. 
     That's a common challenge for growing teams. What's driving this decision 
     right now - are you facing specific pain points with your current process?"

Prospect: "Yes, we're losing track of leads and our sales process is inconsistent. 
          We need to implement something within the next quarter."
```

### System Output
```json
{
  "prospect_profile": {
    "company_size": 25,
    "current_solution": "spreadsheets",
    "decision_timeline": "next_quarter"
  },
  "qualification_score": 78,
  "intent_level": "high_interest",
  "key_signals": [
    "specific_pain_points_identified",
    "defined_timeline",
    "team_size_specified"
  ],
  "next_action": "schedule_demo",
  "crm_tags": ["mid_market", "spreadsheet_migration", "q1_timeline"]
}
```

## System Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Gradio Interface │───▶│ Bot Service     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 ▼                                 │
                       │                    ┌─────────────────┐                           │
                       │                    │ LLM Pipeline    │                           │
                       │                    └─────────────────┘                           │
                       │                                 │                                 │
                       ▼                                 ▼                                 ▼
            ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
            │ Vector Store    │              │ Predictive      │              │ CRM Integration │
            │ (Knowledge RAG) │              │ Scoring Model   │              │ Manager         │
            └─────────────────┘              └─────────────────┘              └─────────────────┘
```

### Technology Components

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Interface** | Gradio | Web-based user interaction |
| **Orchestration** | LangChain | Workflow management |
| **Language Model** | Mistral-7B | Conversation generation |
| **Embeddings** | Sentence Transformers | Text vectorization |
| **Vector Database** | FAISS | Document retrieval |
| **ML Framework** | LightGBM | Predictive scoring |
| **Runtime** | Python 3.8+ | Core application |

## Installation & Setup

### System Requirements
- Python 3.8 or higher
- 8GB RAM minimum
- Internet connection for initial model downloads

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/RohithCherukuri816/AI-Lead-Qualification-Bot.git
   cd AI-Lead-Qualification-Bot
   ```

2. **Setup Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment** (Optional)
   
   Create `.env` file with your API credentials:
   ```bash
   HUGGINGFACE_TOKEN=your_token_here
   HUBSPOT_API_KEY=your_hubspot_key
   SALESFORCE_API_KEY=your_salesforce_key
   ENVIRONMENT=development
   ```

5. **Launch Application**
   ```bash
   python app.py
   ```
   
   Access the interface at `http://localhost:7860`

## Project Structure

```
AI-Lead-Qualification-Bot/
├── app.py                      # Main application entry point
├── test_bot.py                 # Test suite
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
│
├── config/
│   ├── prompts.py             # Conversation templates
│   └── settings.py            # System configuration
│
├── services/
│   └── bot_service.py         # Core conversation logic
│
├── models/
│   ├── llm_pipeline.py        # Language model interface
│   ├── predictive_model.py    # Scoring algorithms
│   └── vector_store.py        # Document retrieval system
│
├── integrations/
│   ├── hubspot.py             # HubSpot CRM connector
│   ├── salesforce.py          # Salesforce CRM connector
│   └── manager.py             # Integration orchestrator
│
├── data/
│   ├── product_docs/          # Product documentation
│   ├── case_studies/          # Customer success stories
│   ├── competitor_battlecards/# Competitive intelligence
│   └── training_data/         # ML training datasets
│
└── utils/
    └── logging.py             # Logging utilities
```

## Configuration & Customization

### Model Settings
Modify `config/settings.py` to adjust model parameters:

```python
# Language model configuration
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Text processing settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MAX_TOKENS = 2048
```

### Conversation Templates
Update `config/prompts.py` to customize:
- System behavior prompts
- Qualification question sequences
- Response formatting templates

### Knowledge Base Management
Organize your content in the `data/` directory:
- `product_docs/` - Technical specifications and feature descriptions
- `case_studies/` - Customer success stories and use cases
- `competitor_battlecards/` - Competitive positioning information

## Testing

Execute the test suite to verify system functionality:

```bash
python test_bot.py
```

The test suite validates:
- Configuration loading
- Model initialization
- Vector store operations
- CRM integration endpoints
- Conversation flow logic

## API Integration

### Response Format
The system outputs structured JSON for easy integration:

```json
{
  "prospect_data": {
    "name": "string|null",
    "email": "string|null", 
    "company": "string|null",
    "role": "string|null",
    "industry": "string|null"
  },
  "qualification_results": {
    "intent_category": "high_interest|moderate_interest|low_interest|not_qualified",
    "score": "0-100",
    "confidence_level": "high|medium|low"
  },
  "conversation_insights": {
    "key_signals": ["array", "of", "signals"],
    "pain_points": ["identified", "challenges"],
    "decision_factors": ["important", "criteria"]
  },
  "recommendations": {
    "next_action": "schedule_demo|send_proposal|nurture_sequence|disqualify",
    "priority_level": "hot|warm|cold",
    "crm_tags": ["relevant", "tags"]
  }
}
```

## Deployment Options

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
```

### Cloud Platform Deployment
The application can be deployed on various platforms:
- Hugging Face Spaces (Gradio-compatible)
- AWS EC2 with Docker
- Google Cloud Run
- Azure Container Instances

## Troubleshooting

### Common Issues

**Module Import Errors**
```bash
pip install -r requirements.txt
```

**Memory Issues**
- Close unnecessary applications
- Adjust `llm_max_length` in configuration
- Consider using a smaller language model

**Authentication Errors**
```bash
export HUGGINGFACE_TOKEN=your_token_here
```

Refer to configuration files and logs for additional troubleshooting guidance.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Development Roadmap

- Multi-language conversation support
- Enhanced analytics dashboard
- Webhook integration capabilities
- Mobile-responsive interface
- Advanced model fine-tuning tools

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Rohith Cherukuri**
- GitHub: [@RohithCherukuri816](https://github.com/RohithCherukuri816)
- Repository: [AI-Lead-Qualification-Bot](https://github.com/RohithCherukuri816/AI-Lead-Qualification-Bot)

---

*Built with open-source technologies and designed for scalable lead qualification automation.*
