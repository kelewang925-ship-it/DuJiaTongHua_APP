import FeaturePage from '../../src/components/FeaturePage';

export default function CoupleSettingsPage() {
  return (
    <FeaturePage
      eyebrow="账号与关联"
      title="情侣信息设置"
      subtitle="设置两个人的昵称、纪念起点和专属空间名称。"
      scene="anniversary"
      tag={{ label: '情侣资料', tone: 'gold' }}
      heroTitle="把你们的关系写进封面"
      heroText="后续会接入真实 couples 表，保存空间名称、恋爱开始日和双方展示资料。"
      sections={[
        { icon: 'people-outline', title: '双方昵称', text: '设置自己和对方在空间中的展示名称。' },
        { icon: 'calendar-outline', title: '恋爱开始日', text: '用于计算恋爱天数和生成周年提醒。' },
        { icon: 'color-palette-outline', title: '空间封面', text: '后续可选择颜色、贴纸和封面插画。' },
      ]}
      primaryAction="保存情侣信息"
      secondaryAction="稍后设置"
    />
  );
}
