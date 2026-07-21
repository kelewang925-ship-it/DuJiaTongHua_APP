import FairyButton from '@/components/FairyButton';

export default function DiaryBindButton({ loading, onPress }) {
  return (
    <FairyButton
      title={loading ? '📖 小精灵正在装订...' : '🌟 装订进故事书'}
      disabled={loading}
      onPress={onPress}
    />
  );
}
