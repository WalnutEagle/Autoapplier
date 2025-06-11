import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

st.set_page_config(
    page_title="Resume Prompt Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem 3rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3rem;
        font-size: 1rem;
        font-weight: 500;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    .stTextInput>div>div>input {
        min-height: 3rem;
    }
    h1 {
        margin-bottom: 2rem;
    }
    .prompt-container {
        background-color: #f8f9fa;
        border: 1px solid #dce0e3;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-message {
        color: #0ec971;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def extract_job_details(url):
    """
    Extract job details (title, company, description) from a given URL
    """
    try:
        # Send a request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize variables
        job_title = ""
        company_name = ""
        job_description = ""
        
        # Extract based on common patterns (this will need customization based on the sites you target)
        # For job title - look for common patterns
        title_candidates = []
        title_candidates.extend(soup.find_all('h1'))
        title_candidates.extend(soup.find_all(['h2', 'h3'], class_=re.compile(r'title|position|job-title', re.I)))
        
        for candidate in title_candidates:
            if candidate.text.strip():
                job_title = candidate.text.strip()
                break
        
        # For company name
        company_candidates = []
        company_candidates.extend(soup.find_all(['div', 'span', 'p'], class_=re.compile(r'company|organization|employer', re.I)))
        company_candidates.extend(soup.find_all('a', class_=re.compile(r'company|organization|employer', re.I)))
        
        for candidate in company_candidates:
            if candidate.text.strip():
                company_name = candidate.text.strip()
                break
        
        # For job description
        description_candidates = []
        description_candidates.extend(soup.find_all(['div', 'section'], class_=re.compile(r'description|details|job-description', re.I)))
        description_candidates.extend(soup.find_all(['div', 'section'], id=re.compile(r'description|details|job-description', re.I)))
        
        for candidate in description_candidates:
            if candidate.text.strip():
                job_description = candidate.text.strip()
                break
        
        # If we couldn't find with specific selectors, try some fallbacks
        if not job_title:
            # Try to find by common title patterns
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                text = heading.text.strip()
                if re.search(r'(job|position|role|opening)', text, re.I):
                    job_title = text
                    break
        
        if not company_name:
            # Look for company in meta tags
            meta_company = soup.find('meta', property='og:site_name')
            if meta_company:
                company_name = meta_company['content']
        
        # Domain fallback for company
        if not company_name:
            domain = urlparse(url).netloc
            domain = domain.replace('www.', '')
            parts = domain.split('.')
            if len(parts) > 1:
                company_name = parts[0].capitalize()
        
        return {
            'job_title': job_title,
            'company_name': company_name,
            'job_description': job_description
        }
    
    except Exception as e:
        st.error(f"Error extracting job details: {str(e)}")
        return {
            'job_title': '',
            'company_name': '',
            'job_description': '',
            'error': str(e)
        }

def create_prompt_from_template(job_details):
    """
    Insert job details into the prompt template
    """
    try:
        # Using the detailed template provided by the user
        template = """ 
You are an expert resume optimizer. Help me tailor my LaTeX resume to match this specific job description.

IMPORTANT CONTEXT:
I've provided detailed narrative files (projectstory.tex and experiencestory.tex) that contain comprehensive accounts of each project and job experience. These files contain the full context, daily tasks, technologies used, challenges faced, and outcomes achieved. You must thoroughly read and understand these stories before making any changes to my main resume files.

INSTRUCTIONS:

1. DETAILED ANALYSIS:
   - FIRST, thoroughly read and analyze projectstory.tex and experiencestory.tex to understand my complete background
   - Create a comprehensive list of ALL skills, qualifications, responsibilities, and keywords from the job description
   - Group these into categories: Required Skills, Preferred Skills, Job Responsibilities, Company Values
   - Identify exact phrases and terminology used by the company
   - Map my actual experiences from the story files to the job requirements

2. EXPERIENCE MAPPING:
   - For each job requirement, identify specific elements from my story files that demonstrate my relevant experience
   - Note specific accomplishments, metrics, and technologies from my stories that align with the position
   - Determine which projects/experiences are most relevant based on this mapping
   - Prepare a plan for which stories to highlight and which to comment out

3. CONSISTENT OPTIMIZATION APPROACH:
   - For ALL sections: Comment out anything not relevant to this specific position using LaTeX comment syntax (%)
   - For ALL sections: Use the EXACT terminology from the job description, not synonyms or paraphrases
   - For ALL sections: Maintain consistent formatting and style
   - Always draw facts and details from my story files - do not invent or assume experiences

4. SECTION-SPECIFIC INSTRUCTIONS:
   A. skills.tex: 
      * Based on my detailed stories, include ONLY skills I actually possess that match the job requirements
      * Reorganize categories to prioritize most relevant skills first
      * REMOVE irrelevant skills (via commenting) even if they seem impressive
      * List skills using the EXACT same terminology as the job description

   B. experience.tex: 
      * Using the rich details from experiencestory.tex, craft concise, powerful bullet points
      * COMMENT OUT any positions that have no relevance to the target job
      * Begin bullets with strong action verbs related to the job responsibilities
      * Include specific metrics and achievements mentioned in my stories
      * Incorporate exact keywords from the job description where they authentically match my experience

   C. projects.tex: 
      * Draw from the detailed projectstory.tex to create compelling, relevant bullet points
      * Place MOST RELEVANT projects for this position FIRST
      * COMMENT OUT projects with little relevance to the target position
      * Emphasize aspects of each project that align with job requirements
      * Use EXACT terminology from the job description where it authentically matches my work
      * Highlight teamwork, technical skills, and problem-solving abilities relevant to the position

5. KEYWORD DENSITY REQUIREMENTS:
   - Include each key skill/requirement from the job description in AT LEAST two different sections where honestly applicable
   - Ensure terminology is IDENTICAL to the job posting (not synonyms)
   - Do not force keywords where they don't naturally fit with my actual experience
   - Concentrate on the REQUIRED qualifications first, then preferred qualifications

6. VERIFICATION STEPS:
   - After completing edits, verify that your modified resume addresses EVERY qualification in the job description
   - Confirm ALL IRRELEVANT content has been commented out or removed
   - Ensure the resume maintains a PROFESSIONAL and COHESIVE flow despite modifications
   - Check that the SAME optimization approach is applied CONSISTENTLY across all sections
   - Verify all bullet points are FACTUALLY ACCURATE based on my story files

IMPORTANT: 
- DO NOT invent skills or experiences not found in my story files
- ONLY comment out irrelevant information (don't delete it)
- Be CONSISTENT in approach across ALL sections
- The resume must pass both ATS screening AND human review
- Draw ONLY from my actual experiences as detailed in the story files

JOB DESCRIPTION: {{JOB_DESCRIPTION}}
COMPANY: {{COMPANY_NAME}}
POSITION: {{JOB_TITLE}}"""
        
        # Replace placeholders in the template
        prompt = template.replace('{{JOB_TITLE}}', job_details['job_title'])
        prompt = prompt.replace('{{COMPANY_NAME}}', job_details['company_name'])
        prompt = prompt.replace('{{JOB_DESCRIPTION}}', job_details['job_description'])
        
        return prompt
    
    except Exception as e:
        st.error(f"Error creating prompt from template: {str(e)}")
        return None

def main():
    st.title("📄 Resume Prompt Generator")
    
    st.write("""
    This tool extracts job details from a posting URL and generates a customized prompt for tailoring your resume using AI.
    Simply paste the URL of a job posting, click the button, and get a ready-to-use prompt.
    """)
    
    # URL input
    url = st.text_input("Job Posting URL:", placeholder="https://example.com/job-posting")
    
    # Generate button
    if st.button("Generate Prompt", type="primary"):
        if not url:
            st.warning("Please enter a job posting URL")
        else:
            with st.spinner("Extracting job details and generating prompt..."):
                # Extract job details
                job_details = extract_job_details(url)
                
                if 'error' in job_details:
                    st.error(f"Failed to extract job details: {job_details['error']}")
                    return
                
                if not job_details['job_title'] and not job_details['company_name'] and not job_details['job_description']:
                    st.error("Failed to extract any job details. The script may need to be adapted for this specific job site.")
                    return
                
                # Create prompt
                prompt = create_prompt_from_template(job_details)
                if not prompt:
                    st.error("Failed to create prompt from template.")
                    return
                
                # Display results
                st.success("Job details extracted successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Job Title", job_details['job_title'] or "Not found")
                with col2:
                    st.metric("Company", job_details['company_name'] or "Not found")
                
                st.write(f"**Description Length:** {len(job_details['job_description'])} characters")
                
                st.subheader("Generated Prompt")
                st.markdown("<div class='prompt-container'>", unsafe_allow_html=True)
                st.text_area("", value=prompt, height=300, key="prompt_area", label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Copy button implementation
                st.write("")  # Spacing
                col1, col2 = st.columns([1, 1])
                with col1:
                    copy_button = st.button("Copy Prompt to Clipboard", type="secondary")
                
                # Use JavaScript to copy to clipboard when the button is clicked
                if copy_button:
                    st.markdown("""
                    <script>
                        var copyText = document.querySelector('textarea[data-baseweb="textarea"]');
                        copyText.select();
                        document.execCommand('copy');
                    </script>
                    """, unsafe_allow_html=True)
                    st.markdown("<p class='success-message'>Prompt copied to clipboard!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
