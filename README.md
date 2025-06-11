# AutoApplier - Job Application Prompt Generator

AutoApplier is a tool that automatically extracts job details from a job posting URL and generates a customized prompt for tailoring your resume using AI.

## How It Works

1. The tool takes a job posting URL as input
2. It scrapes the webpage to extract the job title, company name, and job description
3. It inserts these details into your prompt template
4. It saves the completed prompt to a text file that you can use with an AI agent

## Requirements

- Python 3.6 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

Basic usage:

```
python main.py "https://example.com/job-posting-url"
```

This will use the default template (`prompt_template.txt`) and output the generated prompt to `generated_prompt.txt`.

### Custom Options

You can specify a custom template file and output location:

```
python main.py "https://example.com/job-posting-url" --template "my_template.txt" --output "my_prompt.txt"
```

### Template Format

Your template file should contain the following placeholders:
- `{{JOB_TITLE}}` - Will be replaced with the extracted job title
- `{{COMPANY_NAME}}` - Will be replaced with the extracted company name
- `{{JOB_DESCRIPTION}}` - Will be replaced with the extracted job description

## Customization

The web scraping functionality is designed to work with common job posting sites, but may need adjustment for specific websites. If the tool is not correctly extracting information from your target sites, you may need to modify the `extract_job_details` function in `main.py`.

## Troubleshooting

If you're having trouble with specific job sites, you might need to:

1. Inspect the HTML of the page to understand its structure
2. Modify the selectors in the `extract_job_details` function
3. Add site-specific extraction logic for websites you commonly use

## License

This project is open source and available for personal use.
