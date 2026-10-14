import sqlite3
import json

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE results(task TEXT PRIMARY KEY, body TEXT);
CREATE TABLE outbox(event TEXT PRIMARY KEY, task TEXT);
""")

def commit_result(task, event, result):
    body = json.dumps(result, sort_keys=True)
    with db:
        db.execute("BEGIN IMMEDIATE")
        old_event = db.execute(
            "SELECT task FROM outbox WHERE event=?",
            (event,)).fetchone()
        if old_event and old_event[0] != task:
            raise ValueError('Конфликт задания события')
        old = db.execute(
            "SELECT body FROM results WHERE task=?",
            (task,)).fetchone()
        if old and old[0] != body:
            raise ValueError('Конфликт результата')
        db.execute(
            "INSERT OR IGNORE INTO results VALUES(?,?)",
            (task, body))
        db.execute("INSERT OR IGNORE INTO outbox VALUES(?,?)",
                   (event, task))

commit_result("t1", "e1", {"artifact": "a1"})
commit_result("t1", "e1", {"artifact": "a1"})
for table in ("results", "outbox"):
    count = db.execute("SELECT count(*) FROM " + table)
    assert count.fetchone()[0] == 1
print('Сохранены один результат и одно уведомление')
