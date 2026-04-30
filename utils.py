import os

def ensure_directories():
    """Create required directories if they don't exist."""
    directories = ["input_pdfs", "output_reports", "temp"]
    for d in directories:
        os.makedirs(d, exist_ok=True)


def create_env_example():
    """Create .env example template."""
    env_content = """# Copy this to .env and add your OpenAI key
OPENAI_API_KEY=sk-your-openai-api-key-here
"""
    with open(".env.example", "w") as f:
        f.write(env_content)
