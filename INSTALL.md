# Celeste Map - Installation & Setup Guide

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### 2. Installation Steps

#### Option A: Download and Extract
1. Download the project files
2. Extract to `C:\celeste-map` (or your preferred location)
3. Open Command Prompt or PowerShell

#### Option B: Clone Repository (if using Git)
```bash
git clone <repository-url>
cd celeste-map
```

### 3. Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas & NumPy (data processing)
- Plotly & Folium (visualizations)
- And other required packages

### 5. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at:
`http://localhost:8501`

## Configuration (Optional)

### API Keys for Enhanced Features

To enable IP geolocation API enrichment:

1. Copy the example config:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```

2. Get a free API key from [IPInfo.io](https://ipinfo.io/signup)

3. Edit `config/config.yaml` and add your token:
   ```yaml
   api:
     ipinfo_token: "your_token_here"
   ```

**Note:** The application works fine without API keys using built-in fallback methods.

## Testing with Sample Data

1. Start the application
2. Navigate to "📤 Data Upload" in the sidebar
3. Upload one of the sample files:
   - `data/sample/tor_exit_nodes_sample.csv`
   - `data/sample/vpn_exit_nodes_sample.json`
4. Explore the visualizations!

## Troubleshooting

### Issue: `streamlit: command not found`
**Solution:** Make sure you activated the virtual environment:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Issue: Module import errors
**Solution:** Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Port already in use
**Solution:** Specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Permission denied when activating virtual environment (Windows)
**Solution:** Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Usage Tips

### Uploading Data

Your CSV files should have at minimum:
- `ip` column (required)

Optional columns:
- `port`, `country`, `asn`, `isp`, `first_seen`, `last_seen`, `latitude`, `longitude`

### Navigation

- **Home**: Overview and introduction
- **Data Upload**: Load and process datasets
- **Dashboard**: Analytics and statistics
- **Map View**: Interactive geographic visualization
- **Education**: Cybersecurity awareness content
- **About**: Project information

### Performance

- Datasets are limited to 10,000 records by default
- API enrichment is optional and can be disabled
- Use clustering on maps for better performance with large datasets

## Advanced Configuration

Edit `config/config.yaml` to customize:

- Risk assessment thresholds
- Visualization colors
- Data processing limits
- Map default settings

## Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

## Updating

To get the latest version:

```bash
# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Need Help?

- Check the "📚 Education" section for usage guidance
- Review sample datasets in `data/sample/`
- Ensure all dependencies are properly installed

## Security Note

This application:
- ✅ Runs locally on your machine
- ✅ Does not send data to external servers (except optional API calls)
- ✅ Does not track users
- ✅ Is for educational purposes only

Always use responsibly and ethically!
