const AdultsChildsCount = document.querySelector('#adults-childs-count');
const Count = document.querySelector('.count');
const MinusAdults = document.getElementById("decrement-adults");
const PlusAdults = document.getElementById("increment-adults");
const MinusChilds = document.getElementById("decrement-childs");
const PlusChilds = document.getElementById("increment-childs");
const ChildsCount = document.querySelector(".childs");
const AdultsCount = document.querySelector(".adults");
const  SelectPeople = document.getElementById('select-people');


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


// Обработчик клика на элемент с классом AdultsChildsCount
AdultsChildsCount.addEventListener('click', () => {
  Count.classList.remove('hidden');
});

SelectPeople.addEventListener('click', () => {
  Count.classList.toggle('hidden');
})

// Обработчик клика на окно
window.addEventListener('click', (event) => {
  // Проверяем, что клик был не на Count и не на AdultsChildsCount
  if (!Count.classList.contains('hidden') && 
      event.target !== AdultsChildsCount && 
      event.target !== Count && 
      !Count.contains(event.target)) {
      Count.classList.add('hidden');
  }
});

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

const BurgerBtn = document.querySelector('.burger')
const BurgerMenu = document.querySelector('.header-list')

BurgerBtn.addEventListener('click', () => {
    BurgerMenu.classList.toggle('show')
})