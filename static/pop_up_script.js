const popUp = document.querySelector(".pop_up");
const closeButton = document.querySelector(".close-button");

function hideFlipCards() {
    let three_in_row_flip = document.getElementsByClassName("flip_cards_container");
    let additional_three_in_row = document.getElementsByClassName("additional_cards_container");
    for (let i = 0; i < three_in_row_flip.length; i++) {
        additional_three_in_row[i].classList.remove("hidden");
        three_in_row_flip[i].classList.add("hidden");
    }
}

function showFlipCards() {
    let three_in_row_flip = document.getElementsByClassName("flip_cards_container");
    let additional_three_in_row = document.getElementsByClassName("additional_cards_container");
    for (let i = 0; i < three_in_row_flip.length; i++) {
        additional_three_in_row[i].classList.add("hidden");
        three_in_row_flip[i].classList.remove("hidden");
    }
}

function togglePopUp() {
    popUp.classList.toggle("show-popUp");
}

function closePopUp() {
    setTimeout(function () {
        showFlipCards();
    }, 300);
}

function escapeClick() {
    hideFlipCards();
    togglePopUp();
}

closeButton.addEventListener("click", togglePopUp);