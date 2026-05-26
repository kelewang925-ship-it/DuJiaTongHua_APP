import FeaturePage from '../../src/components/FeaturePage';

export default function ExportPreviewPage() {
  return (
    <FeaturePage
      eyebrow="数据管理"
      title="导出预览"
      subtitle="在生成 PDF 前，先翻看这本回忆册的封面和章节。"
      scene="album"
      tag={{ label: '预览' }}
      heroTitle="我们的恋爱回忆册"
      heroText="封面、目录、日记、照片和 AI 作品都会按绘本章节排版。"
      sections={[
        { icon: 'book-outline', title: '封面预览', text: '奶油纸感封面与情侣插画。' },
        { icon: 'list-outline', title: '章节目录', text: '按时间和纪念日分组。' },
        { icon: 'download-outline', title: '导出文件', text: '确认后生成 PDF 并保存到导出记录。' },
      ]}
      primaryAction="确认导出"
      secondaryAction="返回修改配置"
    />
  );
}
