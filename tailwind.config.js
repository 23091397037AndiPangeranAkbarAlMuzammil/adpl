/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // File HTML di folder templates
    "./static/**/*.html",
    "./static/**/*.js",      // File JS di folder static (jika ada)
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'), // Tambahkan DaisyUI di sini
  ],
  daisyui: {
    themes: ["light", "dark"], // Opsi tema DaisyUI, bisa disesuaikan
  },
}
