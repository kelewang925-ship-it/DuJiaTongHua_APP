import FeaturePage from '../../src/components/FeaturePage';

export default function VideoPreviewPage() {
  return (
    <FeaturePage
      eyebrow="AI 创作"
      title="视频预览 / 编辑"
      subtitle="在导出前确认封面、字幕、音乐和转场。"
      scene="movie"
      tag={{ label: '回忆放映机' }}
      heroTitle="预览这段回忆"
      heroText="这里会展示视频播放器和时间线编辑控件。"
      sections={[
        { icon: 'play-circle-outline', title: '视频预览', text: '查看当前生成效果。' },
        { icon: 'text-outline', title: '字幕编辑', text: '微调旁白、日期和章节标题。' },
        { icon: 'musical-notes-outline', title: '音乐与转场', text: '选择温柔的背景音乐和翻页动效。' },
      ]}
      primaryAction="保存成品"
      secondaryAction="重新生成"
    />
  );
}
