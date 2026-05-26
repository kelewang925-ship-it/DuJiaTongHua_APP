import FeaturePage from '../../src/components/FeaturePage';

export default function NotificationsPage() {
  return (
    <FeaturePage
      eyebrow="情侣互动"
      title="互动通知"
      subtitle="集中展示评论、纪念日、AI 完成和系统提醒。"
      scene="workshop"
      tag={{ label: '提醒中心', tone: 'gold' }}
      heroTitle="别错过对方的小回应"
      heroText="后续会接入 notifications 表，按当前 user_id 读取和标记已读。"
      sections={[
        { icon: 'heart-outline', title: '情侣互动', text: '对方评论、收藏或回应你的记录。' },
        { icon: 'calendar-outline', title: '纪念日提醒', text: '重要日期前自动提醒。' },
        { icon: 'sparkles-outline', title: 'AI 完成通知', text: '漫画、视频、PDF 导出完成后提醒。' },
      ]}
      primaryAction="全部标记已读"
      secondaryAction="通知设置"
    />
  );
}
