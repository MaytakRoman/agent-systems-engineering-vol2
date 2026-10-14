from math import sqrt

def cosine(x, y):
    nx = sqrt(sum(v*v for v in x))
    ny = sqrt(sum(v*v for v in y))
    if not nx or not ny:
        raise ValueError('Нулевой вектор')
    return sum(a*b for a, b in zip(x, y)) / (nx*ny)

def retrieve(rows, tenant, query, limit=2):
    allowed = [r for r in rows
               if r["tenant"] == tenant and r["active"]]
    scored = [(cosine(query, r["vector"]), r["id"])
              for r in allowed]
    return sorted(scored, reverse=True)[:limit]

rows = [
    dict(id="A5", tenant="A", active=True,
         vector=(1.0, 0.1)),
    dict(id="A4", tenant="A", active=False,
         vector=(1.0, 0.0)),
    dict(id="B9", tenant="B", active=True,
         vector=(1.0, 0.0)),
    dict(id="A2", tenant="A", active=True,
         vector=(0.0, 1.0)),
]
answer = retrieve(rows, "A", (1.0, 0.0))
assert [x[1] for x in answer] == ["A5", "A2"]
print('Допустимое ранжирование:', [x[1] for x in answer])
