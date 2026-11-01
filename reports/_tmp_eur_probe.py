import json, io
ART = r"C:\Users\MENGTAO\.minimax\v2\sessions\2026\10\28\14-09-04-319-session_bXZzXzhmNGE4MGI5OTAyZTQwMzFiY2ZlNzcwMTNmMTZjODYy\reports\tool-outputs\1cc6d06af5312c471db135ef-1970f97ae073d5846af8453297fe33062557b1d0c868cf943ff27ea081268cc5.readable.v1.jsonl"
lines = io.open(ART, encoding="utf-8").read().splitlines()
chunks = [json.loads(ln)["text"] for ln in lines if ln.strip() and "text" in json.loads(ln)]
raw = "".join(chunks)
print("RAWLEN", len(raw))
print(repr(raw[:1500]))