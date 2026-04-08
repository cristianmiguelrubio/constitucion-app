/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eef3fa',
          100: '#ccdaef',
          500: '#2563a8',
          700: '#1e3a5f',
          900: '#0f1f33',
        },
      },
    },
  },
  plugins: [],
}
