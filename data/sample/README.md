# Sample Datasets

This directory contains sample datasets for testing and demonstration purposes.

## Files

### tor_exit_nodes_sample.csv
Sample Tor exit node dataset in CSV format.

**Format:**
- ip: Exit node IP address
- port: Port number
- country: Country code (ISO 3166-1 alpha-2)
- asn: Autonomous System Number
- isp: Internet Service Provider name
- first_seen: First detection date
- last_seen: Last detection date
- latitude: Geographic latitude
- longitude: Geographic longitude

**Records:** 50 sample nodes from various countries

### vpn_exit_nodes_sample.json
Sample VPN exit node dataset in JSON format.

**Format:**
```json
{
  "metadata": {
    "description": "Dataset description",
    "collection_date": "YYYY-MM-DD",
    "source": "Data source",
    "total_records": 30
  },
  "nodes": [
    {
      "ip": "IP address",
      "port": port_number,
      "country": "Country code",
      "region": "Region name",
      "city": "City name",
      "asn": "ASN identifier",
      "isp": "ISP name",
      "first_seen": "YYYY-MM-DD",
      "last_seen": "YYYY-MM-DD",
      "latitude": latitude_float,
      "longitude": longitude_float
    }
  ]
}
```

**Records:** 30 sample nodes from various countries

## Usage

1. Start the application: `streamlit run app.py`
2. Navigate to "Data Upload" page
3. Upload one of these sample files
4. Explore the visualizations and analytics

## Notes

- These are **sample datasets** for educational purposes only
- IP addresses use documentation ranges (203.0.113.0/24) or are anonymized
- Not real Tor/VPN exit node data
- Intended for demonstration and testing only
