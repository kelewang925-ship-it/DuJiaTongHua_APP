import FairyButton from '../../components/FairyButton';
import FairyCard from '../../components/FairyCard';
import FairyEmptyState from '../../components/FairyEmptyState';
import WorkshopCard from '../../components/WorkshopCard';

export const devComponents = [
  {
    name: 'FairyButton',
    component: FairyButton,
    props: {
      title: '保存这段童话',
      variant: 'primary',
    },
  },
  {
    name: 'FairyCard',
    component: FairyCard,
    props: {
      children: '这是一张用于调试的奶油纸卡片。',
    },
  },
  {
    name: 'FairyEmptyState',
    component: FairyEmptyState,
    props: {
      title: '还没有记录',
      description: '切换 props 后可以实时查看空状态样式。',
      compact: true,
      icon: 'sparkles-outline',
    },
  },
  {
    name: 'WorkshopCard',
    component: WorkshopCard,
    props: {
      icon: 'color-wand-outline',
      title: '照片变漫画',
      description: '组件实验室里的实时预览。',
    },
  },
];
