from dataclasses import dataclass, asdict
import json


@dataclass(frozen=True)
class Params:
    volume: int = 2400
    hourly: float = 900.0
    manual_minutes: float = 12.0
    review_minutes: float = 2.0
    exception_minutes: float = 3.0
    coverage: float = 0.75
    run_price: float = 7.0
    support: float = 45000.0
    investment: float = 480000.0


def calculate(p: Params):
    if p.volume <= 0 or p.hourly <= 0:
        raise ValueError('Требуются положительные объём и цена часа')
    if not 0 <= p.coverage <= 1:
        raise ValueError('Покрытие вне интервала [0, 1]')
    manual = p.volume * p.manual_minutes / 60 * p.hourly
    active = (p.coverage * p.review_minutes
              + (1 - p.coverage)
              * (p.manual_minutes + p.exception_minutes))
    automated = (p.volume * (active / 60 * p.hourly
                            + p.run_price) + p.support)
    saving = manual - automated
    denominator = (p.manual_minutes + p.exception_minutes
                   - p.review_minutes)
    if denominator <= 0:
        raise ValueError('Проверка не короче маршрута исключения')
    threshold = (p.exception_minutes + 60 / p.hourly
                 * (p.run_price + p.support / p.volume)) / denominator
    return {"manual": manual, "automated": automated,
            "monthly_difference": saving,
            "active_minutes_per_task": active,
            "break_even_coverage": threshold,
            "simple_payback_months":
                p.investment / saving if saving > 0 else None}


if __name__ == "__main__":
    p = Params()
    result = calculate(p)
    assert result["manual"] == 432000
    assert result["automated"] == 250800
    print(json.dumps({"parameters": asdict(p), "result": result},
                     sort_keys=True))
