// Page state by the client's local time. A ?state=<name> URL parameter overrides it for previews.
// Each page calls CampaignState.resolve([{name:'before'},{name:'day1',from:'2026-11-25T08:00'},...]) with
// states in ascending order ("from" = local "YYYY-MM-DDTHH:MM" in TZ), then CampaignState.apply(state).
// Elements with data-state-show="a b" are shown only in those states. apply() sets el.hidden on EVERY
// [data-state-show] element, so an element whose visibility is controlled elsewhere (the offer gate)
// must not carry data-state-show.
(function(){
  var TZ='Europe/Oslo'; // set to the client's timezone
  function offset(ms){
    var p={};new Intl.DateTimeFormat('en-US',{timeZone:TZ,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'})
      .formatToParts(new Date(ms)).forEach(function(x){p[x.type]=+x.value;});
    return Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute,p.second)-ms;
  }
  function localToUtc(s){ // DST-safe
    var m=s.match(/(\d+)-(\d+)-(\d+)T(\d+):(\d+)/);var g=Date.UTC(+m[1],m[2]-1,+m[3],+m[4],+m[5]);
    return g-offset(g-offset(g));
  }
  window.CampaignState={
    localToUtc:localToUtc,
    resolve:function(states){
      var q=new URLSearchParams(location.search).get('state');
      if(q&&states.some(function(s){return s.name===q;}))return q;
      var now=Date.now(),cur=states[0].name;
      states.forEach(function(s){if(!s.from||now>=localToUtc(s.from))cur=s.name;});
      return cur;
    },
    apply:function(state){
      document.documentElement.setAttribute('data-state',state);
      document.querySelectorAll('[data-state-show]').forEach(function(el){
        el.hidden=el.getAttribute('data-state-show').split(' ').indexOf(state)<0;
      });
    }
  };
})();
