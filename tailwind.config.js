/** @type {import('tailwindcss').Config} */
module.exports = {
   content: [
    './templates/**/*.{html,js}',
    '*/templates/**/*.{html,js}',
    '*/templates/*/*.{html,js}',
    './components/**/*.{html,js}',
    './templates/*.{html,js}',
    
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

