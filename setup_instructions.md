# Setup Instructions

Follow these steps to get your Real-Time AI Assistant running:

## Step 1: Install Ollama

1. Go to [ollama.com](https://ollama.com)
2. Download Ollama for your operating system (Windows, Mac, or Linux)
3. Install the application

## Step 2: Download the AI Model

Open your terminal/command prompt and run:
```bash
ollama pull gpt-oss:120b-cloud
```

This downloads the GPT-OSS 120B Cloud model. Note: This is a large model and may take significant time and storage space.

## Step 3: Install Python Dependencies

In your project directory, run:
```bash
pip install -r requirements.txt
```

## Step 4: Run the Assistant

Start the assistant:
```bash
python assistant.py
```

## Verification

To verify everything is working:

1. **Check Ollama**: Run `ollama list` to see if `gpt-oss:120b-cloud` is installed
2. **Test the assistant**: Ask it a current events question to see if web search works
3. **Check responses**: The assistant should provide real-time, web-searched information

## Common Issues

### "Model not found" error
- Make sure you ran `ollama pull gpt-oss:120b-cloud`
- Check with `ollama list` that the model is available

### Slow responses
- The GPT-OSS 120B model is very large and runs locally on your hardware
- First responses may be slower as the model loads
- Consider using a smaller model like `llama3:8b` for faster responses if needed

### Search not working
- Check your internet connection
- DuckDuckGo search requires internet access

## Alternative Models

You can try different models by changing the model name in `assistant.py`:

- `gpt-oss:120b-cloud` - Current large model (high quality, slower)
- `llama3:8b` - Smaller, faster alternative
- `llama3:3b` - Even faster, smaller model
- `mistral:7b` - Alternative model option
- `codellama:7b` - Better for code-related questions

To use a different model:
1. Pull it: `ollama pull llama3:8b`
2. Update the model name in `assistant.py`