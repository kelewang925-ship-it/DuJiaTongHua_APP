import AuthGate from '../../components/AuthGate';
import CoupleTimeline from '../../components/CoupleTimeline';
import FairyBackButton from '../../components/FairyBackButton';
import FairyBackgroundContainer from '../../components/FairyBackgroundContainer';
import FairyButton from '../../components/FairyButton';
import FairyCard from '../../components/FairyCard';
import FairyDialog from '../../components/FairyDialog';
import FairyEmptyState from '../../components/FairyEmptyState';
import FairyHeader from '../../components/FairyHeader';
import FairyHeroImage from '../../components/FairyHeroImage';
import FairyIllustration from '../../components/FairyIllustration';
import FairyImage from '../../components/FairyImage';
import FairyInput from '../../components/FairyInput';
import { FairyMessageProvider } from '../../components/FairyMessage';
import FairyPage from '../../components/FairyPage';
import FairyRichTextEditor from '../../components/FairyRichTextEditor';
import FairyRichTextViewer from '../../components/FairyRichTextViewer';
import FairySticker from '../../components/FairySticker';
import FairySvgIcon from '../../components/FairySvgIcon';
import FairyTabBar from '../../components/FairyTabBar';
import FairyTag from '../../components/FairyTag';
import FairyToast from '../../components/FairyToast';
import FeaturePage from '../../components/FeaturePage';
import MemoryCard from '../../components/MemoryCard';
import MemoryWall from '../../components/MemoryWall';
import RoundedDashedBorder from '../../components/RoundedDashedBorder';
import WorkshopCard from '../../components/WorkshopCard';

const sampleRecords = [
  {
    id: 'memory_001',
    type: 'diary',
    title: 'Evening walk',
    content: '<p>The wind was soft, and an ordinary day became worth keeping.</p>',
    date: 'Today 20:18',
    likes: 12,
    icon: 'book-outline',
  },
  {
    id: 'memory_002',
    type: 'photo',
    title: 'Cream cake',
    content: 'A tiny sweet chapter.',
    date: 'Yesterday',
    likes: 8,
    photoCount: 3,
  },
  {
    id: 'memory_003',
    type: 'comic',
    title: 'Storybook comic',
    content: 'AI turned this memory into a hand-drawn page.',
    date: 'May 23',
    likes: 18,
  },
];

const sampleTimelineItems = [
  {
    id: 'timeline_001',
    tag: 'Diary',
    title: 'First shared note',
    time: 'Today 21:04',
    description: 'A small sentence became a new chapter.',
    icon: 'book-outline',
  },
  {
    id: 'timeline_002',
    tag: 'Photo',
    title: 'New album moment',
    time: 'Yesterday 18:30',
    description: 'Six photos were added to the shared album.',
    icon: 'images-outline',
  },
];

const tabState = {
  index: 0,
  routes: [
    { key: 'index', name: 'index' },
    { key: 'couple', name: 'couple' },
    { key: 'workshop', name: 'workshop' },
    { key: 'mine', name: 'mine' },
  ],
};

const tabDescriptors = {
  index: { options: { title: 'Home' } },
  couple: { options: { title: 'Couple' } },
  workshop: { options: { title: 'Workshop' } },
  mine: { options: { title: 'Mine' } },
};

export const devComponents = [
  {
    name: 'AuthGate',
    description: '登录状态守卫组件。用于在会话校验期间展示加载状态，并在未登录时引导用户进入登录页。',
    component: AuthGate,
    props: {
      children: 'Authenticated content preview',
    },
  },
  {
    name: 'CoupleTimeline',
    description: '情侣动态时间线组件。按时间顺序展示日记、照片和共同创作等双人记录。',
    component: CoupleTimeline,
    props: {
      items: sampleTimelineItems,
    },
  },
  {
    name: 'FairyBackButton',
    description: '统一样式的返回按钮。用于页面头部或浮层中触发返回操作。',
    component: FairyBackButton,
    props: {
      name: 'rollback1',
      width: 42,
      height: 42,
    },
  },
  {
    name: 'FairyBackgroundContainer',
    description: '带童话主题背景的内容容器。用于为局部区域组合背景图、尺寸和自定义样式。',
    component: FairyBackgroundContainer,
    props: {
      children: 'Background container',
      style: {
        height: 140,
        borderRadius: 24,
        backgroundColor: '#FFF0F2',
      },
    },
  },
  {
    name: 'FairyButton',
    description: '项目通用操作按钮。支持不同视觉层级，用于提交、确认或跳转等操作。',
    component: FairyButton,
    props: {
      title: 'Save story',
      variant: 'primary',
    },
  },
  {
    name: 'FairyCard',
    description: '项目通用卡片容器。用于承载信息、操作或自定义内容，并保持统一的圆角和纸张质感。',
    component: FairyCard,
    props: {
      children: 'A soft paper card for isolated preview.',
    },
  },
  {
    name: 'FairyDialog',
    description: '通用确认弹窗。用于需要用户确认或取消的操作，可配置标题、说明、图标和按钮文案。',
    component: FairyDialog,
    props: {
      visible: true,
      title: 'Confirm action',
      description: 'Dialog preview in the component lab.',
      icon: 'heart-outline',
      confirmText: 'Confirm',
      cancelText: 'Cancel',
    },
  },
  {
    name: 'FairyEmptyState',
    description: '空状态提示组件。用于列表或页面暂无内容时展示说明，并可提供后续操作入口。',
    component: FairyEmptyState,
    props: {
      title: 'No records yet',
      description: 'Switch props to inspect compact and illustrated states.',
      compact: true,
      icon: 'sparkles-outline',
      actionTitle: 'Create one',
    },
  },
  {
    name: 'FairyHeader',
    description: '项目通用页面头部。用于展示标题、返回入口以及右侧的辅助操作。',
    component: FairyHeader,
    props: {
      title: 'Story page',
      showBack: true,
      right: 'Edit',
    },
  },
  {
    name: 'FairyHeroImage',
    description: '页面主视觉图片组件。用于展示主题图片，并可控制高度和图片说明。',
    component: FairyHeroImage,
    props: {
      imageKey: 'homeHero',
      height: 160,
      showCaption: true,
    },
  },
  {
    name: 'FairyIllustration',
    description: '童话场景插画组件。根据场景名称展示对应插画，用于页面引导和氛围营造。',
    component: FairyIllustration,
    props: {
      scene: 'workshop',
      height: 170,
    },
  },
  {
    name: 'FairyImage',
    description: '项目图片资源组件。通过资源名称加载预设图片，并统一处理尺寸和圆角。',
    component: FairyImage,
    props: {
      name: 'homeCover',
      height: 170,
      radius: 24,
    },
  },
  {
    name: 'FairyInput',
    description: '项目通用输入框。支持标签、图标、占位提示和辅助文案等表单能力。',
    component: FairyInput,
    props: {
      label: 'Email',
      icon: 'mail-outline',
      placeholder: 'name@example.com',
      helper: 'Helper text preview',
      value: 'story@example.com',
    },
  },
  {
    name: 'FairyMessageProvider',
    description: '全局消息上下文容器。为子组件提供统一的轻提示消息调用能力。',
    component: FairyMessageProvider,
    props: {
      children: 'Message provider host',
    },
  },
  {
    name: 'FairyPage',
    description: '项目通用页面外壳。统一处理主题背景、滚动区域和页面上下留白。',
    component: FairyPage,
    props: {
      children: 'Page shell content',
      backgroundName: 'creamPaper',
      topSpace: 24,
      bottomSpace: 24,
    },
  },
  {
    name: 'FairyRichTextEditor',
    description: '富文本编辑器。用于编辑带格式的长文本内容，并支持高度和字数上限配置。',
    component: FairyRichTextEditor,
    props: {
      value: '<p>A short rich-text story.</p>',
      height: 260,
      maxLength: 500,
    },
  },
  {
    name: 'FairyRichTextViewer',
    description: '富文本只读展示组件。用于渲染 HTML 内容，并在无法渲染时展示纯文本备选内容。',
    component: FairyRichTextViewer,
    props: {
      html: '<p><strong>Story note</strong></p><p>A warm preview paragraph.</p>',
      fallback: 'Fallback plain text',
    },
  },
  {
    name: 'FairySticker',
    description: '装饰贴纸组件。用于添加爱心等童话风格装饰，可调整尺寸和旋转角度。',
    component: FairySticker,
    props: {
      name: 'heart',
      size: 56,
      rotate: '-8deg',
    },
  },
  {
    name: 'FairySvgIcon',
    description: '项目自定义 SVG 图标组件。通过图标名称统一控制尺寸、颜色和描边。',
    component: FairySvgIcon,
    props: {
      name: 'fourPointStar',
      size: 54,
      color: '#E8A044',
      strokeWidth: 1.4,
    },
  },
  {
    name: 'FairyTabBar',
    description: '应用底部标签栏。根据导航状态展示主要页面入口并处理标签切换。',
    component: FairyTabBar,
    props: {
      state: tabState,
      descriptors: tabDescriptors,
      navigation: {
        emit: () => ({ defaultPrevented: true }),
        navigate: () => {},
      },
    },
  },
  {
    name: 'FairyTag',
    description: '轻量标签组件。用于标记内容类型或状态，并支持不同主题色调。',
    component: FairyTag,
    props: {
      children: 'Diary',
      tone: 'gold',
    },
  },
  {
    name: 'FairyToast',
    description: '短时反馈提示组件。用于向用户反馈成功、失败或普通状态消息。',
    component: FairyToast,
    props: {
      visible: true,
      message: 'Saved to the storybook',
      tone: 'success',
      duration: 100000,
    },
  },
  {
    name: 'FeaturePage',
    description: '功能介绍页模板。组合主视觉、功能分区和操作按钮，快速搭建统一风格的功能页面。',
    component: FeaturePage,
    props: {
      title: 'Feature preview',
      subtitle: 'Reusable page composition',
      eyebrow: 'LAB',
      scene: 'cover',
      tag: { label: 'Beta', tone: 'gold' },
      heroText: 'A full-page component preview.',
      sections: [
        { title: 'Section one', text: 'Compact section copy.', icon: 'sparkles-outline', badge: 'New' },
      ],
      primaryAction: 'Start',
      secondaryAction: 'Later',
    },
  },
  {
    name: 'MemoryCard',
    description: '回忆内容卡片。用于展示日记、照片或漫画等记录的标题、摘要、时间和互动信息。',
    component: MemoryCard,
    props: {
      type: 'diary',
      title: 'Evening walk',
      content: '<p>The wind was soft, and the street lights felt gentle.</p>',
      date: 'Today 20:18',
      icon: 'book-outline',
      artwork: 'cover',
      likes: 12,
    },
  },
  {
    name: 'MemoryWall',
    description: '回忆墙列表组件。将多条回忆记录组织为统一的内容流进行展示。',
    component: MemoryWall,
    props: {
      records: sampleRecords,
    },
  },
  {
    name: 'RoundedDashedBorder',
    description: '圆角虚线边框容器。用于突出可上传、可添加或需要视觉分隔的内容区域。',
    component: RoundedDashedBorder,
    props: {
      children: 'Dashed border content',
      radius: 20,
      strokeColor: '#D9A6A0',
      strokeWidth: 2,
      dashArray: '8 6',
      style: {
        minHeight: 120,
        padding: 20,
        justifyContent: 'center',
        alignItems: 'center',
      },
    },
  },
  {
    name: 'WorkshopCard',
    description: '创作工坊功能卡片。用于展示 AI 创作入口及其图标、标题和简要说明。',
    component: WorkshopCard,
    props: {
      icon: 'color-wand-outline',
      title: 'Photo to comic',
      description: 'Live preview inside the component lab.',
    },
  },
];
