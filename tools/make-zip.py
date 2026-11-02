"""Builds dist/dayup-theme.zip with only the Shopify theme folders (upload-ready)."""
import os, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FOLDERS = ['assets', 'config', 'layout', 'locales', 'sections', 'snippets', 'templates']
out = os.path.join(ROOT, 'dist', 'dayup-theme.zip')
os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for folder in FOLDERS:
        for base, _, files in os.walk(os.path.join(ROOT, folder)):
            for f in sorted(files):
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, ROOT))
print(out, os.path.getsize(out), 'bytes')
