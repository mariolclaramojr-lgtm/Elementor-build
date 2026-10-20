"""Get in Touch — reusable Cornerstone Component (place with {"_type":"global-block","global_block_id":id})."""
import json,os,sys
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
from csel import *
els=[section('sp-section sp-white sp-git',[
  row([col([headline('Visit','div','sp-label',font=BODY)])],'100%'),
  row([col([headline('Get in Touch','h2','sp-h2',color=INK),
            text('<p>We would love to connect with you. Feel free to contact us or join us at one of our service times.</p>','sp-copy sp-git-intro'),
            text(TIMES_HTML,'sp-git-times'),
            text(CONTACT_HTML,'sp-git-contact'),
            div([button('Plan Your Visit','/plan-your-visit/','ink'),button('Get Directions',MAPS,'line-ink',blank=True)],'sp-actions')]),
       col([gmap()],'sp-git-map')],'33.33% 66.67%','sp-top',md='100%')],id_='visit',bg_color=WHITE)]
existing=None
p=os.environ['MCPDIR']+'/git_component_id'
if os.path.exists(p): existing=int(open(p).read())
args={'title':'Get in Touch','elements':els}
if existing: args['id']=existing
r=call('cs_save_component',args,timeout=120)
print(json.dumps(r)[:400])
cid=r.get('id')
if cid: open(p,'w').write(str(cid))
