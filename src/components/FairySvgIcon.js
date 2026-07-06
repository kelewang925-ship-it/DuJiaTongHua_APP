import Svg, { Path } from 'react-native-svg';

const iconMap = {
  fourPointStar: {
    viewBox: '0 0 24 24',
    render: ({ color, strokeWidth }) => (
      <Path
        d="M12 3C12.7 8.2 15.2 11.3 20 12C15.2 12.7 12.7 15.8 12 21C11.3 15.8 8.8 12.7 4 12C8.8 11.3 11.3 8.2 12 3Z"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    ),
  },
  heart: {
    viewBox: '0 0 24 24',
    render: ({ color, strokeWidth }) => (
      <Path
        d="M12 20.5C10.4 19.1 3.3 13.7 3.3 8.4C3.3 5.8 5.3 4 7.9 4C9.6 4 11 4.9 12 6.2C13 4.9 14.4 4 16.1 4C18.7 4 20.7 5.8 20.7 8.4C20.7 13.7 13.6 19.1 12 20.5Z"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    ),
  },
  lock: {
    viewBox: '0 0 24 24',
    render: ({ color, strokeWidth }) => (
      <>
        <Path
          d="M7.3 10.2V8.1C7.3 5.5 9.2 3.6 12 3.6C14.8 3.6 16.7 5.5 16.7 8.1V10.2"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M6.1 10.2H17.9C19.1 10.2 19.8 10.9 19.8 12.1V18.5C19.8 19.7 19.1 20.4 17.9 20.4H6.1C4.9 20.4 4.2 19.7 4.2 18.5V12.1C4.2 10.9 4.9 10.2 6.1 10.2Z"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M12 14.1V16.7"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="none"
        />
      </>
    ),
  },
  pencilEdit: {
    viewBox: '0 0 64 64',
    render: ({ color, strokeWidth }) => (
      <>
        <Path
          d="M16 47L19 30L43 6C47 2 54 3 58 7C62 11 62 17 58 21L34 45L16 47Z"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M40 9L55 24"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M35 14L50 29"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M16 47L29 43"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <Path
          d="M29 55H52"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="none"
        />
      </>
    ),
  },
};

export const fairySvgIconNames = Object.keys(iconMap);

export default function FairySvgIcon({
  name,
  size = 24,
  color = '#E8A044',
  strokeWidth = 1.2,
  style,
}) {
  const icon = iconMap[name];

  if (!icon) {
    return null;
  }

  return (
    <Svg width={size} height={size} viewBox={icon.viewBox} fill="none" style={style}>
      {icon.render({ color, strokeWidth })}
    </Svg>
  );
}
