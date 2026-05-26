import FeaturePage from '../src/components/FeaturePage';

export default function SearchPage() {
  return (
    <FeaturePage
      eyebrow="特殊页面"
      title="记录搜索"
      subtitle="按关键词、标签、时间和类型找回某段回忆。"
      scene="album"
      tag={{ label: '回忆索引' }}
      heroTitle="寻找那一页"
      heroText="搜索结果会混合展示日记、照片、纪念日和 AI 作品。"
      sections={[
        { icon: 'search-outline', title: '关键词搜索', text: '输入地点、事件或一句话。' },
        { icon: 'pricetag-outline', title: '标签筛选', text: '按约会、旅行、开心、想念筛选。' },
        { icon: 'calendar-outline', title: '时间范围', text: '按月份或纪念日前后查找。' },
      ]}
      primaryAction="开始搜索"
    />
  );
}
