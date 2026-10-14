"""Gravity Forms matching the design (Plan Your Visit + Prayer Request). Creates new forms; the old ones are untouched."""
import cs, json, os
THANK_YOU = json.load(open('thank_you.json'))['thank_you']

def f(id, type, label, span=6, **kw):
    d = dict(id=id, type=type, label=label, layoutGridColumnSpan=span, isRequired=False, visibility='visible')
    d.update(kw)
    return d

def form(title, fields, button, confirm, subject):
    return dict(
        title=title, description='', labelPlacement='top_label', descriptionPlacement='below',
        subLabelPlacement='below', requiredIndicator='asterisk', markupVersion=2,
        button=dict(type='text', text=button), fields=fields, is_active=True,
        # Confirmation: send people to the Thank You page (Gravity Forms "Page" confirmation)
        confirmations={'5f1e00000000a': dict(id='5f1e00000000a', name='Default Confirmation', isDefault=True,
                                             type='page', pageId=THANK_YOU, message=confirm)},
        notifications={'5f1e00000000b': dict(id='5f1e00000000b', name='Admin Notification', isActive=True,
                                             event='form_submission', to='{admin_email}', toType='email',
                                             subject=subject, message='{all_fields}')})

plan = form("Plan Your Visit (Lewis)", [
    f(1, 'text', 'First name', autocompleteAttribute='given-name', enableAutocomplete=True),
    f(2, 'text', 'Last name', autocompleteAttribute='family-name', enableAutocomplete=True),
    f(3, 'phone', 'Phone', phoneFormat='international', autocompleteAttribute='tel', enableAutocomplete=True),
    f(4, 'date', 'When will you be visiting?', dateType='datepicker', calendarIconType='none', dateFormat='mdy'),
    f(5, 'textarea', 'Will you be bringing anyone?', span=12, placeholder='Names and ages of anyone coming with you'),
], 'Let us know →', "Thanks! We can't wait to meet you.", 'New visit planned: {First name:1} {Last name:2}')

prayer = form("Prayer Request (Lewis)", [
    f(1, 'text', 'First name', autocompleteAttribute='given-name', enableAutocomplete=True),
    f(2, 'text', 'Last name', autocompleteAttribute='family-name', enableAutocomplete=True),
    f(3, 'phone', 'Phone', phoneFormat='international', autocompleteAttribute='tel', enableAutocomplete=True),
    f(4, 'email', 'Email', autocompleteAttribute='email', enableAutocomplete=True),
    f(5, 'textarea', 'How can we pray?', span=12, isRequired=True),
], 'Send request →', "Thank you. We're praying with you.", 'New prayer request from {First name:1} {Last name:2}')

connect = form("Get Connected (Lewis)", [
    f(1, 'text', 'First name', autocompleteAttribute='given-name', enableAutocomplete=True),
    f(2, 'text', 'Last name', autocompleteAttribute='family-name', enableAutocomplete=True),
    f(3, 'email', 'Email', isRequired=True, autocompleteAttribute='email', enableAutocomplete=True),
    f(4, 'phone', 'Phone', phoneFormat='international', autocompleteAttribute='tel', enableAutocomplete=True),
    f(5, 'checkbox', 'I would like to', span=12,
      choices=[{'text': t, 'value': t, 'isSelected': False} for t in (
          'Get more information about the church', 'Learn more about Jesus',
          'Have a staff member contact me', 'Ask some general questions')],
      inputs=[{'id': f'5.{i}', 'label': t} for i, t in enumerate((
          'Get more information about the church', 'Learn more about Jesus',
          'Have a staff member contact me', 'Ask some general questions'), start=1)]),
    f(6, 'textarea', 'Anything else we should know?', span=12),
], 'Get connected →', "Thanks for connecting! Someone from our team will be in touch this week.",
   'New connection card: {First name:1} {Last name:2}')

ids = json.load(open('form_ids.json')) if os.path.exists('form_ids.json') else {}
ids = {k: v for k, v in ids.items() if k.endswith('_v2')}  # v1 forms (5, 6, 7) used message confirmations
for key, fm in (('plan_v2', plan), ('prayer_v2', prayer), ('connect_v2', connect)):
    kw = {'form': fm}
    if ids.get(key): print(key, ids[key], 'exists'); continue
    r = cs.call('gf_save_form', **kw)
    ids[key] = r.get('id') or ids.get(key)
    print(key, ids[key], r.get('summary', r))
old = json.load(open('form_ids.json'))
old.update(ids)
json.dump(old, open('form_ids.json', 'w'))
