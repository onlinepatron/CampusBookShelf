//Reccomended Books Carousel 
const ReccomendedBooks = document.querySelectorAll(".ReccomendedBooks img");
let slideIndex = 0;
let intervalId = null;


initializeSlider();
function initializeSlider(){
    if(ReccomendedBooks.length > 0){
        ReccomendedBooks[slideIndex].classList.add("displaySlide");
        intervalId = setInterval(nextSlide, 7000);
    }
}
function showSlide(index){
    if(index >= ReccomendedBooks.length){
        slideIndex = 0;
    }
    else if(index < 0){
        slideIndex = ReccomendedBooks.length - 1;
    }
    ReccomendedBooks.forEach(Rec => {
        Rec.classList.remove("displaySlide");
    });
    ReccomendedBooks[slideIndex].classList.add("displaySlide");
}
function prevSlide(){
    clearInterval(intervalId);
    slideIndex--;
    showSlide(slideIndex);
}
function nextSlide(){
    slideIndex++;
    showSlide(slideIndex);
}
