# ProdigyPM - Branch Workflow

## Current Setup

**Main Branch** (`main`): Production-ready code with latest design  
**Development Branch** (`kaustubh`): For ongoing development and testing

Both branches currently have the modern NVIDIA/PNC design.

---

## Branch Status

### main (Production)
- Latest stable version
- Modern UI with NVIDIA/PNC styling
- Ready for deployment
- Ready for demos/presentations

### kaustubh (Development)
- Active development branch
- Same code as main (after merge)
- Use this for new features and experiments
- Test changes here first

---

## Workflow for Future Changes

### Making Changes

```bash
# Make sure you're on kaustubh
git checkout kaustubh

# Make your changes...
# Edit files, test, iterate

# Commit changes
git add .
git commit -m "Your descriptive message"
git push origin kaustubh
```

### Merging to Main (When Ready)

```bash
# Switch to main
git checkout main

# Merge kaustubh into main
git merge kaustubh

# Push to GitHub
git push origin main

# Switch back to kaustubh for more work
git checkout kaustubh
```

---

## Quick Commands

### Check current branch:
```bash
git branch
```

### Switch branches:
```bash
git checkout main      # Switch to production
git checkout kaustubh  # Switch to development
```

### See branch differences:
```bash
git diff main kaustubh
```

### View branch history:
```bash
git log --oneline --graph --all
```

---

## When to Use Each Branch

### Use `kaustubh` for:
- New features
- Experiments
- UI tweaks
- Testing changes
- Daily development

### Use `main` for:
- Deployments
- Demos
- Presentations
- Stable releases
- Production code

---

## Git Flow Summary

```
kaustubh (development)
    ↓
  [test & iterate]
    ↓
  [ready?]
    ↓
main (production)
    ↓
  [deploy/demo]
```

---

## Current Status After Merge

**Both branches are identical** and contain:
- ✅ Modern NVIDIA/PNC design
- ✅ All 7 AI agents
- ✅ Updated components
- ✅ API documentation
- ✅ Backend fixes

**Active Branch**: kaustubh (you're here now)

---

## Tips

1. **Always work on kaustubh first**
   - Test thoroughly before merging to main

2. **Commit often**
   - Small, descriptive commits are better

3. **Push regularly**
   - `git push origin kaustubh` backs up your work

4. **Merge to main when stable**
   - Don't merge broken code to main

5. **Keep branches in sync**
   - Regularly merge main back into kaustubh if others contribute

---

## GitHub URLs

**Repository**: https://github.com/Ka2507/hackutd2025

**Branches**:
- Main: https://github.com/Ka2507/hackutd2025/tree/main
- Kaustubh: https://github.com/Ka2507/hackutd2025/tree/kaustubh

---

## Troubleshooting

### If branches diverge:
```bash
git checkout kaustubh
git merge main
# Resolve any conflicts
git push origin kaustubh
```

### If you accidentally commit to main:
```bash
git checkout main
git reset --soft HEAD~1  # Undo last commit (keeps changes)
git stash                # Save changes
git checkout kaustubh
git stash pop           # Apply changes here instead
```

### To see what's different:
```bash
git log main..kaustubh  # Commits in kaustubh not in main
```

---

**Remember**: You're currently on `kaustubh` branch - perfect for development!

