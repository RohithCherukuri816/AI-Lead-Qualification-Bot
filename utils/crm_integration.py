"""
CRM integration utilities for HubSpot and Salesforce.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

from config.settings import crm_config
from utils.logging import get_logger

logger = get_logger(__name__)

class CRMIntegration:
    """Base class for CRM integrations."""
    
    def __init__(self):
        self.api_key = None
        self.base_url = None
        self.mock_mode = crm_config.mock_mode
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in the CRM."""
        raise NotImplementedError
    
    def update_lead(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing lead in the CRM."""
        raise NotImplementedError
    
    def add_note(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Add a note to a lead."""
        raise NotImplementedError
    
    def log_activity(self, lead_id: str, activity_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Log an activity for a lead."""
        raise NotImplementedError

class HubSpotIntegration(CRMIntegration):
    """HubSpot CRM integration."""
    
    def __init__(self):
        super().__init__()
        self.api_key = crm_config.hubspot_api_key
        self.base_url = crm_config.hubspot_base_url
        
        if not self.api_key and not self.mock_mode:
            logger.warning("HubSpot API key not configured, using mock mode")
            self.mock_mode = True
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in HubSpot."""
        if self.mock_mode:
            return self._mock_create_lead(lead_data)
        
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Transform lead data to HubSpot format
            properties = {
                "email": lead_data.get("email"),
                "firstname": lead_data.get("name", "").split()[0] if lead_data.get("name") else "",
                "lastname": " ".join(lead_data.get("name", "").split()[1:]) if lead_data.get("name") else "",
                "company": lead_data.get("company"),
                "jobtitle": lead_data.get("role"),
                "industry": lead_data.get("industry"),
                "lifecyclestage": "lead",
                "lead_status": "NEW"
            }
            
            payload = {"properties": properties}
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created HubSpot lead: {result.get('id')}")
            
            return {
                "success": True,
                "lead_id": result.get("id"),
                "hubspot_id": result.get("id"),
                "message": "Lead created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating HubSpot lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create lead in HubSpot"
            }
    
    def update_lead(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing lead in HubSpot."""
        if self.mock_mode:
            return self._mock_update_lead(lead_id, lead_data)
        
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{lead_id}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            properties = {}
            if lead_data.get("intent"):
                properties["lead_status"] = lead_data["intent"].upper()
            if lead_data.get("score"):
                properties["hs_lead_score"] = lead_data["score"]
            if lead_data.get("company"):
                properties["company"] = lead_data["company"]
            
            payload = {"properties": properties}
            
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"Updated HubSpot lead: {lead_id}")
            
            return {
                "success": True,
                "lead_id": lead_id,
                "message": "Lead updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating HubSpot lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update lead in HubSpot"
            }
    
    def add_note(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Add a note to a HubSpot lead."""
        if self.mock_mode:
            return self._mock_add_note(lead_id, note)
        
        try:
            url = f"{self.base_url}/crm/v3/objects/notes"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "properties": {
                    "hs_note_body": note,
                    "hs_timestamp": datetime.now().isoformat()
                },
                "associations": [
                    {
                        "to": {
                            "id": lead_id
                        },
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 1
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"Added note to HubSpot lead: {lead_id}")
            
            return {
                "success": True,
                "note_id": response.json().get("id"),
                "message": "Note added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding note to HubSpot lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add note to HubSpot lead"
            }
    
    def _mock_create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock implementation for creating a lead."""
        mock_id = f"mock_hubspot_{datetime.now().timestamp()}"
        
        logger.info(f"Mock: Created HubSpot lead {mock_id} with data: {lead_data}")
        
        return {
            "success": True,
            "lead_id": mock_id,
            "hubspot_id": mock_id,
            "message": "Mock lead created successfully"
        }
    
    def _mock_update_lead(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock implementation for updating a lead."""
        logger.info(f"Mock: Updated HubSpot lead {lead_id} with data: {lead_data}")
        
        return {
            "success": True,
            "lead_id": lead_id,
            "message": "Mock lead updated successfully"
        }
    
    def _mock_add_note(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Mock implementation for adding a note."""
        logger.info(f"Mock: Added note to HubSpot lead {lead_id}: {note}")
        
        return {
            "success": True,
            "note_id": f"mock_note_{datetime.now().timestamp()}",
            "message": "Mock note added successfully"
        }

class SalesforceIntegration(CRMIntegration):
    """Salesforce CRM integration."""
    
    def __init__(self):
        super().__init__()
        self.api_key = crm_config.salesforce_api_key
        self.base_url = crm_config.salesforce_base_url
        
        if not self.api_key and not self.mock_mode:
            logger.warning("Salesforce API key not configured, using mock mode")
            self.mock_mode = True
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in Salesforce."""
        if self.mock_mode:
            return self._mock_create_lead(lead_data)
        
        try:
            url = f"{self.base_url}/services/data/v58.0/sobjects/Lead"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Transform lead data to Salesforce format
            payload = {
                "FirstName": lead_data.get("name", "").split()[0] if lead_data.get("name") else "",
                "LastName": " ".join(lead_data.get("name", "").split()[1:]) if lead_data.get("name") else "Unknown",
                "Email": lead_data.get("email"),
                "Company": lead_data.get("company"),
                "Title": lead_data.get("role"),
                "Industry": lead_data.get("industry"),
                "LeadSource": "AI Qualification Bot",
                "Status": "New"
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created Salesforce lead: {result.get('id')}")
            
            return {
                "success": True,
                "lead_id": result.get("id"),
                "salesforce_id": result.get("id"),
                "message": "Lead created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating Salesforce lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create lead in Salesforce"
            }
    
    def update_lead(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing lead in Salesforce."""
        if self.mock_mode:
            return self._mock_update_lead(lead_id, lead_data)
        
        try:
            url = f"{self.base_url}/services/data/v58.0/sobjects/Lead/{lead_id}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {}
            if lead_data.get("intent"):
                payload["Status"] = lead_data["intent"].upper()
            if lead_data.get("score"):
                payload["Lead_Score__c"] = lead_data["score"]
            if lead_data.get("company"):
                payload["Company"] = lead_data["company"]
            
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"Updated Salesforce lead: {lead_id}")
            
            return {
                "success": True,
                "lead_id": lead_id,
                "message": "Lead updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating Salesforce lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update lead in Salesforce"
            }
    
    def add_note(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Add a note to a Salesforce lead."""
        if self.mock_mode:
            return self._mock_add_note(lead_id, note)
        
        try:
            url = f"{self.base_url}/services/data/v58.0/sobjects/Note"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "Title": "AI Qualification Note",
                "Body": note,
                "ParentId": lead_id
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"Added note to Salesforce lead: {lead_id}")
            
            return {
                "success": True,
                "note_id": response.json().get("id"),
                "message": "Note added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding note to Salesforce lead: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add note to Salesforce lead"
            }
    
    def _mock_create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock implementation for creating a lead."""
        mock_id = f"mock_salesforce_{datetime.now().timestamp()}"
        
        logger.info(f"Mock: Created Salesforce lead {mock_id} with data: {lead_data}")
        
        return {
            "success": True,
            "lead_id": mock_id,
            "salesforce_id": mock_id,
            "message": "Mock lead created successfully"
        }
    
    def _mock_update_lead(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock implementation for updating a lead."""
        logger.info(f"Mock: Updated Salesforce lead {lead_id} with data: {lead_data}")
        
        return {
            "success": True,
            "lead_id": lead_id,
            "message": "Mock lead updated successfully"
        }
    
    def _mock_add_note(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Mock implementation for adding a note."""
        logger.info(f"Mock: Added note to Salesforce lead {lead_id}: {note}")
        
        return {
            "success": True,
            "note_id": f"mock_note_{datetime.now().timestamp()}",
            "message": "Mock note added successfully"
        }

class CRMManager:
    """Manager for multiple CRM integrations."""
    
    def __init__(self):
        self.hubspot = HubSpotIntegration()
        self.salesforce = SalesforceIntegration()
    
    def create_lead_in_all_crms(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a lead in all configured CRMs."""
        results = {}
        
        # Create in HubSpot
        if self.hubspot.api_key or self.hubspot.mock_mode:
            results["hubspot"] = self.hubspot.create_lead(lead_data)
        
        # Create in Salesforce
        if self.salesforce.api_key or self.salesforce.mock_mode:
            results["salesforce"] = self.salesforce.create_lead(lead_data)
        
        return results
    
    def update_lead_in_all_crms(self, lead_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a lead in all configured CRMs."""
        results = {}
        
        # Update in HubSpot
        if self.hubspot.api_key or self.hubspot.mock_mode:
            results["hubspot"] = self.hubspot.update_lead(lead_id, lead_data)
        
        # Update in Salesforce
        if self.salesforce.api_key or self.salesforce.mock_mode:
            results["salesforce"] = self.salesforce.update_lead(lead_id, lead_data)
        
        return results
    
    def add_note_to_all_crms(self, lead_id: str, note: str) -> Dict[str, Any]:
        """Add a note to a lead in all configured CRMs."""
        results = {}
        
        # Add note in HubSpot
        if self.hubspot.api_key or self.hubspot.mock_mode:
            results["hubspot"] = self.hubspot.add_note(lead_id, note)
        
        # Add note in Salesforce
        if self.salesforce.api_key or self.salesforce.mock_mode:
            results["salesforce"] = self.salesforce.add_note(lead_id, note)
        
        return results

# Global CRM manager instance
_crm_manager = None

def get_crm_manager() -> CRMManager:
    """Get the global CRM manager instance."""
    global _crm_manager
    if _crm_manager is None:
        _crm_manager = CRMManager()
    return _crm_manager
