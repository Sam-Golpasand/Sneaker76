let index = 0; // the index of the current slide

function moveSlide(step) {
  const slides = document.getElementsByClassName('carousel-slide');
  const totalSlides = 9;

  // Move the index step places and use modulo to wrap around.
  index = (index + step + totalSlides) % totalSlides;
  
  // Calculate the offset based on the current index.
  // This assumes each slide is 100% of the carousel width.
  const offset = -index * 45; // assuming each slide has 100% width
  const slidesContainer = document.querySelector('.carousel-slides');
  
  // Apply the transform to move to the slide.
  slidesContainer.style.transform = `translateX(${offset}%)`;
}
