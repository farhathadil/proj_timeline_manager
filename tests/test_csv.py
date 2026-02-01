from app.csv_utils import parse_csv_bytes

def test_parse_valid_csv():
    csv = """title,task_name,date,description
MyProj,Main,2026-02-01,Started
MyProj,Main,2026-02-02,Second
""".encode('utf-8')
    rows, errors = parse_csv_bytes(csv)
    assert not errors
    assert len(rows) == 2
    assert rows[0]['title'] == 'MyProj'

def test_parse_invalid_date():
    csv = """title,task_name,date,description
P,Main,not-a-date,desc
""".encode('utf-8')
    rows, errors = parse_csv_bytes(csv)
    assert errors
