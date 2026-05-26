import FeaturePage from '../../src/components/FeaturePage';

export default function TimeCapsulePage() {
  return (
    <FeaturePage
      eyebrow="记录相关"
      title="时光胶囊"
      subtitle="把想对未来说的话，藏进某一天再打开。"
      scene="anniversary"
      tag={{ label: '未来开启', tone: 'gold' }}
      heroTitle="写给未来的我们"
      heroText="可以选择开启日期、收件人和关联照片。"
      sections={[
        { icon: 'lock-closed-outline', title: '封存内容', text: '文字、照片和语音后续都可进入胶囊。' },
        { icon: 'calendar-outline', title: '开启日期', text: '到达指定纪念日后提醒双方查看。' },
        { icon: 'notifications-outline', title: '温柔提醒', text: '用通知提示胶囊已经可以打开。' },
      ]}
      primaryAction="创建时光胶囊"
    />
  );
}
