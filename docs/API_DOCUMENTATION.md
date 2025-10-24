# AI Lead Qualification Bot - API Documentation

## Overview

The AI Lead Qualification Bot provides a comprehensive API for lead qualification, conversation management, and CRM integration. This document describes all available endpoints, request/response formats, and usage examples.

## Base URL

```
https://your-domain.com/api/v1
```

## Authentication

All API requests require authentication using API keys. Include your API key in the request headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limits

- **Free Tier**: 100 requests/hour
- **Professional Tier**: 1,000 requests/hour
- **Enterprise Tier**: 10,000 requests/hour

## Endpoints

### 1. Conversation Management

#### Start Conversation
**POST** `/conversations/start`

Start a new conversation and get a conversation ID.

**Request:**
```json
{
  "user_id": "optional_user_id",
  "source": "website|email|social|api",
  "initial_context": {
    "referrer": "google",
    "campaign": "summer_2024",
    "landing_page": "/pricing"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_123456789",
  "greeting": "Hello! I'm here to help you find the right solution...",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Send Message
**POST** `/conversations/{conversation_id}/message`

Send a message in an existing conversation.

**Request:**
```json
{
  "message": "Hi, I'm looking for a CRM solution for our sales team",
  "metadata": {
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1",
    "session_id": "sess_123"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_123456789",
  "response": "Hello! I'd be happy to help you find the right CRM solution...",
  "structured_output": {
    "lead": {
      "name": "Sarah",
      "email": null,
      "company": "TechCorp",
      "role": "Sales Director",
      "industry": "Technology"
    },
    "intent": "buy_soon",
    "score": 85,
    "top_signals": [
      "budget mentioned",
      "timeline specified",
      "pain points clear"
    ],
    "recommended_action": "schedule_demo",
    "explain": "High-scoring lead with clear buying intent",
    "crm_tags": [
      "enterprise",
      "high_priority",
      "hot_lead"
    ]
  },
  "timestamp": "2024-01-15T10:31:00Z"
}
```

#### Get Conversation History
**GET** `/conversations/{conversation_id}/history`

Retrieve the full conversation history.

**Response:**
```json
{
  "conversation_id": "conv_123456789",
  "messages": [
    {
      "role": "user",
      "content": "Hi, I'm looking for a CRM solution",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Hello! I'd be happy to help...",
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ],
  "lead_info": {
    "name": "Sarah",
    "company": "TechCorp",
    "role": "Sales Director"
  },
  "current_score": 85,
  "current_intent": "buy_soon"
}
```

#### End Conversation
**POST** `/conversations/{conversation_id}/end`

End a conversation and get a summary.

**Response:**
```json
{
  "conversation_id": "conv_123456789",
  "summary": "Conversation ended successfully",
  "final_score": 85,
  "final_intent": "buy_soon",
  "total_messages": 8,
  "duration_minutes": 15
}
```

### 2. Lead Qualification

#### Get Lead Score
**POST** `/leads/score`

Get a lead score for a conversation or lead data.

**Request:**
```json
{
  "conversation_id": "conv_123456789",
  "lead_data": {
    "name": "Sarah",
    "company": "TechCorp",
    "role": "Sales Director",
    "industry": "Technology",
    "team_size": 50
  },
  "behavioral_data": {
    "pages_visited": 5,
    "trial_usage": 0.2,
    "email_opens": 3,
    "demo_requested": true
  }
}
```

**Response:**
```json
{
  "score": 85,
  "intent": "buy_soon",
  "confidence": 0.92,
  "signals": [
    "budget mentioned",
    "timeline specified",
    "decision maker identified"
  ],
  "recommendation": "schedule_demo",
  "explanation": "High-scoring lead with clear buying intent"
}
```

#### Batch Lead Scoring
**POST** `/leads/batch-score`

Score multiple leads at once.

**Request:**
```json
{
  "leads": [
    {
      "conversation_id": "conv_123456789",
      "lead_data": {...},
      "behavioral_data": {...}
    },
    {
      "conversation_id": "conv_987654321",
      "lead_data": {...},
      "behavioral_data": {...}
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "conversation_id": "conv_123456789",
      "score": 85,
      "intent": "buy_soon",
      "recommendation": "schedule_demo"
    },
    {
      "conversation_id": "conv_987654321",
      "score": 35,
      "intent": "researching",
      "recommendation": "nurture_email"
    }
  ]
}
```

### 3. CRM Integration

#### Create Lead in CRM
**POST** `/crm/leads`

Create a lead in connected CRM systems.

**Request:**
```json
{
  "conversation_id": "conv_123456789",
  "lead_data": {
    "name": "Sarah Johnson",
    "email": "sarah@techcorp.com",
    "company": "TechCorp",
    "role": "Sales Director",
    "industry": "Technology",
    "phone": "+1-555-0123"
  },
  "qualification_data": {
    "score": 85,
    "intent": "buy_soon",
    "signals": ["budget mentioned", "timeline specified"],
    "recommendation": "schedule_demo"
  },
  "crm_systems": ["hubspot", "salesforce"]
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "hubspot": {
      "success": true,
      "lead_id": "hubspot_123456",
      "message": "Lead created successfully"
    },
    "salesforce": {
      "success": true,
      "lead_id": "salesforce_789012",
      "message": "Lead created successfully"
    }
  }
}
```

#### Update Lead
**PUT** `/crm/leads/{lead_id}`

Update an existing lead in CRM systems.

**Request:**
```json
{
  "lead_data": {
    "score": 90,
    "intent": "buy_soon",
    "status": "qualified"
  },
  "crm_systems": ["hubspot", "salesforce"]
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "hubspot": {
      "success": true,
      "message": "Lead updated successfully"
    },
    "salesforce": {
      "success": true,
      "message": "Lead updated successfully"
    }
  }
}
```

#### Add Note to Lead
**POST** `/crm/leads/{lead_id}/notes`

Add a note to a lead in CRM systems.

**Request:**
```json
{
  "note": "Lead showed strong buying intent during conversation. Budget: $100k, Timeline: 1 month",
  "crm_systems": ["hubspot", "salesforce"]
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "hubspot": {
      "success": true,
      "note_id": "note_123456",
      "message": "Note added successfully"
    },
    "salesforce": {
      "success": true,
      "note_id": "note_789012",
      "message": "Note added successfully"
    }
  }
}
```

### 4. Knowledge Base

#### Search Knowledge Base
**POST** `/knowledge/search`

Search the knowledge base for relevant information.

**Request:**
```json
{
  "query": "pricing information for enterprise customers",
  "document_types": ["product_docs", "case_studies"],
  "limit": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "content": "Our Enterprise plan starts at $2,000/month...",
      "source": "pricing_guide.txt",
      "document_type": "product_docs",
      "score": 0.95
    },
    {
      "content": "TechCorp saw 300% increase in lead quality...",
      "source": "techcorp_case_study.txt",
      "document_type": "case_studies",
      "score": 0.87
    }
  ]
}
```

#### Add Document to Knowledge Base
**POST** `/knowledge/documents`

Add a new document to the knowledge base.

**Request:**
```json
{
  "content": "New product feature documentation...",
  "document_type": "product_docs",
  "metadata": {
    "title": "New Feature Guide",
    "author": "Product Team",
    "version": "1.0"
  }
}
```

**Response:**
```json
{
  "success": true,
  "document_id": "doc_123456",
  "message": "Document added successfully"
}
```

### 5. Model Management

#### Train Model
**POST** `/models/train`

Retrain the predictive model with new data.

**Request:**
```json
{
  "training_data": [
    {
      "conversation_data": {...},
      "outcome": "converted",
      "conversion_value": 50000
    }
  ],
  "model_type": "lead_scoring",
  "parameters": {
    "learning_rate": 0.1,
    "max_depth": 6
  }
}
```

**Response:**
```json
{
  "success": true,
  "model_id": "model_123456",
  "accuracy": 0.85,
  "training_time": "2.5 minutes",
  "message": "Model trained successfully"
}
```

#### Get Model Performance
**GET** `/models/{model_id}/performance`

Get performance metrics for a trained model.

**Response:**
```json
{
  "model_id": "model_123456",
  "accuracy": 0.85,
  "precision": 0.82,
  "recall": 0.88,
  "f1_score": 0.85,
  "feature_importance": {
    "budget_mentioned": 0.15,
    "timeline_mentioned": 0.12,
    "decision_maker": 0.20
  },
  "last_updated": "2024-01-15T10:00:00Z"
}
```

### 6. Analytics

#### Get Conversation Analytics
**GET** `/analytics/conversations`

Get analytics for conversations.

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `intent`: Filter by intent
- `score_range`: Filter by score range

**Response:**
```json
{
  "total_conversations": 1250,
  "average_score": 65.5,
  "intent_distribution": {
    "buy_soon": 0.25,
    "considering": 0.35,
    "researching": 0.30,
    "not_interested": 0.10
  },
  "conversion_rate": 0.18,
  "average_conversation_length": 8.5,
  "top_signals": [
    "budget mentioned",
    "timeline specified",
    "pain points clear"
  ]
}
```

#### Get Lead Quality Metrics
**GET** `/analytics/lead-quality`

Get lead quality metrics.

**Response:**
```json
{
  "total_leads": 1250,
  "qualified_leads": 450,
  "conversion_rate": 0.18,
  "average_lead_score": 65.5,
  "score_distribution": {
    "high_priority": 0.25,
    "medium_priority": 0.45,
    "low_priority": 0.30
  },
  "top_industries": [
    "Technology",
    "Healthcare",
    "Financial Services"
  ]
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes and error messages.

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid conversation ID provided",
    "details": {
      "conversation_id": "must be a valid UUID"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes
- `400`: Bad Request - Invalid input data
- `401`: Unauthorized - Invalid or missing API key
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Server error

## Webhooks

### Configure Webhook
**POST** `/webhooks/configure`

Configure webhook endpoints for real-time notifications.

**Request:**
```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["lead_created", "lead_updated", "conversation_ended"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events

#### Lead Created
```json
{
  "event": "lead_created",
  "conversation_id": "conv_123456789",
  "lead_data": {
    "name": "Sarah",
    "company": "TechCorp",
    "score": 85,
    "intent": "buy_soon"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Lead Updated
```json
{
  "event": "lead_updated",
  "conversation_id": "conv_123456789",
  "lead_data": {
    "score": 90,
    "intent": "buy_soon",
    "recommendation": "schedule_demo"
  },
  "timestamp": "2024-01-15T10:35:00Z"
}
```

## SDKs and Libraries

### Python SDK
```python
from ai_lead_qualification import LeadQualificationBot

bot = LeadQualificationBot(api_key="your_api_key")

# Start conversation
conversation = bot.start_conversation()

# Send message
response = bot.send_message(
    conversation_id=conversation.id,
    message="Hi, I'm looking for a CRM solution"
)

print(response.structured_output.score)
```

### JavaScript SDK
```javascript
const LeadQualificationBot = require('ai-lead-qualification');

const bot = new LeadQualificationBot('your_api_key');

// Start conversation
const conversation = await bot.startConversation();

// Send message
const response = await bot.sendMessage(
    conversation.id,
    'Hi, I\'m looking for a CRM solution'
);

console.log(response.structuredOutput.score);
```

## Rate Limiting

Rate limits are applied per API key and reset every hour. When you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

### Rate Limit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642233600
```

## Best Practices

### 1. Conversation Management
- Always start a conversation before sending messages
- Store conversation IDs for session management
- End conversations when users leave

### 2. Error Handling
- Implement proper error handling for all API calls
- Retry failed requests with exponential backoff
- Log errors for debugging

### 3. Rate Limiting
- Monitor rate limit headers
- Implement request queuing for high-volume applications
- Use batch endpoints when possible

### 4. Security
- Keep API keys secure and rotate regularly
- Use HTTPS for all API calls
- Validate webhook signatures

### 5. Performance
- Cache conversation data when appropriate
- Use batch endpoints for multiple operations
- Implement connection pooling

## Support

For API support and questions:

- **Email**: api-support@aileadqualification.com
- **Documentation**: https://docs.aileadqualification.com
- **Status Page**: https://status.aileadqualification.com
- **Community**: https://community.aileadqualification.com
