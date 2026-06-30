# -*- coding: utf-8 -*-
"""Henter alle læringsopplegg fra Friluftsrådenes læringsportal-API, beriker hvert
opplegg med årstid/sted/kompetansemål/utstyr, og skriver en kompakt JSON-katalog
til ../data/laeringsopplegg.json.

Kjør på nytt når du vil oppdatere katalogen med nye opplegg:
    python verktoy/hent_laeringsopplegg.py
Krever kun Python 3 (standardbibliotek). Tar ca. 1–2 minutter.
"""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://www.friluftsrad.no"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "laeringsopplegg.json")

AGE = {
    "KINDERGARTEN": "Barnehage",
    "FIRST_TO_FOURTH_LEVEL": "1.–4. trinn",
    "FIFTH_TO_SEVENTH_LEVEL": "5.–7. trinn",
    "EIGHTH_TO_TENTH_LEVEL": "8.–10. trinn",
}
SEASONS = ["Vår", "Sommer", "Høst", "Vinter"]
HDRS = {"User-Agent": "Uteklasserommet-katalog/1.0 (Friluftsrådenes Landsforbund)"}


def get_json(url, tries=3):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if t == tries - 1:
                raise
            time.sleep(0.4 * (t + 1))


def strip_html(h):
    if not h:
        return ""
    h = re.sub(r"<[^>]+>", " ", h).replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", h).strip()


def after_label(text, label, n=60):
    i = text.lower().find(label.lower() + ":")
    return text[i + len(label) + 1: i + len(label) + 1 + n].strip() if i >= 0 else ""


def parse_seasons(impl):
    seg = after_label(impl, "Årstid", 35).lower()
    if not seg:
        return []
    if "hele året" in seg:
        return ["Hele året"]
    return [s for s in SEASONS if s.lower() in seg]


def parse_place(impl):
    seg = after_label(impl, "Sted", 60)
    if not seg:
        return ""
    cut = re.search(r"Årstid|Forarbeid|Gjennomf|Tidsbruk|Etterarbeid|Utstyr", seg, re.I)
    if cut:
        seg = seg[:cut.start()]
    return seg.strip(" .:-")[:60]


ARENA_DEF = [
    ("Skog",                 r"skog|barskog|løvskog|granskog|trestamme|tresort|trær|løvtre|bartre"),
    ("Vann, fjære & sjø",    r"vann|fjær|sjø|tjern|bekk|\belv\b|foss|innsjø|\bdam\b|kyst|strand|\bbad|våtmark|\bmyr|brygge|\bbåt|\bhav|fiske"),
    ("Bålplass & leir",      r"bål|\bleir|gapahuk|grill"),
    ("Skolegård & nærmiljø", r"skoleg|nærmilj|nærområd|\bskolen\b|uteområd|skoleplass|skolegård"),
    ("Åpent område",         r"åpent|åpen plass|\beng\b|jorde|\bmark\b|slette|gress|beite|løkke|flatt område"),
]
ARENA_CATCH = r"hvor som helst|overalt|valgfri|hvor du vil|et sted|i naturen|\bnaturen\b|tilpasses"


def arena_of(sted):
    s = (sted or "").lower()
    if not s:
        return []
    hits = [navn for navn, pat in ARENA_DEF if re.search(pat, s)]
    if hits:
        return hits
    return ["Passer hvor som helst"] if re.search(ARENA_CATCH, s) else []


def slug_of(route):
    try:
        return route.rstrip("/").split("/")[-1].split("?")[0]
    except Exception:
        return None


def enrich(a):
    rec = {
        "id": a.get("id"),
        "navn": (a.get("name") or "").strip(),
        "lenke": a.get("route", ""),
        "trinn": AGE.get(a.get("ageRange"), "Ukjent"),
        "trinnKey": a.get("ageRange"),
        "fag": (a.get("subjectArea") or {}).get("name"),
        "bilde": (a.get("picture") or {}).get("medium") or (a.get("picture") or {}).get("thumb"),
        "aarstid": [],
        "sted": "",
    }
    comp = equip = ""
    slug = slug_of(a.get("route", ""))
    if slug:
        try:
            d = get_json(BASE + "/api/learningactivity/" + slug).get("data", {})
            act = d.get("learningActivity", d) if isinstance(d, dict) else {}
            impl = strip_html(act.get("implementation"))
            comp = strip_html(act.get("competence"))
            equip = strip_html(act.get("equipment"))
            rec["aarstid"] = parse_seasons(impl)
            rec["sted"] = parse_place(impl)
        except Exception as e:
            rec["_err"] = str(e)[:40]
    rec["arena"] = arena_of(rec["sted"])
    blob = " ".join(filter(None, [rec["navn"], rec["fag"] or "", rec["trinn"], rec["sted"],
                                   " ".join(rec["aarstid"]), comp[:600], equip[:200]]))
    rec["sok"] = re.sub(r"\s+", " ", blob).strip().lower()
    return rec


def main():
    print("Henter liste …", flush=True)
    acts = get_json(BASE + "/api/learningactivity/all")["data"]["learningActivities"]
    print(f"  {len(acts)} opplegg", flush=True)
    records = [None] * len(acts)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(enrich, a): i for i, a in enumerate(acts)}
        done = 0
        for f in as_completed(futs):
            records[futs[f]] = f.result()
            done += 1
            if done % 100 == 0:
                print(f"  beriket {done}/{len(acts)}", flush=True)
    records = [r for r in records if r]
    today = time.strftime("%Y-%m-%d")
    with open(OUT, "w", encoding="utf-8") as fp:
        json.dump({"oppdatert": today, "antall": len(records), "opplegg": records},
                  fp, ensure_ascii=False, separators=(",", ":"))
    print(f"Skrev {len(records)} opplegg til {os.path.normpath(OUT)} "
          f"({os.path.getsize(OUT)//1024} KB)")


if __name__ == "__main__":
    main()
