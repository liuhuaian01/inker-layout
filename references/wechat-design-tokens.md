# WeChat Article Design Tokens

## Design Philosophy

WeChat articles are consumed on mobile screens (375-414px wide typical) in a scrolling feed. Design must be:
- **Legible**: Large enough type, sufficient contrast
- **Scannable**: Clear hierarchy, visual anchors every 2-3 scrolls
- **Lightweight**: No heavy assets that slow loading
- **Dark-mode tolerant**: Colors and images that survive WeChat's dark mode inversion

## Default Editorial Theme

A warm, readable editorial palette suitable for most content types.

### Colors

#### Primary Palette
| Token | Hex | Usage |
|---|---|---|
| `--text-primary` | `#333333` | Body text |
| `--text-secondary` | `#666666` | Secondary text, captions |
| `--text-tertiary` | `#999999` | Meta info, dates, footnotes |
| `--text-inverse` | `#FFFFFF` | Text on dark/colored backgrounds |
| `--bg-primary` | `#FFFFFF` | Page background |
| `--bg-secondary` | `#F7F7F7` | Section background |
| `--bg-warm` | `#FAF8F5` | Warm highlight background |
| `--border-light` | `#EEEEEE` | Dividers, light borders |
| `--border-medium` | `#E0E0E0` | Card borders |

#### Accent Palette (Warm Editorial)
| Token | Hex | Usage |
|---|---|---|
| `--accent` | `#D4A574` | Primary accent: links, highlights, CTAs |
| `--accent-dark` | `#B8895A` | Hover/dark variant of accent |
| `--accent-light` | `#F5EDE3` | Light accent background |
| `--accent-warm` | `#C49B6C` | Secondary warm accent |

#### Semantic Colors
| Token | Hex | Usage |
|---|---|---|
| `--success` | `#52C41A` | Positive indicators |
| `--warning` | `#FAAD14` | Attention/notices |
| `--error` | `#FF4D4F` | Critical alerts |
| `--info` | `#1890FF` | Informational highlights |

#### Gradient Presets
```css
/* Warm editorial */
background: linear-gradient(135deg, #F5EDE3 0%, #FAF8F5 50%, #F0EAE0 100%);

/* Brand bold */
background: linear-gradient(135deg, #D4A574 0%, #C49B6C 100%);

/* Cool professional */
background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);

/* Fresh natural */
background: linear-gradient(135deg, #A8E6CF 0%, #88D8B0 100%);

/* Sunset warm */
background: linear-gradient(135deg, #FAD0C4 0%, #FFD1FF 100%);
```

### Typography Scale

```
Title:        22px / 1.4 line-height / bold / #333
Section Head: 18px / 1.4 line-height / bold / #333
Sub-head:     16px / 1.5 line-height / bold / #555
Body:         15px / 1.75 line-height / normal / #333
Body-small:   14px / 1.7 line-height / normal / #666
Caption:      13px / 1.5 line-height / normal / #999
Footnote:     12px / 1.4 line-height / normal / #BBB
```

### Spacing Scale

```
xs:  4px   — icon-to-text, tight inline spacing
sm:  8px   — within-card padding, list item gap
md:  16px  — paragraph margin, card padding
lg:  24px  — section margin, large card padding
xl:  32px  — major section separation
2xl: 48px  — article header/footer spacing
3xl: 64px  — major content block separation
```

### Border Radius

```
sm:  4px   — small badges, inline code
md:  8px   — cards, containers
lg:  12px  — large cards, hero sections
xl:  16px  — feature cards, CTA buttons
full: 50%  — avatars, circular badges
```

### Shadow Presets

```css
/* Subtle card */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

/* Elevated card */
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);

/* Floating */
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.10);

/* Text shadow for overlays */
text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
```

## Alternative Themes

### Minimalist Monochrome

A clean, high-contrast theme for serious/analytical content.

```
Text:       #1A1A1A / #4A4A4A / #8A8A8A
Background: #FFFFFF / #FAFAFA / #F0F0F0
Border:     #E5E5E5 / #D0D0D0
Accent:     #000000 (borders, underlines)
```

### Tech Blue

For technology, SaaS, or data-heavy content.

```
Text:       #2C3E50 / #5D6D7E / #95A5A6
Background: #FFFFFF / #F4F6F8 / #EBF0F5
Accent:     #3498DB
Accent-alt: #2980B9
Gradient:   #3498DB → #2C3E50
```

### Lifestyle Warm

For lifestyle, food, travel, or personal content.

```
Text:       #4A3728 / #7B6B5D / #A89888
Background: #FFFDF9 / #FFF8F0 / #FFF0E0
Accent:     #E8A87C
Accent-alt: #D4956B
Gradient:   #FDF2E9 → #FADBD8
```

### Luxury Dark

For luxury, fashion, or premium brand content.

```
Text:       #2D2D2D / #5A5A5A / #909090
Background: #FFFFFF / #F5F0EB / #EBE3D8
Accent:     #C9A96E (gold)
Accent-alt: #B8944A
Gradient:   #2D2D2D → #1A1A1A (for dark sections)
```

### Fresh Green

For health, wellness, sustainability, or education content.

```
Text:       #2D3A2D / #5A6B5A / #8A9A8A
Background: #FFFFFF / #F5F8F5 / #EBF2EB
Accent:     #5B8C5A
Accent-alt: #4A7A49
Gradient:   #E8F5E9 → #C8E6C9
```

### Fashion Editorial (时尚)

High-contrast magazine editorial style. Bold typography, dramatic whitespace, Vogue-like sophistication. For fashion, beauty, luxury lifestyle content.

```
Text:       #1A1A1A / #4D4D4D / #8C8C8C
Background: #FFFFFF / #F8F8F8 / #F0F0F0
Accent:     #C41E3A (crimson red)
Accent-alt: #8B0000 (dark red)
Gradient-1: #1A1A1A → #333333 (dark hero sections)
Gradient-2: #C41E3A → #FF6B6B (accent gradient)
Serif:      Didot, Bodoni, Songti SC (for headings only)
```

**Fashion-specific rules:**
- Title: 24-28px, often uppercase or tracked-out (letter-spacing: 2-4px)
- Section heads: 12-14px uppercase, letter-spacing: 3-6px
- Body text goes smaller: 14px (feels more editorial)
- Generous whitespace: section margins 48-64px
- Hero image always full-width, no border-radius
- Thin lines (1px) as primary dividers
- Quote blocks: centered, large type, no left border — pure typographic emphasis

### Trendy Street (潮流)

Vibrant, energetic, street-culture inspired. Neon accents, bold color blocks, Gen-Z aesthetic. For streetwear, music, youth culture, trending topics.

```
Text:       #1C1C1E / #48484A / #8E8E93
Background: #FFFFFF / #F2F2F7 / #E5E5EA
Accent:     #6C5CE7 (electric purple)
Accent-alt: #00D2FF (cyan)
Accent-hot: #FF6B35 (vibrant orange)
Gradient-1: #6C5CE7 → #00D2FF (cyber gradient)
Gradient-2: #FF6B35 → #FFD93D (sunset gradient)
Gradient-3: #A8E6CF → #FFD3B6 (pastel gradient)
```

**Trendy-specific rules:**
- Use bold color blocks as section backgrounds (not just white/gray)
- Large emoji or icon numbers: 48-64px
- Rounded elements: 16-24px border-radius
- Gradient backgrounds on cards and CTAs
- Mix sans-serif body with bold display moments
- Sticker-like floating badges with strong shadows
- Diagonal or asymmetric layout hints (via angled gradient sections)
- "气泡对话" style quote blocks with colored backgrounds

### Gallery Artistic (艺术)

Museum white, dramatic negative space, serif-forward. For art exhibitions, cultural criticism, photography, creative portfolios.

```
Text:       #1C1C1C / #555555 / #888888
Background: #FAFAFA / #F5F5F5 / #EEEEEE
Accent:     #000000 (black)
Accent-alt: #D4A574 (warm gold, sparingly)
Gradient:   none (avoid gradients; use flat colors)
Paper:      #FDFBF7 (off-white paper texture feel)
```

**Artistic-specific rules:**
- Wide margins: 32-40px padding on mobile (yes, intentionally spacious)
- Serif headings: 20-28px, `font-family: "Songti SC", "SimSun", "Noto Serif CJK SC", serif`
- Body: 15-16px with 2.0 line-height (breathe)
- Image captions: 12px italic, right-aligned or centered
- Dividers: thin 1px black lines, or decorative ornaments
- Cards: no shadows, 1px border, white or paper background
- CTA: underline text links instead of buttons
- Monochrome palette with ONE accent color pop
- Image borders: thin 1px frame around photos (gallery feel)
- Block quotes: large italic serif, indented, no background

### Chinese Ink Wash (国风墨韵)

Traditional Chinese aesthetics. Ink wash tones, Kaishu/Songti typography, vermillion seal accents, rice-paper texture warmth. For cultural, historical, literary, or heritage content.

```
Text:       #2C2416 / #5C4A3A / #8C7B6B
Background: #FDF8F0 (rice paper) / #F5EDE0 / #EBE0D0
Accent:     #C13A2B (vermillion red / 朱砂)
Accent-alt: #8B4513 (dark wood / 檀木)
Gold:       #B8860B (dark gold, sparingly)
Ink:        #1A1A1A (calligraphy black for headings)
Water:      #A8C8D8 (浅青, water-wash blue accent)
```

**Chinese Ink-specific rules:**
- **Typography hierarchy**: Section heads use Kaishu or Songti serif; body uses Songti with generous spacing
- Headings: `font-family: "KaiTi", "STKaiti", "Songti SC", "SimSun", serif` — 20-28px
- Body: `font-family: "Songti SC", "SimSun", "Noto Serif CJK SC", serif` — 15-16px, line-height: 1.9-2.1
- **Divider**: "◆" ornament, "···" or thin vermillion line; never plain lines
- **Background**: Warm off-white (#FDF8F0) simulating rice paper; no pure white
- **Cards**: 1px border in #D4C4A8 (aged gold), subtle shadow, slight rounded corners
- **Headers**: Section numbers as vermillion seal stamps — red circle (#C13A2B) with white text, 28px diameter
- **Quote blocks**: Indented, left vermillion border, slightly smaller KaiTi font, warm background
- **Images**: Thin dark-wood frame (2px #8B4513), no border-radius (traditional framing)
- **CTA**: Vermillion seal-stamp style button — red circular badge, or underline text link in gold
- **Special elements**: Vertical text optional for poetic sections; "seal stamp" decoration for key numbers
- **Color restraint**: Black/ink/vermillion/paper — four colors maximum. Modern additions are diluted

---

## Component Tokens

### Article Header

```
Container: padding-top: 32px; padding-bottom: 24px;
Title: 22px bold #333 center
Meta: 13px #999 center margin-top: 8px
Divider: 1px #EEE margin-top: 20px (optional)
```

### Section Header

```
Container: margin: 32px 0 16px 0
Title: 18px bold #333
Optional accent line: 3px wide × 20px tall, accent color, left of title
```

### Body Paragraph

```
Font: 15px #333 line-height: 1.75
Spacing: margin-bottom: 1em (16px)
First paragraph after heading: no extra top margin
```

### Image

```
Display: block
Width: 100% (max-width: 677px or full container width)
Margin: 1.5em auto (24px)
Caption: 13px #999 center margin-top: 8px
```

### Quote Block

```
Background: #FAF8F5
Border-left: 4px solid accent color (#D4A574)
Padding: 16px 16px 16px 20px
Font: 14px #666 line-height: 1.7
Margin: 24px 0
```

### Card

```
Background: #FFFFFF or #F7F7F7
Border: 1px solid #EEE (optional)
Border-radius: 12px
Padding: 20px 16px
Shadow: 0 2px 8px rgba(0,0,0,0.06)
Margin: 16px 0
```

### Button / CTA

```
Inline-block or block element
Padding: 12px 32px
Border-radius: 24px (pill) or 8px (rounded)
Background: accent color (#D4A574)
Text: #FFFFFF 16px bold center
Max-width: 280px, centered
```

### Divider

```
Thin: 1px solid #EEE, margin: 24px 0
Accent: 40px × 2px accent color, centered, margin: 32px 0
Decorative: text-based (◆ ◆ ◆), #CCC, margin: 32px 0
```

### Footer

```
Container: margin-top: 40px; padding: 24px 0
Text: 13px #999 center
Optional logo/brand line above
Optional QR code for account follow
```

## WeChat-Specific Color Considerations

### Dark Mode Strategy

WeChat's dark mode inverts colors automatically. Strategies:

1. **PNG with transparency**: Images with transparent backgrounds survive dark mode best
2. **Avoid pure white SVGs**: White SVG elements may become dark. Use off-white (#FAFAFA) backgrounds with opacity
3. **Test thin borders**: 1px borders in light grays may become invisible
4. **Colored text in SVGs**: Hardcoded `fill="#333"` will be inverted. Use `fill="currentColor"` where possible
5. **Background images**: JPG backgrounds with white areas will look odd when inverted

### Brand Color Safety

When using brand colors, ensure minimum contrast ratios:
- Body text on white: ≥ 4.5:1 (WCAG AA)
- Large text on white: ≥ 3:1
- Accent on white: check if it works as link color (underlined or bold enough)

## Quick Reference Card

**To apply a theme to an article:**

1. Choose a palette from above
2. Replace the hex values in the article's inline styles
3. Maintain the typography scale (these sizes are tested for readability)
4. Keep spacing consistent (use the spacing scale, do not invent new values)
5. Add at most ONE accent color beyond the text/background palette
6. Provide the complete HTML with all styles inlined
