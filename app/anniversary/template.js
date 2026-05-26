import FeaturePage from '../../src/components/FeaturePage';

export default function AnniversaryTemplatePage() {
  return (
    <FeaturePage
      eyebrow="纪念日相关"
      title="专属记录模板"
      subtitle="为特别的日子提前准备一页漂亮的绘本版式。"
      scene="album"
      tag={{ label: '模板' }}
      heroTitle="这一天要好好收藏"
      heroText="模板会引导填写照片、日记、地点和一句纪念文案。"
      sections={[
        { icon: 'image-outline', title: '照片区域', text: '预留多张照片的拼贴布局。' },
        { icon: 'book-outline', title: '日记区域', text: '引导写下当天最想记住的一幕。' },
        { icon: 'sparkles-outline', title: 'AI 创作入口', text: '一键生成纪念漫画或短视频。' },
      ]}
      primaryAction="使用这个模板"
    />
  );
}
