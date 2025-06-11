# Resume Prompt Generator (Streamlit Version)

A simple Streamlit web application that extracts job details from a posting URL and generates a customized resume prompt.

## What is Streamlit?

Streamlit is an open-source Python library that makes it easy to create beautiful, interactive web applications for data science and machine learning projects. It's famous for its simplicity - you can create powerful web applications with just a few lines of Python code.

## Features

- **Simple Interface**: Clean, user-friendly design
- **One-Click Generation**: Just paste a URL and click
- **Job Detail Extraction**: Automatically pulls job title, company, and description
- **Prompt Generation**: Creates a customized prompt based on the extracted information
- **Copy to Clipboard**: Easy copying of the generated prompt
- **Responsive Design**: Works on desktop and mobile devices

## Installation

```bash
# Create and activate a conda environment (optional but recommended)
conda create -n streamlit-resume python=3.9
conda activate streamlit-resume

# Install the required packages
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Your default web browser will automatically open to http://localhost:8501

3. Paste a job posting URL in the input field

4. Click "Generate Prompt"

5. The application will extract the job details and generate a customized prompt

6. Use the "Copy Prompt to Clipboard" button to copy the generated prompt

7. Paste the prompt to your AI agent of choice (ChatGPT, Claude, etc.) to get a tailored resume

## Advantages of the Streamlit Version

- **Simpler Code**: The entire application is contained in a single Python file
- **No HTML/CSS/JS Knowledge Required**: Everything is handled by Streamlit
- **Better User Experience**: Built-in progress indicators, interactive elements
- **Easy to Deploy**: Can be deployed to Streamlit Cloud with minimal setup
- **Rich Components**: Uses Streamlit's built-in components for better UI/UX
- **Responsive Design**: Automatically adapts to different screen sizes

## Customization

If you need to adapt the extraction logic for specific job sites, you can modify the `extract_job_details` function in the `app.py` file.

## Deployment Options

The Streamlit version can easily be deployed to:

1. **Streamlit Cloud**: Free hosting for public repositories
2. **Heroku**: With a simple Procfile
3. **AWS/Azure/GCP**: Using their Python app hosting services
4. **Local Network**: Share on your local network with `streamlit run app.py --server.address=0.0.0.0`
