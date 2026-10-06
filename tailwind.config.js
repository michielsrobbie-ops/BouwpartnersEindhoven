/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './build.py', './_data.py', './js/*.js'],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: '#27272A', soft: '#52525B', faint: '#A1A1AA' },   // zinc-800 / 600 / 400
        paper: { DEFAULT: '#FFFFFF', soft: '#FAFAF9', warm: '#F5F5F4' },  // white / stone-50 / stone-100
        line: { DEFAULT: '#E7E5E4', soft: '#F0EFEE' },
        merk: { DEFAULT: '#FB6A1E', ink: '#CE4904', hover: '#FD7731', soft: '#FFEDE0' }, // oranje uit het logo
        tuin: { DEFAULT: '#047857', soft: '#D1FAE5', deep: '#065F46' },    // emerald-700 / 100 / 800
      },
      fontFamily: {
        display: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        sans: ['Outfit', 'system-ui', 'sans-serif'],
        label: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        lift: '0 8px 30px rgb(0 0 0 / 0.04)',
        'lift-lg': '0 16px 48px rgb(0 0 0 / 0.06)',
      },
      maxWidth: { reading: '62ch', frame: '1280px' },
      letterSpacing: { label: '0.14em' },
    },
  },
  plugins: [],
};
