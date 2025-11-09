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
          DEFAULT: '#020305',
          lighter: '#0a0d10',
          card: '#0f1418',
          border: '#1a1f24',
        },
        green: {
          DEFAULT: '#95c800',
          dark: '#7aa300',
          light: '#a8d419',
        },
        silver: {
          DEFAULT: '#707b81',
          light: '#8a9399',
          dark: '#565d63',
        },
        orange: {
          DEFAULT: '#ff8127',
          light: '#ff9a4d',
          dark: '#cc681f',
        },
        accent: {
          primary: '#ffffff',
          secondary: '#707b81',
          highlight: '#ffffff',
        },
        gray: {
          50: '#f9fafb',
          100: '#707b81',
          200: '#707b81',
          300: '#707b81',
          400: '#707b81',
          500: '#707b81',
          600: '#565d63',
          700: '#565d63',
          800: '#1a1f24',
          900: '#020305',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-white': 'glowWhite 2s ease-in-out infinite alternate',
        'glow-silver': 'glowSilver 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        glowWhite: {
          '0%': { boxShadow: '0 0 5px rgba(255, 255, 255, 0.2), 0 0 10px rgba(255, 255, 255, 0.1)' },
          '100%': { boxShadow: '0 0 10px rgba(255, 255, 255, 0.4), 0 0 20px rgba(255, 255, 255, 0.2), 0 0 30px rgba(255, 255, 255, 0.1)' },
        },
        glowSilver: {
          '0%': { boxShadow: '0 0 5px rgba(112, 123, 129, 0.3), 0 0 10px rgba(112, 123, 129, 0.2)' },
          '100%': { boxShadow: '0 0 10px rgba(112, 123, 129, 0.5), 0 0 20px rgba(112, 123, 129, 0.3), 0 0 30px rgba(112, 123, 129, 0.2)' },
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

