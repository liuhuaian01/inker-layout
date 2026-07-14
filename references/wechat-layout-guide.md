# WeChat Official Account Layout Guide

## Environment Constraints

### HTML Tag Support

WeChat's rich-text renderer supports a subset of HTML tags. Below is the known-compatible tag list:

**Block elements (supported):**
`<div>`, `<section>`, `<p>`, `<h1>`-`<h6>`, `<blockquote>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`, `<hr>`, `<br>`, `<pre>`

**Inline elements (supported):**
`<span>`, `<a>`, `<strong>`, `<b>`, `<em>`, `<i>`, `<u>`, `<del>`, `<sub>`, `<sup>`, `<code>`, `<img>`

**SVG (supported with caveats):**
`<svg>` can be embedded inline. CSS animations inside SVG work. SMIL animations work. JavaScript does NOT work. `<foreignObject>` is unreliable.

**Blocked/Unreliable:**
`<iframe>`, `<script>`, `<style>` (works inconsistently, avoid), `<link>`, `<form>`, `<input>`, `<button>`, `<video>` (limited), `<audio>`, `<canvas>`, `<object>`, `<embed>`

### CSS Constraints

All CSS must be inline (`style="..."` attribute). Key rules:

- **No external stylesheets**: No `<link rel="stylesheet">`
- **No `<style>` blocks**: While sometimes they work, avoid for maximum compatibility
- **Inline only**: Every element gets `style="property: value; ..."`
- **Limited property support**: Some CSS properties are stripped. Test before relying on:
  - `position: fixed/sticky` — stripped
  - `backdrop-filter` — stripped
  - CSS custom properties (`var()`) — stripped
  - Complex selectors — not applicable (no stylesheets)
  - `@media` queries — not applicable (no stylesheets)

**Reliably supported CSS properties:**
- Box model: `margin`, `padding`, `width`, `max-width`, `height`, `box-sizing`
- Colors: `color`, `background-color`, `background` (simple gradients)
- Typography: `font-size`, `font-family`, `font-weight`, `font-style`, `line-height`, `letter-spacing`, `text-align`, `text-decoration`, `text-indent`, `word-break`, `white-space`
- Borders: `border`, `border-radius`, `border-left/right/top/bottom`
- Visual: `box-shadow`, `opacity`, `display` (limited)
- Flexbox: Partial support. `display: flex`, `flex-direction`, `justify-content`, `align-items` work in many clients. Not guaranteed across all WeChat versions.
- Grid: NOT supported.

### Typography

**Font stack (system fonts only):**

For Chinese text (primary):
```css
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
```

For mixed Chinese/English (editorial):
```css
font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, "Segoe UI", sans-serif;
```

For serif/academic style:
```css
font-family: "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", "SimSun", "STSong", serif;
```

**Font size reference:**
| Element | Size | Notes |
|---|---|---|
| Article title | 20-24px | Bold, often 22px |
| Section heading | 17-19px | Bold, 18px recommended |
| Body text | 14-16px | 15px is the sweet spot |
| Caption/note | 12-13px | Gray color |
| Quote text | 14-15px | Often italic or gray |
| Mobile minimum | ≥12px | WeChat minimum readable |

**Line height:**
- Body text: `1.6-1.8` (1.75 recommended for Chinese)
- Headings: `1.3-1.5`
- Captions: `1.4-1.5`

**Paragraph spacing:**
- Between paragraphs: `margin-bottom: 1em` to `1.5em`
- Section spacing: `margin: 2em 0` or `padding: 1.5em 0`
- First paragraph after heading: no extra margin needed

### Images

**Requirements:**
- Must use absolute URLs (https://)
- Host on WeChat Material Library, Tencent Cloud COS, or a reliable CDN
- Base64 is limited to ~32KB (unreliable, avoid)
- Recommended formats: JPG (photos), PNG (graphics with transparency), GIF (simple animations)
- WebP: supported in newer WeChat versions but not universally

**Image widths (content area is ~677px on most phones):**
| Usage | Width | Notes |
|---|---|---|
| Full-width image | 900-1080px | WeChat auto-scales to screen |
| Content image | 677px | Exact content width |
| Half-width (two-column table) | 330px | With 17px gutter |
| Thumbnail/icon | 60-120px | Small inline images |
| SVG inline | 100% | Use viewBox for scaling |

**Image styling:**
```html
<img src="https://example.com/image.jpg" style="display: block; max-width: 100%; height: auto; margin: 1em auto;" alt="description">
```

**Image considerations:**
- Always set `display: block` to remove inline gap below images
- `max-width: 100%` prevents overflow
- Add descriptive `alt` text for accessibility
- Long articles: consider lazy-loading via WeChat's built-in mechanism (automatic)
- Cover image (封面): 900x500px recommended, 2:1 or 2.35:1 ratio

### Table-Based Layout

Tables are the most reliable multi-column layout method in WeChat.

**Basic two-column table:**
```html
<table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
  <tr>
    <td style="width: 50%; padding: 10px; vertical-align: top;">
      <!-- Left column content -->
    </td>
    <td style="width: 50%; padding: 10px; vertical-align: top;">
      <!-- Right column content -->
    </td>
  </tr>
</table>
```

**Key table rules:**
- Always `border-collapse: collapse`
- Use `table-layout: fixed` for predictable column widths
- Set explicit widths on `<td>` (percentage or pixels)
- `vertical-align: top` prevents misalignment
- Tables within tables are allowed but limit nesting to 2-3 levels
- Remove all default table borders: `border: 0; cellpadding="0"; cellspacing="0"`

### Colors and Backgrounds

**Safe color patterns:**
- Use hex colors (`#333333`) or `rgb()` — both work
- `rgba()` works but test transparency on dark mode
- Gradients: `linear-gradient()` works (`radial-gradient()` is unreliable)
- Background images: `background-image: url()` works but be mindful of WeChat dark mode auto-inversion

**Dark mode consideration:**
WeChat applies automatic color inversion in dark mode. This means:
- White backgrounds become dark, dark text becomes light
- Images and SVGs with white backgrounds may look odd
- Images with transparency (PNG) are safer
- Avoid thin colored borders — they may disappear
- Test critical visual elements in both light and dark mode

### Article Structure Template

```html
<div style="max-width: 677px; margin: 0 auto; padding: 20px 16px;">

  <!-- Title -->
  <h1 style="font-size: 22px; font-weight: bold; color: #333; line-height: 1.4; margin-bottom: 0.5em; text-align: center;">
    Article Title
  </h1>

  <!-- Meta info -->
  <p style="font-size: 13px; color: #999; text-align: center; margin-bottom: 2em;">
    Author Name · YYYY-MM-DD
  </p>

  <!-- Body sections -->
  <section style="margin-bottom: 2em;">
    <p style="font-size: 15px; color: #333; line-height: 1.75; margin-bottom: 1em;">
      Body paragraph text...
    </p>
  </section>

  <!-- Images -->
  <img src="https://..." style="display: block; max-width: 100%; height: auto; margin: 1.5em auto;">

  <!-- Footer / CTA -->
  <div style="margin-top: 3em; padding: 20px; background: #f5f5f5; border-radius: 8px; text-align: center;">
    <p style="font-size: 13px; color: #999; margin: 0;">
      Content footer
    </p>
  </div>

</div>
```

## Common Patterns

### Pattern 1: Quote Block
```html
<blockquote style="margin: 1.5em 0; padding: 1em 1em 1em 1.2em; border-left: 4px solid #d4a574; background: #faf8f5; color: #666; font-size: 14px; line-height: 1.7;">
  Quote text here
</blockquote>
```

### Pattern 2: Highlight Card
```html
<div style="margin: 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #f5f0e8, #faf6f0); border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);">
  <h3 style="font-size: 18px; color: #8b6914; margin: 0 0 0.5em 0;">Card Title</h3>
  <p style="font-size: 14px; color: #555; line-height: 1.7; margin: 0;">Card content</p>
</div>
```

### Pattern 3: Step Numbering
```html
<div style="margin: 1em 0; display: flex; align-items: flex-start;">
  <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; background: #d4a574; color: #fff; text-align: center; font-size: 14px; font-weight: bold; flex-shrink: 0; margin-right: 12px;">1</span>
  <p style="font-size: 14px; color: #333; line-height: 1.7; margin: 0;">Step description</p>
</div>
```

### Pattern 4: Divider
```html
<!-- Thin line -->
<hr style="margin: 2em 0; border: 0; border-top: 1px solid #eee;">

<!-- Decorative -->
<div style="margin: 2em 0; text-align: center;">
  <span style="display: inline-block; width: 40px; height: 2px; background: #d4a574;"></span>
</div>

<!-- Icon divider -->
<p style="text-align: center; margin: 2em 0; font-size: 12px; color: #ccc;">◆ ◆ ◆</p>
```

### Pattern 5: Two-Column Card Grid
```html
<table style="width: 100%; border-collapse: collapse; table-layout: fixed; margin: 1.5em 0;">
  <tr>
    <td style="width: 50%; padding: 8px; vertical-align: top;">
      <div style="padding: 20px 16px; background: #f9f7f4; border-radius: 10px; text-align: center;">
        <p style="font-size: 28px; margin: 0 0 8px 0;">📊</p>
        <p style="font-size: 14px; font-weight: bold; color: #333; margin: 0;">Data Point</p>
        <p style="font-size: 12px; color: #999; margin: 6px 0 0 0;">Description</p>
      </div>
    </td>
    <td style="width: 50%; padding: 8px; vertical-align: top;">
      <div style="padding: 20px 16px; background: #f9f7f4; border-radius: 10px; text-align: center;">
        <p style="font-size: 28px; margin: 0 0 8px 0;">🎯</p>
        <p style="font-size: 14px; font-weight: bold; color: #333; margin: 0;">Goal</p>
        <p style="font-size: 12px; color: #999; margin: 6px 0 0 0;">Description</p>
      </div>
    </td>
  </tr>
</table>
```

## Long-Form Scrolling Article (长图文)

For articles that are essentially one long image:

1. Design the full image at 1080px width (or 1242px for higher quality)
2. Slice into segments if >5MB total (WeChat has upload limits)
3. Wrap each segment: `<img src="..." style="display: block; width: 100%; margin: 0; padding: 0;">`
4. Remove all gaps between images: images must be `display: block` with `margin: 0`
5. No text content needed — the image contains everything

```html
<div style="margin: 0; padding: 0;">
  <img src="https://cdn.example.com/long-image-01.jpg" style="display: block; width: 100%; margin: 0; padding: 0;">
  <img src="https://cdn.example.com/long-image-02.jpg" style="display: block; width: 100%; margin: 0; padding: 0;">
  <img src="https://cdn.example.com/long-image-03.jpg" style="display: block; width: 100%; margin: 0; padding: 0;">
</div>
```

## Pre-Delivery Checklist

- [ ] All styles are inline (`style=""`)
- [ ] No `<script>` tags or event handlers (`onclick`, etc.)
- [ ] All image URLs are absolute and accessible
- [ ] Font stack uses system fonts only
- [ ] SVG interactions tested without JS dependency
- [ ] Run `scripts/validate_mp.py` and fixed all errors
- [ ] Content width ≤ 677px for text, images can be wider
- [ ] Dark mode consideration: transparent/colored-background elements reviewed
- [ ] Cover image exists (if this is a complete article)
- [ ] Title, author, and date included
