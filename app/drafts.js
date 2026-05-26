import FeaturePage from '../src/components/FeaturePage';

export default function DraftsPage() {
  return (
    <FeaturePage
      eyebrow="特殊页面"
      title="草稿箱"
      subtitle="没写完的日记、未完成的漫画配置，都先放在这里。"
      scene="album"
      tag={{ label: '3 个草稿' }}
      heroTitle="未完成也值得被保存"
      heroText="草稿会按最近编辑时间排序，方便继续书写。"
      sections={[
        { icon: 'create-outline', title: '日记草稿', text: '今天的小小童话。', badge: '刚刚' },
        { icon: 'color-palette-outline', title: '漫画草稿', text: '第一次旅行预设。', badge: '昨天' },
        { icon: 'videocam-outline', title: '视频草稿', text: '春天散步纪念视频。', badge: '5月23日' },
      ]}
      primaryAction="继续最近草稿"
    />
  );
}
