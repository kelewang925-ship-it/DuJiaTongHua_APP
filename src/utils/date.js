export const formatDiaryDate = (diary) => {
  if (!diary?.createdAt) {
    return diary?.date || '刚刚';
  }

  const createdAt = new Date(diary.createdAt);
  if (Number.isNaN(createdAt.getTime())) {
    return diary.date || '刚刚';
  }

  const now = new Date();
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfCreatedDay = new Date(
    createdAt.getFullYear(),
    createdAt.getMonth(),
    createdAt.getDate()
  );
  const dayDiff = Math.floor((startOfToday - startOfCreatedDay) / 86400000);
  const timeText = createdAt.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });

  if (dayDiff === 0) {
    return `今天 ${timeText}`;
  }
  if (dayDiff === 1) {
    return `昨天 ${timeText}`;
  }

  return createdAt.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};
