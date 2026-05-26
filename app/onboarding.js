import FeaturePage from '../src/components/FeaturePage';

export default function OnboardingPage() {
  return (
    <FeaturePage
      eyebrow="首次使用"
      title="欢迎来到独家童话"
      subtitle="这里不是打卡工具，而是一本慢慢写满的恋爱绘本。"
      scene="cover"
      tag={{ label: '第一章' }}
      heroTitle="把每一天写成童话"
      heroText="记录日记、照片、纪念日，再用 AI 把回忆变成漫画和放映机。"
      sections={[
        { icon: 'book-outline', title: '记录中心', text: '从首页开始写下今天。' },
        { icon: 'heart-outline', title: '情侣空间', text: '把两个人的动态排成故事时间线。' },
        { icon: 'sparkles-outline', title: '童话工坊', text: '用魔法感承载 AI 创作。' },
      ]}
      primaryAction="开始书写"
    />
  );
}
