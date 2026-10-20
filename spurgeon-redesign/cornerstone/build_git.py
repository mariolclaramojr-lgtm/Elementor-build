"""Get in Touch — reusable Cornerstone Component (place with {"_type":"global-block","global_block_id":id}).
Styled entirely through element settings: service-time tiles are Divs (background + radius + padding),
contact rows are Headlines with a Graphic icon and a bottom border."""
import json,os,sys
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from csel import *

def time_tile(lbl,value):
    return div([info_item(lbl,value,big=True)],'sp-time',bg_color=CREAM,border_radius='14px',padding='22px 24px 20px 24px')

left=col([headline('Get in Touch','h2','sp-h2','h2',color=INK),
          text('<p>We would love to connect with you. Feel free to contact us or join us at one of our service times.</p>',margin='0px 0px 28px 0px'),
          div([time_tile('Sunday Mornings','8:30 &amp; 10:00 am'),time_tile('Wednesday Evenings','6:30 pm')],'sp-times',
              flexbox=True,flex_direction='column',flex_align='stretch',flex_gap='12px',margin='0px 0px 28px 0px'),
          div([contact_row('location-dot','1221 My Street, My Town, XX&nbsp;12212',MAPS,blank=True),
               contact_row('phone','908-123-1234','tel:9081231234'),
               contact_row('envelope','info@yourdomain.com','mailto:info@yourdomain.com')],'sp-contact',
              border_width='1px 0px 0px 0px',border_style='solid',border_color=LINE),
          actions([button('Plan Your Visit','/plan-your-visit/','ink'),button('Get Directions',MAPS,'line-ink',blank=True)],mt='28px')])
els=[section('sp-section sp-git',[row([col([label('Visit')])],'100%'),
  row([left,col([gmap()],'sp-git-map')],'33.33% 66.67%','sp-git-row',md='100%',align='stretch')],id_='visit',bg_color=WHITE)]

existing=None
p=os.environ['MCPDIR']+'/git_component_id'
if os.path.exists(p): existing=int(open(p).read())
args={'title':'Get in Touch','elements':els}
if existing: args['id']=existing
if __name__=='__main__':
    r=call('cs_save_component',args,timeout=120)
    print(json.dumps(r)[:300])
    cid=r.get('id')
    if cid: open(p,'w').write(str(cid))
