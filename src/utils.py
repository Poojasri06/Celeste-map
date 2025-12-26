"""
Utility Functions
Common helper functions used across the application.
"""

import yaml
import os
from typing import Dict, Optional
import logging


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """
    Load application configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Return default configuration if file doesn't exist
            return get_default_config()
    except Exception as e:
        logging.warning(f"Failed to load config: {e}. Using defaults.")
        return get_default_config()


def get_default_config() -> Dict:
    """
    Get default configuration.
    
    Returns:
        Default configuration dictionary
    """
    return {
        'api': {
            'ipinfo_token': '',
            'rate_limit': {
                'requests_per_minute': 50,
                'requests_per_day': 1000
            }
        },
        'risk_engine': {
            'high_risk_ports': [22, 23, 3389, 4444, 5555, 8080, 8888],
            'medium_risk_ports': [80, 443, 8000, 8443],
            'high_risk_countries': [],
            'datacenter_asn_keywords': [
                'hosting', 'datacenter', 'cloud', 'virtual', 'vpn', 'proxy'
            ],
            'thresholds': {
                'high': 7.0,
                'medium': 4.0,
                'low': 0.0
            }
        },
        'visualization': {
            'map': {
                'default_zoom': 2,
                'default_center': [20, 0],
                'cluster_radius': 50,
                'max_cluster_radius': 80
            },
            'colors': {
                'high_risk': '#FF4444',
                'medium_risk': '#FFA500',
                'low_risk': '#44FF44',
                'unknown': '#CCCCCC'
            }
        },
        'data': {
            'max_records': 10000,
            'cache_timeout': 3600,
            'required_columns': ['ip'],
            'optional_columns': [
                'port', 'country', 'asn', 'isp', 
                'first_seen', 'last_seen'
            ]
        },
        'app': {
            'title': 'Celeste Map - Dark Web Awareness & VPN Tracking',
            'page_icon': '🗺️',
            'layout': 'wide',
            'initial_sidebar_state': 'expanded',
            'show_privacy_banner': True,
            'privacy_text': (
                'This is an educational tool. No user data is collected or stored. '
                'All analysis is performed on publicly available datasets only.'
            )
        }
    }


def validate_ip(ip: str) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid, False otherwise
    """
    try:
        import ipaddress
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def format_number(num: int) -> str:
    """
    Format number with thousand separators.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted string
    """
    return f"{num:,}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    return text if len(text) <= max_length else text[:max_length-3] + "..."


def get_risk_color(risk_level: str, config: Dict) -> str:
    """
    Get color for risk level.
    
    Args:
        risk_level: Risk level string
        config: Configuration dictionary
        
    Returns:
        Color hex code
    """
    colors = config.get('visualization', {}).get('colors', {})
    risk_level_lower = risk_level.lower()
    
    if 'high' in risk_level_lower:
        return colors.get('high_risk', '#FF4444')
    elif 'medium' in risk_level_lower:
        return colors.get('medium_risk', '#FFA500')
    elif 'low' in risk_level_lower:
        return colors.get('low_risk', '#44FF44')
    else:
        return colors.get('unknown', '#CCCCCC')


def setup_logging(level: str = "INFO"):
    """
    Setup application logging.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
