# Celeste Map - Dark Web Awareness & VPN Tracking System

A privacy-first cybersecurity awareness web application for educational purposes.

## 🎯 Purpose

This application is designed to raise awareness about:
- Dark web credential trading
- VPN and Tor exit node patterns
- Safe internet practices
- Cybersecurity threats

**Important:** This is an educational tool only. It does NOT perform user tracking, identity deanonymization, or any illegal surveillance activities.

## 🚀 Features

1. **VPN/Tor Exit Node Analysis**
   - Load and analyze public VPN/Tor exit node datasets
   - IP geolocation (country, region)
   - ASN and ISP identification
   - Port usage pattern analysis

2. **Risk Assessment**
   - Rule-based risk scoring (Low/Medium/High)
   - Metadata-driven threat indicators

3. **Interactive Visualizations**
   - World map showing exit node locations
   - Country-wise distribution charts
   - Risk-level analytics dashboard

4. **Educational Module**
   - Dark web credential trading awareness
   - VPN misuse in cybercrime
   - Best practices for online safety

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.8+
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Folium
- **APIs:** IPinfo, GeoIP (free tier)

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd celeste-map
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys (optional):
```bash
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys
```

## 🎮 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Navigate through:
   - Dashboard: Overview and analytics
   - Map View: Interactive global visualization
   - Education: Learning modules
   - Data Upload: Load your own datasets

## 📁 Project Structure

```
celeste-map/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config/
│   ├── config.yaml       # Configuration file
│   └── config.example.yaml
├── src/
│   ├── data_processor.py # Data loading and processing
│   ├── geo_analyzer.py   # Geolocation and metadata analysis
│   ├── risk_engine.py    # Risk assessment logic
│   ├── visualizations.py # Charts and maps
│   └── education.py      # Educational content
├── data/
│   └── sample/           # Sample datasets
└── assets/               # Static assets (images, etc.)
```

## 🔒 Privacy & Ethics

- **No User Tracking:** We do not collect or store user data
- **No Deanonymization:** We do not attempt to identify individuals
- **Public Data Only:** All analysis uses publicly available datasets
- **Educational Focus:** This tool is for awareness and education only

## 📊 Sample Data Format

VPN/Tor exit nodes should be provided in CSV or JSON format:

```csv
ip,port,country,asn,isp,first_seen,last_seen
1.2.3.4,443,US,AS12345,Example ISP,2025-01-01,2025-12-25
```

## 🤝 Contributing

Contributions are welcome! Please ensure all contributions align with the educational and ethical goals of this project.

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This software is provided for educational purposes only. The developers are not responsible for any misuse of this tool. Always respect privacy laws and regulations in your jurisdiction.
