# Copyright Infringement Detection Action

Organization-wide copyright infringement detection using AI analysis for pull requests.

## Usage

Create a workflow file in your repository (e.g., `.github/workflows/copyright-check.yml`):

```yaml
name: Copyright Infringement Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  copyright-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Fetch full history for diff analysis
    
    - name: Run Copyright Infringement Detection
      uses: your-org/copyright-check-action@v1
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
        aacs-url: ${{ secrets.AACS }}
        aacs-api-key: ${{ secrets.AACSAPIKEY }}
        huggingface-token: ${{ secrets.HUGGINGFACE_TOKEN }}
        # Optional parameters:
        # container-registry: 'ghcr.io'  # Default
        # image-name: 'copyright-checker'  # Default
        # pr-number: ${{ github.event.pull_request.number }}  # Auto-detected
```

## Required Secrets

The following secrets must be configured in your organization or repository:

- `AACS`: AACS API endpoint URL
- `AACSAPIKEY`: AACS API key  
- `HUGGINGFACE_TOKEN`: Hugging Face token for model access
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

## Organization Setup

1. Create this action repository in your organization
2. Configure organization-level secrets
3. Add the workflow to each repository that needs copyright checking

## Features

- ✅ AI-powered copyright infringement detection
- ✅ Automated PR comments with results
- ✅ Containerized execution for consistency
- ✅ Caching for improved performance
- ✅ Organization-wide deployment

## Advanced Configuration

### Custom Model

You can specify a custom AI model by modifying the `gitDiffCheck.py` script:

```python
model, tokenizer = load_model("your-custom-model-name")
```

### Custom Analysis Rules

Modify the `analyze_copyright_infringement` function to implement custom detection logic.

## Troubleshooting

### Common Issues

1. **Model Access**: Ensure HUGGINGFACE_TOKEN has access to the required models
2. **Container Registry**: Verify permissions to push/pull from the container registry
3. **API Limits**: Consider rate limiting for high-volume usage

### Debug Mode

Add debug environment variables to the container run:

```yaml
- name: Run with Debug
  uses: your-org/copyright-check-action@v1
  with:
    # ... other parameters
  env:
    DEBUG: true
    LOG_LEVEL: debug
```