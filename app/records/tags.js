import FeaturePage from '../../src/components/FeaturePage';

export default function TagsPage() {
  return (
    <FeaturePage
      eyebrow="记录相关"
      title="标签管理"
      subtitle="整理心情、地点和回忆类型，让故事更容易被找回。"
      scene="album"
      tag={{ label: '手帐索引' }}
      heroTitle="给回忆贴上小标签"
      heroText="标签会用于日记、照片、漫画和搜索筛选。"
      sections={[
        { icon: 'pricetag-outline', title: '心情标签', text: '开心、想念、被爱着、甜甜的。' },
        { icon: 'location-outline', title: '地点标签', text: '咖啡店、公园、海边、旅行。' },
        { icon: 'albums-outline', title: '回忆类型', text: '日记、照片、纪念日、AI 作品。' },
      ]}
      primaryAction="新建标签"
      secondaryAction="整理已有标签"
    />
  );
}
