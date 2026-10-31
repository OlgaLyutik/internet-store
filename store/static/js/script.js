
var P=[
{id:1,n:"Подушка антиалергенна Comfort",e:"🛏️",p:439,o:665,r:38,t:"Подушки",c:"#cfe0ff"},
{id:2,n:"Подушка ортопедична Premium",e:"💤",p:529,o:802,r:26,t:"Подушки",c:"#d9f2e6"},
{id:3,n:"Подушка пухова Extra",e:"☁️",p:1296,o:2057,r:27,t:"Подушки",c:"#fde7c8"},
{id:4,n:"Ковдра антиалергенна Eco",e:"🧺",p:1297,o:6485,r:33,t:"Ковдри",c:"#e6dcff"},
{id:5,n:"Ковдра вовняна Gold",e:"🐑",p:934,o:1394,r:9,t:"Ковдри",c:"#fdd9dc"},
{id:6,n:"Ковдра пухова касетна",e:"🪶",p:3697,o:6846,r:96,t:"Ковдри",c:"#d6f0f7"},
{id:7,n:"Комплект білизни Stripe",e:"🛌",p:999,o:1638,r:20,t:"Білизна",c:"#cfe0ff"},
{id:8,n:"Комплект білизни Light Gray",e:"🛌",p:999,o:1693,r:36,t:"Білизна",c:"#e4e6ee"},
{id:9,n:"Комплект білизни Ranforce",e:"🛌",p:1199,o:1903,r:42,t:"Білизна",c:"#d9f2e6"}
];
var tab="Усі",cart={};
function fmt(n){return n.toLocaleString("uk-UA")+" ₴"}
function render(){
  var tabs=["Усі"].concat([...new Set(P.map(x=>x.t))]);
  document.getElementById("tabs").innerHTML=tabs.map(t=>'<button class="'+(t==tab?"on":"")+'" onclick="tab=\''+t+'\';render()">'+t+'</button>').join("");
  var q=document.getElementById("q").value.toLowerCase();
  var list=P.filter(x=>(tab=="Усі"||x.t==tab)&&x.n.toLowerCase().includes(q));
  document.getElementById("grid").innerHTML=list.length?list.map(x=>{
    var d=Math.round((1-x.p/x.o)*100);
    return '<div class="card"><div class="img" style="background:'+x.c+'"><span class="disc">−'+d+'%</span>'+x.e+'</div><div class="info"><div class="name">'+x.n+'</div><div class="rate">★★★★★ · '+x.r+' відгуків</div><div class="price"><b>'+fmt(x.p)+'</b><s>'+fmt(x.o)+'</s></div><button class="add" onclick="add('+x.id+')">До кошика</button></div></div>'
  }).join(""):'<p class="empty">Нічого не знайдено</p>';
}
function add(id){cart[id]=(cart[id]||0)+1;upd();toggleCart(true)}
function chg(id,d){cart[id]+=d;if(cart[id]<=0)delete cart[id];upd()}
function upd(){
  var ids=Object.keys(cart),n=0,s=0;
  document.getElementById("items").innerHTML=ids.length?ids.map(i=>{var x=P.find(p=>p.id==i),q=cart[i];n+=q;s+=q*x.p;
    return '<div class="row"><span class="n">'+x.n+'<br><b>'+fmt(x.p)+'</b></span><button onclick="chg('+i+',-1)">−</button>'+q+'<button onclick="chg('+i+',1)">+</button></div>'}).join(""):'<p class="empty">Кошик порожній</p>';
  document.getElementById("cnt").textContent=n;document.getElementById("sum").textContent=fmt(s);
}
function toggleCart(o){document.getElementById("drawer").classList.toggle("open",o);document.getElementById("scrim").classList.toggle("on",o)}
var sl=document.querySelectorAll(".slide"),cur=0,dots=document.getElementById("dots");
sl.forEach((_,i)=>{var b=document.createElement("button");b.onclick=()=>go(i);dots.appendChild(b)});
function go(i){cur=i;sl.forEach((s,j)=>s.classList.toggle("on",j==i));[...dots.children].forEach((d,j)=>d.classList.toggle("on",j==i))}
go(0);setInterval(()=>go((cur+1)%sl.length),5000);
render();upd();
