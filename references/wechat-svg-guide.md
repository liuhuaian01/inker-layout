# WeChat SVG Interaction Guide

## Overview

Since WeChat blocks JavaScript execution, interactive SVG in articles relies on three mechanisms:

1. **CSS animations** (`@keyframes` inside `<style>` within SVG) — for motion, reveal, loops
2. **SMIL animations** (`<animate>`, `<animateTransform>`, `<set>`) — for declarative animation
3. **Anchor links** (`<a xlink:href="">`) — for clickable/tappable regions

All three can coexist in a single SVG. The key insight: every "interaction" must be achievable through CSS animation timing, SMIL declarative animation, or URL navigation.

## SVG Structure Requirements

### Minimal Inline SVG Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 677 400" width="100%" height="auto"
     style="display: block; max-width: 677px; margin: 0 auto;">

  <defs>
    <style>
      /* CSS animations go here */
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .fade-in { animation: fadeIn 0.6s ease-out; }
    </style>
  </defs>

  <!-- SVG content -->

</svg>
```

**Critical rules:**
- Always include `xmlns="http://www.w3.org/2000/svg"`
- Always set `viewBox` for responsive scaling
- `width="100%"` + `max-width` for mobile responsiveness
- `<style>` inside `<defs>` is the only reliable place for CSS in SVG
- No JavaScript, no `onclick`, no `onload`
- Avoid `<foreignObject>` — unreliable in WeChat

### SVG Dimensions

| Article Type | viewBox Width | Notes |
|---|---|---|
| Content-embedded SVG | 677 | Same as content width |
| Full-width SVG | 750-1080 | Image-like, wider than text |
| Long scrolling SVG | 677-750 | Tall viewBox for scrollable content |
| Interactive card | 300-677 | Can be smaller for card layouts |

**Height**: Set `viewBox` height to match content. SVG will scale proportionally.

## CSS Animation Patterns

### Pattern 1: Scroll-Triggered Reveal

Since there is no JavaScript scroll detection, use CSS `animation-delay` to stagger reveals. The user's natural scroll speed creates the illusion of scroll-triggered animation.

```css
@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.reveal-1 { animation: slideUp 0.6s 0.2s ease-out both; }
.reveal-2 { animation: slideUp 0.6s 0.5s ease-out both; }
.reveal-3 { animation: slideUp 0.6s 0.8s ease-out both; }
.reveal-4 { animation: slideUp 0.6s 1.1s ease-out both; }
```

**Best practice**: Use 0.3s stagger between items. Animate 5-8 items maximum. The animation plays when the SVG enters the viewport, so earlier items will have already animated by the time the user scrolls to later ones.

### Pattern 2: Loop Animation (Breathing, Pulse, Float)

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.loop-pulse { animation: pulse 2s ease-in-out infinite; }
.loop-float { animation: float 3s ease-in-out infinite; }
.loop-rotate { animation: rotate 8s linear infinite; transform-origin: center; }
```

### Pattern 3: Path Drawing (Line Reveal)

```css
@keyframes drawLine {
  from { stroke-dashoffset: 1000; }
  to { stroke-dashoffset: 0; }
}
.draw-line {
  stroke-dasharray: 1000;
  animation: drawLine 2s ease-out forwards;
}
```

### Pattern 4: Typing Effect

```css
@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

### Pattern 5: Color Cycle

```css
@keyframes colorShift {
  0% { fill: #d4a574; }
  33% { fill: #c49b6c; }
  66% { fill: #b88a5e; }
  100% { fill: #d4a574; }
}
.color-anim { animation: colorShift 4s ease-in-out infinite; }
```

## SMIL Animation Patterns

SMIL (`<animate>`, `<animateTransform>`) is supported in WeChat's SVG renderer and is more reliable than CSS animations in some cases.

### Fade In
```svg
<rect x="0" y="0" width="100" height="100" fill="#d4a574" opacity="0">
  <animate attributeName="opacity" from="0" to="1" dur="0.6s" fill="freeze"/>
</rect>
```

### Slide In From Bottom
```svg
<g>
  <animateTransform attributeName="transform" type="translate"
    from="0 30" to="0 0" dur="0.6s" fill="freeze"/>
  <!-- content -->
</g>
```

### Scale Up
```svg
<g>
  <animateTransform attributeName="transform" type="scale"
    from="0.8" to="1" dur="0.5s" fill="freeze"/>
  <!-- content -->
</g>
```

### Staggered Sequence
```svg
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.4s" fill="freeze"/>
  <!-- item 1 -->
</g>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.5s" dur="0.4s" fill="freeze"/>
  <!-- item 2 -->
</g>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="0.8s" dur="0.4s" fill="freeze"/>
  <!-- item 3 -->
</g>
```

### Auto-Rotating Carousel
```svg
<g>
  <animateTransform attributeName="transform" type="translate"
    values="0 0; -677 0; -1354 0; -677 0; 0 0"
    keyTimes="0; 0.3; 0.35; 0.65; 0.7"
    dur="9s" repeatCount="indefinite"/>
  <!-- carousel slides side by side -->
</g>
```

## Clickable SVG Patterns

### Click to Open Link
```svg
<a xlink:href="https://example.com" target="_blank">
  <rect x="0" y="0" width="300" height="200" rx="12" fill="#f5f5f5"/>
  <text x="150" y="100" text-anchor="middle" font-size="16" fill="#333">Click Me</text>
</a>
```

**Note**: `xlink:href` (not `href`) for maximum compatibility. Always include `target="_blank"` to open in browser.

### Clickable Regions on an Image Map
```svg
<!-- Background image -->
<image href="https://cdn.example.com/map.jpg" x="0" y="0" width="677" height="400"/>

<!-- Clickable hot zones -->
<a xlink:href="https://link1.com" target="_blank">
  <rect x="50" y="80" width="120" height="80" fill="transparent"/>
</a>
<a xlink:href="https://link2.com" target="_blank">
  <rect x="250" y="150" width="120" height="80" fill="transparent"/>
</a>
```

### Multi-State Toggle (CSS-based)

Simulate a toggle by using CSS animation to switch between states on a timer. This is a workaround since no JS click events exist.

```css
@keyframes toggleStates {
  0%, 44% { opacity: 1; }   /* State A visible */
  45%, 49% { opacity: 0; }  /* Transition */
  50%, 94% { opacity: 0; }  /* State B visible */
  95%, 100% { opacity: 1; } /* Transition back */
}
.state-a { animation: toggleStates 6s infinite; }
.state-b { animation: toggleStates 6s infinite; }
```

**Limitation**: Auto-cycling, not truly interactive. For true toggle, use multiple `<a>` links that lead to different pages.

## Accordion Pattern

Use CSS animations with staggered timing to create an auto-expanding accordion:

```css
@keyframes expand1 {
  0%, 20% { max-height: 0; opacity: 0; }
  25%, 100% { max-height: 500px; opacity: 1; }
}
@keyframes expand2 {
  0%, 45% { max-height: 0; opacity: 0; }
  50%, 100% { max-height: 500px; opacity: 1; }
}
```

**Reality check**: A true user-controlled accordion is not possible without JavaScript. This pattern creates a timed reveal sequence. For real user interaction, split content across multiple articles or use anchor links within the article.

## Progress Bar Pattern

```svg
<svg viewBox="0 0 400 20" width="100%" height="auto">
  <rect x="0" y="0" width="400" height="20" rx="10" fill="#eee"/>
  <rect x="0" y="0" width="0" height="20" rx="10" fill="#d4a574">
    <animate attributeName="width" from="0" to="280" dur="2s" fill="freeze"/>
  </rect>
  <text x="200" y="14" text-anchor="middle" font-size="10" fill="#fff" font-weight="bold">
    70%
  </text>
</svg>
```

## Before/After Comparison Slider

Use CSS animation to slide a clip-path reveal:

```css
@keyframes revealAfter {
  0%, 30% { width: 0; }
  70%, 100% { width: 100%; }
}
```

```svg
<!-- Before image (full) -->
<image href="before.jpg" x="0" y="0" width="677" height="400"/>

<!-- After image (revealed by clip) -->
<clipPath id="revealClip">
  <rect x="0" y="0" width="0" height="400">
    <animate attributeName="width" from="0" to="677" dur="3s" fill="freeze"/>
  </rect>
</clipPath>
<image href="after.jpg" x="0" y="0" width="677" height="400" clip-path="url(#revealClip)"/>

<!-- Divider line -->
<line x1="0" y1="0" x2="0" y2="400" stroke="#fff" stroke-width="3">
  <animate attributeName="x1" from="0" to="677" dur="3s" fill="freeze"/>
  <animate attributeName="x2" from="0" to="677" dur="3s" fill="freeze"/>
</line>
```

## Timeline / Milestone Pattern

```svg
<svg viewBox="0 0 677 600" width="100%" height="auto">
  <defs>
    <style>
      @keyframes dotPop { from { r: 0; } to { r: 8; } }
      @keyframes lineGrow { from { stroke-dashoffset: 600; } to { stroke-dashoffset: 0; } }
      .timeline-line { stroke-dasharray: 600; animation: lineGrow 2s ease-out forwards; }
    </style>
  </defs>

  <!-- Vertical line -->
  <line x1="60" y1="50" x2="60" y2="550" stroke="#e0d5c5" stroke-width="2" class="timeline-line"/>

  <!-- Milestone 1 -->
  <circle cx="60" cy="120" r="8" fill="#d4a574">
    <animate attributeName="r" from="0" to="8" dur="0.4s" begin="0.3s" fill="freeze"/>
  </circle>
  <text x="90" y="116" font-size="12" fill="#999">2020</text>
  <text x="90" y="136" font-size="15" fill="#333" font-weight="bold">Milestone Title</text>
  <text x="90" y="156" font-size="13" fill="#666">Description text here</text>

  <!-- Milestone 2 -->
  <circle cx="60" cy="260" r="8" fill="#d4a574">
    <animate attributeName="r" from="0" to="8" dur="0.4s" begin="0.8s" fill="freeze"/>
  </circle>
  <!-- ... -->
</svg>
```

## Common Pitfalls

1. **`<foreignObject>` for HTML in SVG**: Unreliable in WeChat. Do not use.
2. **Complex `<style>` blocks**: Keep CSS inside `<defs><style>`. Avoid `@import`.
3. **Oversized SVGs**: Keep SVG markup under 200KB. Large SVGs may be truncated.
4. **Missing viewBox**: Without viewBox, SVG won't scale properly on different screen sizes.
5. **Text rendering**: Chinese text in SVG should specify `font-family` explicitly; otherwise it may render as a fallback serif font.
6. **`<use>` tags**: Sometimes stripped. Prefer duplicating elements over `<use>` references.
7. **Gradients**: `linearGradient` and `radialGradient` work. Test on iOS and Android separately.
8. **Filters (blur, drop-shadow)**: `feGaussianBlur` works. `feDropShadow` is unreliable. Use multiple elements for shadow effects.
9. **Animation performance**: Limit simultaneous animations to avoid jank on low-end devices.
10. **WeChat version differences**: iOS WeChat generally has better SVG support than Android WeChat. Test on both.

## SVG Size Budget

| Component | Max Size |
|---|---|
| Single SVG | 200KB markup |
| All SVGs combined in article | 500KB markup |
| Embedded images in SVG (`<image href="">`) | 5MB per image |
| CSS keyframes | ~20 rules |
| SMIL animations | ~30 elements |
| DOM elements in SVG | ~500 nodes |

## Minimal Viable SVG Test

Before building complex interactions, verify basic SVG rendering:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="100%" height="auto">
  <rect x="0" y="0" width="200" height="100" rx="10" fill="#d4a574"/>
  <text x="100" y="55" text-anchor="middle" font-size="16" fill="#fff" font-family="PingFang SC, Microsoft YaHei, sans-serif">
    SVG Test ✓
  </text>
</svg>
```
