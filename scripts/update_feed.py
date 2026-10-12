import json, os, urllib.request, pathlib, datetime
url=os.environ.get("GTN_FEED_URL","").strip()
if not url:
    print("No GTN_FEED_URL set; retaining existing data.")
    raise SystemExit(0)
if not url.startswith("https://"):
    raise SystemExit("GTN_FEED_URL must use HTTPS")
request=urllib.request.Request(url,headers={"User-Agent":"GTNMarket/1.0"})
with urllib.request.urlopen(request,timeout=20) as response:
    raw=response.read(2000001)
if len(raw)>2000000:
    raise SystemExit("Feed exceeds 2 MB")
data=json.loads(raw)
if data.get("server")!="Star Forge" or not isinstance(data.get("observations"),list):
    raise SystemExit("Expected Star Forge observations JSON")
rows=[]
for x in data["observations"][-10000:]:
    try:
        assert isinstance(x["item"],str) and 0<len(x["item"])<=100
        assert type(x["price"]) is int and x["price"]>0
        assert type(x["quantity"]) is int and x["quantity"]>0
        datetime.datetime.fromisoformat(x["date"].replace("Z","+00:00"))
        rows.append({k:x[k] for k in ("item","price","quantity","date")})
    except (AssertionError,KeyError,ValueError,TypeError):
        continue
output={"server":"Star Forge","source":str(data.get("source","External source"))[:120],"updated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"observations":rows}
pathlib.Path("data/market.json").write_text(json.dumps(output,indent=2))
print(f"Saved {len(rows)} valid observations")
