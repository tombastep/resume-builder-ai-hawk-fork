from lib_resume_builder_AIHawk.template_base import *


prompt_header = (
    """
Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished header for the resume. The header should:

1. **Name**: Specify the candidate's name.
2. **Job Title**: Specify the candidate's job title.

- **Name:**
  {name}
  
- **Job Title:**
  {job_title}

"""
    + prompt_header_template
)


prompt_contact_section = (
    """
Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished contact section for the resume.

The Section should include:
1. **Section Title**: Specify the section title (omit if `None`).
2. **Section Icon**: Specify the sections's font awesome icon class name (omit if `None`).
3. **Address (omit if `None`)**:  Specify the applicant's address
4. **Phone (omit if `None`)**: Specify the applicant's phone number.
5. **Email (omit if `None`)**: Specify the applicant's email address.
6. **LinkedIn (omit if `None`)**: Specify the applicant's linkedin profile url.
7. **Github (omit if `None`)**: Specify the applicant's github profile url.
8. **Website (omit if `None`)**: Specify the applicant's website url.
9. **Custom Entries**: Omit if `None`, otherwise each entry should include:
  a. **Entry Icon**: Specify the entry's icon (font awesome icon class name).
  b. **Entry Title**: Specify the entry title.
  c. **Entry Link** : Specify the entry's link if applicable (omit if `None`).

- **Section Title:**  
  {title}

- **Section Icon:**  
  {icon}

- **Address:**
  {address}
  
- **Phone:**
  {phone}
  
- **Email:**
  {email}
  
- **LinkedIn:**
  {linkedin}
  
- **Github:**
  {github}
  
- **Website:**
  {website}
  
- **Custom Entries:**  
  {custom_entries}

"""
    + prompt_contact_section_template
)


prompt_summary_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate the summary section for a resume.

The Section should include:
1. **Section Content**: Specify the section's text content, keeping it concise and clear. If you make changes to the content, make sure you keep it roughly the same length as the provided content.
2. **Section Title**: Specify the section title (omit if `None`).
3. **Section Icon**: Specify the sections's font awesome icon class name (omit if `None`).

- **Section Content:**  
  {content}
  
- **Section Title:**  
  {title}

- **Section Icon:**  
  {icon}

"""
    + prompt_summary_section_template
)


prompt_chronological_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate this section for a resume.

The Section should include:
1. **Section Title**: Specify the section title.
2. **Section Icon**: Specify the sections's font awesome icon class name (omit if `None`).
3. **Section Entries**: Omit if `None`, otherwise each entry should include:
  a. **Entry Dates**: Specify the entry's start date and end date delimited by " - " if applicable (omit `None` values).
  b. **Entry Title**: Specify the entry title.
  c. **Entry Location Name**: Specify the entry location's name.
  d. **Entry Location Address**: Specify the entry location's address.
  e. **Entry Link**: Specify the entry's link if applicable (omit if `None`).
  f. **Entry Content**: Specify the entry's text content if provided (omit if `None`).
  g. **Entry Details**: If applicable (omit if `None`), describe each entry's detail, emphasizing measurable results and specific contributions. If you make some changes to the entry's content, make sure you keep it roughly the same length.

- **Section Title:**  
  {title}

- **Section Icon=:**  
  {icon}

- **Section Entries:**  
  {entries}

"""
    + prompt_chronological_section_template
)


prompt_list_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate this section for a resume.

The section should include:
1. **Section Icon**: Specify the sections's icon (font awesome icon class name).
2. **Section Title**: Specify the section title.
3. **Section Orientation**: Specify the section's orientation ("horizontal" or "vertical").

The Section should include:
1. **Section Title**: Specify the section title.
2. **Section Icon**: Specify the sections's font awesome icon class name (omit if `None`).
3. **Section Orientation**: Specify the section's orientation ("horizontal" or "vertical").
4. **Section Entries**: each entry should include:
  a. **Entry Title**: Specify the entry title.
  b. **Entry Link**: Specify the entry's link if applicable (not `None`).
  c. **Entry Orientation**: Specify the entry's orientation ("horizontal" or "vertical") if applicable (omit if `None`).
  d. **Entry Content**: Specify the entry's text content if provided (omit if `None`).
  e. **Entry Details**: If applicable (not `None`), describe each entry's detail, emphasizing measurable results and specific contributions. If you make some changes to the entry's content, make sure you keep it roughly the same length.

- **Section Title:**  
  {title}

- **Section Icon (omit if `None`):**  
  {icon}

- **Section Orientation:**  
  {orientation}

- **Section Entries:**  
  {entries}

"""
    + prompt_list_section_template
)
