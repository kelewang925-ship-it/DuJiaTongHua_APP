import FeaturePage from '../../src/components/FeaturePage';

export default function CoupleActivityDetailPage() {
  return (
    <FeaturePage
      eyebrow="情侣空间"
      title="情侣动态详情"
      subtitle="查看某一条双人动态背后的日记、照片、评论和互动。"
      scene="anniversary"
      tag={{ label: '故事节点', tone: 'gold' }}
      heroTitle="这一章发生了什么"
      heroText="后续会根据 target_type 和 target_id 读取日记、照片或 AI 作品详情。"
      sections={[
        { icon: 'document-text-outline', title: '动态内容', text: '展示关联日记、照片、纪念日或 AI 作品。' },
        { icon: 'chatbubble-ellipses-outline', title: '互动评论', text: '承载两个人对这一条回忆的回复。' },
        { icon: 'heart-outline', title: '收藏动作', text: '后续可以标记重要章节，导出 PDF 时优先收录。' },
      ]}
      primaryAction="查看评论"
      secondaryAction="加入纪念册"
    />
  );
}
