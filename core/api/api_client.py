import requests
import logging
from core.utils.config_manager import ConfigManager

class APIClient:
    """API Client for making API requests"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.base_url = self.config.get_api_base_url()
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
    
    def get(self, endpoint, params=None, headers=None):
        """Make a GET request to the API"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making GET request to {url}")
        
        try:
            response = self.session.get(url, params=params, headers=headers)
            self.logger.info(f"Response status code: {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Error making GET request: {str(e)}")
            raise
    
    def post(self, endpoint, data=None, json=None, headers=None):
        """Make a POST request to the API"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making POST request to {url}")
        
        try:
            response = self.session.post(url, data=data, json=json, headers=headers)
            self.logger.info(f"Response status code: {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Error making POST request: {str(e)}")
            raise
    
    def put(self, endpoint, data=None, json=None, headers=None):
        """Make a PUT request to the API"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making PUT request to {url}")
        
        try:
            response = self.session.put(url, data=data, json=json, headers=headers)
            self.logger.info(f"Response status code: {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Error making PUT request: {str(e)}")
            raise
    
    def delete(self, endpoint, headers=None):
        """Make a DELETE request to the API"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making DELETE request to {url}")
        
        try:
            response = self.session.delete(url, headers=headers)
            self.logger.info(f"Response status code: {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Error making DELETE request: {str(e)}")
            raise 