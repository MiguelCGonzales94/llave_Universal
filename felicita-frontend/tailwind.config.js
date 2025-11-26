/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'felicita-blue': '#2563EB', // Un azul corporativo bonito
        'felicita-dark': '#1E293B',
      }
    },
  },
  plugins: [],
}