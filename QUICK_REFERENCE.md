# Celeste Map - Quick Reference Guide

## 🚀 Quick Start Commands

### Windows
```cmd
run.bat
```

### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

### Manual
```bash
streamlit run app.py
```

## 📁 File Formats

### CSV Format
```csv
ip,port,country,asn,isp,first_seen,last_seen
1.2.3.4,443,US,AS12345,Example ISP,2025-01-01,2025-12-25
```

**Required:** `ip`  
**Optional:** `port`, `country`, `asn`, `isp`, `first_seen`, `last_seen`, `latitude`, `longitude`

### JSON Format
```json
{
  "nodes": [
    {
      "ip": "1.2.3.4",
      "port": 443,
      "country": "US",
      "asn": "AS12345",
      "isp": "Example ISP"
    }
  ]
}
```

## 🎯 Risk Level Criteria

| Level | Score Range | Color | Description |
|-------|------------|-------|-------------|
| **High** | ≥ 7.0 | 🔴 Red | Multiple risk factors |
| **Medium** | 4.0-6.9 | 🟠 Orange | Some risk indicators |
| **Low** | 0.1-3.9 | 🟢 Green | Minimal risk factors |
| **Unknown** | 0.0 | ⚪ Gray | No risk data available |

## 🔍 Risk Factors

### Port-Based (+3.0 High Risk)
- 22 (SSH)
- 23 (Telnet)
- 3389 (RDP)
- 4444, 5555 (Common backdoor ports)
- 8080, 8888 (Proxy ports)

### ISP/ASN Patterns (+1.5-2.0)
- Datacenter hosting providers
- VPN service providers
- Cloud infrastructure keywords

### Data Quality (-0.5)
- Missing geolocation
- Missing ISP information
- Incomplete metadata

## 📊 Dashboard Sections

| Section | Description |
|---------|-------------|
| **Overview** | Total nodes, risk distribution, average scores |
| **Risk Distribution** | Pie chart of risk levels |
| **Risk Histogram** | Distribution of risk scores |
| **Country Analysis** | Top 15 countries by node count |
| **Port Analysis** | Top 15 ports by usage |
| **Geographic Scatter** | World map with risk overlay |
| **Data Table** | Filterable detailed node list |

## 🗺️ Map Features

### Marker Map
- Color-coded markers by risk level
- Clustering for dense areas
- Popup with detailed node info
- Multiple tile layer options

### Heat Map
- Risk-weighted density visualization
- Color gradient (blue → red)
- Shows concentration areas
- Useful for pattern recognition

## 🎨 Visualization Colors

```
High Risk:   #FF4444 (Red)
Medium Risk: #FFA500 (Orange)
Low Risk:    #44FF44 (Green)
Unknown:     #CCCCCC (Gray)
```

## ⚙️ Configuration Quick Edit

**File:** `config/config.yaml`

### Change Risk Thresholds
```yaml
risk_engine:
  thresholds:
    high: 7.0
    medium: 4.0
    low: 0.0
```

### Add API Token
```yaml
api:
  ipinfo_token: "your_token_here"
```

### Adjust Map Settings
```yaml
visualization:
  map:
    default_zoom: 2
    default_center: [20, 0]
```

### Change Data Limits
```yaml
data:
  max_records: 10000
```

## 🔌 API Integration

### IPInfo (Optional)
1. Sign up at https://ipinfo.io/signup
2. Get free API token (50,000 requests/month)
3. Add to `config/config.yaml`
4. Enable "API enrichment" in Data Upload

### IP-API (Free, No Key)
- Automatically used as fallback
- 45 requests per minute
- No signup required

## 📚 Navigation Pages

1. **🏠 Home** - Welcome and overview
2. **📤 Data Upload** - Import and process datasets
3. **📊 Dashboard** - Analytics and statistics
4. **🗺️ Map View** - Interactive geographic visualization
5. **📚 Education** - Cybersecurity learning modules
6. **ℹ️ About** - Project information

## 🔒 Privacy Features

- ✅ No user tracking
- ✅ No data storage (session only)
- ✅ Local processing
- ✅ Optional API calls
- ✅ No personal data collection

## 🛠️ Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Permission Denied (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 Sample Data

**Location:** `data/sample/`

- `tor_exit_nodes_sample.csv` - 50 Tor nodes
- `vpn_exit_nodes_sample.json` - 30 VPN nodes

Perfect for testing and demonstrations!

## 💡 Pro Tips

1. **Large Datasets**: Enable clustering on maps for better performance
2. **API Calls**: Limit to 50-100 for free tier compliance
3. **Filtering**: Use dashboard filters to focus on high-risk nodes
4. **Export**: Copy data from tables for external analysis
5. **Education**: Share Education section with team for awareness training

## 📞 Support

- **Documentation**: See README.md and INSTALL.md
- **Sample Data**: Check data/sample/README.md
- **Configuration**: Review config/config.example.yaml

## ⚡ Keyboard Shortcuts (Streamlit)

- `R` - Rerun the app
- `Ctrl+C` - Stop the server
- `Ctrl+Shift+R` - Clear cache and rerun

## 🎯 Use Cases

1. **Security Research** - Analyze VPN exit node patterns
2. **Network Security** - Identify potentially risky connections
3. **Education** - Learn about cybersecurity threats
4. **Training** - Demonstrate threat intelligence concepts
5. **Awareness** - Understand dark web ecosystem

## 📈 Performance Tips

- Keep datasets under 10,000 records
- Use clustering for maps with 100+ nodes
- Disable API enrichment for faster processing
- Close unused browser tabs
- Clear cache if app becomes slow (from sidebar)

---

**Quick Help**: Press `?` in the app for Streamlit keyboard shortcuts!
