# Fairy Components Guideline

## FairyButton

Purpose:

Unified action button component.

Types:

- primary: important actions
- secondary: alternative actions
- ghost: lightweight actions

Requirements:

- rounded shape
- soft shadow
- press feedback
- loading state support

Example:

```jsx
<FairyButton type="primary">
 保存回忆
</FairyButton>
```

## FairyDialog

Used for:

- confirmation
- destructive actions
- important reminders

Structure:

- illustration
- title
- description
- actions

## FairyToast

Used for lightweight feedback.

Types:

- success
- error
- info
- magic

## FairyCard

Unified content container.

Rules:

- consistent radius
- paper background
- gentle shadow

## FairyInput

Unified input experience.

Support:

- label
- helper text
- error state
- single/multi line

## FairyEmptyState

Empty pages should provide:

- illustration
- title
- description
- optional action

## AI Component Development Rules

Before creating a new component:

1. Check existing Fairy components.
2. Extend existing components when possible.
3. Add documentation for new components.
