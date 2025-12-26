"""
Data Processing Module
Handles loading, parsing, and processing of VPN/Tor exit node datasets.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
import logging
from io import StringIO
import json
from src.risk_engine import VPNNode
from src.utils import validate_ip


class DataProcessor:
    """
    Processes VPN/Tor exit node datasets from various formats.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize data processor with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.data_config = config.get('data', {})
        self.max_records = self.data_config.get('max_records', 10000)
        self.required_columns = self.data_config.get('required_columns', ['ip'])
        self.logger = logging.getLogger(__name__)
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame containing the data
        """
        try:
            df = pd.read_csv(file_path, nrows=self.max_records)
            self.logger.info(f"Loaded {len(df)} records from CSV")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load CSV: {e}")
            raise
    
    def load_csv_from_upload(self, uploaded_file) -> pd.DataFrame:
        """
        Load data from uploaded CSV file (Streamlit file uploader).
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            DataFrame containing the data
        """
        try:
            df = pd.read_csv(uploaded_file, nrows=self.max_records)
            self.logger.info(f"Loaded {len(df)} records from uploaded CSV")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load uploaded CSV: {e}")
            raise
    
    def load_json(self, file_path: str) -> pd.DataFrame:
        """
        Load data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            DataFrame containing the data
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict) and 'nodes' in data:
                df = pd.DataFrame(data['nodes'])
            else:
                df = pd.DataFrame([data])
            
            df = df.head(self.max_records)
            self.logger.info(f"Loaded {len(df)} records from JSON")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load JSON: {e}")
            raise
    
    def load_json_from_upload(self, uploaded_file) -> pd.DataFrame:
        """
        Load data from uploaded JSON file (Streamlit file uploader).
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            DataFrame containing the data
        """
        try:
            data = json.load(uploaded_file)
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict) and 'nodes' in data:
                df = pd.DataFrame(data['nodes'])
            else:
                df = pd.DataFrame([data])
            
            df = df.head(self.max_records)
            self.logger.info(f"Loaded {len(df)} records from uploaded JSON")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load uploaded JSON: {e}")
            raise
    
    def validate_dataframe(self, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """
        Validate that DataFrame has required columns.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for required columns
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("DataFrame is empty")
        
        # Validate IP addresses
        if 'ip' in df.columns:
            invalid_ips = df[~df['ip'].apply(validate_ip)]
            if not invalid_ips.empty:
                errors.append(f"Found {len(invalid_ips)} invalid IP addresses")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize DataFrame.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        
        # Remove rows with invalid IPs
        if 'ip' in df.columns:
            df = df[df['ip'].apply(validate_ip)]
        
        # Remove duplicates based on IP
        df = df.drop_duplicates(subset=['ip'], keep='first')
        
        # Standardize column names
        column_mapping = {
            'IP': 'ip',
            'Port': 'port',
            'Country': 'country',
            'ASN': 'asn',
            'ISP': 'isp',
            'First Seen': 'first_seen',
            'Last Seen': 'last_seen',
            'Latitude': 'latitude',
            'Longitude': 'longitude'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Convert port to integer where possible
        if 'port' in df.columns:
            df['port'] = pd.to_numeric(df['port'], errors='coerce').fillna(0).astype(int)
            df.loc[df['port'] == 0, 'port'] = None
        
        # Convert lat/lon to float
        for col in ['latitude', 'longitude']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
        
        self.logger.info(f"Cleaned DataFrame: {len(df)} records remaining")
        return df
    
    def dataframe_to_nodes(self, df: pd.DataFrame) -> List[VPNNode]:
        """
        Convert DataFrame to list of VPNNode objects.
        
        Args:
            df: DataFrame containing node data
            
        Returns:
            List of VPNNode objects
        """
        nodes = []
        
        for _, row in df.iterrows():
            try:
                node = VPNNode(
                    ip=row.get('ip'),
                    port=row.get('port'),
                    country=row.get('country'),
                    region=row.get('region'),
                    city=row.get('city'),
                    asn=row.get('asn'),
                    isp=row.get('isp'),
                    first_seen=row.get('first_seen'),
                    last_seen=row.get('last_seen'),
                    latitude=row.get('latitude'),
                    longitude=row.get('longitude')
                )
                nodes.append(node)
            except Exception as e:
                self.logger.warning(f"Failed to create node for IP {row.get('ip')}: {e}")
                continue
        
        self.logger.info(f"Created {len(nodes)} VPNNode objects")
        return nodes
    
    def nodes_to_dataframe(self, nodes: List[VPNNode]) -> pd.DataFrame:
        """
        Convert list of VPNNode objects to DataFrame.
        
        Args:
            nodes: List of VPNNode objects
            
        Returns:
            DataFrame containing node data
        """
        data = [node.to_dict() for node in nodes]
        df = pd.DataFrame(data)
        return df
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics for the dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing summary statistics
        """
        stats = {
            'total_records': len(df),
            'unique_ips': df['ip'].nunique() if 'ip' in df.columns else 0,
            'countries': df['country'].nunique() if 'country' in df.columns else 0,
            'ports': df['port'].nunique() if 'port' in df.columns else 0,
        }
        
        # Most common countries
        if 'country' in df.columns:
            top_countries = df['country'].value_counts().head(10).to_dict()
            stats['top_countries'] = top_countries
        
        # Most common ports
        if 'port' in df.columns:
            top_ports = df['port'].value_counts().head(10).to_dict()
            stats['top_ports'] = top_ports
        
        # Most common ISPs
        if 'isp' in df.columns:
            top_isps = df['isp'].value_counts().head(10).to_dict()
            stats['top_isps'] = top_isps
        
        return stats
