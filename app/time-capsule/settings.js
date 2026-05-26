import FeaturePage from '../../src/components/FeaturePage';

export default function TimeCapsuleSettingsPage() {
  return (
    <FeaturePage
      eyebrow="记录中心"
      title="时光胶囊设置"
      subtitle="把某段话、照片或愿望封存到未来某一天再打开。"
      scene="album"
      tag={{ label: '未来章节', tone: 'pink' }}
      heroTitle="给未来的你们写一封信"
      heroText="当前先作为页面骨架，后续会接入定时提醒、锁定内容和解锁动画。"
      sections={[
        { icon: 'time-outline', title: '开启时间', text: '选择未来某一天，让系统到时提醒两个人。' },
        { icon: 'lock-closed-outline', title: '封存内容', text: '封存前可以写文字、选择照片或关联一篇日记。' },
        { icon: 'gift-outline', title: '打开仪式', text: '用童话动画展示被打开的回忆。' },
      ]}
      primaryAction="创建时光胶囊"
      secondaryAction="查看已有胶囊"
    />
  );
}
