# CyberDef25 Detector — Automated Threat Detection Tool
<img width="975" height="468" alt="image" src="https://github.com/user-attachments/assets/d9c69526-e2a7-4047-94e7-4222420c38d2" />


A Python-based automated threat detection tool developed for the **CyberDef 2025** challenge. Analyzes system logs and network data to identify Indicators of Compromise (IOCs) and Indicators of Attack (IOAs), producing structured reports for incident response.

---

## Overview

CyberDef25 Detector bridges cybersecurity and DevOps — it is designed to be **scriptable, modular, and CI/CD-friendly**, making it suitable for integration into automated security pipelines (DevSecOps). It can run as a standalone tool or be invoked as a pipeline stage in Jenkins/GitHub Actions to continuously scan artifacts and logs for threats.

---

## Features

- **IOC Detection** — scans logs for known malicious IPs, hashes, domains, and file paths
- **IOA Behavioral Analysis** — identifies suspicious behavioral patterns (privilege escalation attempts, lateral movement, unusual process spawning)
- **PCAP Parsing** — analyzes network capture files for anomalous traffic patterns
- **Log Ingestion** — supports Windows Event Logs, Linux syslog, and Apache/Nginx access logs
- **Structured Reporting** — outputs findings as JSON and human-readable text reports
- **Exit Codes** — returns non-zero on detected threats, enabling CI pipeline fail-fast behavior

---

## Project Structure

```
cyberdef25-detector/
├── detector.py                  # Main entry point
├── modules/
│   ├── ioc_scanner.py           # IOC matching engine
│   ├── ioa_analyzer.py          # Behavioral pattern analysis
│   ├── pcap_parser.py           # Network traffic analysis
│   └── log_ingester.py          # Multi-format log parser
├── signatures/
│   ├── ioc_list.txt             # Known malicious IPs, hashes, domains
│   └── patterns.json            # Behavioral detection rules
├── reports/
│   └── ...                      # Generated scan reports (gitignored)
├── tests/
│   ├── test_ioc_scanner.py
│   └── test_log_ingester.py
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Hamza-Shaukat078/cyberdef25-detector.git
cd cyberdef25-detector

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
scapy>=2.5.0
pyshark>=0.6
python-evtx>=0.7.4
colorama>=0.4.6
tabulate>=0.9.0
```

---

## Usage

### Scan a log file for IOCs
```bash
python detector.py --mode ioc --input /var/log/auth.log
```

### Analyze a PCAP file
```bash
python detector.py --mode pcap --input capture.pcap
```

### Full analysis (IOC + IOA + PCAP)
```bash
python detector.py --mode full --input /path/to/logs/ --output reports/scan_result.json
```

### Output formats
```bash
python detector.py --mode ioc --input auth.log --format json    # JSON report
python detector.py --mode ioc --input auth.log --format text    # Human-readable
```

---

## Sample Output

```
[CyberDef25 Detector] Scanning: auth.log
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[!] IOC MATCH — IP: 185.220.101.47 (Known Tor Exit Node)
    Line 342: Failed password for root from 185.220.101.47 port 54821

[!] IOA DETECTED — Brute Force Pattern
    23 failed login attempts from single source within 60 seconds
    Source IP: 192.168.1.105

[+] Scan complete. 2 threats detected.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Exit code: 1  (threats detected)
```

---

## CI/CD Integration

The tool's non-zero exit code on threat detection makes it compatible with any CI/CD pipeline. Example Jenkins stage:

```groovy
stage('Security Scan') {
    steps {
        sh 'python detector.py --mode full --input ./logs/ --output reports/scan.json'
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/scan.json', fingerprint: true
        }
        failure {
            echo 'Threats detected — blocking deployment.'
        }
    }
}
```

This integrates threat detection directly into the delivery pipeline, embodying **DevSecOps** principles — security as a first-class pipeline citizen, not an afterthought.

---

## Detection Signatures

IOC signatures are maintained in `signatures/ioc_list.txt`:
```
# Format: type,value,description
ip,185.220.101.47,Tor Exit Node
hash,e3b0c44298fc1c149afb,Known Ransomware Hash
domain,malicious-c2.xyz,C2 Server
```

Behavioral rules in `signatures/patterns.json` define thresholds and sequences for IOA detection (e.g., brute force = 10+ failed logins in 30 seconds from one source).

---

## Key Concepts Demonstrated

- **Modular architecture** — each detection method is an independent, testable module
- **CI/CD compatibility** — exit code design enables pipeline fail-fast on security findings
- **Signature-driven detection** — external rule files allow updates without code changes
- **Multi-source ingestion** — handles diverse log formats common in real SOC environments
- **DevSecOps mindset** — security tooling built for automation, not just manual use

---

## Author

**Hamza Shaukat** — BS Cybersecurity, COMSATS University Islamabad  
[GitHub](https://github.com/Hamza-Shaukat078) · [LinkedIn](https://www.linkedin.com/in/hamza-shaukat-7185792b7/)
