# Real-Time AI Assistant Using RAG + LangChain

A powerful, real-time AI assistant collection that can answer questions by searching the web using 100% free, open-source tools. This project demonstrates multiple approaches to building RAG (Retrieval-Augmented Generation) systems using Ollama, LangChain, and DuckDuckGo Search.

## 🚀 Features

- **Real-time web search**: Uses DuckDuckGo to fetch current information
- **Multiple AI models**: Support for various open-source LLMs via Ollama
- **Dual-model system**: Intelligent coordination between multiple models
- **No API costs**: Completely free to run on your own machine
- **Interactive chat**: Command-line interface for natural conversations
- **RAG architecture**: Combines retrieval and generation for accurate, up-to-date responses
- **Conversation history**: Save and manage chat sessions
- **Smart model selection**: Automatically chooses the best model for each task

## 📁 Project Structure

```
Real-Time AI Assistant Using RAG + LangChain/
├── assistant.py                 # Single model assistant (GPT-OSS 120B)
├── advanced_example.py          # Enhanced single model with history
├── dual_model_assistant.py      # Smart dual-model system
├── simple_dual_model.py         # Side-by-side dual model comparison
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── setup_instructions.md        # Basic setup guide
└── dual_model_setup.md         # Dual model setup guide
```

## 🤖 Available Assistants

### 1. Single Model Assistant (`assistant.py`)
- Uses `gpt-oss:120b-cloud` model
- Simple, fast, and efficient
- Perfect for general-purpose tasks

### 2. Advanced Single Model (`advanced_example.py`)
- Enhanced version with conversation history
- Source citations and better error handling
- Save conversations to JSON files

### 3. Smart Dual-Model System (`dual_model_assistant.py`)
- Uses both `qwen3-vl:235b-cloud` and `gpt-oss:120b-cloud`
- Intelligent model selection based on question type
- Four coordination strategies:
  - **QWEN**: Vision, multimodal, Chinese language tasks
  - **GPT**: General reasoning, complex analysis
  - **BOTH**: Combined responses for comprehensive answers
  - **QWEN→GPT**: Sequential processing for refined results

### 4. Simple Dual-Model (`simple_dual_model.py`)
- Always uses both models for comparison
- Shows responses side-by-side
- Great for evaluating model differences

## 🛠️ Prerequisites

### Required Software
1. **Install Ollama**: Download from [ollama.com](https://ollama.com)
2. **Python 3.8+**: Make sure Python is installed

### Model Options

#### For Single Model:
```bash
ollama pull gpt-oss:120b-cloud
```

#### For Dual Model System:
```bash
ollama pull qwen3-vl:235b-cloud    # Vision & multimodal
ollama pull gpt-oss:120b-cloud     # General reasoning
```

#### Alternative Smaller Models (faster):
```bash
ollama pull llama3:8b              # General purpose
ollama pull qwen2-vl:7b           # Vision tasks
```

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Real-Time AI Assistant Using RAG + LangChain"
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Pull your desired models** (see Prerequisites above)

## 🚀 Usage

### Single Model Assistant
```bash
python assistant.py
```

### Advanced Single Model
```bash
python advanced_example.py
```

### Smart Dual-Model System
```bash
python dual_model_assistant.py
```

### Simple Dual-Model Comparison
```bash
python simple_dual_model.py
```

## 💬 Example Interactions

### Single Model
```
🤖 Hello! I'm a real-time AI assistant. What's new?
You: What are the latest developments in AI?
🤖 Thinking...
🤖: Based on recent web search results...
```

### Dual Model System
```
🤖 Dual-Model Assistant Ready!
You: Analyze this image and explain the trends
📋 Strategy: QWEN_THEN_GPT
🟡 Getting Qwen3-VL response...
🔵 Refining with GPT-OSS...
🤖: **Models Used:** Qwen3-VL → GPT-OSS (Sequential)
```

## 🏗️ Architecture

### RAG Pipeline
1. **User Input**: Question or request
2. **Web Search**: DuckDuckGo fetches current information
3. **Context Assembly**: Search results formatted as context
4. **Model Processing**: AI generates response using context + knowledge
5. **Response**: Informed, up-to-date answer

### Dual-Model Coordination
```
Question → Strategy Selection → Model(s) Execution → Response Combination
```

### Technology Stack
- **Models**: Ollama (qwen3-vl:235b-cloud, gpt-oss:120b-cloud)
- **Search**: DuckDuckGo Search (no API key required)
- **Framework**: LangChain with LCEL (LangChain Expression Language)
- **Language**: Python 3.8+

## ⚙️ Configuration

### Model Selection Criteria (Dual-Model System)

| Task Type | Recommended Strategy | Models Used |
|-----------|---------------------|-------------|
| Vision/Images | QWEN | Qwen3-VL only |
| Text Analysis | GPT | GPT-OSS only |
| Complex Research | BOTH | Both combined |
| Multimodal + Analysis | QWEN→GPT | Sequential |

### Available Commands
- `exit` / `quit` - Exit the assistant
- `save` - Save conversation to JSON file
- `clear` - Clear conversation history
- `models` - Show available models (dual-model only)

## 🔧 Hardware Requirements

### Minimum Requirements
- **RAM**: 16GB (single model), 32GB+ (dual model)
- **Storage**: 50GB+ free space
- **CPU**: Modern multi-core processor

### Recommended Requirements
- **RAM**: 32GB+ (single), 64GB+ (dual)
- **GPU**: NVIDIA GPU with 16GB+ VRAM (optional but faster)
- **Storage**: SSD with 100GB+ free space

## 🐛 Troubleshooting

### Common Issues

#### "Model not found" error
```bash
# Check installed models
ollama list

# Pull missing models
ollama pull gpt-oss:120b-cloud
ollama pull qwen3-vl:235b-cloud
```

#### Slow performance
- Models are very large (120B-235B parameters)
- First response is slower (model loading)
- Consider smaller alternatives for speed
- Close other applications to free RAM

#### Memory issues
- Reduce model size or use one model at a time
- Monitor system resources
- Consider cloud deployment for large models

#### Search errors
- Check internet connection
- DuckDuckGo search requires web access
- Firewall may block search requests

## 🔄 Extending the Project

### Adding Document RAG
Replace web search with document search:

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="gpt-oss:120b-cloud")
vectorstore = Chroma(embedding_function=embeddings)
retriever = vectorstore.as_retriever()
```

### Adding More Models
1. Pull additional models with Ollama
2. Add model initialization in the assistant
3. Update model selection logic
4. Test compatibility and performance

### Custom Model Strategies
Modify the coordinator prompt in `dual_model_assistant.py` to:
- Add new model selection criteria
- Create custom combination strategies
- Implement domain-specific routing

## 📊 Performance Comparison

| Assistant Type | Speed | Quality | Resource Usage | Best For |
|----------------|-------|---------|----------------|----------|
| Single Model | Fast | High | Moderate | General tasks |
| Advanced Single | Fast | High | Moderate | Enhanced features |
| Smart Dual | Slow | Highest | High | Complex analysis |
| Simple Dual | Slowest | Highest | Highest | Model comparison |

## 📄 License

This project is open-source and free to use for educational and personal purposes.

## 🙏 Credits

- Based on the tutorial from [AmanXAI](https://amanxai.com/2025/11/18/build-a-real-time-ai-assistant-using-rag-langchain/)
- Built with [LangChain](https://langchain.com/)
- Powered by [Ollama](https://ollama.com/)
- Search provided by [DuckDuckGo](https://duckduckgo.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for improvement:
- Additional model integrations
- Enhanced UI/UX
- Performance optimizations
- New RAG strategies
- Documentation improvements

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review setup instructions
3. Verify model installations
4. Check system requirements
5. Open an issue on GitHub

---

**Happy AI Assisting! 🤖✨**
## Credits

Based on the tutorial from [AmanXAI](https://amanxai.com/2025/11/18/build-a-real-time-ai-assistant-using-rag-langchain/)