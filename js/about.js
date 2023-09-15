var id = null;
var deg = 0;
var limit = 0;

var facts = ["1 Fact <br> У медуз нет мозгов и кровеносных сосудов.", "2 Fact <br>Китайский язык является самым популярным в мире.", "3 Fact <br>Правое лёгкое человека вмещает больше воздуха, чем левое."];

var fact_id = 0;

// console.log("Start");

function setFact(){
    const el = document.getElementById("fact");
    // el.textContent = facts[fact_id];
    el.innerHTML = facts[fact_id];

    fact_id += 1;
    fact_id = fact_id % facts.length;
}

function getFact() {
    var elem = document.getElementById("wheel");
    clearInterval(id);
    limit+=800;
    id = setInterval(frame, 10);
    function frame() {
      if (deg >= limit) {
        clearInterval(id);
        setFact();
      } else {
        deg+=3;
        elem.style.transform = "rotate("+deg%360+"deg)";
      }
    }
  }

// getFact();