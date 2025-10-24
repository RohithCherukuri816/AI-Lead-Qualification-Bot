# Troubleshooting Guide

This guide helps resolve common issues when running the AI Lead Qualification Bot.

## Common Issues and Solutions

### 1. LLM Model Access Issues

**Problem**: Error messages like "You are trying to access a gated repo" or "401 Client Error"

**Cause**: The default model (`mistralai/Mistral-7B-Instruct-v0.2`) requires Hugging Face authentication.

**Solutions**:

#### Option A: Use Hugging Face Token (Recommended)
1. Create a Hugging Face account at https://huggingface.co
2. Accept the model terms at https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
3. Create a token at https://huggingface.co/settings/tokens
4. Set the token as an environment variable:
   ```bash
   export HUGGING_FACE_HUB_TOKEN=your_token_here
   ```
   Or on Windows:
   ```cmd
   set HUGGING_FACE_HUB_TOKEN=your_token_here
   ```

#### Option B: Use Alternative Model (Current Default)
The application now uses `microsoft/DialoGPT-medium` by default, which doesn't require authentication.

To change back to Mistral after getting authentication:
1. Edit `config/settings.py`
2. Change `llm_model_name` to `"mistralai/Mistral-7B-Instruct-v0.2"`

### 2. Predictive Model Training Errors

**Problem**: "invalid syntax" errors during model training

**Cause**: The training data parsing was using `eval()` on malformed strings with escaped quotes.

**Solution**: Fixed in the code. The application now:
1. Uses `ast.literal_eval()` for safer parsing
2. Cleans up escaped quotes (`\\'` → `'`)
3. Removes outer quotes if present
4. Falls back to `json.loads()` if `ast.literal_eval()` fails

### 3. LangChain Deprecation Warnings

**Problem**: Warnings about deprecated imports

**Solution**: Fixed in the code. Updated imports to use `langchain_community`.

### 4. Missing Accelerate Package

**Problem**: Error "Using a `device_map` requires `accelerate`"

**Cause**: The `accelerate` package is required for automatic device mapping in transformers.

**Solution**: 
1. Install accelerate: `pip install accelerate`
2. Or add it to requirements.txt (already done in the latest version)

### 5. Hugging Face Hub Cache Warnings

**Problem**: Warnings about symlink limitations on Windows

**Cause**: Windows file system limitations with Hugging Face caching.

**Solutions**:
1. **Ignore the warning** - The application still works
2. **Enable Developer Mode** on Windows:
   - Go to Settings > Update & Security > For Developers
   - Turn on Developer Mode
3. **Run as Administrator** - Run Python/IDE as administrator
4. **Set environment variable**:
   ```cmd
   set HF_HUB_DISABLE_SYMLINKS_WARNING=1
   ```

### 6. Memory Issues

**Problem**: Out of memory errors when loading large models

**Solutions**:
1. **Use smaller model**: Change to a smaller model in `config/settings.py`
2. **Reduce batch size**: Modify `llm_max_length` in settings
3. **Use CPU only**: Set `device_map="cpu"` in LLM initialization
4. **Increase system memory**: Add more RAM to your system

### 7. Missing Dependencies

**Problem**: Import errors for required packages

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### 8. File Path Issues

**Problem**: File not found errors

**Solutions**:
1. **Check file structure**: Ensure all directories exist as shown in README
2. **Use absolute paths**: Modify paths in `config/settings.py`
3. **Create missing directories**: Run the application once to auto-create directories

### 9. Vector Database Issues

**Problem**: FAISS index errors

**Solutions**:
1. **Delete and rebuild**: Remove `data/vector_store/` directory
2. **Check embeddings**: Ensure embedding model is accessible
3. **Reduce chunk size**: Modify `chunk_size` in settings

## Testing Your Setup

Run the test script to verify everything works:

```bash
python test_bot.py
```

This will test:
- Configuration validation
- Vector store functionality
- Predictive model training
- LLM initialization
- CRM integration
- Conversation flow
- Sample data processing

## Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look for detailed error messages in the console output
2. **Review configuration**: Verify settings in `config/settings.py`
3. **Test components**: Use `test_bot.py` for component-specific testing
4. **Check dependencies**: Ensure all packages are installed correctly

## Performance Optimization

For better performance:

1. **Use GPU**: Install PyTorch with CUDA support
2. **Reduce model size**: Use smaller models for faster inference
3. **Optimize batch processing**: Adjust batch sizes in settings
4. **Use caching**: Enable model caching where possible

## Security Notes

- Never commit API keys or tokens to version control
- Use environment variables for sensitive configuration
- Regularly update dependencies for security patches
- Monitor model outputs for sensitive information
