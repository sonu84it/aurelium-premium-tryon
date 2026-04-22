import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ivory: "#f7f1e8",
        parchment: "#efe4d2",
        champagne: "#dbc08f",
        charcoal: "#23211f",
        gold: "#b89352",
        stone: "#7b7268",
      },
      boxShadow: {
        halo: "0 20px 60px rgba(35,33,31,0.08)",
      },
      fontFamily: {
        display: ["Cormorant Garamond", "serif"],
        sans: ["Manrope", "sans-serif"],
      },
      backgroundImage: {
        "editorial-glow": "radial-gradient(circle at top, rgba(219,192,143,0.28), transparent 40%), linear-gradient(180deg, #fbf6ef 0%, #f4eee3 100%)",
      },
    },
  },
  plugins: [],
};

export default config;
