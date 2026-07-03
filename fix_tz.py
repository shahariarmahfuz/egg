import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    
    # Check if file has any datetime or utcnow usage
    if 'datetime' not in content:
        return
        
    # Make sure we import dhaka_now and dhaka_now_date
    if filepath.endswith('models.py'):
        # models.py already has the import due to my sed command earlier, wait, no, I just put dhaka_now in it.
        # Let's clean it up properly.
        content = re.sub(r'from datetime import datetime\nfrom zoneinfo import ZoneInfo\n\ndef dhaka_now\(\):\n    return datetime.now\(ZoneInfo\("Asia/Dhaka"\)\).replace\(tzinfo=None\)', 'from datetime import datetime\nfrom zoneinfo import ZoneInfo\n\ndef dhaka_now():\n    return datetime.now(ZoneInfo("Asia/Dhaka")).replace(tzinfo=None)\n\ndef dhaka_now_date():\n    return dhaka_now().date()', content)
        if 'dhaka_now_date' not in content:
            # Maybe the sed failed or didn't match exactly?
            pass
            
    # Replace default=datetime.utcnow().date with default=dhaka_now_date
    content = re.sub(r'default\s*=\s*datetime\.utcnow\(\)\.date', 'default=dhaka_now_date', content)
    
    # Replace default=datetime.utcnow with default=dhaka_now
    content = re.sub(r'default\s*=\s*datetime\.utcnow', 'default=dhaka_now', content)
    
    # Replace onupdate=datetime.utcnow with onupdate=dhaka_now
    content = re.sub(r'onupdate\s*=\s*datetime\.utcnow', 'onupdate=dhaka_now', content)
    
    # Replace datetime.utcnow().date() with dhaka_now().date()
    content = re.sub(r'datetime\.utcnow\(\)\.date\(\)', 'dhaka_now().date()', content)

    # Replace datetime.utcnow() with dhaka_now()
    content = re.sub(r'datetime\.utcnow\(\)', 'dhaka_now()', content)

    if content != original_content:
        # If it's not models.py, we need to import dhaka_now
        if not filepath.endswith('models.py') and ('dhaka_now' in content):
            if 'from models import' in content:
                content = re.sub(r'(from models import .*?)(?=\n)', r'\1, dhaka_now', content, count=1)
            else:
                # Add import after other imports
                content = re.sub(r'(from datetime import datetime\n?)', r'\1from models import dhaka_now\n', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py') and f != 'fix_tz.py':
            fix_file(os.path.join(root, f))
