import FeaturePage from '../../src/components/FeaturePage';

export default function CoupleStoryDetailPage() {
  return (
    <FeaturePage
      eyebrow="互动相关"
      title="情侣动态详情"
      subtitle="查看一条动态背后的照片、日记和互动。"
      scene="cover"
      tag={{ label: '双人动态' }}
      heroTitle="第 428 天的小故事"
      heroText="把动态当作故事章节，而不是普通社交发布。"
      sections={[
        { icon: 'book-outline', title: '关联记录', text: '日记、照片和 AI 作品可以组成一条动态。' },
        { icon: 'heart-outline', title: '点赞', text: '只在两个人之间表达喜欢。' },
        { icon: 'chatbubble-ellipses-outline', title: '评论', text: '留下悄悄话和当天的补充记忆。' },
      ]}
      primaryAction="写一句回应"
    />
  );
}
