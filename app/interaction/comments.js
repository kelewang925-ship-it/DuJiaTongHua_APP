import FeaturePage from '../../src/components/FeaturePage';

export default function CommentsPage() {
  return (
    <FeaturePage
      eyebrow="互动相关"
      title="评论列表"
      subtitle="所有温柔回应，都收在这一页。"
      scene="album"
      tag={{ label: '悄悄话' }}
      heroTitle="这一天也被回应了"
      heroText="评论只属于情侣空间，不做公开社交扩散。"
      sections={[
        { icon: 'person-circle-outline', title: '林小满', text: '今天的晚风真的很好闻。' },
        { icon: 'heart-circle-outline', title: '陆星河', text: '下次还走这条路。' },
        { icon: 'add-circle-outline', title: '添加评论', text: '用一句短短的话接住这段回忆。' },
      ]}
      primaryAction="发送评论"
    />
  );
}
