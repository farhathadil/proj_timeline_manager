# Project Timeline Manager – User Guide

## Overview

**Project Timeline Manager** is a lightweight, self-hosted web app for managing simple projects and their timelines. Built with FastAPI + SQLite, it runs efficiently in small containers (Proxmox LXC, Docker, etc.) and is optimized for mobile viewing.

---

## Getting Started

### Access the App

- **Web UI**: Open `http://localhost:8001` (or your LAN IP:8001)
- **Import CSV**: Go to `/import` to load initial data
- **Manage via Portainer**: `http://localhost:9000` (optional Docker UI)

### First Steps

1. **Import seed data**: Use the CSV import feature to populate projects
2. **Browse projects**: View all projects on the home screen
3. **Explore timelines**: Click any project to see its timeline

---

## Main Features

### 1) Projects List (Home Screen)

The home screen shows all your projects in a clean, dark-themed card layout.

#### What You See
- **Project Title** – Main project name
- **Category** – Organizational tag (or "Uncategorized")
- **Task Name** – The main task/goal for the project
- **Timeline Span** – Date range of the earliest to latest timeline entry (e.g., "2026-01-05 → 2026-02-15")

#### Search & Filter
- **Search Bar**: Type to find projects by title, category, or task name
- **Category Filter**: Dropdown to filter by project category
- **Filter Button**: Apply search/category constraints

### 2) Project Detail View

Click any project card to open its detail page.

#### What You See
- **Project Header** – Title, category, and task name
- **Gantt Timeline Visual** – Lightweight SVG chart showing timeline items as markers
  - **X-axis**: Date range (auto-scaled)
  - **Markers**: Each timeline entry shown as a small colored marker
  - **Tap/Click**: Click a marker to see its description
- **Timeline List** – Chronological list of all entries with dates and descriptions

#### Add Timeline Items
1. Scroll to the "Add" form at the bottom
2. Enter a **date** (calendar picker)
3. Enter a **description** (text field)
4. Click **Add** to create the entry
5. Page refreshes; new item appears in list and on chart

---

## CSV Import

### Why Import?

Bulk-load multiple projects and timeline items from a CSV file instead of manually entering each one.

### CSV Format

Expected columns (case-insensitive):

| Column | Required | Example |
|--------|----------|---------|
| `title` | Yes | "Home Renovation" |
| `category` | No | "House" (omit for uncategorized) |
| `task` or `task_name` | Yes | "Painting" |
| `date` | Yes | "2026-01-05" (ISO format) |
| `description` | Yes | "Order paint and supplies" |

### Import Workflow

1. **Upload CSV**
   - Go to `/import`
   - Click "Choose File" and select your CSV
   - Click "Upload & Preview"

2. **Review Preview**
   - Check parsed rows for correctness
   - Errors are shown with row numbers (e.g., invalid dates)
   - Review the table before importing

3. **Confirm & Import**
   - Click **Import** button
   - Projects are created/updated
   - Timeline items are added
   - See summary: "Projects created: X, Timeline items created: Y"

4. **View Results**
   - Go back to home (`/`)
   - New projects appear in the list

### Import Logic

- **Same project?**: If multiple CSV rows have the same `title` + `task_name` + `category`, they merge into one project with multiple timeline items
- **Validation**: Rows with missing title/task or invalid dates are skipped with error messages
- **Upsert**: Existing projects are updated with new timeline entries

### Example CSV

```csv
title,category,task_name,date,description
Home Renovation,House,Painting,2026-01-05,Order paint and supplies
Home Renovation,House,Painting,2026-01-10,Begin priming
Website Redesign,,Redesign,2026-02-01,Kickoff meeting
Website Redesign,,Redesign,2026-02-15,First draft
```

Result: 2 projects (one with 2 timeline items, one with 2 timeline items).

---

## Timeline Visualization

### Gantt-Style Chart

Each project detail page includes a lightweight gantt chart:

- **Chart Type**: SVG-based, no heavy dependencies
- **Markers**: Small colored rectangles represent timeline items
- **Date Range**: Auto-scales from earliest to latest date
- **Single Date**: If only one timeline entry exists, the range expands slightly for visibility
- **Interaction**: Tap/click any marker to see its description in a popup

### Mobile-Friendly

- Responsive layout fits phone screens
- Large touch targets for markers
- Description popup fits small screens

---

## UI & Design

### Dark Theme

- **Default**: True dark mode (high contrast, easy on the eyes)
- **Colors**:
  - Background: Deep blue-black (#0b0f12)
  - Cards: Slightly lighter (#0f1416)
  - Accent: Bright cyan (#08f)
  - Text: Light gray (#e6eef3)

### Mobile-First Layout

- **Max width**: Optimized for portrait phone view (~760px max)
- **Tap targets**: Large buttons and links for easy interaction
- **Sticky header**: Top bar always visible for navigation
- **Sticky footer**: Attribution bar at bottom

### Accessibility

- Clean, readable fonts
- High contrast ratios
- No animations that distract
- Keyboard-navigable forms

---

## Tips & Tricks

### Best Practices

1. **Consistent naming**: Use the same project title and task name for related items
2. **Clear descriptions**: Write concise timeline descriptions (1–2 sentences)
3. **Batch import**: Use CSV for bulk data; manual add for quick updates
4. **Categorize**: Use categories to organize by team, area, or phase

### Performance

- SQLite database runs locally; no network calls
- Single-command startup (Docker or direct Uvicorn)
- Lightweight CSS/JS; minimal page size
- Loads fast even on low-bandwidth LAN

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **Projects not showing** | Refresh page; check import didn't have errors |
| **Gantt markers missing** | Check timeline has entries; ensure dates are valid ISO format |
| **Search not working** | Check spelling; search is case-insensitive but requires exact substring match |
| **Import file rejected** | Verify CSV is UTF-8 encoded; check required columns exist |

---

## Data Storage

### Database

- **Type**: SQLite (`proj2.db`)
- **Location**: `/app/proj2.db` (or set via `DATABASE_URL` env var)
- **Schema**: Auto-created on first run
- **Backup**: Copy `proj2.db` to external storage for backup

### Docker Volume

When using Docker:
```bash
docker run -v proj2_db:/app proj2
```

Database persists across container restarts.

---

## Admin & Deployment

### Environment Variables

- `DATABASE_URL` – SQLite path (default: `sqlite:///./proj2.db`)
- `HOST` – Server bind address (default: `0.0.0.0`)
- `PORT` – Server port (default: `8000`)

### Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Running in Docker

```bash
docker build -t proj2 .
docker run -p 8001:8000 -v proj2_db:/app proj2
```

### Proxmox LXC

- Install Python 3.11, create venv, install deps, run Uvicorn
- Or use Docker inside the LXC for isolation
- Minimal resource footprint (SQLite + FastAPI)

---

## Keyboard Shortcuts & Forms

### Search Page

- **Tab**: Navigate between search bar, category dropdown, and buttons
- **Enter**: Submit search/filter
- **Escape**: Clear search (manual delete of text)

### Project Detail

- **Tab**: Navigate form fields
- **Enter**: Submit form to add timeline item
- **Backspace**: Clear date picker (manual)

---

## FAQ

**Q: Can I edit or delete projects?**  
A: Currently, timeline items can be added. For deletions, use the Portainer UI or direct DB access. Full edit UI may be added in future releases.

**Q: How many projects can I store?**  
A: SQLite scales to millions of records. For Proxmox LXC, storage is your limiting factor.

**Q: Is there user authentication?**  
A: No. This app is for trusted LAN use only. For public access, add a reverse proxy with auth (e.g., Nginx + BasicAuth or OAuth).

**Q: Can I export data?**  
A: Yes, copy `proj2.db` or query it directly with `sqlite3` CLI. CSV export coming in future versions.

**Q: Does it work offline?**  
A: Yes, it's fully self-contained. Runs on local LAN with no external dependencies.

---

## Support & Feedback

- **Bug reports**: Check GitHub issues at https://github.com/farhathadil/proj_timeline_manager
- **Feature requests**: Open a discussion or PR
- **Local testing**: Use the seed CSV (`data/seed.csv`) to test import workflow

---

**Version**: 1.0  
**Last updated**: February 2026
