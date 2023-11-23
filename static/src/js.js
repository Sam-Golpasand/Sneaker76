let index = 0; // the index of the current slide

function moveSlide(step) {
  const slides = document.getElementsByClassName('carousel-slide');
  const totalSlides = 3;

  // Move the index step places and use modulo to wrap around.
  index = (index + step + totalSlides) % totalSlides;
  
  // Calculate the offset based on the current index.
  // This assumes each slide is 100% of the carousel width.
  const offset = -index * 45; // assuming each slide has 100% width
  const slidesContainer = document.querySelector('.carousel-slides');
  
  // Apply the transform to move to the slide.
  slidesContainer.style.transform = `translateX(${offset}%)`;
}

// Set a timeout of 5000 milliseconds (5 seconds)
setTimeout(function() {
  // Select the flash message container
  var flashMessage = document.getElementById('flash-message');
  // Check if it exists
  if (flashMessage) {
    // Fade out the flash message
    flashMessage.style.opacity = '0';
    // Optional: remove the flash message element after the fade-out transition
    setTimeout(function() {
      flashMessage.style.display = 'none';
    }, 600); // Adjust timing to match your CSS transition
  }
}, 5000); // Time in milliseconds before the flash message disappears




function updateQuantity(button, delta) {
  var form = button.closest('form');
  var input = form.querySelector('input[name="quantity"]');
  var currentQuantity = parseInt(input.value);
  var newQuantity = currentQuantity + delta;
  input.value = newQuantity > 0 ? newQuantity : 1;
  form.submit();
}
