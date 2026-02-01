# Project Timeline Manager (Lightweight, LXC-friendly)

This is a minimal FastAPI + SQLite app for managing simple projects and timeline items. Designed to run in a Proxmox LXC or small VM.

Quick start (local / LXC):

1. Install Python 3.11 and create a virtualenv (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Open on LAN: http://<LXC_IP>:8000

Docker (optional):

```bash
docker build -t proj2 .
docker run -p 8000:8000 -v $(pwd)/proj2.db:/app/proj2.db proj2
```

CSV Import

- See `data/seed.csv` for example format. Columns (case-insensitive): `title`, `category` (optional), `task` or `task_name`, `date`, `description`.
- Upload via `/import`, preview, then commit.

Testing

```bash
pytest -q
```

Notes

- Database is SQLite stored at `proj2.db` by default.
- Schema auto-creates on first run.
