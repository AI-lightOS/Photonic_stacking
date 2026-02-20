# GitHub Upload Guide (Without Git CLI)

## Method: Using GitHub Web Interface

Since git command-line tools are not installed, follow these steps to upload your project to GitHub using the web interface:

### Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top-right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `photonic_computing`
   - **Description**: "Photonic Computing Platform with TFLN Characterization and Gerber Viewer"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 2: Prepare Your Files for Upload

Your project is located at:
```
/Users/cartik_sharma/Downloads/photonic_computing
```

**Important files to upload:**
- `app.py` - Main Flask application
- `gerber_viewer.py` - Gerber file parser
- `tfln_plots.py` - TFLN characterization
- `templates/index.html` - Web interface
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules
- `TFLN_INTEGRATION_SUMMARY.md` - TFLN documentation
- `GERBER_VIEWER_SUMMARY.md` - Gerber viewer documentation
- `gerber_files/` directory - All PCB files
- `static/` directory (if exists) - CSS/JS files

**Files to EXCLUDE (already in .gitignore):**
- `__pycache__/` folders
- `.DS_Store` files
- `venv/` or `env/` folders
- `*.pyc` files
- `outputs/` folder

### Step 3: Upload Files via Web Interface

#### Option A: Drag and Drop (Recommended for small projects)

1. On your new repository page, click **"uploading an existing file"** link
2. Open Finder and navigate to `/Users/cartik_sharma/Downloads/photonic_computing`
3. Select all files and folders (except those in .gitignore)
4. Drag and drop them into the GitHub upload area
5. Add commit message: "Initial commit: Photonic Computing Platform"
6. Click **"Commit changes"**

#### Option B: GitHub Desktop (Alternative)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in to GitHub
3. Click **"Add"** → **"Add Existing Repository"**
4. Browse to `/Users/cartik_sharma/Downloads/photonic_computing`
5. Click **"Add Repository"**
6. Click **"Publish repository"** to push to GitHub

#### Option C: Upload via Command Line (Requires Xcode Tools)

If you want to install git later:
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Navigate to project
cd /Users/cartik_sharma/Downloads/photonic_computing

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Photonic Computing Platform"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/photonic_computing.git

# Push
git push -u origin main
```

### Step 4: Verify Upload

1. Go to your repository: `https://github.com/YOUR_USERNAME/photonic_computing`
2. Verify all files are present
3. Check that README.md displays correctly on the main page

### Step 5: Add Repository Topics (Optional)

On your repository page:
1. Click the gear icon next to "About"
2. Add topics: `photonics`, `tfln`, `gerber-viewer`, `pcb`, `flask`, `python`, `photonic-computing`
3. Save changes

## Project Structure to Upload

```
photonic_computing/
├── .gitignore                      ✅ Upload
├── README.md                       ✅ Upload
├── app.py                          ✅ Upload
├── gerber_viewer.py                ✅ Upload
├── tfln_plots.py                   ✅ Upload (if exists)
├── TFLN_INTEGRATION_SUMMARY.md     ✅ Upload
├── GERBER_VIEWER_SUMMARY.md        ✅ Upload
├── templates/
│   └── index.html                  ✅ Upload
├── static/                         ✅ Upload (if exists)
│   ├── css/
│   └── js/
├── gerber_files/                   ✅ Upload
│   ├── *.gbr                       ✅ Upload
│   └── *.drl                       ✅ Upload
├── __pycache__/                    ❌ Skip (in .gitignore)
├── venv/                           ❌ Skip (in .gitignore)
└── outputs/                        ❌ Skip (in .gitignore)
```

## Quick Upload Checklist

- [ ] Create new repository on GitHub
- [ ] Prepare files (exclude .gitignore items)
- [ ] Upload files via web interface or GitHub Desktop
- [ ] Verify README displays correctly
- [ ] Add repository description and topics
- [ ] Share repository link

## Repository URL

After creation, your repository will be at:
```
https://github.com/YOUR_USERNAME/photonic_computing
```

## Next Steps After Upload

1. **Add a License**: Go to "Add file" → "Create new file" → name it `LICENSE`
2. **Enable GitHub Pages** (optional): Settings → Pages → Deploy from main branch
3. **Add Collaborators** (optional): Settings → Collaborators
4. **Create Issues/Projects** for future enhancements

## Troubleshooting

**File too large error?**
- GitHub has a 100MB file size limit
- Check if any gerber files or outputs are too large
- Use Git LFS for large files (requires git CLI)

**Upload failed?**
- Try uploading in smaller batches
- Ensure you're signed in to GitHub
- Check your internet connection

**Missing files after upload?**
- Verify files aren't in .gitignore
- Check file permissions in Finder
- Try uploading individual folders

---

**Created**: January 30, 2026
**Status**: Ready to upload ✅
