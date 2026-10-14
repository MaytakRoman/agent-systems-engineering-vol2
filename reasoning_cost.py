from math import isclose

# Доли, цены и вероятности заданы для расчётного примера.
share_easy, share_hard = 0.7, 0.3
manual = 200
cheap, expensive = 20, 44
q_easy_cheap, q_easy_expensive = 0.95, 0.97
q_hard_cheap, q_hard_expensive = 0.50, 0.85

def total(cost, quality):
    return cost + (1 - quality) * manual

all_cheap = (share_easy * total(cheap, q_easy_cheap)
             + share_hard * total(cheap, q_hard_cheap))
all_expensive = (
    share_easy * total(expensive, q_easy_expensive)
    + share_hard * total(expensive, q_hard_expensive))
selective = (share_easy * total(cheap, q_easy_cheap)
             + share_hard * total(expensive,
                                  q_hard_expensive))
assert isclose(all_cheap, 57)
assert isclose(all_expensive, 57.2)
assert isclose(selective, 43.2)
assert isclose(share_easy + share_hard, 1)
print("Дешёвый:", all_cheap)
print("Дорогой:", all_expensive)
print("Идеальная селекция:", selective)
