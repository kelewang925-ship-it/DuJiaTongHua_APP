# DuJiaTongHua Design System V1

## Brand

Product name: 独家童话

Core idea: turn a couple's daily life into a private storybook that grows over time.

Keywords: fairy tale picture book, warm, soft paper, peach pink, dried rose, cocoa brown, hand drawn icons, sticker-like cards, memory collection, gentle AI magic.

## Visual Direction

The app should feel like a romantic illustrated diary, not a social feed or a cold AI tool.

Avoid: high saturation pink, cyber tech style, heavy illustrations, noisy banners, generic component libraries.

Prefer: large blank space, warm paper background, rounded cards, light borders, soft shadows, small hand drawn decorations.

## Colors

- Primary / 桃夭: #F6BEC8
- Primary Deep: #DFA0AC
- Secondary / 藕丝秋半: #E9D7D2
- Accent / 枯玫瑰: #B08A8F
- Text / 可可棕: #6B4F4F
- Soft Text: #9B7A7A
- Background / 月白: #F8F6F2
- Card: #FFF9F4
- Card Pink: #FFF0F2
- Gold / 琥珀金: #D8B384

## Typography

Use clear sans-serif text for readability. Titles can use a slightly warmer style later if custom fonts are added.

- Page title: 28-30, bold
- Section title: 20, bold
- Body: 14-16
- Caption: 12

## Radius

- Small: 12
- Medium: 20
- Large: 24-30

## Components

### FairyPage

Unified page shell for normal content pages. It owns the warm paper background, horizontal page padding, top spacing and bottom safe space. Use it before creating a new `ScrollView` manually.

Recommended use:

```jsx
<FairyPage>
  <FairyHeader title="设置" subtitle="调整提醒、隐私和视觉体验。" showBack />
  {/* page content */}
</FairyPage>
```

### FairyHeader

Unified page header for title, subtitle, eyebrow, optional back button and optional right action. It should replace repeated title/subtitle blocks in secondary pages.

### FairyCard

Paper-like card with rounded corners, soft border, warm background and light shadow.

### FairyButton

Primary button uses peach pink. Secondary button uses warm paper or lotus pink.

### FairyTag

Small capsule label for mood, memory type, AI state, and membership.

### FairyInput

Unified input component for diary, photo, anniversary and AI configuration forms. It supports label, icon, helper text, error state, single-line and multi-line input.

### FairyEmptyState

Unified empty state with illustration, title, description and optional action. Use it for album, search, drafts, creation history and no-diary states.

### FairyDialog

Unified modal-style confirmation component. Use it for delete confirmation, generation confirmation and leaving editor confirmation.

### FairyToast

Lightweight floating feedback component. Use it for save success, upload complete, generation started and failure hints. Keep copy short and warm.

Recommended tones:

- `success`: save/upload/generation created
- `error`: validation or request failure
- `info`: neutral process hints

### FairyImage

Unified image access component. Pages should use `name` mapping, such as `homeCover`, `coupleCover`, `workshopCover`. If real PNG/WebP assets are missing, it falls back to `FairyIllustration`.

### MemoryCard

Used for diary, photo, comic, anniversary and video records.

### MemoryWall

Home memory collage component. Used to present records as sticker-like fragments instead of a cold list.

### CoupleTimeline

Couple space timeline component. Used to present diary, photo, anniversary and AI updates as a hand-drawn story line.

### WorkshopCard

Used for AI comic and memory video entrance.

### FeaturePage

Generic content page template for settings-like secondary pages. It now uses `FairyPage` and `FairyHeader` internally.

## Motion

- Card press: slight scale down
- Page transition: soft and calm
- Toast: fade in, pause, fade out
- AI generation: ink reveal, small sparkles, warm progress wording

## Tone

Use romantic but not exaggerated text. Examples:

- 今天也被好好爱着。
- 把今天写进童话。
- 每段回忆，都值得被收藏。
- 正在把故事画成童话。