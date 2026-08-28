---
name: Lumina Gastronomy
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#c4c7c9'
  on-secondary: '#2d3133'
  secondary-container: '#464a4b'
  on-secondary-container: '#b6b9bb'
  tertiary: '#b9c7e0'
  on-tertiary: '#233144'
  tertiary-container: '#8392a9'
  on-tertiary-container: '#1c2a3d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#d5e3fd'
  tertiary-fixed-dim: '#b9c7e0'
  on-tertiary-fixed: '#0d1c2f'
  on-tertiary-fixed-variant: '#3a485c'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  interactive-label:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding-mobile: 1rem
  container-padding-desktop: 2.5rem
  gutter: 1.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style
The design system embodies a premium, high-energy aesthetic tailored for a sophisticated nightlife and dining audience. It leverages a **Glassmorphic-Modern** style, blending deep, immersive dark backgrounds with vibrant, glowing accents. The personality is confident, intelligent, and "always-on," mimicking the ambient glow of a modern city at night.

The visual language focuses on high-quality imagery, depth through translucency, and intentional focal points created by radiant crimson highlights. The interface should feel like a premium concierge—refined, intuitive, and visually arresting.

## Colors
The palette is rooted in **Deep Black (#0B1120)** and **Rich Navy (#0F172A)** to create infinite depth. 

- **Primary:** Crimson Red (#E23744) is reserved for high-intent actions, active indicators, and critical brand moments. 
- **Surfaces:** Use translucent layers of Dark Gray with `backdrop-filter: blur(12px)` to maintain context while isolating interactive elements. 
- **Accent Effects:** Implement subtle inner glows on primary buttons and "outer-glow" box shadows on featured cards using the Crimson palette to simulate an OLED-style luminance.

## Typography
The system uses a dual-font strategy to balance character with utility. 

**Outfit** is used for headlines and interactive labels (buttons, tabs) to provide a modern, geometric, and friendly tone. **Inter** is utilized for body text and metadata, ensuring maximum legibility against dark backgrounds. 

For display text, utilize tight letter spacing to emphasize the "bold" personality. Secondary text should always maintain a minimum contrast ratio of 4.5:1, typically using a muted slate gray to prevent visual fatigue while keeping the focus on primary content.

## Layout & Spacing
This design system utilizes a **Fluid-Fixed Hybrid** grid. 
- **Desktop:** 12-column grid with a maximum content width of 1440px. 
- **Mobile:** Single-column layout with 16px horizontal margins.

Spacing follows a strict 4px base unit. Use generous "Stack" spacing (32px+) between major sections to emphasize the premium feel and avoid clutter. Sidebar navigation should be fixed-width (280px) with a heavy backdrop-blur to allow underlying content to peek through during scrolls.

## Elevation & Depth
Depth is communicated through **Z-index translucency** rather than traditional heavy shadows.

1.  **Level 0 (Base):** Deep Navy (#0B1120).
2.  **Level 1 (Cards):** Translucent gray (#FFFFFF at 5% opacity) with a 1px border (#FFFFFF at 10% opacity) and 12px blur.
3.  **Level 2 (Featured/Active):** Same as Level 1, but with a 2px Crimson stroke or a soft Crimson outer glow (`0 0 20px rgba(226, 55, 68, 0.2)`).
4.  **Level 3 (Modals):** High-contrast glass with a darker backdrop dimming effect (60% black overlay).

Avoid solid-colored surfaces; every elevated element should feel like a piece of glass caught in the light.

## Shapes
The shape language is smooth and organic. 
- **Standard UI elements** (Inputs, small buttons) use `rounded-lg` (16px).
- **Primary containers** (Restaurant cards, Modals) use `rounded-xl` (24px).
- **Interactive Chips** use a full pill-shape to distinguish them from structural elements.

Borders should be kept thin (1px) to maintain a precise, technical feel, except when highlighting a selected state.

## Components

### Buttons
- **Primary:** Solid Crimson (#E23744) with white text. Apply a subtle inner top-light (white at 15%) to give a tactile, slightly beveled feel.
- **Secondary:** Glass-style with a white/10 border. On hover, the border becomes Crimson.

### Cards
Restaurant cards must feature high-resolution imagery as the background. Use a bottom-to-top dark gradient overlay (black/80 to transparent) to ensure text legibility. Add a 1px "specular highlight" on the top border.

### Input Fields
Inputs are dark with a white/5 fill. The focus state replaces the border with a 2px Crimson stroke and a soft Crimson glow. Labels sit above the field in `label-caps`.

### Featured Recommendations
Special AI-curated picks should use a "Live Border"—a slow-moving gradient stroke that travels around the perimeter of the card in the primary Crimson hue.

### Sidebar
The sidebar is a vertical glass pane. Navigation items use high-contrast white for active states and muted slate for inactive states. Active items are marked with a vertical Crimson bar on the left edge.