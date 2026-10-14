import cs, json
hx=lambda s: s.encode().hex()
colors=[
 {"title":"Lewis Red (Accent)","value":"#A51C30","_id":"4272616e64205365636f6e64617279"},
 {"title":"Lewis Red Dark","value":"#7F1424","_id":"4c696e6b"},
 {"title":"Lewis Red Light (on dark)","value":"#E85D6C","_id":"4272616e64205072696d617279"},
 {"title":"Espresso (Ink)","value":"#1F1B17","_id":"32b99313-937c-45b5-a6e4-6f57cce68eee"},
 {"title":"Espresso 2","value":"#2A2420","_id":"4c696e6b20496e746572616374696f6e"},
 {"title":"Ink Soft","value":"#57504A","_id":hx("Ink Soft")},
 {"title":"Ivory (Page)","value":"#F7F2EB","_id":hx("Ivory")},
 {"title":"Linen (Sand)","value":"#EDE4D8","_id":hx("Linen")},
 {"title":"White","value":"#FFFFFF","_id":"50ddadf6-aee0-46f7-9b1c-c4304f61a36b"},
 {"title":"Line Light","value":"rgba(23, 19, 15, 0.12)","_id":hx("Line Light")},
 {"title":"Line Dark","value":"rgba(255, 255, 255, 0.14)","_id":hx("Line Dark")},
 {"title":"Photo Overlay","value":"rgba(15, 12, 9, 0.62)","_id":hx("Photo Overlay")},
]
fonts=[
 {"title":"Body (Inter)","family":"Inter","stack":"\"Inter\", system-ui, sans-serif","source":"google","order":0,"weights":["400","500","600","700"],"_id":"426f647920436f7079"},
 {"title":"Headings (Fraunces)","family":"Fraunces","stack":"\"Fraunces\", Georgia, serif","source":"google","order":1,"weights":["400","400i","500","500i","600"],"_id":"48656164696e6773"},
 {"title":"Font 3","family":"Caudex","stack":"\"Caudex\", serif","source":"google","order":3,"weights":["400","400i","700","700i"],"_id":"864dad39-1971-4e31-8237-217a46e392c7"},
]
print(cs.call('cs_update_option',name='cornerstone_color_items',value=colors).get('summary','ok'))
print(cs.call('cs_update_option',name='cornerstone_font_items',value=fonts).get('summary','ok'))
opts={
 'x_enable_font_manager':'1',
 'x_body_font_family_selection':'426f647920436f7079','x_body_font_weight_selection':'400',
 'x_headings_font_family_selection':'48656164696e6773','x_headings_font_weight_selection':'500',
 'x_body_font_family':'Inter','x_headings_font_family':'Fraunces',
 'x_body_font_color':'#57504A','x_headings_font_color':'#1F1B17',
 'x_body_font_size':'17','x_content_font_size':'17',
 'x_h1_letter_spacing':'-0.02','x_h2_letter_spacing':'-0.02','x_h3_letter_spacing':'-0.02',
 'x_design_bg_color':'#F7F2EB',
 'x_site_link_color':'global-color:4272616e64205365636f6e64617279','x_site_link_color_hover':'global-color:4c696e6b',
 'x_button_background_color':'global-color:4272616e64205365636f6e64617279','x_button_background_color_hover':'global-color:4c696e6b',
 'x_layout_site_max_width':'1200','x_layout_site_width':'92',
}
for k,v in opts.items():
    r=cs.call('cs_update_option',name=k,value=v); print(k,'prev=',r.get('previous'))
