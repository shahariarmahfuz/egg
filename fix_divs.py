import os
import glob
import re

template_dir = '/workspaces/egg/templates'
report_files = glob.glob(os.path.join(template_dir, '*_report.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Check if there is </table>\s*{% endblock %}
    # If so, replace with </table>\n</div>\n{% endblock %}
    
    pattern = r'</table>\s*{% endblock %}'
    if re.search(pattern, content):
        content = re.sub(pattern, '</table>\n</div>\n{% endblock %}', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed unclosed div in {os.path.basename(filepath)}")

for filepath in report_files:
    process_file(filepath)

print("Done fixing divs.")
