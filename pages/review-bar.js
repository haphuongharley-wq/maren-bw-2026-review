// Prototype only: a bar with one link per page state (?state=...), built from <body data-states="name:Label|...">.
(function(){
  var spec=document.body.getAttribute('data-states');if(!spec)return;
  var cur=document.documentElement.getAttribute('data-state');
  var bar=document.createElement('nav');bar.className='rv-bar';bar.setAttribute('aria-label','Xem trước trạng thái');
  bar.innerHTML='<b>Xem trước:</b>';
  spec.split('|').forEach(function(pair){
    var i=pair.indexOf(':'),name=pair.slice(0,i),label=pair.slice(i+1),a=document.createElement('a');
    a.href='?state='+name+(document.body.hasAttribute('data-keep-hash')?'':'');a.textContent=label;
    if(name===cur){a.className='on';a.setAttribute('aria-current','true');}
    bar.appendChild(a);
  });
  var home=document.createElement('a');home.href=location.pathname.indexOf('/vi/')>0?'../../':'../';home.className='home';home.textContent='← Tổng quan';bar.appendChild(home);
  document.body.insertBefore(bar,document.body.firstChild);
})();
