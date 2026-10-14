import hashlib
import json
import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute(
    "CREATE TABLE drafts("
    "id INTEGER PRIMARY KEY, text TEXT)")
connection.execute("""CREATE TABLE operations(
    subject TEXT, intent TEXT,
    fingerprint TEXT, draft_id INTEGER,
    PRIMARY KEY(subject, intent))""")

def create(subject, intent, text):
    payload = json.dumps({"subject": subject, "text": text},
                         sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"))
    raw = payload.encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT fingerprint, draft_id FROM operations "
            "WHERE subject=? AND intent=?", (subject, intent)
        ).fetchone()
        if row:
            if row[0] != digest:
                raise ValueError("конфликт ключа")
            return row[1]
        cursor = connection.execute(
            "INSERT INTO drafts(text) VALUES(?)", (text,))
        draft_id = cursor.lastrowid
        connection.execute(
            "INSERT INTO operations VALUES(?,?,?,?)",
            (subject, intent, digest, draft_id))
        return draft_id

first = create("user-1", "I-1", "проект")
assert create("user-1", "I-1", "проект") == first
count = connection.execute(
    "SELECT count(*) FROM drafts").fetchone()[0]
assert count == 1
try:
    create("user-1", "I-1", "изменённый проект")
except ValueError:
    pass
else:
    raise AssertionError("конфликт ключа не найден")
count = connection.execute(
    "SELECT count(*) FROM drafts").fetchone()[0]
assert count == 1
print("SQLite: один проект при повторе")
