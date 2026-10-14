/* Spurgeon — shared behaviour: sticky header, mobile menu, reveal on scroll, events view toggle */
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
  document.querySelectorAll('.seg').forEach(function(seg){
    seg.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
      seg.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)})});
  });
})();
