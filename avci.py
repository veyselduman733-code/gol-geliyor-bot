import requests
import json
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

SOURCES = {
    "LIVE_WIDGET":
        "https://sportsbookv2.iddaa.com/sportsbook/live-events-for-widget",

    "EVENTS":
        "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0"
}

def get_json(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    print("HTTP:", r.status_code)
    print("BYTE:", len(r.content))
    r.raise_for_status()
    return r.json()

def analyse(name, root):

    data = root.get("data")

    if name == "LIVE_WIDGET":
        events = data if isinstance(data, list) else []
    else:
        events = (data or {}).get("events", [])

    football = [
        e for e in events
        if e.get("sid") == 1
    ]

    sc_matches = [
        e for e in football
        if isinstance(e.get("sc"), dict)
    ]

    real_minute = [
        e for e in sc_matches
        if e["sc"].get("min") is not None
    ]

    print()
    print("TOPLAM EVENT :", len(events))
    print("FUTBOL       :", len(football))
    print("SC VAR       :", len(sc_matches))
    print("GERCEK DAKIKA:", len(real_minute))
    print()

    for e in real_minute[:50]:

        sc = e.get("sc", {})
        ht = sc.get("ht") or {}
        at = sc.get("at") or {}

        hs = ht.get("r", ht.get("c", "?"))
        as_ = at.get("r", at.get("c", "?"))

        print(
            str(sc.get("min")) + "'",
            "|",
            e.get("hn"),
            hs,
            "-",
            as_,
            e.get("an"),
            "| ID:",
            e.get("i")
        )

    return {
        "source": name,
        "total": len(events),
        "football": len(football),
        "with_sc": len(sc_matches),
        "real_minute": len(real_minute)
    }

def main():

    print("=" * 55)
    print("KURT VERI AVCISI")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 55)

    results = []

    for name, url in SOURCES.items():

        print()
        print("=" * 55)
        print(name)
        print("=" * 55)

        try:
            root = get_json(url)
            results.append(analyse(name, root))

        except Exception as exc:
            print("HATA:", repr(exc))

            results.append({
                "source": name,
                "error": repr(exc)
            })

    print()
    print("=" * 55)
    print("SONUC")
    print("=" * 55)

    for r in results:
        print(r)

    with open("avci-sonuc.json", "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )

if __name__ == "__main__":
    main()
