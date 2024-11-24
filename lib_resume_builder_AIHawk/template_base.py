prompt_header_template = """
- **Template to Use**
```
<header>
  <h1>[Name]</h1>
  <h2>[Job Title]</h2>
</header>
```
Follow the intructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, explanations or additional text and also without ```html ```"""


prompt_contact_section_template = """
- **Template to Use**
```
<section class="contact">

  # An example for an entry with NO link data provided
  <div class="entry">
    <i class="[Entry Icon]"></i>
    <span class="entry-title">
      [Entry Title]
    </span>
  </div>

  # An example for an entry with link data provided
  <div class="entry">
    <a href="[Entry Link]">
      <i class="[Entry Icon]"></i>
      <span class="entry-title">
        [Entry Title]
      </span>
    </a>
  </div>

</section>
```
Follow the intructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, explanations or additional text and also without ```html ```"""


prompt_summary_section_template = """
- **Template to Use**
```
<section class="summary">

  # Include this only if section title and icon data is applicable (not `None`)
  <div class="section-header">
    <i class="[Section Icon]"></i>
    <h3>[Section Title]</h3>
  </div>

  <p class="summary-content>
    [Summary Content]
  </p>
</section>
```
Follow the intructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, explanations or additional text and also without ```html ```"""


prompt_chronological_section_template = """
- **Template to Use**
```
<section class="chronological">
  <div class="section-header">
    <i class="[Section Icon]"></i>
    <h3>[Section Title]</h3>
  </div>
  <div class="entry">
    <div class="entry-left">
      <span class="entry-dates">
        [Entry Dates]
      </span>
    </div>
    <div class="entry-middle">
      <div class="entry-header">

        # Include this only if entry link data is applicable (not `None`)
        <a href="[Entry Link]">
          <span class="entry-title">
            [Entry Title]
          </span>
          <span class="entry-location-name">
            [Entry Location Name]
          </span>
          <i class="fa-solid fa-link"></i>
        </a>

        # Include this only if entry link data was NOT provided (i.e: `None`)
        <span class="entry-title">
          [Entry Title]
        </span>
        <span class="entry-location-name">
          [Entry Location Name]
        </span>

      </div>

      # Include this only if entry details data is applicable (not `None`)
      <ul class="entry-details">
        <li>[Entry Detail]</li>
        <li>[Entry Detail]</li>
        <li>[Entry Detail]</li>
      </ul>

    </div>
    <div class="entry-right">
      <span class="entry-address">
        [Entry Location Address]
      </span>
    </div>
  </div>
</section>
```
Follow the intructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, explanations or additional text and also without ```html ```"""


prompt_list_section_template = """
- **Template to Use**
```
<section class="simple-list [Section Orientation]">
  <div class="section-header">
    <i class="[Section Icon]"></i>
    <h3>[Section Title]</h3>
  </div>
  <div class="entry">

    # Include this only if entry link data is applicable (not `None`)
    <div class="entry-header">
      <a href="[Entry Link]">
        <span class="entry-title">
          [Entry Title]
        </span>

        # Include this only entry description data is applicable (not `None`)
        <span class="entry-description">
          [Entry Description]
        </span>

        <i class="fa-solid fa-link"></i>
      </a>
    </div>

    # Include this only if entry link data was NOT provided (i.e: `None`)
    <div class="entry-header">
        <span class="entry-title">
          [Entry Title]
        </span>

        # Include this only entry description data is applicable (not `None`)
        <span class="entry-description">
          [Entry Description]
        </span>

    </div>

    # Include this only if entry details data is applicable (not `None`)
    <ul class="entry-details">
      <li>[Entry Detail]</li>
      <li>[Entry Detail]</li>
      <li>[Entry Detail]</li>
    </ul>
    
  </div>

</section>
```
Follow the intructions commented within the above template if applicable.
The results should be provided in html format, Provide only the html code for the resume, without any comments, explanations or additional text and also without ```html ```"""
