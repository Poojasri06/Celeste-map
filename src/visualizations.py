"""
Visualization Module
Creates interactive maps and charts for VPN/Tor exit node analysis.
"""

import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd
from typing import List, Dict
import logging
from src.risk_engine import VPNNode, RiskLevel
from src.utils import get_risk_color


class Visualizer:
    """
    Creates visualizations for VPN/Tor exit node data.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize visualizer with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.viz_config = config.get('visualization', {})
        self.map_config = self.viz_config.get('map', {})
        self.colors = self.viz_config.get('colors', {})
        self.logger = logging.getLogger(__name__)
    
    def create_world_map(self, nodes: List[VPNNode], use_clusters: bool = True) -> folium.Map:
        """
        Create interactive world map with VPN exit nodes.
        
        Args:
            nodes: List of VPNNode objects
            use_clusters: Whether to cluster nearby markers
            
        Returns:
            Folium Map object
        """
        # Create base map
        center = self.map_config.get('default_center', [20, 0])
        zoom = self.map_config.get('default_zoom', 2)
        
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        
        # Add alternative tile layers
        folium.TileLayer('CartoDB positron').add_to(m)
        folium.TileLayer('CartoDB dark_matter').add_to(m)
        
        # Prepare marker cluster if enabled
        if use_clusters:
            marker_cluster = MarkerCluster(
                name='VPN/Tor Exit Nodes',
                overlay=True,
                control=True
            ).add_to(m)
        
        # Add markers for each node
        for node in nodes:
            if node.latitude is None or node.longitude is None:
                continue
            
            # Determine marker color based on risk level
            if node.risk_level == RiskLevel.HIGH:
                color = 'red'
                icon = 'exclamation-triangle'
            elif node.risk_level == RiskLevel.MEDIUM:
                color = 'orange'
                icon = 'exclamation-circle'
            elif node.risk_level == RiskLevel.LOW:
                color = 'green'
                icon = 'info-circle'
            else:
                color = 'gray'
                icon = 'question-circle'
            
            # Create popup content
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; min-width: 200px;">
                <b>IP:</b> {node.ip}<br>
                <b>Port:</b> {node.port or 'N/A'}<br>
                <b>Country:</b> {node.country or 'Unknown'}<br>
                <b>City:</b> {node.city or 'Unknown'}<br>
                <b>ISP:</b> {node.isp or 'Unknown'}<br>
                <b>ASN:</b> {node.asn or 'Unknown'}<br>
                <b>Risk Level:</b> <span style="color: {color}; font-weight: bold;">
                    {node.risk_level.value}
                </span><br>
                <b>Risk Score:</b> {node.risk_score}<br>
                {'<b>Risk Factors:</b><br>' + '<br>'.join(f'• {f}' for f in node.risk_factors) if node.risk_factors else ''}
            </div>
            """
            
            popup = folium.Popup(popup_html, max_width=300)
            
            # Create marker
            marker = folium.Marker(
                location=[node.latitude, node.longitude],
                popup=popup,
                tooltip=f"{node.ip} ({node.country})",
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            )
            
            # Add to cluster or directly to map
            if use_clusters:
                marker.add_to(marker_cluster)
            else:
                marker.add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        self.logger.info(f"Created world map with {len(nodes)} nodes")
        return m
    
    def create_heatmap(self, nodes: List[VPNNode]) -> folium.Map:
        """
        Create heat map of VPN exit node density.
        
        Args:
            nodes: List of VPNNode objects
            
        Returns:
            Folium Map object with heat map
        """
        center = self.map_config.get('default_center', [20, 0])
        zoom = self.map_config.get('default_zoom', 2)
        
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles='CartoDB dark_matter'
        )
        
        # Prepare heat map data
        heat_data = []
        for node in nodes:
            if node.latitude and node.longitude:
                # Weight by risk score
                weight = node.risk_score if node.risk_score > 0 else 1.0
                heat_data.append([node.latitude, node.longitude, weight])
        
        if heat_data:
            HeatMap(
                heat_data,
                min_opacity=0.2,
                max_zoom=13,
                radius=15,
                blur=25,
                gradient={
                    0.0: 'blue',
                    0.4: 'lime',
                    0.6: 'yellow',
                    0.8: 'orange',
                    1.0: 'red'
                }
            ).add_to(m)
        
        self.logger.info(f"Created heat map with {len(heat_data)} points")
        return m
    
    def create_risk_distribution_chart(self, nodes: List[VPNNode]) -> go.Figure:
        """
        Create pie chart showing risk level distribution.
        
        Args:
            nodes: List of VPNNode objects
            
        Returns:
            Plotly Figure object
        """
        risk_counts = {
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'Unknown': 0
        }
        
        for node in nodes:
            risk_counts[node.risk_level.value] += 1
        
        colors = [
            self.colors.get('high_risk', '#FF4444'),
            self.colors.get('medium_risk', '#FFA500'),
            self.colors.get('low_risk', '#44FF44'),
            self.colors.get('unknown', '#CCCCCC')
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=list(risk_counts.keys()),
            values=list(risk_counts.values()),
            marker=dict(colors=colors),
            hole=0.3,
            textinfo='label+percent+value',
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Risk Level Distribution',
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_country_distribution_chart(self, nodes: List[VPNNode], top_n: int = 15) -> go.Figure:
        """
        Create bar chart showing country-wise distribution.
        
        Args:
            nodes: List of VPNNode objects
            top_n: Number of top countries to show
            
        Returns:
            Plotly Figure object
        """
        # Count nodes by country
        country_counts = {}
        for node in nodes:
            country = node.country or 'Unknown'
            country_counts[country] = country_counts.get(country, 0) + 1
        
        # Sort and get top N
        sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        countries, counts = zip(*sorted_countries) if sorted_countries else ([], [])
        
        fig = go.Figure(data=[go.Bar(
            x=list(countries),
            y=list(counts),
            marker=dict(
                color=list(counts),
                colorscale='Viridis',
                showscale=True
            ),
            text=list(counts),
            textposition='auto'
        )])
        
        fig.update_layout(
            title=f'Top {top_n} Countries by Exit Node Count',
            xaxis_title='Country',
            yaxis_title='Number of Nodes',
            height=400
        )
        
        return fig
    
    def create_port_distribution_chart(self, nodes: List[VPNNode], top_n: int = 15) -> go.Figure:
        """
        Create bar chart showing port usage distribution.
        
        Args:
            nodes: List of VPNNode objects
            top_n: Number of top ports to show
            
        Returns:
            Plotly Figure object
        """
        port_counts = {}
        for node in nodes:
            if node.port:
                port_counts[node.port] = port_counts.get(node.port, 0) + 1
        
        sorted_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        ports, counts = zip(*sorted_ports) if sorted_ports else ([], [])
        
        fig = go.Figure(data=[go.Bar(
            x=[str(p) for p in ports],
            y=list(counts),
            marker=dict(color='lightblue'),
            text=list(counts),
            textposition='auto'
        )])
        
        fig.update_layout(
            title=f'Top {top_n} Ports by Usage',
            xaxis_title='Port Number',
            yaxis_title='Number of Nodes',
            height=400
        )
        
        return fig
    
    def create_risk_score_histogram(self, nodes: List[VPNNode]) -> go.Figure:
        """
        Create histogram of risk scores.
        
        Args:
            nodes: List of VPNNode objects
            
        Returns:
            Plotly Figure object
        """
        risk_scores = [node.risk_score for node in nodes]
        
        fig = go.Figure(data=[go.Histogram(
            x=risk_scores,
            nbinsx=20,
            marker=dict(
                color='steelblue',
                line=dict(color='white', width=1)
            )
        )])
        
        fig.update_layout(
            title='Risk Score Distribution',
            xaxis_title='Risk Score',
            yaxis_title='Frequency',
            height=400
        )
        
        return fig
    
    def create_geographic_scatter(self, nodes: List[VPNNode]) -> go.Figure:
        """
        Create geographic scatter plot on world map.
        
        Args:
            nodes: List of VPNNode objects
            
        Returns:
            Plotly Figure object
        """
        df_data = []
        
        for node in nodes:
            if node.latitude and node.longitude:
                df_data.append({
                    'lat': node.latitude,
                    'lon': node.longitude,
                    'ip': node.ip,
                    'country': node.country or 'Unknown',
                    'risk_level': node.risk_level.value,
                    'risk_score': node.risk_score,
                    'isp': node.isp or 'Unknown'
                })
        
        df = pd.DataFrame(df_data)
        
        if df.empty:
            # Return empty figure
            fig = go.Figure()
            fig.update_layout(title='No geographic data available')
            return fig
        
        fig = px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            color='risk_level',
            hover_name='ip',
            hover_data=['country', 'risk_score', 'isp'],
            color_discrete_map={
                'High': self.colors.get('high_risk', '#FF4444'),
                'Medium': self.colors.get('medium_risk', '#FFA500'),
                'Low': self.colors.get('low_risk', '#44FF44'),
                'Unknown': self.colors.get('unknown', '#CCCCCC')
            },
            size_max=10
        )
        
        fig.update_layout(
            title='Global VPN/Tor Exit Node Distribution',
            height=600,
            geo=dict(
                showland=True,
                landcolor='lightgray',
                coastlinecolor='white',
                projection_type='natural earth'
            )
        )
        
        return fig
