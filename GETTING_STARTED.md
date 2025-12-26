# 🚀 Getting Started with Celeste Map

Welcome! This guide will help you get Celeste Map up and running in minutes.

## ⚡ Super Quick Start (Recommended)

### Windows Users
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```cmd
   cd C:\celeste-map
   ```
3. Run the quick start script:
   ```cmd
   run.bat
   ```
4. Wait for your browser to open automatically!

### Mac/Linux Users
1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd /path/to/celeste-map
   ```
3. Run the quick start script:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
4. Wait for your browser to open automatically!

That's it! The application should now be running at `http://localhost:8501`

---

## 📖 First Time Using the App?

### Step 1: Explore the Home Page
- Read the welcome message
- Understand the features
- Review the disclaimer

### Step 2: Upload Sample Data
1. Click **"📤 Data Upload"** in the sidebar
2. Click the **"Choose a file"** button
3. Navigate to `data/sample/`
4. Select `tor_exit_nodes_sample.csv` or `vpn_exit_nodes_sample.json`
5. Click **Open**
6. Wait for processing (should take 5-10 seconds)

### Step 3: View the Dashboard
1. Click **"📊 Dashboard"** in the sidebar
2. Explore the statistics and charts
3. Try the filtering options in the "Detailed Node Data" section

### Step 4: Check the Map
1. Click **"🗺️ Map View"** in the sidebar
2. Choose between **Marker Map** or **Heat Map**
3. Click on markers to see detailed information
4. Try different map tile layers

### Step 5: Learn About Security
1. Click **"📚 Education"** in the sidebar
2. Read through the tabs:
   - Dark Web Awareness
   - VPN & Tor
   - Safe Practices
   - Resources

---

## 🎯 Quick Tutorial: Using Your Own Data

### Preparing Your Data

#### Option 1: CSV File
Create a file named `my_vpn_data.csv`:
```csv
ip,port,country,asn,isp
192.0.2.1,443,US,AS15169,Example ISP
192.0.2.2,1194,GB,AS8075,Another ISP
192.0.2.3,8080,DE,AS16509,Third ISP
```

**Required column:** `ip`
**Optional columns:** `port`, `country`, `asn`, `isp`, `first_seen`, `last_seen`, `latitude`, `longitude`

#### Option 2: JSON File
Create a file named `my_vpn_data.json`:
```json
{
  "nodes": [
    {
      "ip": "192.0.2.1",
      "port": 443,
      "country": "US",
      "asn": "AS15169",
      "isp": "Example ISP"
    },
    {
      "ip": "192.0.2.2",
      "port": 1194,
      "country": "GB",
      "asn": "AS8075",
      "isp": "Another ISP"
    }
  ]
}
```

### Uploading Your Data
1. Go to **"📤 Data Upload"**
2. Click **"Choose a file"**
3. Select your CSV or JSON file
4. Optionally enable **"API enrichment"** (requires API key)
5. Wait for processing
6. View results in Dashboard or Map View!

---

## ⚙️ Optional: API Configuration

To enable automatic geolocation for IPs without coordinates:

### Get a Free API Key
1. Visit https://ipinfo.io/signup
2. Sign up for free (50,000 requests/month)
3. Copy your API token

### Add to Configuration
1. Open `config/config.yaml` in a text editor
2. Find the line: `ipinfo_token: ""`
3. Replace with: `ipinfo_token: "your_token_here"`
4. Save the file
5. Restart the application

**Note:** The app works fine without an API key using fallback methods!

---

## 🎨 Understanding Risk Levels

The app automatically assigns risk levels to each node:

### 🔴 High Risk (Score ≥ 7.0)
- Uses high-risk ports (SSH, RDP, etc.)
- Datacenter hosting patterns
- Multiple risk factors present

### 🟠 Medium Risk (Score 4.0-6.9)
- Common proxy ports
- Some datacenter indicators
- Moderate risk factors

### 🟢 Low Risk (Score 0.1-3.9)
- Standard ports
- Residential ISPs
- Minimal risk indicators

### ⚪ Unknown (Score 0.0)
- No risk factors detected
- Insufficient data

---

## 🗺️ Understanding the Visualizations

### Marker Map
- Each marker = one VPN/Tor exit node
- Color indicates risk level
- Click markers for details
- Clustering groups nearby nodes

### Heat Map
- Red areas = high density/risk
- Blue areas = low density/risk
- Shows geographic patterns
- Weighted by risk scores

### Dashboard Charts
- **Pie Chart**: Overall risk distribution
- **Histogram**: Risk score spread
- **Bar Charts**: Top countries and ports
- **Scatter Map**: Global distribution with risk overlay

---

## 💡 Pro Tips for Best Experience

### 1. Performance
- Keep datasets under 10,000 records for smooth performance
- Use clustering on maps with 100+ markers
- Close unused browser tabs

### 2. Data Quality
- Include geolocation data when possible (latitude, longitude)
- Provide ISP/ASN info for better risk assessment
- Use consistent date formats

### 3. Analysis
- Filter the data table by risk level to focus on threats
- Compare country distributions to identify patterns
- Review risk factors in marker popups

### 4. Learning
- Read the Education section thoroughly
- Share safe practices with your team
- Use as training material for security awareness

### 5. Customization
- Edit `config/config.yaml` to adjust risk thresholds
- Modify colors to match your organization's style
- Change map default zoom and center

---

## 🛠️ Troubleshooting

### Problem: App won't start
**Solution:**
```bash
# Make sure you're in the project directory
cd celeste-map

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Try starting again
streamlit run app.py
```

### Problem: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Port already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Problem: Permission denied (Windows)
**Solution:** Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Data upload fails
**Solution:**
- Check file format matches CSV or JSON requirements
- Ensure `ip` column exists and contains valid IPs
- Verify file isn't corrupted
- Try with sample data first to confirm app works

---

## 📱 Application Pages Overview

### 🏠 Home
- Welcome message
- Feature overview
- Getting started guide
- Important disclaimers

### 📤 Data Upload
- File upload interface
- Data validation
- Processing options
- Statistics preview

### 📊 Dashboard
- Summary metrics
- Interactive charts
- Data filtering
- Detailed tables

### 🗺️ Map View
- Interactive world map
- Risk visualization
- Geographic analysis
- Multiple map styles

### 📚 Education
- **Dark Web Awareness**: Learn about credential trading and threats
- **VPN & Tor**: Understand privacy tools and their misuse
- **Safe Practices**: Comprehensive security guide
- **Resources**: Useful tools and links

### ℹ️ About
- Project information
- Technology stack
- Privacy policy
- License details

---

## 🎓 Learning Path

### Beginner
1. ✅ Start with sample data
2. ✅ Explore all pages
3. ✅ Read Education section
4. ✅ Try uploading your own data

### Intermediate
1. ✅ Customize risk thresholds
2. ✅ Enable API enrichment
3. ✅ Analyze patterns in data
4. ✅ Export results for reporting

### Advanced
1. ✅ Integrate with threat intelligence feeds
2. ✅ Modify risk assessment rules
3. ✅ Extend with custom visualizations
4. ✅ Deploy for team use

---

## 📞 Need More Help?

- **Installation Issues**: See `INSTALL.md`
- **Feature Details**: Check `README.md`
- **Quick Commands**: Reference `QUICK_REFERENCE.md`
- **Project Overview**: Read `PROJECT_SUMMARY.md`
- **File Structure**: See `FILE_LISTING.md`

---

## 🎉 You're Ready!

You now know everything you need to use Celeste Map effectively. Remember:

✅ **This is an educational tool** - Use it to learn and raise awareness
✅ **Privacy first** - No user tracking or data collection
✅ **Ethical use only** - Follow all applicable laws
✅ **Share knowledge** - Help others understand cybersecurity

**Enjoy exploring the world of VPN/Tor exit nodes and staying cyber-safe!** 🛡️

---

**Questions?** Review the documentation files or check the Education section within the app.

**Ready to start?** Run `run.bat` (Windows) or `./run.sh` (Mac/Linux) and begin your journey!
