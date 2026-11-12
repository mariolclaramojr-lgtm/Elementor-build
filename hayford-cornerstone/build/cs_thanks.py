import json,sys
SP='/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad'
sys.path.insert(0,SP)
from hf import gc,F
from cs_home import el,bp,reveal,H,T,eyebrow,btn,div,img
copy=el('layout-column',[
  reveal(eyebrow('Message received', color='accent_light', margin='0px 0px 24px 0px')),
  reveal(H('Thank you for reaching out', tag='h1', size='clamp(48px, 7vw, 104px)', color='white', lh='0.95', ls='-0.05em',
           text_max_width='900px'), .1),
  reveal(T("We've received your message and someone from our team will be in touch soon. We can't wait to meet you!",
           color='white', size='18px', lh='1.7', text_max_width='560px', text_margin='26px 0px 0px 0px', effects_opacity='0.78'), .2),
  reveal(div([btn('Back to Home','/'), btn('Plan Your Visit','/plan-your-visit/', style='glass')],
             layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_wrap=True, layout_div_flex_gap='12px',
             layout_div_margin='40px 0px 0px 0px'), .3)],
  layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_justify='flex-end')
row=el('layout-row',[copy],layout_row_global_container=True,layout_row_layout='100%')
hero=el('section',[row],_label='1. Thank You banner',section_padding='clamp(180px, 30vh, 320px) 0px 96px 0px',
  section_bg_color=gc('ink'),section_bg_advanced=True,section_overflow='hidden',
  bg_lower_type='image',bg_lower_image=img('img_cta'),bg_lower_image_size='cover',bg_lower_image_position='center 55%',
  bg_upper_type='color',bg_upper_color='linear-gradient(90deg, rgba(9, 10, 13, 0.9) 0%, rgba(9, 10, 13, 0.55) 60%, rgba(9, 10, 13, 0.4) 100%), linear-gradient(0deg, rgba(9, 10, 13, 0.6) 0%, rgba(9, 10, 13, 0) 60%)')
bp(hero,'section_padding',md='150px 0px 64px 0px',sm='130px 0px 48px 0px')
json.dump([hero,{'_type':'global-block','global_block_id':'592','_label':'2. Service Times + Contact + Map (component)'}],open(f'{SP}/cs/thanks_tree.json','w'))
print('ok')
