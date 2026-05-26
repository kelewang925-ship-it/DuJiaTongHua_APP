import FeaturePage from '../src/components/FeaturePage';

export default function LoginPage() {
  return (
    <FeaturePage
      eyebrow="账号与关联"
      title="登录 / 授权"
      subtitle="先确认身份，再打开只属于你们两个人的童话。"
      scene="cover"
      tag={{ label: '安全进入' }}
      heroTitle="欢迎回来"
      heroText="支持手机号、微信或 Apple 授权登录，后续会接入真实认证。"
      sections={[
        { icon: 'phone-portrait-outline', title: '手机号登录', text: '适合快速进入与找回账号。' },
        { icon: 'logo-wechat', title: '微信授权', text: '保留更自然的移动端登录体验。' },
        { icon: 'heart-outline', title: '绑定状态检查', text: '登录后判断是否已有情侣空间。' },
      ]}
      primaryAction="进入独家童话"
      secondaryAction="稍后再绑定"
    />
  );
}
