# Project-Golu
# 🚀 Smart Reminder with AI Integration

[![Puch AI Compatible](https://img.shields.io/badge/Puch_AI-MCP_Enabled-green)](https://puch.ai)
[![Twitter API](https://img.shields.io/badge/Twitter_API-Integrated-blue)](https://developer.twitter.com)

An intelligent reminder system that combines task scheduling with educational content and social media insights, powered by Puch AI's MCP protocol.

![App Screenshot](screenshot.png) *(Upload your screenshot later)*

## ✨ Key Features

### ✅ Currently Working
- **Smart Task Management**
  - Notebook-style task organization (Upcoming/Ongoing/Done)
  - Time-based desktop notifications
  - One-click status updates

- **Educational Boost**
  - Auto-generated facts/news during study breaks
  - Manual content refresh button
  - Content relevance scoring

- **Puch AI Integration**
  - MCP protocol for secure connections
  - Natural language task entry
  - Voice command support (via Puch)

### 🚧 Coming Soon (Upcoming Features)
| Feature | Status | ETA |
|---------|--------|-----|
| **Twitter/X Integration** | 🔧 In Development | v1.1 |
| *Real-time tweets related to your tasks* | | |
| **Reddit Content Feed** | ⏳ Planned | v1.2 |
| *Subreddit discussions based on interests* | | |
| **AI Content Summarization** | 💡 Proposed | v1.3 |
| *Condensed social media highlights* | | |

## 🛠️ Technical Stack
```mermaid
graph TD
    A[Frontend] -->|HTTPS| B[FastAPI]
    B --> C[(SQLite)]
    B --> D[Twitter API]
    A --> E[Puch AI]
    E -->|MCP| B