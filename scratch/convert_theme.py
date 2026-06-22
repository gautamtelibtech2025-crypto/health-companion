import re
import os

replacements = [
    # Primary green colors
    (r'#006c45', '#10b981'),
    (r'#3ecf8e', '#10b981'),
    (r'#004d31', '#064e3b'),
    (r'#008a59', '#34d399'),
    
    # Text colors
    (r'color:\s*#121c2a', 'color: #f3f4f6'),
    (r'color:\s*#3d4a41', 'color: #c9d1d9'),
    (r'color:\s*#6c7a70', 'color: #8892b0'),
    (r'color:\s*#006c45', 'color: #10b981'),
    
    # Backgrounds
    (r'background-color:\s*#ffffff', 'background-color: #161b22'),
    (r'background-color:\s*#f8f9ff', 'background-color: #0d1117'),
    (r'background:\s*#ffffff', 'background: #161b22'),
    (r'background:\s*#f8f9ff', 'background: #0d1117'),
    
    # Borders and Shadows
    (r'border-bottom:\s*1px solid rgba\(0,\s*108,\s*69,\s*0\.15\);\s*box-shadow:\s*0\s*1px\s*0\s*#ffffff;', 'border-bottom: 1px solid rgba(16, 185, 129, 0.15);'),
    (r'box-shadow:\s*0\s*1px\s*0\s*#ffffff;', ''),
    (r'box-shadow:\s*6px\s*6px\s*12px\s*#d1d9e6,\s*-6px\s*-6px\s*12px\s*#ffffff', 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'),
    (r'box-shadow:\s*inset\s*2px\s*2px\s*5px\s*#d1d9e6,\s*inset\s*-2px\s*-2px\s*5px\s*#ffffff', 'box-shadow: none'),
    (r'box-shadow:\s*inset\s*4px\s*4px\s*8px\s*#d1d9e6,\s*inset\s*-4px\s*-4px\s*8px\s*#ffffff', 'box-shadow: none'),
    (r'box-shadow:\s*0\s*8px\s*32px\s*0\s*rgba\(0,\s*108,\s*69,\s*0\.04\)', 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1)'),
    (r'box-shadow:\s*0\s*4px\s*12px\s*rgba\(0,\s*108,\s*69,\s*0\.15\)', 'box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15)'),
    (r'border:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.12\)', 'border: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.1\)', 'border: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.15\)', 'border: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border-bottom:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.15\)', 'border-bottom: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border-bottom:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.1\)', 'border-bottom: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border-bottom:\s*1\.5px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.08\)', 'border-bottom: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border-top:\s*1px\s*solid\s*rgba\(0,\s*108,\s*69,\s*0\.08\)', 'border-top: 1px solid rgba(16, 185, 129, 0.15)'),
    (r'border:\s*1\.5px\s*solid\s*rgba\(62,\s*207,\s*142,\s*0\.4\)', 'border: 1.5px solid rgba(16, 185, 129, 0.4)'),
    
    # rgba transitions
    (r'rgba\(0,\s*108,\s*69,', 'rgba(16, 185, 129,'),
    (r'rgba\(62,\s*207,\s*142,', 'rgba(16, 185, 129,'),
    
    # Specific buttons/links
    (r'background-color:\s*#ffffff;\s*color:\s*#006c45\s*!important;', 'background-color: #10b981; color: #0d1117 !important;'),
    
    # Error boxes (red/pink warning box to dark red/burgundy)
    (r'background-color:\s*#FFDAD6;\s*border:\s*1\.5px\s*solid\s*#FFB4AB;', 'background-color: #7f1d1d; border: 1.5px solid #ef4444;'),
    (r'color:\s*#410002', 'color: #fca5a5'),
]

files = [
    'views/analysis.py',
    'views/assessment.py',
    'views/ml_explorer.py',
    'views/reports.py',
    'views/settings_page.py',
]

for filename in files:
    if not os.path.exists(filename):
        print(f"Skipping {filename}: Not found")
        continue
    
    print(f"Processing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix Plotly default colors in charts
    content = content.replace('color_discrete_sequence=["#006c45"]', 'color_discrete_sequence=["#10b981"]')
    content = content.replace('color_discrete_sequence=[\'#006c45\']', 'color_discrete_sequence=["#10b981"]')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done converting theme!")
