import json, os, sys, time, urllib.request

TOKEN = os.environ.get("FOOTBALL_DATA_TOKEN", "").strip()
COMPS = ["PL", "PD", "BL1", "SA", "FL1", "CL"]
OUT = "data/matches.json"

if not TOKEN:
    sys.exit("Нет секрета FOOTBALL_DATA_TOKEN. Добавь его: Settings, Secrets and variables, Actions.")


def get(code):
    req = urllib.request.Request(
        f"https://api.football-data.org/v4/competitions/{code}/matches",
        headers={"X-Auth-Token": TOKEN},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


try:
    with open(OUT, encoding="utf-8") as f:
        old = json.load(f)
except Exception:
    old = {"teams": {}, "matches": []}

raw, failed = [], []
for i, code in enumerate(COMPS):
    if i:
        time.sleep(8)  # лимит бесплатного тарифа: 10 запросов в минуту
    try:
        for x in get(code).get("matches", []):
            raw.append((code, x))
        print(code, "ok")
    except Exception as e:
        print(code, "ошибка:", e)
        failed.append(code)

if len(failed) == len(COMPS):
    sys.exit("Ни одна лига не загрузилась. Проверь токен и доступ к лигам.")

teams = {}
for code, x in raw:
    for t in (x["homeTeam"], x["awayTeam"]):
        if t.get("id"):
            teams.setdefault(str(t["id"]), {"n": t.get("shortName") or t.get("name"), "cr": t.get("crest")})
for k, v in old.get("teams", {}).items():
    teams.setdefault(k, v)

matches = []
for code, x in raw:
    hi, ai = x["homeTeam"].get("id"), x["awayTeam"].get("id")
    if not hi or not ai:
        continue  # пары плей-офф, которые ещё не определены
    ft = (x.get("score") or {}).get("fullTime") or {}
    fin = x.get("status") == "FINISHED" and ft.get("home") is not None
    if not fin and x.get("status") not in ("SCHEDULED", "TIMED"):
        continue
    matches.append({
        "id": x["id"], "c": code, "d": x["utcDate"][:10], "md": x.get("matchday"), "st": x.get("stage"),
        "h": teams[str(hi)]["n"], "a": teams[str(ai)]["n"],
        "hg": ft["home"] if fin else None, "ag": ft["away"] if fin else None,
    })
for m in old.get("matches", []):
    if m.get("c") in failed:
        matches.append(m)  # если лига не загрузилась, оставляем прежние данные
matches.sort(key=lambda m: (m["d"], m["id"]))

if old.get("matches") == matches and old.get("teams") == teams:
    print("Без изменений")
    sys.exit(0)

os.makedirs("data", exist_ok=True)
out = {"updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "teams": teams, "matches": matches}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print("Записано матчей:", len(matches), "команд:", len(teams), "ошибки:", failed or "нет")
