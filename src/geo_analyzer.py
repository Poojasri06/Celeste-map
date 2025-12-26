"""
Geolocation and Metadata Analysis Module
Performs IP geolocation, ASN lookups, and metadata enrichment.
"""

import requests
import logging
from typing import Dict, Optional, List
import time
from src.risk_engine import VPNNode


class GeoAnalyzer:
    """
    Analyzes IP addresses to extract geolocation and metadata.
    Supports multiple data sources with fallback mechanisms.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize geo analyzer with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api_config = config.get('api', {})
        self.ipinfo_token = self.api_config.get('ipinfo_token', '')
        self.rate_limit = self.api_config.get('rate_limit', {})
        self.requests_count = 0
        self.last_request_time = time.time()
        self.logger = logging.getLogger(__name__)
        
        # Known country code to name mapping (subset)
        self.country_names = {
            'US': 'United States', 'GB': 'United Kingdom', 'DE': 'Germany',
            'FR': 'France', 'NL': 'Netherlands', 'CA': 'Canada',
            'AU': 'Australia', 'JP': 'Japan', 'CN': 'China',
            'IN': 'India', 'BR': 'Brazil', 'RU': 'Russia',
            'ES': 'Spain', 'IT': 'Italy', 'SE': 'Sweden',
            'NO': 'Norway', 'FI': 'Finland', 'DK': 'Denmark',
            'PL': 'Poland', 'CH': 'Switzerland', 'AT': 'Austria',
            'BE': 'Belgium', 'IE': 'Ireland', 'SG': 'Singapore',
            'HK': 'Hong Kong', 'KR': 'South Korea', 'TW': 'Taiwan',
            'MX': 'Mexico', 'AR': 'Argentina', 'ZA': 'South Africa'
        }
    
    def _respect_rate_limit(self):
        """Implement rate limiting for API requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        # Simple rate limiting: wait at least 0.1 seconds between requests
        if time_since_last_request < 0.1:
            time.sleep(0.1 - time_since_last_request)
        
        self.last_request_time = time.time()
        self.requests_count += 1
    
    def lookup_ip_ipinfo(self, ip: str) -> Optional[Dict]:
        """
        Lookup IP information using IPInfo API.
        
        Args:
            ip: IP address to lookup
            
        Returns:
            Dictionary containing IP information or None
        """
        if not self.ipinfo_token:
            return None
        
        try:
            self._respect_rate_limit()
            
            url = f"https://ipinfo.io/{ip}"
            headers = {'Authorization': f'Bearer {self.ipinfo_token}'}
            
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'latitude': float(data.get('loc', '0,0').split(',')[0]),
                    'longitude': float(data.get('loc', '0,0').split(',')[1]),
                    'asn': data.get('org', '').split()[0] if data.get('org') else None,
                    'isp': data.get('org', '')
                }
            else:
                self.logger.warning(f"IPInfo lookup failed for {ip}: {response.status_code}")
                return None
        
        except Exception as e:
            self.logger.error(f"IPInfo lookup error for {ip}: {e}")
            return None
    
    def lookup_ip_free_api(self, ip: str) -> Optional[Dict]:
        """
        Lookup IP information using free IP API (no key required).
        
        Args:
            ip: IP address to lookup
            
        Returns:
            Dictionary containing IP information or None
        """
        try:
            self._respect_rate_limit()
            
            # Using ip-api.com (free, no key required, 45 requests/minute)
            url = f"http://ip-api.com/json/{ip}"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    return {
                        'country': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'asn': data.get('as', '').split()[0] if data.get('as') else None,
                        'isp': data.get('isp', '')
                    }
            
            return None
        
        except Exception as e:
            self.logger.error(f"Free API lookup error for {ip}: {e}")
            return None
    
    def enrich_node(self, node: VPNNode, use_api: bool = False) -> VPNNode:
        """
        Enrich node with geolocation and metadata.
        
        Args:
            node: VPNNode to enrich
            use_api: Whether to use external APIs for lookup
            
        Returns:
            Enriched VPNNode
        """
        # If node already has all required fields, skip enrichment
        if node.latitude and node.longitude and node.country:
            return node
        
        if not use_api:
            # Use fallback/mock data for demonstration
            return self._apply_fallback_data(node)
        
        # Try API lookup
        ip_data = None
        
        if self.ipinfo_token:
            ip_data = self.lookup_ip_ipinfo(node.ip)
        
        if not ip_data:
            ip_data = self.lookup_ip_free_api(node.ip)
        
        if ip_data:
            node.country = node.country or ip_data.get('country')
            node.region = node.region or ip_data.get('region')
            node.city = node.city or ip_data.get('city')
            node.latitude = node.latitude or ip_data.get('latitude')
            node.longitude = node.longitude or ip_data.get('longitude')
            node.asn = node.asn or ip_data.get('asn')
            node.isp = node.isp or ip_data.get('isp')
        else:
            # Use fallback if API lookup fails
            node = self._apply_fallback_data(node)
        
        return node
    
    def _apply_fallback_data(self, node: VPNNode) -> VPNNode:
        """
        Apply fallback/estimated data when API is not available.
        
        Args:
            node: VPNNode to enrich
            
        Returns:
            Enriched VPNNode with estimated data
        """
        # Simple heuristic: use IP's first octet to estimate region
        # This is for demonstration only and not accurate
        try:
            first_octet = int(node.ip.split('.')[0])
            
            # Rough regional mapping (demonstration only)
            if not node.country:
                if first_octet < 50:
                    node.country = 'US'
                elif first_octet < 100:
                    node.country = 'EU'
                elif first_octet < 150:
                    node.country = 'CN'
                else:
                    node.country = 'Unknown'
            
            # Assign approximate coordinates if missing
            if not node.latitude or not node.longitude:
                coords = self._get_country_coordinates(node.country)
                node.latitude = coords[0]
                node.longitude = coords[1]
        
        except Exception as e:
            self.logger.warning(f"Fallback enrichment failed for {node.ip}: {e}")
        
        return node
    
    def _get_country_coordinates(self, country_code: str) -> tuple:
        """
        Get approximate coordinates for a country code.
        
        Args:
            country_code: ISO country code
            
        Returns:
            Tuple of (latitude, longitude)
        """
        # Approximate center coordinates for common countries
        coordinates = {
            'US': (37.0902, -95.7129),
            'GB': (55.3781, -3.4360),
            'DE': (51.1657, 10.4515),
            'FR': (46.2276, 2.2137),
            'NL': (52.1326, 5.2913),
            'CA': (56.1304, -106.3468),
            'AU': (-25.2744, 133.7751),
            'JP': (36.2048, 138.2529),
            'CN': (35.8617, 104.1954),
            'IN': (20.5937, 78.9629),
            'BR': (-14.2350, -51.9253),
            'RU': (61.5240, 105.3188),
            'SG': (1.3521, 103.8198),
            'EU': (50.8503, 4.3517),  # Brussels as generic EU
        }
        
        return coordinates.get(country_code, (0, 0))
    
    def enrich_nodes(self, nodes: List[VPNNode], use_api: bool = False, 
                     max_api_calls: int = 100) -> List[VPNNode]:
        """
        Enrich multiple nodes with geolocation data.
        
        Args:
            nodes: List of VPNNodes to enrich
            use_api: Whether to use external APIs
            max_api_calls: Maximum number of API calls to make
            
        Returns:
            List of enriched VPNNodes
        """
        enriched_nodes = []
        api_calls_made = 0
        
        for node in nodes:
            # Limit API calls to avoid rate limits and costs
            should_use_api = use_api and api_calls_made < max_api_calls
            
            enriched_node = self.enrich_node(node, use_api=should_use_api)
            enriched_nodes.append(enriched_node)
            
            if should_use_api and enriched_node.latitude:
                api_calls_made += 1
        
        self.logger.info(f"Enriched {len(enriched_nodes)} nodes ({api_calls_made} API calls)")
        return enriched_nodes
    
    def get_country_name(self, country_code: str) -> str:
        """
        Get full country name from country code.
        
        Args:
            country_code: ISO country code
            
        Returns:
            Full country name or code if not found
        """
        return self.country_names.get(country_code, country_code)
