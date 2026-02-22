# CodeX Treasure Hunt: Cicada: SQL Injection & Network Recon

A multi-layered cybersecurity, capture-the-flag (CTF) platform built for a tech-integrated treasure hunt hosted by CodeX. This project challenges participants to use network scanning, file carving, and SQL injection to retrieve hidden intel across a distributed node network.

## Project Overview
The platform was designed for a multi-stage technical competition where participants must navigate through three distinct layers of security challenges:
1. **Cryptographic File Extraction**: Identifying and programmatically extracting core payloads from 50-layer nested ZIP archives containing decoy data.
2. **Network Reconnaissance**: Performing active service discovery via Nmap to locate hidden Flask-based server nodes within a local area network.
3. **Database Exploitation**: Identifying and exploiting a SQL injection vulnerability within a custom Matrix-themed web interface to extract mission-critical intelligence.

## Technical Components
* **Web Server Node (`web.py`)**: A Flask application utilizing an intentionally vulnerable SQLite3 backend to facilitate UNION-based SQL injection attacks.
* **Payload Generator (`zipping.py`)**: A Python utility developed to generate complex, multi-layered file archives for data carving exercises.
* **Automated Solver (`zip_solve.py`)**: A verification script designed to demonstrate the feasibility of programmatic extraction through the nested archive structures.
* **Database Schema (`database_alpha.db`)**: A team-specific relational database containing encrypted clues and station access codes.

## Technical Specifications
* **Language**: Python 3.x
* **Framework**: Flask
* **Database Engine**: SQLite3
* **Frontend**: HTML5, CSS3, JavaScript (Canvas API for terminal UI)
* **Concepts Demonstrated**: ICMP/TCP network protocols, SQLi (UNION SELECT), Database Schema Enumeration, and Scripting for Automation.

---
Developed by a First-Year B.Tech Computer Science student for the CodeX Coding Club, February 2026.