let id = null;
let deg = 0;
let limit = 0;

let facts = ["1 Fact <br> У медуз нет мозгов и кровеносных сосудов.", "2 Fact <br>Китайский язык является самым популярным в мире.", "3 Fact <br>Правое лёгкое человека вмещает больше воздуха, чем левое."];

let fact_id = 0;


function setFact(){
    const el = document.getElementById("fact");
    el.innerHTML = facts[fact_id];

    fact_id += 1;
    fact_id = fact_id % facts.length;
}

function getFact() {
    let elem = document.getElementById("wheel");
    clearInterval(id);
    limit+=800;
    id = setInterval(frame, 10);

    function frame() {
      if (deg >= limit) {
        clearInterval(id);
        setFact();
      } else {
        deg+=3;
        elem.style.transform = "rotate(" + deg % 360 + "deg)";
      }
    }
  }

