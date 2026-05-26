import FeaturePage from '../src/components/FeaturePage';

export default function MembershipPage() {
  return (
    <FeaturePage
      eyebrow="特殊页面"
      title="童话会员"
      subtitle="不是 VIP，而是为回忆提供更长久的收藏空间。"
      scene="anniversary"
      tag={{ label: '琥珀金', tone: 'gold' }}
      heroTitle="让童话保存得更久"
      heroText="会员权益围绕存储、导出、AI 创作额度和高级模板。"
      sections={[
        { icon: 'cloud-outline', title: '更大云空间', text: '保存更多照片、漫画和视频。' },
        { icon: 'sparkles-outline', title: 'AI 创作额度', text: '更多漫画页和回忆短视频。' },
        { icon: 'book-outline', title: '高级导出模板', text: '纸雕感封面、金箔纹理和章节页。' },
      ]}
      primaryAction="开通童话会员"
    />
  );
}
