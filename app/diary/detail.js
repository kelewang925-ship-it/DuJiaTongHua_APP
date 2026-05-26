import FeaturePage from '../../src/components/FeaturePage';

export default function DiaryDetailPage() {
  return (
    <FeaturePage
      eyebrow="记录详情"
      title="一起散步的傍晚"
      subtitle="一页已经写好的恋爱绘本。"
      scene="memory"
      tag={{ label: '日记' }}
      heroTitle="晚风很轻"
      heroText="普通的一天，也因为两个人一起走过而变得值得收藏。"
      sections={[
        { icon: 'heart-outline', title: '心情', text: '被爱着 · 日常 · 开心' },
        { icon: 'image-outline', title: '关联照片', text: '可在这里查看这篇日记绑定的照片。' },
        { icon: 'sparkles-outline', title: '创作入口', text: '把这篇日记生成漫画或回忆短片。' },
      ]}
      primaryAction="把这篇变成漫画"
      secondaryAction="编辑这一页"
    />
  );
}
