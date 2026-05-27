import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyHeader from '../../src/components/FairyHeader';
import FairyInput from '../../src/components/FairyInput';
import FairyPage from '../../src/components/FairyPage';
import FairyToast from '../../src/components/FairyToast';
import spacing from '../../src/theme/spacing';

export default function CoupleInfoPage() {
  const [myName, setMyName] = useState('林小满');
  const [partnerName, setPartnerName] = useState('陆星河');
  const [startDate, setStartDate] = useState('2025-03-23');
  const [toastVisible, setToastVisible] = useState(false);

  const save = () => {
    setToastVisible(true);
    setTimeout(() => router.push('/(tabs)'), 400);
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="账号与关联"
        title="情侣信息设置"
        subtitle="设置昵称和起始日，让故事从第一页开始。"
      />

      <FairyCard style={styles.form}>
        <FairyInput label="我的昵称" icon="person-outline" value={myName} onChangeText={setMyName} />
        <FairyInput label="伴侣昵称" icon="people-outline" value={partnerName} onChangeText={setPartnerName} />
        <FairyInput label="恋爱起始日" icon="calendar-outline" value={startDate} onChangeText={setStartDate} />
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton title="完成设置并进入首页" onPress={save} />
      </View>

      <FairyToast
        visible={toastVisible}
        tone="success"
        message="情侣信息已保存到 mock 配置。"
        onHide={() => setToastVisible(false)}
      />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  form: { marginBottom: spacing.xl },
  actions: { gap: spacing.md },
});
