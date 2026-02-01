import csv
import io
from dateutil import parser as dateparser

def parse_csv_bytes(file_bytes):
    text = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    errors = []
    for i, r in enumerate(reader, start=1):
        # normalize keys
        row = {k.strip().lower(): (v.strip() if v is not None else "") for k, v in r.items()}
        title = row.get('title','')
        task = row.get('task') or row.get('task_name') or ''
        category = row.get('category') or None
        date_raw = row.get('date','')
        description = row.get('description','')
        if not title or not task:
            errors.append((i, 'missing title or task'))
            continue
        try:
            dt = dateparser.parse(date_raw).date()
        except Exception:
            errors.append((i, f'invalid date: {date_raw}'))
            continue
        rows.append({
            'title': title,
            'task_name': task,
            'category': category,
            'date': dt.isoformat(),
            'description': description,
        })
    return rows, errors
