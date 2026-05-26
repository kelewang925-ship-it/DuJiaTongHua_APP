import FeaturePage from '../../src/components/FeaturePage';

export default function TagManagementPage() {
  return (
    <FeaturePage
      eyebrow="记录中心"
      title="标签管理"
      subtitle="整理日记、照片和 AI 作品中的高频主题。"
      scene="cover"
      tag={{ label: '回忆索引', tone: 'pink' }}
      heroTitle="给每段回忆贴上小标签"
      heroText="后续会支持新增、合并、重命名标签，并用于搜索和 PDF 导出筛选。"
      sections={[
        { icon: 'pricetags-outline', title: '常用标签', text: '例如约会、旅行、吵架和好、生日、第一次。' },
        { icon: 'git-merge-outline', title: '标签合并', text: '把相似标签合并，避免回忆分类越来越乱。' },
        { icon: 'search-outline', title: '标签检索', text: '从标签快速找到对应日记、照片和作品。' },
      ]}
      primaryAction="新增标签"
      secondaryAction="整理重复标签"
    />
  );
}
