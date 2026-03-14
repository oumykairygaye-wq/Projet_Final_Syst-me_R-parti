# Distributed Monitoring System

A lightweight **Distributed Monitoring System** implemented in Python.
This project demonstrates a **client–server architecture** where multiple monitoring agents collect system metrics and send them to a centralized server.

The project was developed as part of a **Distributed Systems course**.

---

# Project Overview

Monitoring systems are essential for maintaining the reliability and performance of IT infrastructures.

This project implements a simplified distributed monitoring platform where:

• Client agents collect system metrics
• Metrics are sent to a central monitoring server
• The server processes and stores monitoring data
• The system detects abnormal system behavior

---

# System Architecture

The monitoring system follows a **centralized architecture**.

Client Node 1
Client Node 2  → Monitoring Server → SQLite Database
Client Node 3

Each client periodically sends system information to the monitoring server.

---

# Key Features

• Distributed monitoring architecture
• Multi-client support
• CPU usage monitoring
• Memory usage monitoring
• System uptime monitoring
• Network port monitoring
• Service detection
• Metrics storage using SQLite database
• Logging system for monitoring events

---

# Project Structure

```
distributed-monitoring-system
│
├── client
│   └── client.py
│
├── server
│   └── server.py
│
├── config
│   └── config.py
│
├── database
│
├── logs
│
├── metrics.db
├── monitoring.db
│
└── README.md
```

---

# Technologies Used

Python
TCP Sockets
JSON
SQLite
Multi-threading
Logging

---

# How the System Works

1. The client collects system metrics.
2. The metrics are converted to JSON format.
3. The client sends data to the monitoring server using TCP sockets.
4. The server receives and processes the data.
5. The metrics are stored in the SQLite database.

---

# Example Metrics Sent by Client

```json
{
  "node": "client-node",
  "os": "Windows",
  "cpu": 45,
  "memory": 70,
  "uptime": 15000
}
```

---

# Installation

Clone the repository:

```
git clone https://github.com/oumykairygaye-wq/Projet_Final_Syst-me_R-parti.git
```

Navigate to the project directory:

```
cd distributed-monitoring-system
```

Install required dependency:

```
pip install psutil
```

---

# Running the Project

Start the server:

```
python server/server.py
```

Start the client:

```
python client/client.py
```

The client will start sending monitoring metrics to the server.

---

# Future Improvements

Possible improvements include:

• Web monitoring dashboard
• Data visualization graphs
• Email alert system
• Secure communication between nodes

---

# Academic Context

This project was developed for the **Distributed Systems course**.

Master 1 – Networks and Virtual Infrastructure
Université Numérique Cheikh Hamidou Kane

---

# Author

Oumy Kairy Gaye


