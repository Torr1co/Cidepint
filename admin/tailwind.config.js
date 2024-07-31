/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/web/templates/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Open Sans', 'sans'],
      },},
  },
  content: ["./node_modules/flowbite/**/*.js"],
  plugins: [
      require('flowbite/plugin')
  ],
  purge: {
    enabled: true,
    content: ["./src/web/templates/**/*.html"],
  },
};
