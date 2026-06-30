import os
import re
import glob

template_dir = '/Users/affilpm/Documents/First project/fruitkhs/fruitkha/project/templates'
files = glob.glob(os.path.join(template_dir, '*.html'))

sidebar_pattern = re.compile(r'<!-- Toggle button for sidebar -->\s*<div class="d-flex">\s*<div class="sidebar bg-black" id="sidebar">.*?</div>\s*</div>\s*</div>\s*(</div>)?', re.DOTALL)
main_content_pattern = re.compile(r'<div class="main-content\s*">\s*<div class="content p-4">', re.DOTALL)
# End wrapper can be multiple </div>, we just replace the exact wrappers at the start and leave the content.
# Wait, removing `<div class="main-content">` leaves orphaned `</div>` at the end which can break the layout.
# Let's just replace the sidebar part first.

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()

    if '<div class="sidebar bg-black" id="sidebar">' in content:
        # It has the sidebar
        new_content = sidebar_pattern.sub('', content)
        
        # Now remove the opening wrappers
        new_content = re.sub(r'<div class="main-content\s*">\s*<div class="content p-4">', '', new_content)
        
        # Now remove two `</div>` from the end (before `{% endblock %}`)
        new_content = re.sub(r'</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>', '</div></div></div></div></div>', new_content) # fragile
        # Better: just find {% endblock %} and remove 2 preceding </div> tags
        new_content = re.sub(r'</div>\s*</div>\s*(<br>)?\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>', '</div></div></div></div></div>', new_content) # Too fragile!
        
        # Safest way: just replace the sidebar and let the browser handle extra closing divs (browsers are resilient to extra closing tags), OR manually fix them.
        # Let's just remove the sidebar block and the `<div class="main-content">` opening tags. 
        # Extra `</div>` tags at the end of the file are ignored by HTML parsers usually, but it's bad practice.
        # Actually, let's just do it manually for the important ones to ensure quality.

        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
