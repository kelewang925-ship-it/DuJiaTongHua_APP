import FeaturePage from '../src/components/FeaturePage';

export default function HelpFeedbackPage() {
  return (
    <FeaturePage
      eyebrow="特殊页面"
      title="帮助与反馈"
      subtitle="遇到问题或有新的想法，都可以在这里告诉我们。"
      scene="workshop"
      tag={{ label: '小信箱' }}
      heroTitle="把建议投进信箱"
      heroText="反馈会按账号、AI 生成、数据导出和视觉体验分类。"
      sections={[
        { icon: 'help-circle-outline', title: '常见问题', text: '绑定、备份、导出和生成相关说明。' },
        { icon: 'bug-outline', title: '问题反馈', text: '描述问题并附上发生页面。' },
        { icon: 'bulb-outline', title: '功能建议', text: '告诉我们还想收藏什么样的回忆。' },
      ]}
      primaryAction="提交反馈"
    />
  );
}
