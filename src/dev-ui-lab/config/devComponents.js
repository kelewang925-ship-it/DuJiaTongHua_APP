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
    component: AuthGate,
    props: {
      children: 'Authenticated content preview',
    },
  },
  {
    name: 'CoupleTimeline',
    component: CoupleTimeline,
    props: {
      items: sampleTimelineItems,
    },
  },
  {
    name: 'FairyBackButton',
    component: FairyBackButton,
    props: {
      name: 'rollback1',
      width: 42,
      height: 42,
    },
  },
  {
    name: 'FairyBackgroundContainer',
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
    component: FairyButton,
    props: {
      title: 'Save story',
      variant: 'primary',
    },
  },
  {
    name: 'FairyCard',
    component: FairyCard,
    props: {
      children: 'A soft paper card for isolated preview.',
    },
  },
  {
    name: 'FairyDialog',
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
    component: FairyHeader,
    props: {
      title: 'Story page',
      showBack: true,
      right: 'Edit',
    },
  },
  {
    name: 'FairyHeroImage',
    component: FairyHeroImage,
    props: {
      imageKey: 'homeHero',
      height: 160,
      showCaption: true,
    },
  },
  {
    name: 'FairyIllustration',
    component: FairyIllustration,
    props: {
      scene: 'workshop',
      height: 170,
    },
  },
  {
    name: 'FairyImage',
    component: FairyImage,
    props: {
      name: 'homeCover',
      height: 170,
      radius: 24,
    },
  },
  {
    name: 'FairyInput',
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
    component: FairyMessageProvider,
    props: {
      children: 'Message provider host',
    },
  },
  {
    name: 'FairyPage',
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
    component: FairyRichTextEditor,
    props: {
      value: '<p>A short rich-text story.</p>',
      height: 260,
      maxLength: 500,
    },
  },
  {
    name: 'FairyRichTextViewer',
    component: FairyRichTextViewer,
    props: {
      html: '<p><strong>Story note</strong></p><p>A warm preview paragraph.</p>',
      fallback: 'Fallback plain text',
    },
  },
  {
    name: 'FairySticker',
    component: FairySticker,
    props: {
      name: 'heart',
      size: 56,
      rotate: '-8deg',
    },
  },
  {
    name: 'FairySvgIcon',
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
    component: FairyTag,
    props: {
      children: 'Diary',
      tone: 'gold',
    },
  },
  {
    name: 'FairyToast',
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
    component: MemoryWall,
    props: {
      records: sampleRecords,
    },
  },
  {
    name: 'RoundedDashedBorder',
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
    component: WorkshopCard,
    props: {
      icon: 'color-wand-outline',
      title: 'Photo to comic',
      description: 'Live preview inside the component lab.',
    },
  },
];
