// Video/sales page behaviour (needs campaign-state.js). Two rounds, two days each, Oslo time.
// Markup contract: [data-state-show], [data-buy="full|split"], [data-price], [data-split], [data-countdown],
// [data-reveal], <main id="tilbud" data-gate hidden>, #bli-med, #sticky, [data-qa=live|replay].
(function(){
  // ---- CONFIG ----
  var STATES=[
    {name:'before'},
    {name:'r1d1',from:'2026-11-25T08:00'},{name:'r1d2',from:'2026-11-26T00:00'},
    {name:'between',from:'2026-11-27T00:00'},
    {name:'r2d1',from:'2026-12-09T08:00'},{name:'r2d2',from:'2026-12-10T00:00'},
    {name:'closed',from:'2026-12-11T00:00'}
  ];
  var DAY={r1d1:1,r2d1:1,r1d2:2,r2d2:2};
  var PRICE={1:{full:'7 997 kr',split:'3 × 2 797 kr',total:'8 391 kr',save:'6 993 kr'},2:{full:'8 997 kr',split:'3 × 3 147 kr',total:'9 441 kr',save:'5 993 kr'}};
  var OFFERS={1:{full:'#checkout-7997',split:'#checkout-3x2797'},2:{full:'#checkout-8997',split:'#checkout-3x3147'}};  // real Kajabi offer URLs later
  var END={r1d1:'2026-11-25T23:59',r1d2:'2026-11-26T23:59',r2d1:'2026-12-09T23:59',r2d2:'2026-12-10T23:59'};
  var QA={live:'#zoom-lenke',replay:'#opptak-lenke',replayFrom:'2026-12-10T20:45'};
  var KEY='maren-bw26-offer-seen';
  // ----------------
  var params=new URLSearchParams(location.search),preview=params.get('state');
  var state=CampaignState.resolve(STATES);
  CampaignState.apply(state);
  var day=DAY[state];
  if(day){
    var P=PRICE[day];
    document.querySelectorAll('[data-price]').forEach(function(el){el.textContent=P[el.getAttribute('data-price')];});
    document.querySelectorAll('[data-buy]').forEach(function(a){a.href=OFFERS[day][a.getAttribute('data-buy')];});
  }
  var live=document.querySelector('[data-qa=live]'),rep=document.querySelector('[data-qa=replay]');
  if(live&&rep&&state==='r2d2'){
    var replay=params.get('qa')==='replay'||(!preview&&Date.now()>=CampaignState.localToUtc(QA.replayFrom));
    live.hidden=replay;rep.hidden=!replay;
  }
  function p(n){return(n<10?'0':'')+n;}
  document.querySelectorAll('[data-countdown]').forEach(function(el){
    var at=el.getAttribute('data-countdown');if(at==='end')at=END[state];if(!at)return;
    var target=CampaignState.localToUtc(at)+(at.slice(-5)==='23:59'?59000:0);
    function tick(){
      var t=Math.max(0,target-Date.now());
      if(preview&&(t===0||t>7*86400000))t=(9*3600+17*60+42)*1000+(el.querySelector('[data-cd=d]')?2*86400000:0);  // stable demo value in previews
      var s=Math.floor(t/1000),d=el.querySelector('[data-cd=d]'),h=Math.floor(s/3600);
      if(d){d.textContent=Math.floor(h/24);h%=24;}
      el.querySelector('[data-cd=h]').textContent=p(h);
      el.querySelector('[data-cd=m]').textContent=p(Math.floor(s%3600/60));
      el.querySelector('[data-cd=s]').textContent=p(s%60);
    }
    tick();setInterval(tick,1000);
  });
  // Video first: the offer shows after a click, via #tilbud/#bli-med, or if seen before (not in previews).
  var gate=document.querySelector('[data-gate]'),sticky=document.getElementById('sticky');
  if(!gate||!day)return;
  function seen(){try{return localStorage.getItem(KEY)==='1';}catch(e){return false;}}
  function reveal(scroll){
    gate.hidden=false;
    try{localStorage.setItem(KEY,'1');}catch(e){}
    if(scroll)document.getElementById('bli-med').scrollIntoView({block:'start'});
  }
  var hash=location.hash==='#tilbud'||location.hash==='#bli-med';
  if(hash||(!preview&&seen()))reveal(hash);
  document.querySelectorAll('[data-reveal]').forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault();reveal(true);history.replaceState(null,'',location.search+'#tilbud');});
  });
  if(sticky)window.addEventListener('scroll',function(){sticky.classList.toggle('show',!gate.hidden&&gate.getBoundingClientRect().top<0);},{passive:true});
})();
