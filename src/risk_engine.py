"""
Risk Assessment Engine
Evaluates VPN/Tor exit nodes and assigns risk levels based on multiple factors.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk level classification."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    UNKNOWN = "Unknown"


@dataclass
class VPNNode:
    """Data model for VPN/Tor exit node."""
    ip: str
    port: Optional[int] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    asn: Optional[str] = None
    isp: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    risk_factors: List[str] = None
    
    def __post_init__(self):
        """Initialize mutable default values."""
        if self.risk_factors is None:
            self.risk_factors = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'ip': self.ip,
            'port': self.port,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'asn': self.asn,
            'isp': self.isp,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level.value,
            'risk_factors': self.risk_factors
        }


class RiskEngine:
    """
    Rule-based risk assessment engine for VPN/Tor exit nodes.
    Uses metadata analysis to determine risk levels.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize risk engine with configuration.
        
        Args:
            config: Configuration dictionary containing risk rules
        """
        self.config = config
        self.high_risk_ports = set(config.get('high_risk_ports', []))
        self.medium_risk_ports = set(config.get('medium_risk_ports', []))
        self.datacenter_keywords = [
            kw.lower() for kw in config.get('datacenter_asn_keywords', [])
        ]
        self.thresholds = config.get('thresholds', {
            'high': 7.0,
            'medium': 4.0,
            'low': 0.0
        })
    
    def assess_node(self, node: VPNNode) -> VPNNode:
        """
        Assess risk level for a VPN node.
        
        Args:
            node: VPNNode instance to assess
            
        Returns:
            Updated VPNNode with risk score and level
        """
        risk_score = 0.0
        risk_factors = []
        
        # Port-based risk assessment
        if node.port:
            if node.port in self.high_risk_ports:
                risk_score += 3.0
                risk_factors.append(f"High-risk port ({node.port})")
            elif node.port in self.medium_risk_ports:
                risk_score += 1.5
                risk_factors.append(f"Medium-risk port ({node.port})")
        
        # ISP/ASN analysis - datacenter hosting indicator
        if node.isp:
            isp_lower = node.isp.lower()
            if any(keyword in isp_lower for keyword in self.datacenter_keywords):
                risk_score += 2.0
                risk_factors.append("Datacenter/hosting provider")
        
        if node.asn:
            asn_lower = node.asn.lower()
            if any(keyword in asn_lower for keyword in self.datacenter_keywords):
                risk_score += 1.5
                risk_factors.append("Datacenter ASN pattern")
        
        # Multiple active ports on same IP (would need historical data)
        # This is a placeholder for demonstration
        
        # Known VPN provider indicators
        if node.isp and 'vpn' in node.isp.lower():
            risk_score += 1.0
            risk_factors.append("Known VPN provider")
        
        # Missing metadata increases uncertainty
        missing_fields = 0
        if not node.country:
            missing_fields += 1
        if not node.isp:
            missing_fields += 1
        if not node.asn:
            missing_fields += 1
        
        if missing_fields >= 2:
            risk_score += 0.5
            risk_factors.append("Insufficient metadata")
        
        # Determine risk level based on thresholds
        if risk_score >= self.thresholds['high']:
            risk_level = RiskLevel.HIGH
        elif risk_score >= self.thresholds['medium']:
            risk_level = RiskLevel.MEDIUM
        elif risk_score > 0:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.UNKNOWN
        
        # Update node
        node.risk_score = round(risk_score, 2)
        node.risk_level = risk_level
        node.risk_factors = risk_factors
        
        return node
    
    def assess_nodes(self, nodes: List[VPNNode]) -> List[VPNNode]:
        """
        Assess multiple nodes.
        
        Args:
            nodes: List of VPNNode instances
            
        Returns:
            List of assessed VPNNode instances
        """
        return [self.assess_node(node) for node in nodes]
    
    def get_statistics(self, nodes: List[VPNNode]) -> Dict:
        """
        Calculate risk statistics for a collection of nodes.
        
        Args:
            nodes: List of assessed VPNNode instances
            
        Returns:
            Dictionary containing risk statistics
        """
        total = len(nodes)
        if total == 0:
            return {
                'total': 0,
                'high_risk': 0,
                'medium_risk': 0,
                'low_risk': 0,
                'unknown': 0,
                'average_score': 0.0
            }
        
        risk_counts = {
            RiskLevel.HIGH: 0,
            RiskLevel.MEDIUM: 0,
            RiskLevel.LOW: 0,
            RiskLevel.UNKNOWN: 0
        }
        
        total_score = 0.0
        
        for node in nodes:
            risk_counts[node.risk_level] += 1
            total_score += node.risk_score
        
        return {
            'total': total,
            'high_risk': risk_counts[RiskLevel.HIGH],
            'medium_risk': risk_counts[RiskLevel.MEDIUM],
            'low_risk': risk_counts[RiskLevel.LOW],
            'unknown': risk_counts[RiskLevel.UNKNOWN],
            'average_score': round(total_score / total, 2) if total > 0 else 0.0,
            'high_risk_pct': round(risk_counts[RiskLevel.HIGH] / total * 100, 1),
            'medium_risk_pct': round(risk_counts[RiskLevel.MEDIUM] / total * 100, 1),
            'low_risk_pct': round(risk_counts[RiskLevel.LOW] / total * 100, 1),
            'unknown_pct': round(risk_counts[RiskLevel.UNKNOWN] / total * 100, 1)
        }
