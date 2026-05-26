import FeaturePage from '../../src/components/FeaturePage';

export default function PhotoToComicPage() {
  return (
    <FeaturePage
      eyebrow="AI 创作"
      title="照片转漫画"
      subtitle="选择照片，把真实瞬间画成一页恋爱漫画。"
      scene="album"
      tag={{ label: '照片魔法', tone: 'gold' }}
      heroTitle="让照片变成绘本"
      heroText="适合约会、旅行、纪念日晚餐等有画面感的回忆。"
      sections={[
        { icon: 'images-outline', title: '选择照片', text: '支持单图或多图生成连续分镜。' },
        { icon: 'sparkles-outline', title: '绘本化处理', text: '保留情绪和场景，弱化工具感。' },
        { icon: 'albums-outline', title: '生成结果', text: '作品会进入童话工坊创作历史。' },
      ]}
      primaryAction="选择照片生成"
    />
  );
}
