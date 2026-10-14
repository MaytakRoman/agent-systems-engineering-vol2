import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE requests("
            "id TEXT PRIMARY KEY, version INT, text TEXT)")
con.execute("INSERT INTO requests VALUES("
            "'REQ-7', 12, 'старый текст')")
con.commit()

def save(expected, text):
    with con:
        cursor = con.execute(
            "UPDATE requests SET text=?, version=version+1 "
            "WHERE id='REQ-7' AND version=?",
            (text, expected))
        if cursor.rowcount != 1:
            raise ValueError("конфликт версии")
    row = con.execute(
        "SELECT version FROM requests").fetchone()
    return row[0]

assert save(12, "проект A") == 13
try:
    save(12, "проект B")
except ValueError:
    pass
else:
    raise AssertionError("устаревшая запись прошла")
row = con.execute("SELECT text FROM requests").fetchone()
assert row[0] == "проект A"
assert save(13, "пересмотренный проект") == 14
print("Версии: устаревшая запись отклонена")
