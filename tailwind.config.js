/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ["light", "cupcake"],
  },
  plugins: [require("daisyui")],
}

