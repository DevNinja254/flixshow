    /** @type {import('tailwindcss').Config} */
    module.exports = {
      content: [
        './templates/**/*.html',
        './**/templates/**/*.html',  //Include templates in app directories
       //'./src/**/*.js', //If you have javascript files using tailwind classes
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    }

