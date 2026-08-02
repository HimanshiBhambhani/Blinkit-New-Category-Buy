import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "system-ui", "sans-serif"],
      },
      colors: {
        "primary-container": "#f8cb46",
        "on-primary-container": "#6e5600",
        secondary: "#1c6d00",
        "on-secondary-container": "#1e7400",
        "secondary-container": "#9ef97c",
        "blinkit-green": "#318616",
        "blinkit-trust-bg": "#F0FAF0",
        surface: "#f9f9f9",
        "surface-bright": "#f9f9f9",
        "surface-container-low": "#f3f3f4",
        "surface-container-lowest": "#ffffff",
        "surface-container": "#eeeeee",
        "surface-container-highest": "#e2e2e2",
        "surface-variant": "#e2e2e2",
        "on-surface": "#1a1c1c",
        "on-surface-variant": "#4e4634",
        outline: "#7f7662",
        "outline-variant": "#d1c5ae",
        primary: "#755b00",
        "primary-fixed-dim": "#edc13d",
        error: "#ba1a1a",
        "error-container": "#ffdad6",
        "on-error-container": "#93000a",
      },
      spacing: {
        "container-padding": "16px",
        "section-margin": "24px",
        "stack-xs": "4px",
        "stack-sm": "8px",
        "stack-md": "12px",
        "grid-gap": "12px",
      },
      fontSize: {
        display: ["22px", { lineHeight: "28px", fontWeight: "800" }],
        headline: ["18px", { lineHeight: "22px", fontWeight: "600" }],
        "headline-sm": ["16px", { lineHeight: "20px", fontWeight: "600" }],
        price: ["18px", { lineHeight: "24px", fontWeight: "700" }],
        body: ["14px", { lineHeight: "20px", fontWeight: "400" }],
        trust: ["13px", { lineHeight: "16px", fontWeight: "400" }],
        caps: [
          "11px",
          {
            lineHeight: "14px",
            letterSpacing: "0.5px",
            fontWeight: "700",
          },
        ],
      },
      borderRadius: {
        card: "12px",
      },
      maxWidth: {
        phone: "430px",
      },
    },
  },
  plugins: [],
};
export default config;
