You are a senior full-stack engineer. Build a **lightweight self-hosted web app** to manage **simple projects** running inside a **Proxmox LXC** (Linux container). Prioritize **low resource usage**, **fast startup**, and **simple deployment**.

### 1\) Core Data Model (Must Match)

Create these entities:

**Project**

* `id` (auto)  
* `title` (required string)  
* `category` (optional string; some projects have no category)  
* `task_name` (required string) → this is the project’s main “Task” label

**TaskTimelineItem** (timeline entries for a project’s task)

* `id` (auto)  
* `project_id` (FK)  
* `date` (required date, ISO format)  
* `description` (required string)

Rules:

* Each Project has **many** TaskTimelineItems.  
* Timeline items must be **sortable by date**.  
* Category is nullable/optional and should render gracefully (e.g., “Uncategorized”).

### 2\) Key Features (MVP)

Implement the following screens optimized for **mobile**:

#### A) Projects List (Home)

* Dark mode UI by default (no light theme needed).  
* Search bar (search by title, category, task\_name, timeline description).  
* Filter by category (including “Uncategorized”).  
* Each project card shows:  
  * Title  
  * Category (or “Uncategorized”)  
  * Task name  
  * Timeline span: earliest date → latest date (if timeline exists)  
  * Quick action: open project

#### B) Project Detail

* Shows project fields \+ full timeline list (date \+ description).  
* Add / edit / delete timeline items.  
* Optional: edit project title/category/task\_name.

#### C) Simple “Gantt-like” Visual (Per Project)

* Create a **lightweight Gantt-style visual** for the project based on the timeline items:  
  * X-axis: dates (auto range from earliest to latest; if only one date, show a small range around it)  
  * Each timeline item appears as a **marker** or **small bar** on the timeline  
  * Display description on tap/click (mobile-friendly)  
* Do not use heavy charting libs if possible; prefer a minimal SVG/Canvas or simple HTML/CSS approach.

### 3\) CSV Import (Initial Data)

The initial data will be imported from a CSV. Implement a CSV import page:

* Upload CSV (UTF-8).  
* Preview parsed rows before import.  
* “Import” button writes to DB.  
* Must handle missing category.

Make reasonable assumptions about CSV columns and implement robust mapping:

* Expected columns (case-insensitive, flexible):  
  * `title`  
  * `category` (optional)  
  * `task` or `task_name`  
  * `date` (for timeline item)  
  * `description` (for timeline item)


* If multiple rows share the same project title+task\_name(+category), they belong to the same Project and become multiple timeline items.  
    
* Validate:  
    
  * date must parse (reject row with clear error message)  
  * title and task\_name required


* Show an import summary: projects created, timeline items created, rows skipped.

### 4\) Tech/Architecture Constraints (Lightweight, LXC-friendly)

* Keep dependencies minimal.  
* Use a small embedded DB: **SQLite**.  
* Provide a single-command start (and optional Dockerfile if you think it helps, but it must still be LXC-friendly).  
* Must run behind local LAN; include basic config for host/port binding.

### 5\) UI / UX Requirements

* Dark theme (true dark, high contrast, accessible font sizes).  
* Mobile-first layout:  
  * max width optimized for phone  
  * large tap targets  
  * sticky bottom action bar on detail screens (optional)  
* Use a clean modern look, no heavy animations.

### 6\) Deliverables Required

Produce:

1. The full project code scaffold (frontend \+ backend).  
2. Database schema/migrations (or auto-create schema on first run).  
3. README with:  
   * install steps  
   * run steps on LXC  
   * CSV format examples  
4. Seed/example CSV file.  
5. Basic tests for CSV parsing and date handling.

### 7\) Suggested Implementation (Use this unless you have a better minimal option)

Choose one lightweight stack and proceed without asking questions:

* Option A: **Python FastAPI \+ SQLite \+ Jinja/HTMX** (minimal JS)  
* Option B: **Node.js Express \+ SQLite \+ small templating** (minimal JS)

Prefer server-rendered pages with a tiny bit of JS only for:

* CSV preview  
* tooltip/tap details on gantt markers

### 8\) Acceptance Criteria (Must Pass)

* Works on mobile screen smoothly.  
* Dark theme throughout.  
* Can import CSV and correctly groups timeline items into projects.  
* Can view a project and see a gantt-like timeline visual.  
* Runs reliably in a Proxmox LXC with low resource usage.

Now implement it.  
