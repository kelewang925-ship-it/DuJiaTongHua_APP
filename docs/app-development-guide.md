# App Development Guide

## Goal

Build an iOS and Android mobile app with React Native, Expo and JavaScript.

## Tech Stack

- React Native
- Expo
- Expo Router
- JavaScript
- React Native SVG
- Expo Linear Gradient
- Zustand later for state management

## Folder Rules

- app: routes and page stacks
- src/components: reusable visual components
- src/theme: design tokens
- src/screens: complex screen implementations if a route becomes large
- assets/design: design reference images
- docs: product and design documents

## Code Style

- Keep page files readable and modular
- Prefer custom components over generic UI libraries
- Keep colors from src/theme/colors.js
- Use warm paper background for all main pages
- Use FairyCard for content blocks
- Use emotional copywriting but keep it restrained

## Current Main Routes

- app/(tabs)/index.js: Home
- app/(tabs)/couple.js: Couple Space
- app/(tabs)/workshop.js: Fairy Workshop
- app/(tabs)/mine.js: Mine
- app/diary/editor.js: Diary editor
- app/anniversary/index.js: Anniversary list
- app/ai/comic-config.js: AI comic configuration

## UI Consistency Checklist

Before finishing any screen, check:

- Background is #F8F6F2
- Main cards use warm paper or pink card
- Text uses cocoa brown
- Accent uses dried rose or amber gold
- Corner radius is soft
- Page has enough blank space
- AI pages feel magical, not technical
- Couple pages feel private, not social-platform-like

## Next Engineering Needs

- Add local state store
- Add mock data layer
- Add navigation actions
- Add form validation
- Add image picker
- Add persistent storage
- Add API client
- Add auth flow
- Add design assets usage
