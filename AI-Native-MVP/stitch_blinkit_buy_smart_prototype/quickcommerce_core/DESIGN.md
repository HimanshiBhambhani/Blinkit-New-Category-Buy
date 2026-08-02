---
name: QuickCommerce Core
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f4'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#4e4634'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#7f7662'
  outline-variant: '#d1c5ae'
  surface-tint: '#755b00'
  primary: '#755b00'
  on-primary: '#ffffff'
  primary-container: '#f8cb46'
  on-primary-container: '#6e5600'
  inverse-primary: '#edc13d'
  secondary: '#1c6d00'
  on-secondary: '#ffffff'
  secondary-container: '#9ef97c'
  on-secondary-container: '#1e7400'
  tertiary: '#576159'
  on-tertiary: '#ffffff'
  tertiary-container: '#c9d3ca'
  on-tertiary-container: '#525b54'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffe08f'
  primary-fixed-dim: '#edc13d'
  on-primary-fixed: '#241a00'
  on-primary-fixed-variant: '#584400'
  secondary-fixed: '#9ef97c'
  secondary-fixed-dim: '#83dc63'
  on-secondary-fixed: '#042100'
  on-secondary-fixed-variant: '#135200'
  tertiary-fixed: '#dbe5db'
  tertiary-fixed-dim: '#bfc9c0'
  on-tertiary-fixed: '#151e18'
  on-tertiary-fixed-variant: '#404942'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-header:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '800'
    lineHeight: 28px
  headline-product:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 22px
  headline-product-mobile:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 20px
  price-bold:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 24px
  body-main:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-trust:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 16px
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-padding: 16px
  grid-gap: 12px
  section-margin: 24px
  stack-xs: 4px
  stack-sm: 8px
  stack-md: 12px
---

## Brand & Style

The design system is engineered for **Hyper-Efficiency** and **Trust**. It targets urban consumers who prioritize speed, reliability, and ease of use. The brand personality is energetic yet grounded, using high-visibility color blocks to guide the user through a dense marketplace.

The visual style is **Corporate Modern with High-Density Functionalism**. It avoids unnecessary decorative elements in favor of clear information hierarchy, high-contrast action centers, and "trust signals" that reassure the user of quality and speed. The interface relies on a clean white canvas to make colorful product photography the hero.

## Colors

The palette is optimized for instant recognition and conversion:
- **Brand Yellow (#F8CB46):** Used for the global header and primary brand moments. It evokes energy and promptness.
- **Action Green (#318616):** Reserved strictly for primary CTAs (ADD buttons), "Buy Smart" trust signals, and success states. It represents freshness and the "Go" signal for commerce.
- **Trust Mint (#F0FAF0):** A soft background tint used for informational banners and value-proposition strips to differentiate them from the shopping grid.
- **Surface White (#FFFFFF):** The primary background color to ensure maximum readability and product pop.

## Typography

This design system utilizes **Inter** for its neutral, highly legible character at small sizes. 
- **Product Titles:** Use 18px (Desktop) or 16px (Mobile) semibold to ensure items are identifiable at a glance in a dense grid.
- **Pricing:** Always bold and slightly larger than the surrounding text to emphasize value.
- **Trust Signals:** 13px regular weight for secondary information like "Refund if not fresh" or "Sealed with safety."
- **Search Bar:** Uses a medium weight for the placeholder text to ensure it stands out against the yellow header background.

## Layout & Spacing

The system follows a **High-Density Fluid Grid** model optimized for mobile-first commerce.
- **Horizontal Padding:** Main containers utilize a strict 16px margin to provide breathing room from the device edge.
- **Grid Systems:** Product grids use a 12px gap between cards. This density allows the user to see more options without excessive scrolling.
- **Header Structure:** A fixed top-area housing the delivery location and search bar, utilizing the Primary Yellow as a full-bleed background.
- **Vertical Rhythm:** Elements within cards (Image to Title to Price) follow a tight 4px or 8px vertical stack.

## Elevation & Depth

Visual hierarchy is achieved through a mix of **Tonal Layering** and **Subtle Ambient Shadows**.
- **Base Layer:** The white background (#FFFFFF) is the lowest level.
- **Product Cards:** Elevated slightly using a specific shadow: `0 1px 4px rgba(0,0,0,0.08)`. This creates a "lifted" effect without cluttering the screen with heavy dark spots.
- **Floating Actions:** Primary buttons or cart summaries can use a higher elevation (e.g., 8px blur) to appear above the main scrollable content.
- **Search Bar:** Inset shadow or a subtle border to indicate interactivity against the yellow header.

## Shapes

The shape language is **Soft and Approachable**, moving away from sharp edges to feel more consumer-friendly.
- **Product Cards:** A standard 12px radius (`rounded-lg`) is applied to all container edges.
- **Buttons:** All primary actions use a full pill-shape (radius: 999px) to differentiate "Action" elements from "Content" elements.
- **Category Icons:** Soft rounded squares or circles are used to frame category imagery, ensuring a consistent silhouette across the shop-by-category section.

## Components

### Buttons
- **Primary (ADD):** Green pill (#318616) with white semibold text. When an item is added, this transforms into a quantity selector ( - 1 + ) with a white background and green border.
- **Secondary:** Transparent background with a subtle gray border for "View All" or "More" actions.

### Cards
- **Product Card:** 12px radius, white background, subtle shadow. Contains an image area (top), title (middle), and a footer containing price and the ADD button.
- **Category Card:** Centered image with a label underneath. No shadow; background can be a very subtle tint of the primary category color.

### Input Fields
- **Global Search:** White background, 8px radius, height of 48px. Includes a magnifying glass icon and "Search for..." placeholder in medium gray.

### Chips & Badges
- **Discount Badge:** High-contrast orange or red small pill placed on the top-left of product images.
- **Delivery Time Badge:** Small label near the title or image indicating "8 mins" or "12 mins" in bold green text.

### Trust Strip (Buy Smart)
- A full-width horizontal strip with #F0FAF0 background. Contains small icons paired with 13px text ("Straight from farm," "Lowest price," etc.).