## Installation & Setup Guide

### Current Content
This section outlines the setup process for a LangChain workshop project with three main components:
- Installing Python dependencies
- Running an MCP (Model Context Protocol) server
- Running an Ollama service
- Running an MCP client

### Installation Requirements

```bash
pip install -r requirements.txt
```

### Ollama Setup

#### Install Ollama
Visit [ollama.ai](https://ollama.ai) and download the installer for your operating system (macOS, Linux, or Windows).

#### Start Ollama Service
```bash
ollama serve
```

#### Download Models

**Qwen 7B:**
```bash
ollama pull qwen:7b
```

**DeepSeek 7B:**
```bash
ollama pull deepseek-coder:7b
```

### Running the Application

#### Start MCP Server
```bash
python -m mcp_server.main
```

#### Start MCP Client
```bash
python -m mcp_client.main
```

#### Run workshop_learnings files
```bash
python -m workshop_learnings.basic_agent
```

```bash
python -m workshop_learnings.basic_tool_call
```