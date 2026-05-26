import FeaturePage from '../../src/components/FeaturePage';

export default function CoupleInvitePage() {
  return (
    <FeaturePage
      eyebrow="账号与关联"
      title="情侣邀请"
      subtitle="生成一张温柔的小卡片，把对方邀请进双人宇宙。"
      scene="album"
      tag={{ label: '邀请码 DFT520', tone: 'gold' }}
      heroTitle="邀请 TA 一起写童话"
      heroText="这里会展示邀请码和二维码，适合分享给另一半完成绑定。"
      sections={[
        { icon: 'qr-code-outline', title: '邀请码 / 二维码', text: '支持扫码或输入邀请码加入。' },
        { icon: 'share-social-outline', title: '分享邀请卡', text: '生成手帐风邀请图，带有有效期提示。' },
        { icon: 'time-outline', title: '等待对方确认', text: '未绑定前可以随时刷新邀请码。' },
      ]}
      primaryAction="生成邀请卡"
      secondaryAction="输入对方的邀请码"
    />
  );
}
