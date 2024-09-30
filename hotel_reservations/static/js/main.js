const AdultsChildsCount = document.querySelector('#adults-childs-count');
const Count = document.querySelector('.count');
const MinusAdults = document.getElementById("decrement-adults");
const PlusAdults = document.getElementById("increment-adults");
const MinusChilds = document.getElementById("decrement-childs");
const PlusChilds = document.getElementById("increment-childs");
const ChildsCount = document.querySelector(".childs");
const AdultsCount = document.querySelector(".adults");

const rangeAge = document.getElementById('range');
const valueAge = document.getElementById('value');

let counterAdults = 2;
let counterChilds = 0;

function updateCount() {
    let adultText = counterAdults === 1 ? "взрослый" : "взрослых";
    let childText = counterChilds === 1 ? "ребёнок" : "ребёнка";
    AdultsChildsCount.value = `${counterAdults} ${adultText}${counterChilds > 0 ? ", " + counterChilds + " " + childText : ""}`;
}


updateCount();
MinusChilds.disabled = true;

AdultsChildsCount.addEventListener('click', () => {
    Count.classList.toggle('hidden')
})

MinusAdults.addEventListener('click', () => {
    counterAdults--;
    AdultsCount.innerHTML = counterAdults;
    MinusAdults.disabled = counterAdults === 1;
    PlusAdults.disabled = counterAdults === 6;
    updateCount();
});

PlusAdults.addEventListener('click', () => {
    counterAdults++;
    AdultsCount.innerHTML = counterAdults;
    PlusAdults.disabled = counterAdults === 6;
    MinusAdults.disabled = counterAdults === 1;
    updateCount();
});

PlusChilds.addEventListener('click', () => {
    counterChilds++;
    ChildsCount.innerHTML = counterChilds;
    PlusChilds.disabled = counterChilds === 3;
    MinusChilds.disabled = false;
    updateCount();
});

MinusChilds.addEventListener('click', () => {
    counterChilds--;
    ChildsCount.innerHTML = counterChilds;
    MinusChilds.disabled = counterChilds === 0;
    PlusChilds.disabled = counterChilds === 3;
    updateCount();
});

rangeAge.oninput = function() {
    const value = this.value;
    const suffixes = ['лет', 'год', 'года'];
    let word;

    if (value == 1) {
        word = suffixes[1];
    } else if (value < 5 && value > 0) {
        word = suffixes[2];
    } else {
        word = suffixes[0];
    }

    valueAge.innerHTML = `${value} ${word}`;
}