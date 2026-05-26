import FeaturePage from '../../src/components/FeaturePage';

export default function BindConfirmPage() {
  return (
    <FeaturePage
      eyebrow="账号与关联"
      title="绑定确认"
      subtitle="确认后，你们的日记、照片和作品会进入同一个私密空间。"
      scene="cover"
      tag={{ label: '双人宇宙' }}
      heroTitle="我们在一起啦"
      heroText="这里会展示双方头像、昵称和恋爱开始日期。"
      sections={[
        { icon: 'people-outline', title: '双方身份', text: '核对邀请人与加入人信息。' },
        { icon: 'calendar-outline', title: '恋爱起始日', text: '用于计算恋爱天数和纪念章节。' },
        { icon: 'lock-closed-outline', title: '私密空间', text: '绑定后默认仅双方可见。' },
      ]}
      primaryAction="确认绑定"
      secondaryAction="返回修改"
    />
  );
}
