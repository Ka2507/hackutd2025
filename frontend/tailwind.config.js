/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          DEFAULT: '#212529',
          lighter: '#343a40',
          card: '#343a40',
          border: '#495057',
        },
        primary: {
          DEFAULT: '#6c757d',
          light: '#adb5bd',
          lighter: '#ced4da',
        },
        accent: {
          DEFAULT: '#495057',
          light: '#6c757d',
          dark: '#343a40',
        },
        light: {
          DEFAULT: '#f8f9fa',
          gray: '#e9ecef',
          border: '#dee2e6',
        },
        gray: {
          50: '#f8f9fa',
          100: '#e9ecef',
          200: '#dee2e6',
          300: '#ced4da',
          400: '#adb5bd',
          500: '#6c757d',
          600: '#495057',
          700: '#343a40',
          800: '#212529',
          900: '#212529',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-green': 'glowGreen 2s ease-in-out infinite alternate',
        'glow-blue': 'glowBlue 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        glowGreen: {
          '0%': { boxShadow: '0 0 5px rgba(118, 185, 0, 0.3), 0 0 10px rgba(118, 185, 0, 0.2)' },
          '100%': { boxShadow: '0 0 10px rgba(118, 185, 0, 0.5), 0 0 20px rgba(118, 185, 0, 0.3), 0 0 30px rgba(118, 185, 0, 0.2)' },
        },
        glowBlue: {
          '0%': { boxShadow: '0 0 5px rgba(0, 71, 187, 0.3), 0 0 10px rgba(0, 71, 187, 0.2)' },
          '100%': { boxShadow: '0 0 10px rgba(0, 71, 187, 0.5), 0 0 20px rgba(0, 71, 187, 0.3), 0 0 30px rgba(0, 71, 187, 0.2)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}

