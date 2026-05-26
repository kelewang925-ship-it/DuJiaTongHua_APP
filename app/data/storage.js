import FeaturePage from '../../src/components/FeaturePage';

export default function StoragePage() {
  return (
    <FeaturePage
      eyebrow="数据管理"
      title="存储空间管理"
      subtitle="查看照片、漫画、视频和导出文件占用。"
      scene="workshop"
      tag={{ label: '3.2GB / 10GB', tone: 'gold' }}
      heroTitle="回忆还有很多位置"
      heroText="后续会显示云端空间、缓存清理和大文件管理。"
      sections={[
        { icon: 'images-outline', title: '照片与相册', text: '约 1.8GB，包含原图和缩略图。' },
        { icon: 'sparkles-outline', title: 'AI 作品', text: '约 980MB，包含漫画和视频草稿。' },
        { icon: 'document-text-outline', title: '导出文件', text: '约 420MB，可清理旧版本。' },
      ]}
      primaryAction="清理缓存"
      secondaryAction="升级童话会员"
    />
  );
}
