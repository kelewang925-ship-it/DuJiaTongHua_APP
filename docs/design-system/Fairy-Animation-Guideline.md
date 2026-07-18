# Fairy Animation Guideline

## Principle

Animation should create warmth and emotional connection.

Avoid:

- excessive effects
- fast movement
- decorative animation without purpose

## Button Interaction

Recommended:

press
→ scale down
→ spring back
→ optional heart/sparkle feedback

## Dialog Animation

Open:

- opacity 0 to 1
- scale 0.92 to 1
- translateY 20 to 0

Close:

- fade out
- gentle scale down

## Page Transition

Preferred styles:

- book page transition
- fade
- paper slide

## AI Process Animation

For AI creation pages:

Use:

- magic wand feeling
- sparkle
- progress storytelling

Example:

"正在写入你的童话故事"

instead of:

"Loading..."

## Implementation

Recommended technologies:

- react-native-reanimated
- expo-haptics

Keep animations reusable through shared components.
