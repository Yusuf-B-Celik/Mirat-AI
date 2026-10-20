import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        mirat: {
          bg: "#090d16",
          card: "#0f172a",
          cardHover: "#162035",
          border: "#1e293b",
          borderLight: "#334155",
          gold: "#f59e0b",
          goldLight: "#fbbf24",
          goldDark: "#b45309",
          cyan: "#06b6d4",
          cyanLight: "#22d3ee",
          cyanDark: "#0891b2",
          emerald: "#10b981",
          emeraldLight: "#34d399",
          amber: "#f59e0b",
          purple: "#8b5cf6",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        arabic: ["var(--font-amiri)", "Scheherazade New", "Amiri", "Traditional Arabic", "serif"],
        mono: ["var(--font-mono)", "JetBrains Mono", "Fira Code", "Courier New", "monospace"],
      },
      boxShadow: {
        glowCyan: "0 0 25px -5px rgba(6, 182, 212, 0.25)",
        glowGold: "0 0 25px -5px rgba(245, 158, 11, 0.25)",
        glowEmerald: "0 0 25px -5px rgba(16, 185, 129, 0.25)",
      },
    },
  },
  plugins: [],
};
export default config;

