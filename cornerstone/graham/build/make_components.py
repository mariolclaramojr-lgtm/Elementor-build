import json, cs, copy
ns = {}
exec(open('build_home.py').read().replace("json.dump(tree, open('home-tree-new.json', 'w'), indent=1)", "pass"), ns)
visit = ns['visit']                  # 5. Get In Touch section (with the client's map embed already fixed in)
src = open('build_hf.py').read()
start = src.index('brand = div('); end = src.index('menu = {')
exec(src.split('# ---------------- 1. HERO')[0] if False else '', ns)
exec(src[start:end], ns)             # builds `brand` with the same helpers
brand = ns['brand']
def clean(e):
    if isinstance(e, dict):
        for k in [k for k, v in e.items() if v is None]: del e[k]
        e.pop('_region', None)
        for v in e.values(): clean(v)
    elif isinstance(e, list):
        for x in e: clean(x)
clean(visit); clean(brand)
try: ids = json.load(open('components.json'))
except Exception: ids = {}
for key, title, elems in [('logo', 'Graham – Logo', [brand]), ('gettouch', 'Graham – Get In Touch', [visit])]:
    args = {'title': title, 'elements': elems}
    if key in ids: args['id'] = ids[key]
    r = json.loads(cs.call('cs_save_component', args)); print(key, {k: r.get(k) for k in ('id', 'title', 'summary')})
    ids[key] = r['id']
json.dump(ids, open('components.json', 'w'))
