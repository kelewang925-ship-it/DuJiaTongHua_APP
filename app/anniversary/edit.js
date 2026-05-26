import FeaturePage from '../../src/components/FeaturePage';

export default function AnniversaryEditPage() {
  return (
    <FeaturePage
      eyebrow="纪念日相关"
      title="纪念日添加 / 编辑"
      subtitle="把重要日子写成童话里的章节标题。"
      scene="anniversary"
      tag={{ label: '重要章节' }}
      heroTitle="新增一个章节"
      heroText="例如第一次见面、第一次旅行、第一次一起跨年。"
      sections={[
        { icon: 'create-outline', title: '章节名称', text: '用更有故事感的名字替代普通事件名。' },
        { icon: 'calendar-outline', title: '日期与重复', text: '支持一次性、每年、每月提醒。' },
        { icon: 'flower-outline', title: '模板样式', text: '选择花朵、胶带、相纸等贴纸元素。' },
      ]}
      primaryAction="保存纪念日"
    />
  );
}
