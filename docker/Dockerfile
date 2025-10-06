# Dockerfile for Copyright Infringement Detection
FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip git curl gh && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    transformers \
    torch \
    accelerate \
    requests \
    numpy \
    GitPython

# Set work directory
WORKDIR /app

# Copy the analysis scripts (assuming build context is action root)
COPY gitDiffCheck.py /app/gitDiffCheck.py
#COPY testScript.py /app/testScript.py

# Make scripts executable
# RUN chmod +x /app/gitDiffCheck.py /app/testScript.py
RUN chmod +x /app/gitDiffCheck.py

CMD ["python3", "gitDiffCheck.py"]

