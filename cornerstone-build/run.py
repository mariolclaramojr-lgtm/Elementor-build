import cs, sys, json, pages
name, pid = sys.argv[1], int(sys.argv[2])
tree = pages.PAGES[name]()
json.dump(tree, open(f'out-{name}.json','w'), indent=1)
r = cs.call('cs_save_element_tree', id=pid, tree=tree)
print(r.get('summary'))
cs.call('cs_purge_cache', id=pid)
