# Dual-Model Setup Instructions

Follow these steps to set up the dual-model AI assistant using both Qwen3-VL and GPT-OSS:

## Step 1: Install Ollama

1. Go to [ollama.com](https://ollama.com)
2. Download Ollama for your operating system (Windows, Mac, or Linux)
3. Install the application

## Step 2: Download Both AI Models

Open your terminal/command prompt and run these commands:

```bash
# Pull the Qwen3-VL model (for vision and multimodal tasks)
ollama pull qwen3-vl:235b-cloud

# Pull the GPT-OSS model (for general reasoning)
ollama pull gpt-oss:120b-cloud
```

**Note:** These are very large models and will require significant storage space and download time.

## Step 3: Install Python Dependencies

In your project directory, run:
```bash
pip install -r requirements.txt
```

## Step 4: Run the Dual-Model Assistant

Start the assistant:
```bash
python dual_model_assistant.py
```

## How the Dual-Model System Works

The assistant intelligently chooses which model(s) to use based on your question:

### Model Selection Strategies:

1. **QWEN Only** - For vision tasks, image analysis, multimodal content, Chinese language
2. **GPT Only** - For general reasoning, complex analysis, English text generation  
3. **BOTH** - Uses both models and combines their responses for comprehensive answers
4. **QWEN_THEN_GPT** - Uses Qwen first for initial analysis, then GPT to refine and enhance

### Example Use Cases:

- **Vision/Images**: "Analyze this image" → Uses Qwen3-VL
- **Complex Reasoning**: "Explain quantum computing" → Uses GPT-OSS
- **Comprehensive Analysis**: "Compare AI models" → Uses BOTH models
- **Multimodal + Analysis**: "Describe this chart and analyze trends" → Uses QWEN_THEN_GPT

## Verification

To verify everything is working:

1. **Check both models**: Run `ollama list` to see both models installed:
   - `qwen3-vl:235b-cloud`
   - `gpt-oss:120b-cloud`

2. **Test the assistant**: Ask different types of questions to see model selection in action

3. **Check model switching**: The assistant will show which strategy it's using for each question

## Commands Available

- `exit` - Quit the assistant
- `save` - Save conversation to JSON file
- `clear` - Clear conversation history
- `models` - Show information about available models

## Performance Notes

### Expected Behavior:
- **Model Selection**: ~2-3 seconds to determine strategy
- **Single Model**: Response time depends on model size and complexity
- **Dual Model**: Longer response time as it uses multiple models
- **First Run**: Models need to load initially (slower first response)

### Hardware Requirements:
- **RAM**: Minimum 32GB recommended for both models
- **Storage**: ~400GB+ for both models
- **GPU**: Optional but significantly improves performance

## Troubleshooting

### "Model not found" errors
```bash
# Verify both models are installed
ollama list

# If missing, pull them:
ollama pull qwen3-vl:235b-cloud
ollama pull gpt-oss:120b-cloud
```

### Slow performance
- Both models are very large (235B and 120B parameters)
- Consider using smaller alternatives if speed is critical:
  - `qwen2-vl:7b` instead of `qwen3-vl:235b-cloud`
  - `llama3:8b` instead of `gpt-oss:120b-cloud`

### Memory issues
- Close other applications to free RAM
- Consider using one model at a time if system resources are limited

### Model selection issues
- The system defaults to GPT-OSS if strategy determination fails
- You can manually specify model preference by modifying the coordinator prompt

## Alternative Configurations

You can modify `dual_model_assistant.py` to:
- Force specific model combinations
- Adjust model selection criteria
- Add more models to the system
- Change the combination strategy