import FeaturePage from '../../src/components/FeaturePage';

export default function AiCreationHistoryPage() {
  return (
    <FeaturePage
      eyebrow="AI 童话工坊"
      title="创作历史"
      subtitle="集中查看已经生成或正在生成的漫画、视频和纪念册。"
      scene="workshop"
      tag={{ label: '作品库', tone: 'gold' }}
      heroTitle="你们的童话作品都在这里"
      heroText="后续会接入 ai_jobs 和导出记录，支持按类型、状态和时间筛选。"
      sections={[
        { icon: 'albums-outline', title: '作品列表', text: '展示漫画、视频、PDF 等生成结果。' },
        { icon: 'hourglass-outline', title: '生成状态', text: '区分生成中、已完成、失败和草稿。' },
        { icon: 'share-social-outline', title: '分享与保存', text: '支持保存到相册、加入纪念册或分享预览。' },
      ]}
      primaryAction="查看最新作品"
      secondaryAction="筛选作品"
    />
  );
}
