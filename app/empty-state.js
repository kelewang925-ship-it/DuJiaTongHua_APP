import FeaturePage from '../src/components/FeaturePage';

export default function EmptyStatePage() {
  return (
    <FeaturePage
      eyebrow="通用状态"
      title="空状态页"
      subtitle="当用户还没有日记、照片、评论或 AI 作品时，用温柔提示引导下一步。"
      scene="cover"
      tag={{ label: '组件规范', tone: 'pink' }}
      heroTitle="这一页还在等故事发生"
      heroText="空状态不应该冷冰冰地告诉用户没有数据，而应该给出一个轻松明确的行动入口。"
      sections={[
        { icon: 'document-text-outline', title: '无日记', text: '提示用户写下今天的小小童话。' },
        { icon: 'images-outline', title: '无照片', text: '引导用户上传第一张照片。' },
        { icon: 'sparkles-outline', title: '无 AI 作品', text: '推荐从最近一篇日记生成漫画。' },
      ]}
      primaryAction="查看空状态组件"
      secondaryAction="返回上一页"
    />
  );
}
