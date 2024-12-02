prompt_header_template = """
- **Template to Use**
```
<header>
  <h1>[Name]</h1>

  # Include this only if job title is applicable (not `None`)
  <h2>[Job Title]</h2>
  
</header>
```
Follow the instructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, unnecessary spaces, explanations, or additional text and also without ```html ```"""


prompt_contact_section_template = """
- **Template to Use**
```
<section class="contact">
  <div class="entries horizontal wrappable">
  
    # Include only if "Address" entry is provided
    <div class="entry horizontal centered">
      <i class="fa-solid fa-location-dot"></i>
      <span class="entry-title">[Address]</span>
    </div>
    
    # Include only if "Email" entry is provided
    <div class="entry horizontal centered">
      <a href="mailto:[Email]">
        <i class="fa-solid fa-envelope"></i>
        <span class="entry-title">[Email]</span>
      </a>
    </div>
    
    # Include only if "Phone" entry is provided
    <div class="entry horizontal centered">
      <a href="tel:[Phone]">
        <i class="fa-solid fa-phone"></i>
        <span class="entry-title">[Phone]</span>
      </a>
    </div>
    
    # Include this div only if "Linkedin" entry is applicable (not `None`)
    <div class="entry horizontal centered">
      <a href="[Linkedin]">
        <i class="fa-brands fa-linkedin"></i>
        <span class="entry-title">[Linkedin]</span>
      </a>
    </div>
    
    
    # Include this div only if "Github" entry is applicable (not `None`)
    <div class="entry horizontal centered ">
      <a href="[Github]">
        <i class="fa-brands fa-github"></i>
        <span class="entry-title">[Github]</span>
      </a>
    </div>
    
    # Include this div only if "Website" entry is applicable (not `None`)
    <div class="entry horizontal centered">
      <a href="[Website]">
        <i class="fa-solid fa-globe"></i>
        <span class="entry-title">[Website]</span>
      </a>
    </div>
    
    # If "Custom Entries" is applicable (not `None`) create divs for each entry according to one of these templates:
      
      # Template div for an entry with NO "Link" property provided (e.g `None`)
      <div class="entry horizontal centered">
        <i class="[Entry Icon]"></i>
        <span class="entry-title">[Entry Title]</span>
      </div>
      
      # Template div for an entry WITH "Link" property provided (not `None`)
      <div class="entry horizontal centered">
        <a href="[Entry Link]">
          <i class="[Entry Icon]"></i>
          <span class="entry-title">[Entry Title]</span>
        </a>
      </div>
      
  </div>
</section>
```
Follow the instructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, unnecessary spaces, explanations, or additional text and also without ```html ```"""


prompt_summary_section_template = """
- **Template to Use**
```
<section class="summary">

  # Include this div only if "Section Title" is applicable (not `None`)
  <div class="section-header">
  
    # Include this i tag only if "Section Icon" is provided (not `None`)
    <i class="[Section Icon]"></i>
    
    <h3>[Section Title]</h3>
  </div>

  <p class="content">[Section Content]</p>
</section>
```
Follow the instructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, unnecessary spaces, explanations, or additional text and also without ```html ```"""


prompt_chronological_section_template = """
- **Template to Use**
```
<section class="chronological">
  <div class="section-header">
  
    # Include this i tag only if "Section Icon" is provided (not `None`)
    <i class="[Section Icon]"></i>
    
    <h3>[Section Title]</h3>
  </div>
  
  <div class="entries">
  
    # For each entry in "Entries" create a div following this template:
    <div class="entry horizontal">
      <div class="entry-left">
        <span class="entry-dates">[Entry Dates]</span>
      </div>
      <div class="entry-middle">
    
        # Include this div only if entry "Entry Link" property is provided (not `None`)
        <div class="entry-header">
          <a href="[Entry Link]">
            <span class="entry-title">[Entry Title]</span>
    
            # Include this span only if "Entry Location Name" property is provided (not `None`)
            <span class="entry-location-name">[Entry Location Name]</span>
    
            <i class="fa-solid fa-link"></i>
          </a>
        </div>
    
        # Include this div only if "Entry Link" property is not provided (e.g `None`)
        <div class="entry-header">
          <span class="entry-title">[Entry Title]</span>
    
          # Include this span only if "Entry Location Name" property is provided (not `None`)
          <span class="entry-location-name">[Entry Location Name]</span>
    
        </div>
        # Include this span only if "Entry Content" property is provided (not `None`)
        <span class="entry-content">[Entry Content]</span>
        
        # Include this ul tag only if "Entry Details" property was provided (not `None`)
        <ul class="entry-details">
          # For each "Entry Detail" in "Entry Details" create a li tag
          <li>[Entry Detail]</li>
        </ul>
        
        # Include this span only if "Entry Content" property is provided (not `None`)
        <span class="entry-content">[Entry Content]</span>
    
    </div>
  </div>
  
</section>
```
Follow the instructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, unnecessary spaces, explanations, or additional text and also without ```html ```"""


prompt_list_section_template = """
- **Template to Use**
```
<section class="list">
  <div class="section-header">
  
    # Include this i tag only if "Section Icon" is provided (not `None`)
    <i class="[Section Icon]"></i>
    
    <h3>[Section Title]</h3>
  </div>
  
  <div class="entries [Section Orientation]">
  
    # For each entry in "Entries" create a div following this template:
    <div class="entry">
    
      # Include this div only if entry "Entry Link" property is provided (not `None`)
      <div class="entry-header">
        <a href="[Entry Link]">
          <span class="entry-title">[Entry Title]</span>
          
          # Include this span only if "Entry Description" property is provided (not `None`)
          <span class="entry-description">[Entry Description]</span>
          <i class="fa-solid fa-link"></i>
        </a>
      </div>
      
      # Include this div only if "Entry Link" property is not provided (e.g `None`)
      <div class="entry-header">
          <span class="entry-title">[Entry Title]</span>
          
          # Include this span tag only if "Entry Description" property is provided (not `None`)
          <span class="entry-description">[Entry Description]</span>
    
      </div>
      
      # Include this ul tag only if "Entry Details" property was provided (not `None`)
      <ul class="entry-details">
        # For each "Entry Detail" in "Entry Details" create a li tag
        <li>[Entry Detail]</li>
      </ul>
      
      # Include this span only if "Entry Content" property is provided (not `None`)
      <span class="entry-content">[Entry Content]</span>
    
    </div>
  </div>

</section>
```
Follow the instructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, unnecessary spaces, explanations, or additional text and also without ```html ```"""
