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
          DEFAULT: '#0A0E14',
          lighter: '#141821',
          card: '#1A1F2E',
          border: '#2A2F3E',
        },
        nvidia: {
          green: '#76B900',
          'green-dark': '#5A8F00',
          'green-light': '#8BC919',
        },
        pnc: {
          blue: '#003087',
          'blue-light': '#0047BB',
          orange: '#F77F00',
        },
        accent: {
          primary: '#76B900',
          secondary: '#0047BB',
          highlight: '#F77F00',
        },
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
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

