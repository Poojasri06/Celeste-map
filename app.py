"""
Celeste Map - Dark Web Awareness & VPN Tracking System
Main Streamlit Application

A privacy-first cybersecurity awareness web application for educational purposes.
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import logging
from typing import List

# Import custom modules
from src.utils import load_config, setup_logging, format_number
from src.data_processor import DataProcessor
from src.geo_analyzer import GeoAnalyzer
from src.risk_engine import RiskEngine, VPNNode
from src.visualizations import Visualizer
from src.education import EducationModule


# Page configuration
st.set_page_config(
    page_title="Celeste Map - Dark Web Awareness",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration
@st.cache_resource
def load_app_config():
    """Load application configuration."""
    return load_config()

config = load_app_config()

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize application components."""
    data_processor = DataProcessor(config)
    geo_analyzer = GeoAnalyzer(config)
    risk_engine = RiskEngine(config.get('risk_engine', {}))
    visualizer = Visualizer(config)
    education = EducationModule()
    return data_processor, geo_analyzer, risk_engine, visualizer, education

data_processor, geo_analyzer, risk_engine, visualizer, education = initialize_components()


def show_privacy_banner():
    """Display privacy and ethics banner."""
    if config.get('app', {}).get('show_privacy_banner', True):
        st.info(config.get('app', {}).get('privacy_text', 
            'This is an educational tool. No user data is collected or stored.'))


def render_home():
    """Render home page."""
    st.title("🗺️ Celeste Map")
    st.subheader("Dark Web Awareness & VPN Tracking System")
    
    show_privacy_banner()
    
    st.markdown("""
    ---
    
    ### Welcome to Celeste Map
    
    This application is designed to raise awareness about **dark web threats**, **VPN/Tor exit node patterns**, 
    and **cybersecurity best practices**.
    
    #### 🎯 What You Can Do:
    
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Analyze VPN Data**
        - Upload VPN/Tor exit node datasets
        - Perform risk assessment
        - View interactive visualizations
        - Understand threat patterns
        """)
    
    with col2:
        st.markdown("""
        **🗺️ Explore Maps**
        - Interactive world map
        - Geographic distribution
        - Risk-based clustering
        - Heat map visualization
        """)
    
    with col3:
        st.markdown("""
        **📚 Learn & Stay Safe**
        - Dark web awareness
        - VPN misuse patterns
        - Cybersecurity best practices
        - Protection strategies
        """)
    
    st.markdown("""
    ---
    
    ### 🚀 Getting Started
    
    1. **Upload Data:** Go to the "Data Upload" page to load VPN/Tor exit node datasets
    2. **Analyze:** View the Dashboard for insights and statistics
    3. **Visualize:** Explore the interactive Map View
    4. **Learn:** Visit the Education section for cybersecurity awareness
    
    ### ⚠️ Important Disclaimer
    
    This tool is for **educational and research purposes only**:
    
    - ✅ Analyzes publicly available exit node data
    - ✅ Helps organizations understand security risks
    - ✅ Promotes cybersecurity awareness
    - ❌ Does NOT track individual users
    - ❌ Does NOT attempt deanonymization
    - ❌ Should NOT be used for illegal surveillance
    
    Using VPN or Tor is **legal** and **legitimate** for privacy protection.
    """)
    
    st.success("""
    **Ready to begin?** Use the sidebar to navigate to different sections of the application.
    """)


def render_data_upload():
    """Render data upload page."""
    st.title("📤 Data Upload & Processing")
    
    show_privacy_banner()
    
    st.markdown("""
    Upload your VPN/Tor exit node datasets in **CSV** or **JSON** format.
    
    ### Required Format:
    - **CSV:** Must contain an `ip` column (required)
    - **Optional columns:** `port`, `country`, `asn`, `isp`, `first_seen`, `last_seen`, `latitude`, `longitude`
    
    ### Sample CSV Format:
    ```
    ip,port,country,asn,isp,first_seen,last_seen
    1.2.3.4,443,US,AS12345,Example ISP,2025-01-01,2025-12-25
    ```
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'json'],
        help="Upload VPN/Tor exit node data in CSV or JSON format"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        use_api_enrichment = st.checkbox(
            "Enable API enrichment",
            value=False,
            help="Use external APIs to enrich missing geolocation data (slower)"
        )
    
    with col2:
        max_api_calls = st.number_input(
            "Max API calls",
            min_value=0,
            max_value=1000,
            value=50,
            help="Limit the number of API calls to avoid rate limits"
        )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Loading data..."):
                # Load data based on file type
                if uploaded_file.name.endswith('.csv'):
                    df = data_processor.load_csv_from_upload(uploaded_file)
                else:
                    df = data_processor.load_json_from_upload(uploaded_file)
                
                st.success(f"✅ Loaded {len(df)} records from {uploaded_file.name}")
                
                # Validate data
                is_valid, errors = data_processor.validate_dataframe(df)
                
                if not is_valid:
                    st.error("❌ Data validation failed:")
                    for error in errors:
                        st.write(f"- {error}")
                    return
                
                # Clean data
                df = data_processor.clean_dataframe(df)
                st.info(f"🧹 Cleaned data: {len(df)} records remaining")
                
                # Show preview
                with st.expander("📋 Data Preview", expanded=True):
                    st.dataframe(df.head(20), use_container_width=True)
                
                # Convert to nodes
                with st.spinner("Converting to node objects..."):
                    nodes = data_processor.dataframe_to_nodes(df)
                
                # Enrich with geolocation
                with st.spinner("Enriching with geolocation data..."):
                    nodes = geo_analyzer.enrich_nodes(
                        nodes, 
                        use_api=use_api_enrichment,
                        max_api_calls=max_api_calls
                    )
                
                # Perform risk assessment
                with st.spinner("Performing risk assessment..."):
                    nodes = risk_engine.assess_nodes(nodes)
                
                # Store in session state
                st.session_state['nodes'] = nodes
                st.session_state['df'] = data_processor.nodes_to_dataframe(nodes)
                
                st.success("✅ Data processed successfully!")
                
                # Show statistics
                stats = risk_engine.get_statistics(nodes)
                
                st.markdown("### 📊 Dataset Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Nodes", format_number(stats['total']))
                    st.metric("High Risk", format_number(stats['high_risk']))
                
                with col2:
                    st.metric("Average Risk Score", stats['average_score'])
                    st.metric("Medium Risk", format_number(stats['medium_risk']))
                
                with col3:
                    st.metric("High Risk %", f"{stats['high_risk_pct']}%")
                    st.metric("Low Risk", format_number(stats['low_risk']))
                
                with col4:
                    st.metric("Medium Risk %", f"{stats['medium_risk_pct']}%")
                    st.metric("Unknown", format_number(stats['unknown']))
                
                st.info("💡 **Tip:** Navigate to the Dashboard or Map View to visualize this data!")
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logger.error(f"File processing error: {e}", exc_info=True)
    
    else:
        st.info("👆 Upload a file to get started")


def render_dashboard():
    """Render analytics dashboard."""
    st.title("📊 Analytics Dashboard")
    
    show_privacy_banner()
    
    # Check if data is loaded
    if 'nodes' not in st.session_state or not st.session_state['nodes']:
        st.warning("⚠️ No data loaded. Please upload data first in the 'Data Upload' section.")
        return
    
    nodes: List[VPNNode] = st.session_state['nodes']
    
    # Summary statistics
    st.markdown("### 📈 Overview")
    
    stats = risk_engine.get_statistics(nodes)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Nodes", format_number(stats['total']))
    with col2:
        st.metric("High Risk", format_number(stats['high_risk']), 
                  delta=f"{stats['high_risk_pct']}%", delta_color="inverse")
    with col3:
        st.metric("Medium Risk", format_number(stats['medium_risk']),
                  delta=f"{stats['medium_risk_pct']}%", delta_color="off")
    with col4:
        st.metric("Low Risk", format_number(stats['low_risk']),
                  delta=f"{stats['low_risk_pct']}%", delta_color="normal")
    with col5:
        st.metric("Avg Risk Score", stats['average_score'])
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Risk Level Distribution")
        fig = visualizer.create_risk_distribution_chart(nodes)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Risk Score Distribution")
        fig = visualizer.create_risk_score_histogram(nodes)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic and port analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Top Countries")
        fig = visualizer.create_country_distribution_chart(nodes, top_n=15)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔌 Port Usage")
        fig = visualizer.create_port_distribution_chart(nodes, top_n=15)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic scatter plot
    st.markdown("### 🗺️ Geographic Distribution")
    fig = visualizer.create_geographic_scatter(nodes)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed data table
    with st.expander("📋 Detailed Node Data", expanded=False):
        df = st.session_state['df']
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                options=['High', 'Medium', 'Low', 'Unknown'],
                default=['High', 'Medium', 'Low', 'Unknown']
            )
        
        with col2:
            countries = df['country'].unique().tolist()
            country_filter = st.multiselect(
                "Filter by Country",
                options=countries,
                default=countries[:10] if len(countries) > 10 else countries
            )
        
        with col3:
            min_risk_score = st.slider(
                "Minimum Risk Score",
                min_value=0.0,
                max_value=float(df['risk_score'].max()),
                value=0.0
            )
        
        # Apply filters
        filtered_df = df[
            (df['risk_level'].isin(risk_filter)) &
            (df['country'].isin(country_filter)) &
            (df['risk_score'] >= min_risk_score)
        ]
        
        st.write(f"Showing {len(filtered_df)} of {len(df)} nodes")
        st.dataframe(filtered_df, use_container_width=True, height=400)


def render_map_view():
    """Render interactive map view."""
    st.title("🗺️ Interactive Map View")
    
    show_privacy_banner()
    
    # Check if data is loaded
    if 'nodes' not in st.session_state or not st.session_state['nodes']:
        st.warning("⚠️ No data loaded. Please upload data first in the 'Data Upload' section.")
        return
    
    nodes: List[VPNNode] = st.session_state['nodes']
    
    # Map options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        map_type = st.radio(
            "Map Type",
            options=["Marker Map", "Heat Map"],
            horizontal=True
        )
    
    with col2:
        if map_type == "Marker Map":
            use_clusters = st.checkbox("Use Clustering", value=True)
    
    # Create map
    with st.spinner("Generating map..."):
        if map_type == "Heat Map":
            map_obj = visualizer.create_heatmap(nodes)
        else:
            use_clusters = use_clusters if map_type == "Marker Map" else True
            map_obj = visualizer.create_world_map(nodes, use_clusters=use_clusters)
    
    # Display map
    st_folium(map_obj, width=1400, height=600)
    
    # Map legend
    st.markdown("""
    ### 🎨 Map Legend
    
    - 🔴 **Red:** High Risk nodes (risk score ≥ 7.0)
    - 🟠 **Orange:** Medium Risk nodes (risk score 4.0 - 6.9)
    - 🟢 **Green:** Low Risk nodes (risk score 0.1 - 3.9)
    - ⚪ **Gray:** Unknown/No risk factors identified
    
    Click on markers to see detailed information about each node.
    """)


def render_education():
    """Render education section."""
    st.title("📚 Cybersecurity Education")
    
    # Education tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🕵️ Dark Web Awareness",
        "🔒 VPN & Tor",
        "🛡️ Safe Practices",
        "📚 Resources"
    ])
    
    with tab1:
        education.render_dark_web_awareness()
    
    with tab2:
        education.render_vpn_misuse_content()
    
    with tab3:
        education.render_safe_practices()
    
    with tab4:
        education.render_resources()


def validate_ip(ip: str) -> bool:
    """Validate IP address format."""
    import re
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(ip_pattern, ip):
        return False
    
    # Check octets are 0-255
    parts = ip.split('.')
    for part in parts:
        if int(part) > 255:
            return False
    
    return True


def render_ip_lookup():
    """Render IP lookup page."""
    st.title("🔍 IP Lookup")
    st.subheader("Find Information About Any IP Address")
    
    show_privacy_banner()
    
    st.markdown("""
    Enter a single IP address to find out:
    - **Location** - Country, Region, City
    - **ISP Information** - Internet Service Provider and ASN
    - **Risk Level** - Assessment based on patterns
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ip_input = st.text_input(
            "Enter IP Address",
            placeholder="e.g., 8.8.8.8",
            label_visibility="collapsed"
        )
    
    with col2:
        lookup_button = st.button("🔍 Lookup", use_container_width=True)
    
    st.markdown("---")
    
    if lookup_button and ip_input:
        # Validate IP
        if not validate_ip(ip_input):
            st.error("❌ Invalid IP address format. Please enter a valid IP address.")
            return
        
        with st.spinner(f"Looking up {ip_input}..."):
            try:
                # Use free API (no key required)
                ip_data = geo_analyzer.lookup_ip_free_api(ip_input)
                
                if ip_data:
                    # Create VPNNode for risk assessment
                    node = VPNNode(
                        ip=ip_input,
                        country=ip_data.get('country'),
                        region=ip_data.get('region'),
                        city=ip_data.get('city'),
                        latitude=ip_data.get('latitude'),
                        longitude=ip_data.get('longitude'),
                        asn=ip_data.get('asn'),
                        isp=ip_data.get('isp')
                    )
                    
                    # Calculate risk using risk engine
                    assessed = risk_engine.assess_node(node)
                    risk_score = assessed.risk_score
                    risk_level = assessed.risk_level.value
                    risk_factors = assessed.risk_factors
                    
                    # Store in session state for persistence
                    st.session_state['ip_lookup_data'] = {
                        'ip': ip_input,
                        'ip_data': ip_data,
                        'risk_score': risk_score,
                        'risk_level': risk_level,
                        'risk_factors': risk_factors
                    }
                
                else:
                    st.error(f"❌ Could not find information for IP: {ip_input}")
                    st.info("The IP address may not be valid or the lookup service is temporarily unavailable.")
                    st.session_state.pop('ip_lookup_data', None)
            
            except Exception as e:
                st.error(f"❌ Error during lookup: {str(e)}")
                logger.error(f"IP Lookup error for {ip_input}: {e}")
                st.session_state.pop('ip_lookup_data', None)
    
    # Display stored results if available
    if 'ip_lookup_data' in st.session_state:
        data = st.session_state['ip_lookup_data']
        ip_input = data['ip']
        ip_data = data['ip_data']
        risk_score = data['risk_score']
        risk_level = data['risk_level']
        risk_factors = data['risk_factors']
        
        st.success("✅ IP Information Found!")
        
        # Display in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Risk Level", risk_level)
            st.metric("Risk Score", f"{risk_score:.1f}/10")
        
        with col2:
            st.metric("Country", ip_data.get('country', 'Unknown'))
            st.metric("Region", ip_data.get('region', 'Unknown'))
            st.metric("City", ip_data.get('city', 'Unknown'))
        
        with col3:
            st.metric("ISP", ip_data.get('isp', 'Unknown')[:25])
            st.metric("ASN", ip_data.get('asn', 'Unknown'))
        
        st.markdown("---")
        
        # Display detailed info
        st.subheader("📍 Detailed Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.markdown(f"""
            **IP Address:** `{ip_input}`
            
            **Location:**
            - Country: {ip_data.get('country', 'Unknown')}
            - Region: {ip_data.get('region', 'Unknown')}
            - City: {ip_data.get('city', 'Unknown')}
            - Latitude: {ip_data.get('latitude', 'N/A')}
            - Longitude: {ip_data.get('longitude', 'N/A')}
            """)
        
        with info_col2:
            st.markdown(f"""
            **Network Information:**
            - ISP: {ip_data.get('isp', 'Unknown')}
            - ASN: {ip_data.get('asn', 'Unknown')}
            
            **Risk Assessment:**
            - Risk Level: {risk_level}
            - Risk Score: {risk_score:.1f}/10
            - Risk Factors: {', '.join(risk_factors) if risk_factors else 'None'}
            """)
        
        # Show on map if coordinates available
        if ip_data.get('latitude') and ip_data.get('longitude'):
            st.markdown("---")
            st.subheader("🗺️ Location on Map")
            
            # Create a simple map
            import folium
            
            # Determine marker color based on risk
            if risk_score >= 7:
                marker_color = 'red'
            elif risk_score >= 4:
                marker_color = 'orange'
            else:
                marker_color = 'green'
            
            m = folium.Map(
                location=[ip_data.get('latitude'), ip_data.get('longitude')],
                zoom_start=5,
                tiles='OpenStreetMap'
            )
            
            folium.Marker(
                location=[ip_data.get('latitude'), ip_data.get('longitude')],
                popup=f"{ip_input}<br>{ip_data.get('city', 'Unknown')}, {ip_data.get('country', 'Unknown')}",
                tooltip=f"Risk: {risk_level}",
                icon=folium.Icon(color=marker_color, icon='info-sign')
            ).add_to(m)
            
            st_folium(m, width=700, height=400)
        
        # Clear button
        st.markdown("---")
        if st.button("🗑️ Clear Results"):
            st.session_state.pop('ip_lookup_data', None)
            st.rerun()


def render_about():
    """Render about page."""
    st.title("ℹ️ About Celeste Map")
    
    st.markdown("""
    ## Dark Web Awareness & VPN Tracking System
    
    **Version:** 1.0.0  
    **Purpose:** Educational & Awareness
    
    ### 🎯 Mission
    
    Celeste Map is designed to raise awareness about cybersecurity threats related to:
    - Dark web credential trading
    - VPN and Tor exit node patterns
    - Internet privacy and security
    
    ### 🔒 Privacy & Ethics
    
    This application strictly adheres to ethical principles:
    
    ✅ **What We Do:**
    - Analyze publicly available VPN/Tor exit node data
    - Perform metadata-based risk assessment
    - Provide educational content
    - Visualize threat patterns
    
    ❌ **What We DON'T Do:**
    - Track individual users
    - Attempt deanonymization
    - Collect personal data
    - Perform illegal surveillance
    - Store or share user information
    
    ### 🛠️ Technology Stack
    
    - **Frontend:** Streamlit
    - **Backend:** Python 3.8+
    - **Data Processing:** Pandas, NumPy
    - **Visualization:** Plotly, Folium
    - **APIs:** IPinfo, IP-API (optional)
    
    ### 📄 License
    
    MIT License - This software is free to use for educational purposes.
    
    ### ⚠️ Disclaimer
    
    This software is provided "as is" for educational purposes only. The developers are not 
    responsible for any misuse of this tool. Always respect privacy laws and regulations in 
    your jurisdiction.
    
    ### 🤝 Contributing
    
    Contributions are welcome! Please ensure all contributions align with the educational and 
    ethical goals of this project.
    
    ---
    
    **Developed with ❤️ for cybersecurity awareness and education.**
    """)


def main():
    """Main application function."""
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        [
            "🏠 Home",
            "🔍 IP Lookup",
            "📤 Data Upload",
            "📊 Dashboard",
            "🗺️ Map View",
            "📚 Education",
            "ℹ️ About"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats in sidebar if data is loaded
    if 'nodes' in st.session_state and st.session_state['nodes']:
        st.sidebar.markdown("### 📊 Current Dataset")
        stats = risk_engine.get_statistics(st.session_state['nodes'])
        st.sidebar.metric("Total Nodes", format_number(stats['total']))
        st.sidebar.metric("High Risk", format_number(stats['high_risk']))
        st.sidebar.metric("Avg Risk", stats['average_score'])
        
        if st.sidebar.button("🗑️ Clear Data"):
            st.session_state.pop('nodes', None)
            st.session_state.pop('df', None)
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🔒 Privacy Notice
    This is an educational tool.  
    No user data is collected.
    """)
    
    # Route to selected page
    if page == "🏠 Home":
        render_home()
    elif page == "🔍 IP Lookup":
        render_ip_lookup()
    elif page == "📤 Data Upload":
        render_data_upload()
    elif page == "📊 Dashboard":
        render_dashboard()
    elif page == "🗺️ Map View":
        render_map_view()
    elif page == "📚 Education":
        render_education()
    elif page == "ℹ️ About":
        render_about()


if __name__ == "__main__":
    main()
