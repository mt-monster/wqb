import os, ast, collections
ROOT="."
EXCLUDE={".venv","__pycache__","node_modules","tracking",".git",".workbuddy"}
funcs=collections.defaultdict(list)
classes=collections.defaultdict(list)
imports_unused=collections.Counter()
todo=0
bare_except=0
files_analyzed=0
for dp,dn,fn in os.walk(ROOT):
    parts=dp.replace("\\","/").split("/")
    if any(p in EXCLUDE for p in parts): continue
    for f in fn:
        if not f.endswith(".py"): continue
        p=os.path.join(dp,f).replace("\\","/")
        try:
            src=open(p,encoding="utf-8",errors="ignore").read()
        except: continue
        try:
            tree=ast.parse(src)
        except SyntaxError:
            continue
        files_analyzed+=1
        todo+=src.count("# TODO")+src.count("# FIXME")+src.count("# HACK")
        for node in ast.walk(tree):
            if isinstance(node,ast.ExceptHandler):
                if node.type is None: bare_except+=1
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                funcs[node.name].append(p)
            elif isinstance(node,ast.ClassDef):
                classes[node.name].append(p)
print("files analyzed:",files_analyzed)
print("TODO/FIXME/HACK markers:",todo)
print("bare excepts (except:):",bare_except)
print("\n=== DUPLICATE FUNCTION NAMES (defined in >1 file) TOP 25 ===")
dups=sorted([(n,len(v)) for n,v in funcs.items() if len(v)>1],key=lambda x:-x[1])
for n,c in dups[:25]:
    print(f"  {n}: {c} files")
print("  ... total duplicate-named functions:",len(dups))
print("\n=== DUPLICATE CLASS NAMES (defined in >1 file) ===")
cdups=sorted([(n,len(v)) for n,v in classes.items() if len(v)>1],key=lambda x:-x[1])
for n,c in cdups[:20]:
    print(f"  {n}: {c}")
