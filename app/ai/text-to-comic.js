import FeaturePage from '../../src/components/FeaturePage';

export default function TextToComicPage() {
  return (
    <FeaturePage
      eyebrow="AI 创作"
      title="文本转漫画"
      subtitle="输入一段故事，让它变成温柔的绘本分镜。"
      scene="workshop"
      tag={{ label: '文字魔法' }}
      heroTitle="把回忆变成童话"
      heroText="适合把日记、聊天摘录或自由文字生成漫画。"
      sections={[
        { icon: 'document-text-outline', title: '故事文本', text: '填写场景、人物和想保留的细节。' },
        { icon: 'color-palette-outline', title: '漫画风格', text: '童话绘本、暖色漫画、手帐贴纸。' },
        { icon: 'people-outline', title: '角色人设', text: '选择双方稳定人设，减少角色漂移。' },
      ]}
      primaryAction="生成童话漫画"
    />
  );
}
