module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './berkeh/**/*.py'
  ],
  rtl: true,
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#3b82f6',
          600: '#2563eb'
        },
        dark: {
          800: '#1e293b',
          900: '#0f172a'
        }
      },
      fontFamily: {
        sans: ['Vazir', 'sans-serif']
      }
    }
  }
}