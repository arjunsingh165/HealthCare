/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'health-primary': '#0066cc',
        'health-secondary': '#00cc99',
        'health-accent': '#ff6b6b',
        'health-light': '#f8fafc',
        'health-dark': '#1e293b',
      },
      fontFamily: {
        'health': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}