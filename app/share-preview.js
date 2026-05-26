import FeaturePage from '../src/components/FeaturePage';

export default function SharePreviewPage() {
  return (
    <FeaturePage
      eyebrow="特殊页面"
      title="分享预览"
      subtitle="生成一张克制、温柔、不泄露隐私的分享卡。"
      scene="cover"
      tag={{ label: '分享卡' }}
      heroTitle="我们的一页童话"
      heroText="默认只展示封面、日期和一句文案，不暴露完整内容。"
      sections={[
        { icon: 'image-outline', title: '封面图', text: '使用绘本插画或照片拼贴。' },
        { icon: 'text-outline', title: '分享文案', text: '每段回忆，都值得被收藏。' },
        { icon: 'lock-closed-outline', title: '隐私控制', text: '可隐藏昵称、日期和具体地点。' },
      ]}
      primaryAction="生成分享图"
    />
  );
}
