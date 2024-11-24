from lib_resume_builder_AIHawk.template_tomba import *


prompt_header = (
    """
Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished header for the resume. The header should:

1. **Name**: Specify the candidate's name.
2. **Job Title**: Specify the candidate's job title.

- **Name:**  {first_name} {last_name}
- **Job Title:**  {job_title}

"""
    + prompt_header_template
)


prompt_contact_section = (
    """
Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished contact section for the resume.

Each of this section's entry should include:
1. **Entry Icon**: Specify the entry's icon (font awesome icon class name).
2. **Entry Title**: Specify the entry title.
3. **Entry Link** : Specify the entry's link if applicable (not `None`).

- **Section Entries:**  
  {section_entries}

"""
    + prompt_contact_section_template
)


prompt_summary_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate the summary section for a resume, ensuring it aligns with the provided job description.
Attempt to use keywords from the job description only if applicable and possible.

If you make some changes to the summary's content, make sure you keep it roughly the same length.

- **Section Icon:**  
  {section_icon}

- **Section Title:**  
  {section_title}

- **Summary Content:**  
  {section_content}

- **Job Description:**  
  {job_description}

"""
    + prompt_summary_section_template
)


prompt_chronological_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate the {section_title} section for a resume, ensuring it aligns with the provided job description.

The Section should include:
1. **Section Icon**: Specify the sections's icon (font awesome icon class name).
2. **Section Title**: Specify the section title.

Each entry should include:
1. **Entry Dates**: Specify the entry's start date and end date delimited by " - " if applicable (omit `None` values).
2. **Entry Title**: Specify the entry title.
3. **Entry Location Name**: Specify the entry location's name.
4. **Entry Location Address**: Specify the entry location's adress.
5. **Entry Link**: Specify the entry's link if applicable (not `None`).
6. **Entry Details**: If applicable (not `None`), describe each entry's detail, emphasizing measurable results and specific contributions. Attempt to use keywords from the job description only if applicable and possible. If you make some changes to the entry's content, make sure you keep it roughly the same length.


- **Section Icon:**  
  {section_icon}

- **Section Title:**  
  {section_title}

- **Section Entries:**  
  {section_entries}

- **Job Description:**  
  {job_description}

"""
    + prompt_chronological_section_template
)


prompt_list_section = (
    """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate the {section_title} section for a resume, ensuring it aligns with the provided job description.

The Section should include:
1. **Section Icon**: Specify the sections's icon (font awesome icon class name).
2. **Section Title**: Specify the section title.
3. **Section Orientation**: Specify the section's orientation ("horizontal" or "vertical").

Each entry should include:
1. **Entry Dates**: Specify the entry's start date and end date delimited by " - " if applicable (omit `None` values).
2. **Entry Title**: Specify the entry title.
5. **Entry Link**: Specify the entry's link if applicable (not `None`).
6. **Entry Details**: If applicable (not `None`), describe each entry's detail, emphasizing measurable results and specific contributions. Attempt to use keywords from the job description only if applicable and possible. If you make some changes to the entry's content, make sure you keep it roughly the same length.

- **Section Icon:**  
  {section_icon}

- **Section Title:**  
  {section_title}

- **Section Orientation:**  
  {section_orientation}

- **Section Entries:**  
  {section_entries}

- **Job Description:**  
  {job_description}

"""
    + prompt_list_section_template
)

summarize_prompt_template = """
As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

Rules:
Remove boilerplate text
Include only relevant information to match the job description against the resume

# Analysis Requirements
Your analysis should include the following sections:
Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
Professional Experience: Describe the relevant work experiences that are required or preferred.
Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

# Final Result:
Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

# Job Description:
```
{text}
```

---

# Job Description Summary"""
