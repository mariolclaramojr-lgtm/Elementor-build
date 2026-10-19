/* Spurgeon — shared behaviour: sticky header, mobile menu, reveal on scroll, events view toggle,
   form confirmation, message filters, Connect sign-up pre-select */
(function(){
  var header=document.querySelector('.header'),nav=document.querySelector('.nav'),toggle=document.querySelector('.menu-toggle');
  function onScroll(){header.classList.toggle('solid',scrollY>40)}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  function setMenu(o){nav.classList.toggle('open',o);document.body.classList.toggle('menu-open',o);toggle.setAttribute('aria-expanded',o);toggle.setAttribute('aria-label',o?'Close menu':'Open menu')}
  toggle.addEventListener('click',function(){setMenu(!nav.classList.contains('open'))});
  nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  } else document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});

  // Events: Monthly / List / Tile toggle
  document.querySelectorAll('.seg').forEach(function(seg){
    seg.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
      seg.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)})});
  });

  // Forms: validate, then show a thank-you message (wire to Cornerstone Forms / Gravity Forms on the live site)
  document.querySelectorAll('.js-form').forEach(function(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(!form.checkValidity()){form.reportValidity();return}
      var done=document.createElement('div');done.className='form-done';done.setAttribute('role','status');done.tabIndex=-1;
      done.innerHTML='<h3>Thank you!</h3><p class="muted">We’ve received your note and will be in touch soon.</p>';
      form.replaceWith(done);done.focus();
    });
  });

  // Connect: "Get Connected" buttons pre-select their ministry in the sign-up form
  document.querySelectorAll('[data-ministry]').forEach(function(a){
    a.addEventListener('click',function(){var s=document.getElementById('c-ministry');if(s)s.value=a.getAttribute('data-ministry')});
  });

  // Messages: filters (dropdowns + ?speaker= / ?series= / ?topic= / ?book= / ?service= links)
  var filters=document.querySelector('.js-filters');
  if(filters){
    var cards=document.querySelectorAll('.sermon'),none=document.querySelector('.js-no-results');
    var params=new URLSearchParams(location.search);
    filters.querySelectorAll('select').forEach(function(s){var v=params.get(s.name);if(v)s.value=v});
    var fromLink=true; // until the visitor changes a dropdown, the link's filters apply as given
    function apply(){
      var want={};
      if(fromLink)['speaker','series','topic','book','service'].forEach(function(k){if(params.get(k))want[k]=params.get(k)});
      filters.querySelectorAll('select').forEach(function(s){if(s.value)want[s.name]=s.value});
      var shown=0;
      cards.forEach(function(c){var ok=Object.keys(want).every(function(k){return c.getAttribute('data-'+k)===want[k]});c.hidden=!ok;if(ok)shown++});
      if(none)none.hidden=shown>0;
    }
    filters.addEventListener('change',function(){fromLink=false;apply()});
    apply();
  }
})();
