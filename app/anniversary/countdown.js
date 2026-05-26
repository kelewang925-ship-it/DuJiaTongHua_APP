import FeaturePage from '../../src/components/FeaturePage';

export default function AnniversaryCountdownPage() {
  return (
    <FeaturePage
      eyebrow="纪念日相关"
      title="纪念日倒计时"
      subtitle="把等待也变成有仪式感的一页。"
      scene="anniversary"
      tag={{ label: '还有 24 天', tone: 'gold' }}
      heroTitle="第一次旅行"
      heroText="到那一天时，系统会自动生成专属记录入口。"
      sections={[
        { icon: 'hourglass-outline', title: '倒计时', text: '显示剩余天数和纪念日说明。' },
        { icon: 'notifications-outline', title: '提醒设置', text: '提前 7 天、1 天和当天提醒。' },
        { icon: 'gift-outline', title: '准备清单', text: '可以放礼物、地点和小愿望。' },
      ]}
      primaryAction="准备记录模板"
    />
  );
}
