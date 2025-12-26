"""
Educational Content Module
Provides educational information about dark web, VPN misuse, and cybersecurity.
"""

import streamlit as st
from typing import Dict


class EducationModule:
    """
    Educational content about dark web awareness and cybersecurity.
    """
    
    def __init__(self):
        """Initialize education module."""
        pass
    
    def render_dark_web_awareness(self):
        """Render dark web awareness content."""
        st.header("🕵️ Understanding the Dark Web")
        
        st.markdown("""
        ### What is the Dark Web?
        
        The **dark web** is a part of the internet that is not indexed by traditional search engines 
        and requires special software (like Tor) to access. It's important to understand that:
        
        - **Not all dark web content is illegal** - it includes legitimate privacy-focused services
        - However, it is also used for **illegal activities** including credential trading
        - Access requires anonymization tools like Tor, I2P, or Freenet
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Legitimate Uses:**
            - Whistleblowing platforms
            - Privacy-focused communication
            - Censorship circumvention
            - Research and journalism
            """)
        
        with col2:
            st.warning("""
            **Illegal Activities:**
            - Stolen credential marketplaces
            - Malware distribution
            - Illegal goods trading
            - Cybercrime-as-a-service
            """)
        
        st.markdown("""
        ### Dark Web Credential Trading
        
        One of the most significant threats from the dark web is the **trading of stolen credentials**:
        
        #### How Credentials Are Stolen:
        1. **Data Breaches** - Large-scale hacks of companies and services
        2. **Phishing Attacks** - Fake websites and emails trick users into revealing passwords
        3. **Keyloggers & Malware** - Software that records everything you type
        4. **Social Engineering** - Manipulating people into giving up their information
        
        #### What Happens to Stolen Credentials:
        - Sold in **bulk databases** on dark web marketplaces
        - Used for **credential stuffing attacks** (trying the same password across multiple sites)
        - Compiled into **combo lists** (username:password pairs)
        - Can sell for **$0.50 to $100+** depending on the account type
        
        #### High-Value Targets:
        - 🏦 Banking and financial accounts
        - 📧 Email accounts (gateway to password resets)
        - 🎮 Gaming accounts with valuable items
        - 💼 Corporate credentials
        - 🏥 Healthcare records
        """)
        
        st.error("""
        **Real-World Impact:**
        
        According to cybersecurity reports:
        - Over **24 billion username/password combinations** are available on the dark web
        - Average cost of a stolen identity: **$1,000 - $2,000**
        - **80% of data breaches** involve weak or stolen passwords
        """)
        
        st.markdown("""
        ### Protection Strategies
        
        #### 1. Strong Password Practices
        - Use **unique passwords** for every account
        - Enable **multi-factor authentication (MFA)** everywhere possible
        - Use a **password manager** to generate and store strong passwords
        - Password should be 12+ characters with mixed case, numbers, and symbols
        
        #### 2. Monitor Your Digital Footprint
        - Use services like "Have I Been Pwned" to check if your email is compromised
        - Set up **breach alerts** for your accounts
        - Regularly review account activity and login locations
        
        #### 3. Be Skeptical
        - **Never click suspicious links** in emails or messages
        - Verify website URLs before entering credentials
        - Be wary of urgent requests for personal information
        - Double-check the sender's email address
        
        #### 4. Keep Software Updated
        - Install security updates promptly
        - Use reputable antivirus software
        - Keep browsers and operating systems current
        """)
    
    def render_vpn_misuse_content(self):
        """Render VPN and Tor misuse content."""
        st.header("🔒 VPN & Tor: Privacy Tools and Their Misuse")
        
        st.markdown("""
        ### What Are VPNs and Tor?
        
        **VPN (Virtual Private Network)** and **Tor (The Onion Router)** are legitimate privacy tools, 
        but like any technology, they can be misused.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### VPN (Virtual Private Network)
            
            **How it works:**
            - Encrypts your internet connection
            - Routes traffic through remote servers
            - Masks your real IP address
            
            **Legitimate Uses:**
            - ✅ Protect privacy on public WiFi
            - ✅ Access geo-restricted content
            - ✅ Secure remote work connections
            - ✅ Avoid ISP throttling
            
            **Potential Misuse:**
            - ❌ Hide identity during cyberattacks
            - ❌ Bypass network security monitoring
            - ❌ Access blocked malicious sites
            """)
        
        with col2:
            st.markdown("""
            #### Tor (The Onion Router)
            
            **How it works:**
            - Routes traffic through multiple nodes
            - Provides strong anonymity
            - Access to .onion sites (dark web)
            
            **Legitimate Uses:**
            - ✅ Protect journalist sources
            - ✅ Circumvent censorship
            - ✅ Anonymous whistleblowing
            - ✅ Privacy-focused browsing
            
            **Potential Misuse:**
            - ❌ Anonymous illegal activities
            - ❌ Access illegal marketplaces
            - ❌ Hide attack origin
            """)
        
        st.markdown("""
        ### Understanding Exit Nodes
        
        **Exit nodes** are the final relay in VPN/Tor networks where encrypted traffic leaves the 
        anonymization network and connects to its destination.
        
        #### Why Exit Nodes Matter:
        - They are the **visible IP address** to the destination server
        - Can be monitored by law enforcement and researchers
        - May be blocked by security-conscious organizations
        - Can reveal patterns about VPN/Tor network usage
        
        #### This Application's Purpose:
        This tool analyzes **public exit node data** to help organizations and individuals:
        - Understand the scope of VPN/Tor network infrastructure
        - Identify potential security risks from anonymization services
        - Make informed decisions about network security policies
        - Educate about privacy technology usage patterns
        """)
        
        st.warning("""
        **Important Ethical Note:**
        
        Using VPN or Tor is **NOT illegal** in most countries. These are legitimate privacy tools 
        used by millions of people for lawful purposes. This application:
        
        - Does **NOT** identify individual users
        - Does **NOT** track or monitor anyone
        - Analyzes only **publicly available exit node information**
        - Is for **educational and security awareness purposes only**
        """)
        
        st.markdown("""
        ### VPN Exit Nodes in Cybercrime
        
        #### Common Attack Patterns:
        
        1. **Credential Stuffing Attacks**
           - Attackers use VPNs to hide their location
           - Rotate through different exit nodes to avoid rate limiting
           - Test stolen credentials against multiple services
        
        2. **Distributed Denial of Service (DDoS)**
           - VPN networks used to amplify attack traffic
           - Makes source attribution difficult
        
        3. **Phishing Campaigns**
           - Phishing sites hosted behind VPN exit nodes
           - Quickly change locations to evade takedown
        
        4. **Data Exfiltration**
           - Stolen data tunneled through VPN connections
           - Difficult to trace back to attacker
        
        #### Risk Indicators:
        - Multiple connections from same exit node to sensitive services
        - Unusual geographic patterns (e.g., VPN exit in unexpected country)
        - High-risk port usage (SSH, RDP on exit nodes)
        - Datacenter hosting providers (common for VPN services)
        """)
    
    def render_safe_practices(self):
        """Render safe internet practices content."""
        st.header("🛡️ Safe Internet Practices")
        
        st.markdown("""
        ### Comprehensive Cybersecurity Guide
        
        Protecting yourself online requires a multi-layered approach. Follow these best practices:
        """)
        
        # Password Security
        with st.expander("🔐 Password Security", expanded=True):
            st.markdown("""
            #### Create Strong Passwords
            - **Length matters:** Aim for 12-16+ characters
            - **Complexity:** Mix uppercase, lowercase, numbers, and symbols
            - **Uniqueness:** Never reuse passwords across sites
            - **Avoid common patterns:** No "Password123" or "qwerty"
            
            #### Password Manager Benefits
            - Generates cryptographically random passwords
            - Stores passwords securely with encryption
            - Auto-fills credentials to prevent keyloggers
            - Syncs across devices securely
            
            **Recommended Password Managers:** Bitwarden, 1Password, LastPass, Dashlane
            
            #### Passphrase Method
            Instead of complex passwords, use memorable passphrases:
            - ❌ Bad: `P@ssw0rd123`
            - ✅ Good: `Blue!Elephant#Dances$At7am`
            """)
        
        # Multi-Factor Authentication
        with st.expander("📱 Multi-Factor Authentication (MFA)"):
            st.markdown("""
            #### Why MFA is Critical
            Even if your password is compromised, MFA provides an additional security layer.
            
            #### Types of MFA (from least to most secure):
            1. **SMS Codes** - Better than nothing, but vulnerable to SIM swapping
            2. **Email Codes** - Depends on email account security
            3. **Authenticator Apps** - Much more secure (Google Authenticator, Authy, Microsoft Authenticator)
            4. **Hardware Keys** - Most secure option (YubiKey, Google Titan)
            
            #### Where to Enable MFA:
            - 📧 Email accounts (critical!)
            - 🏦 Banking and financial services
            - 🛒 Shopping accounts
            - 💼 Work accounts
            - 🎮 Gaming platforms
            - ☁️ Cloud storage services
            """)
        
        # Email Security
        with st.expander("📧 Email Security"):
            st.markdown("""
            #### Spotting Phishing Emails
            - **Check sender address carefully** - look for subtle misspellings
            - **Hover over links** before clicking to see real destination
            - **Be skeptical of urgency** - "Act now!" is a red flag
            - **Look for grammar errors** - professional companies proofread
            - **Verify unexpected attachments** - call the sender to confirm
            
            #### Red Flags:
            - ⚠️ Requests for passwords or sensitive information
            - ⚠️ Threats or time pressure ("account will be closed")
            - ⚠️ Too good to be true offers
            - ⚠️ Unexpected password reset emails
            - ⚠️ Invoices for things you didn't buy
            
            #### Safe Email Practices:
            - Use a separate email for online shopping/newsletters
            - Never click "unsubscribe" in suspicious emails
            - Report phishing attempts to your email provider
            - Enable spam filtering
            """)
        
        # Software Updates
        with st.expander("🔄 Software Updates & Patching"):
            st.markdown("""
            #### Why Updates Matter
            Software updates often contain **critical security patches** that fix vulnerabilities 
            actively exploited by attackers.
            
            #### What to Keep Updated:
            - ✅ Operating System (Windows, macOS, Linux)
            - ✅ Web browsers (Chrome, Firefox, Safari, Edge)
            - ✅ Antivirus/Anti-malware software
            - ✅ Mobile apps
            - ✅ Router firmware
            - ✅ Smart home devices
            
            #### Best Practices:
            - Enable automatic updates when possible
            - Don't postpone security updates
            - Restart devices to complete updates
            - Uninstall software you no longer use
            """)
        
        # Network Security
        with st.expander("🌐 Network Security"):
            st.markdown("""
            #### Secure Your Home Network
            1. **Change default router password**
            2. **Use WPA3 or WPA2 encryption** (not WEP)
            3. **Create a strong WiFi password**
            4. **Disable WPS** (WiFi Protected Setup)
            5. **Update router firmware regularly**
            6. **Use a guest network** for visitors and IoT devices
            
            #### Public WiFi Safety
            - ❌ Avoid accessing sensitive accounts on public WiFi
            - ✅ Use a VPN when on public networks
            - ❌ Don't enable "Auto-Connect" to networks
            - ✅ Forget networks after use
            - ❌ Turn off file sharing
            """)
        
        # Data Backup
        with st.expander("💾 Data Backup"):
            st.markdown("""
            #### Follow the 3-2-1 Rule
            - **3** copies of your data
            - **2** different storage media
            - **1** copy offsite (cloud or external drive in different location)
            
            #### What to Backup:
            - Important documents and photos
            - Financial records
            - Contacts and calendars
            - Project files
            
            #### Backup Solutions:
            - **Cloud:** Google Drive, OneDrive, Dropbox, iCloud
            - **Local:** External hard drive, NAS (Network Attached Storage)
            - **Automated:** Set up scheduled backups
            """)
        
        # Social Media Privacy
        with st.expander("📱 Social Media Privacy"):
            st.markdown("""
            #### Protect Your Privacy
            1. **Review privacy settings** regularly
            2. **Limit who can see your posts** (friends only)
            3. **Be cautious about location sharing**
            4. **Think before posting** - it's permanent
            5. **Don't accept friend requests from strangers**
            
            #### Information to Avoid Sharing:
            - ❌ Full birth date
            - ❌ Home address
            - ❌ Phone number
            - ❌ Vacation plans (wait until you're back)
            - ❌ Photos of IDs, credit cards, tickets with barcodes
            """)
        
        # Device Security
        with st.expander("📲 Device Security"):
            st.markdown("""
            #### Mobile Device Protection
            - Use biometric locks (fingerprint/face) plus PIN
            - Enable "Find My Device" features
            - Install apps only from official stores
            - Review app permissions regularly
            - Use device encryption
            
            #### Computer Security
            - Enable disk encryption (BitLocker, FileVault)
            - Use a standard account (not admin) for daily use
            - Enable firewall
            - Install reputable antivirus software
            - Lock computer when stepping away
            """)
        
        st.success("""
        ### Quick Security Checklist
        
        ✅ Using unique passwords for all accounts  
        ✅ Password manager installed and used  
        ✅ MFA enabled on critical accounts  
        ✅ Software and OS fully updated  
        ✅ Antivirus installed and running  
        ✅ Router has strong password and updated firmware  
        ✅ Regular backups configured  
        ✅ Reviewing email links before clicking  
        ✅ Using VPN on public WiFi  
        ✅ Social media privacy settings configured  
        """)
    
    def render_resources(self):
        """Render additional resources."""
        st.header("📚 Additional Resources")
        
        st.markdown("""
        ### Useful Tools and Websites
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Security Check Tools
            - **Have I Been Pwned** - Check if your email was in a data breach
            - **Password Strength Checker** - Test password quality
            - **VirusTotal** - Scan suspicious files and URLs
            - **SSL Labs** - Test website SSL/TLS configuration
            
            #### Educational Resources
            - **NIST Cybersecurity Framework** - Industry standards
            - **OWASP** - Web application security
            - **SANS Security Resources** - Training and research
            - **Krebs on Security** - Cybersecurity news blog
            """)
        
        with col2:
            st.markdown("""
            #### Government Resources
            - **US-CERT** - US Computer Emergency Readiness Team
            - **FBI IC3** - Internet Crime Complaint Center
            - **FTC Identity Theft** - Report identity theft
            - **CISA** - Cybersecurity & Infrastructure Security Agency
            
            #### Privacy Tools
            - **EFF Privacy Badger** - Block trackers
            - **uBlock Origin** - Ad and tracker blocker
            - **Signal** - Encrypted messaging
            - **ProtonMail** - Encrypted email
            """)
        
        st.info("""
        **Remember:** Cybersecurity is an ongoing process, not a one-time task. 
        Stay informed, stay vigilant, and regularly review your security practices.
        """)
