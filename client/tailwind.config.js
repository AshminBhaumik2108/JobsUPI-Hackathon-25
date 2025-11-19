/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f5f7ff",
          100: "#e6ecff",
          500: "#4f46e5",
          600: "#4338ca"
        }
      }
    }
  },
  plugins: []
};
