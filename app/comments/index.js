import FeaturePage from '../../src/components/FeaturePage';

export default function CommentsPage() {
  return (
    <FeaturePage
      eyebrow="情侣互动"
      title="评论列表"
      subtitle="两个人围绕某一段回忆留下的小回应。"
      scene="cover"
      tag={{ label: '互动', tone: 'pink' }}
      heroTitle="把话说在这一页"
      heroText="后续会接入 comments 表，按 target_type 和 target_id 读取评论。"
      sections={[
        { icon: 'chatbubble-outline', title: '评论流', text: '展示双方对日记、照片或 AI 作品的回复。' },
        { icon: 'send-outline', title: '快速回复', text: '支持表情、短句和温柔贴纸式回复。' },
        { icon: 'notifications-outline', title: '互动提醒', text: '对方回复后生成通知。' },
      ]}
      primaryAction="写一条评论"
      secondaryAction="返回动态"
    />
  );
}
