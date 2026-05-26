import Svg, {
  Circle,
  Defs,
  Ellipse,
  G,
  LinearGradient,
  Path,
  Rect,
  Stop,
} from 'react-native-svg';
import colors from '../theme/colors';

function Sticker({ x, y, rotate = 0, scale = 1 }) {
  return (
    <G transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`}>
      <Path d="M0 10 C4 0 14 0 17 8 C21 0 32 2 31 13 C29 25 18 29 16 31 C14 29 2 24 0 10Z" fill="#F7A7B7" opacity="0.82" />
      <Path d="M5 12 C8 6 13 6 16 12" stroke="#A86F76" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.35" />
    </G>
  );
}

function CoupleBook() {
  return (
    <G>
      <Ellipse cx="96" cy="165" rx="64" ry="11" fill="#E9D7D2" opacity="0.55" />
      <Rect x="46" y="110" width="100" height="50" rx="9" fill="#FFF9F4" stroke="#E7C7C2" strokeWidth="2" />
      <Path d="M96 113 L96 158" stroke="#E7C7C2" strokeWidth="2" />
      <Circle cx="79" cy="76" r="22" fill="#9B6A51" />
      <Circle cx="113" cy="76" r="22" fill="#7B584A" />
      <Path d="M61 107 C65 91 77 86 91 93 L96 124 L52 124 C53 116 56 111 61 107Z" fill="#F7D4CD" />
      <Path d="M103 93 C118 85 132 92 137 108 C140 116 140 122 140 124 L96 124 L101 99Z" fill="#E9C0B9" />
      <Circle cx="79" cy="82" r="15" fill="#F7D7C9" />
      <Circle cx="113" cy="82" r="15" fill="#F2CDBD" />
      <Path d="M72 78 C77 70 88 71 93 79" fill="#9B6A51" />
      <Path d="M101 78 C108 69 122 71 129 82" fill="#7B584A" />
      <Path d="M88 99 C93 104 100 104 105 99" stroke={colors.accent} strokeWidth="2" fill="none" strokeLinecap="round" />
      <Path d="M56 126 C75 119 86 119 96 126 C107 119 121 119 140 126" stroke="#D8B384" strokeWidth="2" fill="none" />
    </G>
  );
}

function AlbumStack() {
  return (
    <G>
      <Rect x="37" y="59" width="118" height="88" rx="17" fill="#FFEDEF" stroke="#E7C7C2" strokeWidth="2" transform="rotate(-5 96 103)" />
      <Rect x="50" y="48" width="112" height="92" rx="17" fill="#FFF9F4" stroke="#E7C7C2" strokeWidth="2" transform="rotate(5 106 94)" />
      <Rect x="62" y="63" width="76" height="50" rx="12" fill="#F7C7B8" />
      <Path d="M62 103 L89 83 L108 98 L120 88 L138 103 L138 113 L62 113Z" fill="#D8B384" opacity="0.6" />
      <Circle cx="120" cy="78" r="8" fill="#FFF5DF" />
      <Path d="M67 125 C83 132 116 133 135 124" stroke={colors.accent} strokeWidth="3" fill="none" strokeLinecap="round" />
    </G>
  );
}

function MagicWorkshop() {
  return (
    <G>
      <Rect x="35" y="54" width="122" height="96" rx="22" fill="#FFF0F2" stroke="#E7C7C2" strokeWidth="2" />
      <Path d="M55 124 C78 100 104 101 137 124" fill="#F8D7D2" />
      <Circle cx="80" cy="86" r="25" fill="#F6BEC8" opacity="0.72" />
      <Circle cx="116" cy="84" r="24" fill="#D8B384" opacity="0.45" />
      <Path d="M73 92 C83 82 102 78 119 90" stroke="#6B4F4F" strokeWidth="2" fill="none" strokeLinecap="round" />
      <Path d="M111 48 L119 65 L137 68 L123 80 L127 98 L111 89 L95 98 L99 80 L85 68 L103 65Z" fill="#FFF5DF" stroke="#D8B384" strokeWidth="2" />
      <Path d="M54 57 C47 45 59 39 67 48" stroke="#F7A7B7" strokeWidth="3" fill="none" strokeLinecap="round" />
    </G>
  );
}

function AnniversaryJar() {
  return (
    <G>
      <Rect x="62" y="38" width="68" height="18" rx="7" fill="#D8B384" />
      <Path d="M58 58 C53 88 56 134 96 148 C136 134 139 88 134 58Z" fill="#FFF9F4" stroke="#D8B384" strokeWidth="2" />
      <Path d="M66 103 C79 85 112 85 126 104 C120 128 74 128 66 103Z" fill="#F8D7D2" />
      <Path d="M84 101 C88 91 100 91 103 100 C108 91 121 94 120 106 C118 120 105 126 102 128 C99 126 85 119 84 101Z" fill="#F7A7B7" />
      <Path d="M80 71 C89 64 103 64 113 72" stroke={colors.accent} strokeWidth="2" fill="none" strokeLinecap="round" />
    </G>
  );
}

export default function FairyIllustration({ scene = 'cover', width = '100%', height = 180, style }) {
  const Scene = scene === 'album'
    ? AlbumStack
    : scene === 'workshop' || scene === 'movie'
      ? MagicWorkshop
      : scene === 'anniversary'
        ? AnniversaryJar
        : CoupleBook;

  return (
    <Svg width={width} height={height} viewBox="0 0 192 192" style={style}>
      <Defs>
        <LinearGradient id="paper" x1="0" y1="0" x2="1" y2="1">
          <Stop offset="0" stopColor="#FFF9F4" />
          <Stop offset="1" stopColor="#FFF0F2" />
        </LinearGradient>
      </Defs>
      <Rect x="6" y="8" width="180" height="176" rx="36" fill="url(#paper)" />
      <Circle cx="30" cy="31" r="9" fill="#F6BEC8" opacity="0.22" />
      <Circle cx="166" cy="49" r="7" fill="#D8B384" opacity="0.24" />
      <Circle cx="33" cy="154" r="5" fill="#B08A8F" opacity="0.18" />
      <Path d="M28 68 C54 50 74 50 93 64" stroke="#E9D7D2" strokeWidth="3" strokeLinecap="round" fill="none" />
      <Path d="M128 143 C145 132 161 135 170 148" stroke="#E9D7D2" strokeWidth="3" strokeLinecap="round" fill="none" />
      <Sticker x="145" y="18" rotate="12" scale="0.62" />
      <Sticker x="23" y="126" rotate="-14" scale="0.42" />
      <Scene />
    </Svg>
  );
}
