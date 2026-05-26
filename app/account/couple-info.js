import FeaturePage from '../../src/components/FeaturePage';

export default function CoupleInfoPage() {
  return (
    <FeaturePage
      eyebrow="账号与关联"
      title="情侣信息设置"
      subtitle="设置昵称、头像和恋爱起始日，让故事从第一页开始。"
      scene="anniversary"
      tag={{ label: '初始资料' }}
      heroTitle="写下你们的第一页"
      heroText="后续会接入头像选择、日期选择和关系状态设置。"
      sections={[
        { icon: 'person-circle-outline', title: '双方昵称与头像', text: '用于情侣空间、动态流和导出封面。' },
        { icon: 'heart-outline', title: '恋爱开始日期', text: '自动生成恋爱天数计数器。' },
        { icon: 'color-palette-outline', title: '专属主题', text: '可选择封面贴纸和空间名称。' },
      ]}
      primaryAction="保存并进入"
    />
  );
}
