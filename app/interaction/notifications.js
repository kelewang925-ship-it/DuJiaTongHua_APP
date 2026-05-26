import FeaturePage from '../../src/components/FeaturePage';

export default function NotificationsPage() {
  return (
    <FeaturePage
      eyebrow="互动相关"
      title="互动通知"
      subtitle="点赞、评论、纪念日和生成完成提醒都在这里。"
      scene="workshop"
      tag={{ label: '消息盒子' }}
      heroTitle="新的回忆提醒"
      heroText="通知会保持克制，像贴在纸页边缘的小便签。"
      sections={[
        { icon: 'heart-outline', title: 'TA 喜欢了你的日记', text: '一起散步的傍晚。' },
        { icon: 'sparkles-outline', title: '漫画生成完成', text: '第一次约会的小漫画已放进工坊。' },
        { icon: 'calendar-outline', title: '纪念日提醒', text: '第一次旅行还有 24 天。' },
      ]}
      primaryAction="全部标记已读"
    />
  );
}
