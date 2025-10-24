#!/usr/bin/env python3
"""
Simple test script for the AI Lead Qualification Bot.
"""

import json
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.llm_pipeline import get_llm_pipeline
from models.vector_store import get_vector_store
from models.predictive_model import get_predictive_model
from utils.crm_integration import get_crm_manager
from config.settings import validate_config

def test_configuration():
    """Test that the configuration is valid."""
    print("🔧 Testing configuration...")
    
    if validate_config():
        print("✅ Configuration is valid")
        return True
    else:
        print("❌ Configuration validation failed")
        return False

def test_vector_store():
    """Test the vector store functionality."""
    print("\n📚 Testing vector store...")
    
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        print(f"✅ Vector store initialized with {stats['total_documents']} documents")
        return True
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False

def test_predictive_model():
    """Test the predictive model functionality."""
    print("\n🤖 Testing predictive model...")
    
    try:
        model = get_predictive_model()
        
        # Test with sample conversation data
        sample_data = {
            'messages': [
                {'role': 'user', 'content': 'Hi, I need a CRM solution for our 50-person team'},
                {'role': 'assistant', 'content': 'Hello! I can help with that. What challenges are you facing?'},
                {'role': 'user', 'content': 'We have a budget of $100k and need to decide within a month'}
            ],
            'lead_info': {
                'name': 'Sarah',
                'company': 'TechCorp',
                'role': 'Sales Director',
                'industry': 'Technology',
                'team_size': 50
            },
            'behavioral_data': {
                'pages_visited': 5,
                'trial_usage': 0.2,
                'email_opens': 3,
                'demo_requested': True
            }
        }
        
        prediction = model.predict(sample_data)
        print(f"✅ Predictive model working - Score: {prediction['score']}, Intent: {prediction['intent']}")
        return True
    except Exception as e:
        print(f"❌ Predictive model test failed: {e}")
        return False

def test_crm_integration():
    """Test the CRM integration functionality."""
    print("\n🔗 Testing CRM integration...")
    
    try:
        crm_manager = get_crm_manager()
        
        # Test with sample lead data
        sample_lead = {
            'name': 'Sarah Johnson',
            'email': 'sarah@techcorp.com',
            'company': 'TechCorp',
            'role': 'Sales Director',
            'industry': 'Technology',
            'intent': 'buy_soon',
            'score': 85,
            'tags': ['enterprise', 'high_priority']
        }
        
        results = crm_manager.create_lead_in_all_crms(sample_lead)
        print(f"✅ CRM integration working - {len(results)} CRM systems configured")
        return True
    except Exception as e:
        print(f"❌ CRM integration test failed: {e}")
        return False

def test_conversation():
    """Test a sample conversation."""
    print("\n💬 Testing conversation flow...")
    
    try:
        llm_pipeline = get_llm_pipeline()
        
        # Start a conversation
        conversation_id = "test_conv_123"
        greeting = llm_pipeline.start_conversation(conversation_id)
        print(f"✅ Conversation started: {greeting[:50]}...")
        
        # Send a test message
        test_message = "Hi, I'm Sarah from TechCorp. We're looking for a CRM solution for our 50-person sales team. We're currently using Salesforce but it's too expensive and complex for our needs."
        
        result = llm_pipeline.process_message(conversation_id, test_message)
        
        print(f"✅ Message processed successfully")
        print(f"   Response: {result['response'][:100]}...")
        print(f"   Score: {result['structured_output']['score']}")
        print(f"   Intent: {result['structured_output']['intent']}")
        print(f"   Recommendation: {result['structured_output']['recommended_action']}")
        
        return True
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        return False

def test_sample_data():
    """Test with sample conversation data."""
    print("\n📊 Testing with sample data...")
    
    try:
        # Load sample conversations
        with open('examples/sample_conversations.json', 'r') as f:
            sample_conversations = json.load(f)
        
        llm_pipeline = get_llm_pipeline()
        
        for i, conv in enumerate(sample_conversations[:2]):  # Test first 2 conversations
            conversation_id = f"sample_conv_{i}"
            
            # Start conversation
            llm_pipeline.start_conversation(conversation_id)
            
            # Process first message
            first_message = conv['messages'][0]['content']
            result = llm_pipeline.process_message(conversation_id, first_message)
            
            print(f"✅ Sample conversation {i+1}: Score {result['structured_output']['score']}, Intent {result['structured_output']['intent']}")
        
        return True
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting AI Lead Qualification Bot Tests\n")
    
    tests = [
        ("Configuration", test_configuration),
        ("Vector Store", test_vector_store),
        ("Predictive Model", test_predictive_model),
        ("CRM Integration", test_crm_integration),
        ("Conversation Flow", test_conversation),
        ("Sample Data", test_sample_data)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print(f"\n📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration and dependencies.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
