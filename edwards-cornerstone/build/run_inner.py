"""Save inner pages. Usage: python3 run_inner.py [slug ...]  (default: all)"""
import json, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
spec = importlib.util.spec_from_file_location('m', os.environ['EDW_MCP']); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
st = json.load(open(os.environ['EDW_STATE']))
def tool(n, **a):
    r = m.call('tools/call', {'name': n, 'arguments': a}); t = r['result']['content'][0]['text']
    if r['result'].get('isError'): raise SystemExit(n + ' ERROR ' + t[:1500])
    try: return json.loads(t)
    except Exception: return t
import inner
slugs = sys.argv[1:] or list(inner.PAGES)
for slug in slugs:
    pid, fn = inner.PAGES[slug]
    tree = fn(st['visit_component']) if slug in ('plan-your-visit', 'about', 'get-connected') else fn()
    r = tool('cs_save_element_tree', id=pid, tree=tree)
    print(slug, pid, 'elements', r.get('elements'), 'storage ok' if (r.get('storage') or {}).get('ok') else r.get('storage'))
tool('cs_purge_cache', all=True); print('purged')
