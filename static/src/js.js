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


// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCGz2QQz554Rh_gIMIuz2WnZoWMYPWQbgQ",
  authDomain: "sneaker76-c33c7.firebaseapp.com",
  projectId: "sneaker76-c33c7",
  storageBucket: "sneaker76-c33c7.appspot.com",
  messagingSenderId: "438905707405",
  appId: "1:438905707405:web:e51418633e3d83f163bbc4",
  measurementId: "G-CTYQHD1XH2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);