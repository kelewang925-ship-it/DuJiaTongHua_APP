import React, {
  forwardRef,
  useCallback,
  useEffect,
  useImperativeHandle,
  useMemo,
  useRef,
  useState,
} from 'react';
import {
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { richTextToPlainText } from '../utils/richText';
import FairyCard from './FairyCard';

const COUNT_DEBOUNCE_MS = 400;
const CHANGE_DEBOUNCE_MS = 800;

const FairyRichTextEditor = forwardRef(function FairyRichTextEditor(
  {
    initialValue,
    value,
    placeholder = '写下今天的小故事...',
    maxLength = 2000,
    height = 360,
    editable = true,
    style,
    onChange,
    onDirtyChange,
    onFocus,
    onBlur,
  },
  forwardedRef
) {
  // 兼容旧调用方式，但正文只在首次挂载时初始化，避免编辑过程中外部 value 回写。
  const initialHtmlRef = useRef(initialValue ?? value ?? '');

  if (Platform.OS === 'web') {
    return (
      <WebContentEditableEditor
        ref={forwardedRef}
        initialValue={initialHtmlRef.current}
        placeholder={placeholder}
        maxLength={maxLength}
        height={height}
        editable={editable}
        style={style}
        onChange={onChange}
        onDirtyChange={onDirtyChange}
        onFocus={onFocus}
        onBlur={onBlur}
      />
    );
  }

  return (
    <NativePellRichEditor
      ref={forwardedRef}
      initialValue={initialHtmlRef.current}
      placeholder={placeholder}
      maxLength={maxLength}
      height={height}
      editable={editable}
      style={style}
      onChange={onChange}
      onDirtyChange={onDirtyChange}
      onFocus={onFocus}
      onBlur={onBlur}
    />
  );
});

export default React.memo(FairyRichTextEditor);

const WebContentEditableEditor = forwardRef(function WebContentEditableEditor(
  {
    initialValue,
    placeholder,
    maxLength,
    height,
    editable,
    style,
    onChange,
    onDirtyChange,
    onFocus,
    onBlur,
  },
  forwardedRef
) {
  const editorRef = useRef(null);
  const latestHtmlRef = useRef(initialValue || '');
  const latestTextRef = useRef(richTextToPlainText(initialValue, { trim: false }));
  const initialHtmlRef = useRef({ __html: initialValue || '' });
  const savedSelectionRef = useRef(null);
  const composingRef = useRef(false);
  const dirtyRef = useRef(false);
  const countTimerRef = useRef(null);
  const changeTimerRef = useRef(null);
  const formatFrameRef = useRef(null);
  const [count, setCount] = useState(getTextLength(latestTextRef.current));
  const [focused, setFocused] = useState(false);
  const [activeFormats, setActiveFormats] = useState({});

  const clearTimers = useCallback(() => {
    if (countTimerRef.current) clearTimeout(countTimerRef.current);
    if (changeTimerRef.current) clearTimeout(changeTimerRef.current);
    countTimerRef.current = null;
    changeTimerRef.current = null;
  }, []);

  const emitLatestChange = useCallback(() => {
    if (!dirtyRef.current) return;
    onChange?.({
      html: latestHtmlRef.current,
      text: latestTextRef.current,
      count: getTextLength(latestTextRef.current),
      isOverLimit: getTextLength(latestTextRef.current) > maxLength,
    });
  }, [maxLength, onChange]);

  const markDirty = useCallback(() => {
    if (!dirtyRef.current) {
      dirtyRef.current = true;
      onDirtyChange?.(true);
    }
  }, [onDirtyChange]);

  const scheduleDerivedState = useCallback(() => {
    if (countTimerRef.current) clearTimeout(countTimerRef.current);
    countTimerRef.current = setTimeout(() => {
      countTimerRef.current = null;
      setCount(getTextLength(latestTextRef.current));
    }, COUNT_DEBOUNCE_MS);

    if (changeTimerRef.current) clearTimeout(changeTimerRef.current);
    changeTimerRef.current = setTimeout(() => {
      changeTimerRef.current = null;
      emitLatestChange();
    }, CHANGE_DEBOUNCE_MS);
  }, [emitLatestChange]);

  useImperativeHandle(
    forwardedRef,
    () => ({
      getHTML: () => latestHtmlRef.current,
      getText: () => latestTextRef.current,
      getCount: () => getTextLength(latestTextRef.current),
      isOverLimit: () => getTextLength(latestTextRef.current) > maxLength,
      setHTML: (html = '') => {
        latestHtmlRef.current = html;
        latestTextRef.current = richTextToPlainText(html, { trim: false });
        dirtyRef.current = false;
        if (editorRef.current) editorRef.current.innerHTML = html;
        setCount(getTextLength(latestTextRef.current));
        onDirtyChange?.(false);
      },
      focus: () => editorRef.current?.focus(),
      blur: () => editorRef.current?.blur(),
      flush: () => {
        clearTimers();
        setCount(getTextLength(latestTextRef.current));
        emitLatestChange();
        return latestHtmlRef.current;
      },
      markSaved: () => {
        dirtyRef.current = false;
        onDirtyChange?.(false);
      },
    }),
    [clearTimers, emitLatestChange, maxLength, onDirtyChange]
  );

  useEffect(() => clearTimers, [clearTimers]);

  const saveSelection = () => {
    if (typeof window === 'undefined') return;
    const editor = editorRef.current;
    const selection = window.getSelection();
    if (!editor || !selection || selection.rangeCount === 0) return;
    if (!isNodeInside(editor, selection.anchorNode) || !isNodeInside(editor, selection.focusNode)) return;
    savedSelectionRef.current = selection.getRangeAt(0).cloneRange();
  };

  const restoreSelection = () => {
    if (typeof window === 'undefined') return false;
    const editor = editorRef.current;
    const range = savedSelectionRef.current;
    if (!editor || !range) return false;
    if (!range.startContainer?.isConnected || !range.endContainer?.isConnected) {
      savedSelectionRef.current = null;
      return false;
    }

    const selection = window.getSelection();
    if (!selection) return false;

    try {
      editor.focus();
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    } catch (error) {
      savedSelectionRef.current = null;
      return false;
    }
  };

  const updateActiveFormats = () => {
    if (typeof document === 'undefined') return;
    const editor = editorRef.current;
    if (!editor) return;
    const selection = window.getSelection?.();
    if (selection?.rangeCount && !isNodeInside(editor, selection.anchorNode)) return;

    const isCommandActive = (command) => {
      try {
        return document.queryCommandState(command);
      } catch (error) {
        return false;
      }
    };

    let blockValue = '';
    try {
      blockValue = document.queryCommandValue('formatBlock') || '';
    } catch (error) {
      blockValue = '';
    }

    const nextFormats = {
      bold: isCommandActive('bold'),
      italic: isCommandActive('italic'),
      underline: isCommandActive('underline'),
      strikeThrough: isCommandActive('strikeThrough'),
      insertOrderedList: isCommandActive('insertOrderedList'),
      insertUnorderedList: isCommandActive('insertUnorderedList'),
      formatBlock: /blockquote/i.test(blockValue),
    };

    setActiveFormats((current) => (areFormatStatesEqual(current, nextFormats) ? current : nextFormats));
  };

  const queueSelectionUpdate = useCallback(() => {
    if (typeof window === 'undefined') return;
    if (formatFrameRef.current !== null) window.cancelAnimationFrame(formatFrameRef.current);
    formatFrameRef.current = window.requestAnimationFrame(() => {
      formatFrameRef.current = null;
      saveSelection();
      updateActiveFormats();
    });
  }, []);

  useEffect(() => {
    if (typeof document === 'undefined') return undefined;
    const handleSelectionChange = () => {
      const editor = editorRef.current;
      const selection = window.getSelection?.();
      if (!editor || !selection?.rangeCount || !isNodeInside(editor, selection.anchorNode)) return;
      queueSelectionUpdate();
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      if (formatFrameRef.current !== null) window.cancelAnimationFrame(formatFrameRef.current);
    };
  }, [queueSelectionUpdate]);

  const captureContent = ({ force = false } = {}) => {
    const editor = editorRef.current;
    if (!editor || (composingRef.current && !force)) return;

    latestHtmlRef.current = editor.innerHTML || '';
    latestTextRef.current = editor.innerText || '';
    markDirty();
    scheduleDerivedState();
    saveSelection();
    queueSelectionUpdate();
  };

  const exec = (command, commandValue) => {
    if (!editable || typeof document === 'undefined') return;
    if (!restoreSelection()) editorRef.current?.focus();
    document.execCommand(command, false, commandValue || null);
    captureContent({ force: true });
  };

  const handleBlur = () => {
    if (!composingRef.current) captureContent({ force: true });
    clearTimers();
    setCount(getTextLength(latestTextRef.current));
    emitLatestChange();
    saveSelection();
    setFocused(false);
    onBlur?.();
  };

  return (
    <FairyCard
      shadow="soft"
      radius={16}
      padding={0}
      borderWidth={0}
      backgroundColor="transparent"
      shadowStyle={style}
      contentStyle={[styles.container, { height }]}
    >
      <Toolbar activeFormats={activeFormats} editable={editable} onExec={exec} />
      <View style={styles.webEditorWrap}>
        {React.createElement('div', {
          ref: editorRef,
          contentEditable: editable,
          suppressContentEditableWarning: true,
          onInput: captureContent,
          onCompositionStart: () => {
            composingRef.current = true;
          },
          onCompositionEnd: () => {
            composingRef.current = false;
            captureContent({ force: true });
          },
          onFocus: () => {
            setFocused(true);
            saveSelection();
            queueSelectionUpdate();
            onFocus?.();
          },
          onBlur: handleBlur,
          onKeyUp: queueSelectionUpdate,
          onMouseUp: queueSelectionUpdate,
          onTouchEnd: queueSelectionUpdate,
          dangerouslySetInnerHTML: initialHtmlRef.current,
          style: {
            width: '100%',
            height: '100%',
            padding: '18px 20px 48px',
            boxSizing: 'border-box',
            overflowY: 'auto',
            WebkitOverflowScrolling: 'touch',
            outline: 'none',
            fontSize: 16,
            lineHeight: 1.8,
            color: '#6F5144',
            wordBreak: 'break-word',
            whiteSpace: 'pre-wrap',
            fontFamily: '-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif',
          },
        })}
        {!focused && count === 0 ? (
          <Pressable style={styles.placeholder} onPress={() => editorRef.current?.focus()}>
            <Text style={styles.placeholderText}>{placeholder}</Text>
          </Pressable>
        ) : null}
      </View>
      <Text pointerEvents="none" style={[styles.count, count > maxLength && styles.countOverLimit]}>
        {count}/{maxLength}
      </Text>
    </FairyCard>
  );
});

const NativePellRichEditor = forwardRef(function NativePellRichEditor(
  {
    initialValue,
    placeholder,
    maxLength,
    height,
    editable,
    style,
    onChange,
    onDirtyChange,
    onFocus,
    onBlur,
  },
  forwardedRef
) {
  const { RichEditor, RichToolbar, actions } = require('react-native-pell-rich-editor');
  const editorRef = useRef(null);
  const latestHtmlRef = useRef(initialValue || '');
  const latestTextRef = useRef(richTextToPlainText(initialValue, { trim: false }));
  const dirtyRef = useRef(false);
  const countTimerRef = useRef(null);
  const changeTimerRef = useRef(null);
  const [count, setCount] = useState(getTextLength(latestTextRef.current));

  const toolbarActions = useMemo(
    () => [
      actions.setBold,
      actions.setItalic,
      actions.setUnderline,
      actions.setStrikethrough,
      actions.insertOrderedList,
      actions.insertBulletsList,
      actions.blockquote,
    ],
    [actions]
  );

  const iconMap = useMemo(
    () => ({
      [actions.setBold]: ({ tintColor }) => <ToolbarIcon label="B" color={tintColor} textStyle={styles.bold} />,
      [actions.setItalic]: ({ tintColor }) => <ToolbarIcon label="I" color={tintColor} textStyle={styles.italic} />,
      [actions.setUnderline]: ({ tintColor }) => <ToolbarIcon label="U" color={tintColor} textStyle={styles.underline} />,
      [actions.setStrikethrough]: ({ tintColor }) => <ToolbarIcon label="S" color={tintColor} textStyle={styles.strike} />,
      [actions.insertOrderedList]: ({ tintColor }) => <ToolbarIcon label="1." color={tintColor} />,
      [actions.insertBulletsList]: ({ tintColor }) => <ToolbarIcon label="-" color={tintColor} />,
      [actions.blockquote]: ({ tintColor }) => <ToolbarIcon label={'"'} color={tintColor} />,
    }),
    [actions]
  );

  const clearTimers = useCallback(() => {
    if (countTimerRef.current) clearTimeout(countTimerRef.current);
    if (changeTimerRef.current) clearTimeout(changeTimerRef.current);
    countTimerRef.current = null;
    changeTimerRef.current = null;
  }, []);

  const emitLatestChange = useCallback(() => {
    if (!dirtyRef.current) return;
    const currentCount = getTextLength(latestTextRef.current);
    onChange?.({
      html: latestHtmlRef.current,
      text: latestTextRef.current,
      count: currentCount,
      isOverLimit: currentCount > maxLength,
    });
  }, [maxLength, onChange]);

  const scheduleDerivedState = useCallback(() => {
    if (countTimerRef.current) clearTimeout(countTimerRef.current);
    countTimerRef.current = setTimeout(() => {
      countTimerRef.current = null;
      setCount(getTextLength(latestTextRef.current));
    }, COUNT_DEBOUNCE_MS);

    if (changeTimerRef.current) clearTimeout(changeTimerRef.current);
    changeTimerRef.current = setTimeout(() => {
      changeTimerRef.current = null;
      emitLatestChange();
    }, CHANGE_DEBOUNCE_MS);
  }, [emitLatestChange]);

  const handleChange = useCallback(
    (html) => {
      latestHtmlRef.current = html || '';

      // Pell 仍会逐键跨 WebView Bridge 返回 HTML，但全文解析、计数和父层通知已改为低频执行。
      if (!dirtyRef.current) {
        dirtyRef.current = true;
        onDirtyChange?.(true);
      }

      if (countTimerRef.current) clearTimeout(countTimerRef.current);
      countTimerRef.current = setTimeout(() => {
        countTimerRef.current = null;
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        setCount(getTextLength(latestTextRef.current));
      }, COUNT_DEBOUNCE_MS);

      if (changeTimerRef.current) clearTimeout(changeTimerRef.current);
      changeTimerRef.current = setTimeout(() => {
        changeTimerRef.current = null;
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        emitLatestChange();
      }, CHANGE_DEBOUNCE_MS);
    },
    [emitLatestChange, onDirtyChange]
  );

  useImperativeHandle(
    forwardedRef,
    () => ({
      getHTML: () => latestHtmlRef.current,
      getText: () => {
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        return latestTextRef.current;
      },
      getCount: () => {
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        return getTextLength(latestTextRef.current);
      },
      isOverLimit: () => {
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        return getTextLength(latestTextRef.current) > maxLength;
      },
      setHTML: (html = '') => {
        clearTimers();
        latestHtmlRef.current = html;
        latestTextRef.current = richTextToPlainText(html, { trim: false });
        dirtyRef.current = false;
        editorRef.current?.setContentHTML(html);
        setCount(getTextLength(latestTextRef.current));
        onDirtyChange?.(false);
      },
      focus: () => editorRef.current?.focusContentEditor(),
      blur: () => editorRef.current?.blurContentEditor(),
      flush: () => {
        clearTimers();
        latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
        setCount(getTextLength(latestTextRef.current));
        emitLatestChange();
        return latestHtmlRef.current;
      },
      markSaved: () => {
        dirtyRef.current = false;
        onDirtyChange?.(false);
      },
    }),
    [clearTimers, emitLatestChange, maxLength, onDirtyChange]
  );

  useEffect(() => clearTimers, [clearTimers]);

  const handleBlur = useCallback(() => {
    clearTimers();
    latestTextRef.current = richTextToPlainText(latestHtmlRef.current, { trim: false });
    setCount(getTextLength(latestTextRef.current));
    emitLatestChange();
    onBlur?.();
  }, [clearTimers, emitLatestChange, onBlur]);

  return (
    <FairyCard
      shadow="soft"
      radius={16}
      padding={0}
      borderWidth={0}
      backgroundColor="transparent"
      style={style}
      contentStyle={[styles.container, { height }]}
    >
      <RichToolbar
        editor={editorRef}
        actions={toolbarActions}
        iconMap={iconMap}
        iconTint="#8A6856"
        selectedIconTint="#6F5144"
        disabled={!editable}
        style={styles.toolbar}
        itemStyle={styles.pellToolbarItem}
        selectedButtonStyle={styles.toolSelected}
      />
      <RichEditor
        ref={editorRef}
        initialContentHTML={initialValue || ''}
        placeholder={placeholder}
        disabled={!editable}
        initialHeight={height - 76}
        onChange={handleChange}
        onFocus={onFocus}
        onBlur={handleBlur}
        useContainer={false}
        style={styles.pellEditor}
        editorStyle={pellEditorStyle}
        pasteAsPlainText
        autoCorrect
      />
      <Text pointerEvents="none" style={[styles.count, count > maxLength && styles.countOverLimit]}>
        {count}/{maxLength}
      </Text>
    </FairyCard>
  );
});

function Toolbar({ activeFormats, editable, onExec }) {
  return (
    <ScrollView
      horizontal
      keyboardShouldPersistTaps="always"
      showsHorizontalScrollIndicator={false}
      style={styles.webToolbar}
      contentContainerStyle={styles.webToolbarContent}
    >
      {toolbarItems.map((item) => {
        if (item.divider) return <View key={item.key} style={styles.divider} />;
        return (
          <Tool
            key={item.key}
            label={item.label}
            selected={activeFormats[item.key]}
            disabled={!editable}
            textStyle={item.textStyle}
            onPress={() => onExec(item.key, item.value)}
          />
        );
      })}
    </ScrollView>
  );
}

function Tool({ label, selected, disabled, textStyle, onPress }) {
  return (
    <Pressable
      disabled={disabled}
      style={[styles.tool, selected && styles.toolSelected, disabled && styles.toolDisabled]}
      onMouseDown={(event) => event.preventDefault()}
      onPointerDown={(event) => event.preventDefault()}
      onPress={onPress}
    >
      <Text style={[styles.toolText, selected && styles.toolTextSelected, textStyle]}>{label}</Text>
    </Pressable>
  );
}

function ToolbarIcon({ label, color, textStyle }) {
  return <Text style={[styles.toolText, { color }, textStyle]}>{label}</Text>;
}

function isNodeInside(parent, node) {
  if (!parent || !node) return false;
  return node === parent || parent.contains(node);
}

function getTextLength(text = '') {
  if (typeof Intl !== 'undefined' && Intl.Segmenter) {
    const segmenter = new Intl.Segmenter('zh-CN', { granularity: 'grapheme' });
    return Array.from(segmenter.segment(text)).length;
  }
  return Array.from(text).length;
}

function areFormatStatesEqual(current, next) {
  const keys = Object.keys(next);
  return keys.length === Object.keys(current).length && keys.every((key) => current[key] === next[key]);
}

const pellEditorStyle = {
  backgroundColor: '#FFF8EE',
  color: '#6F5144',
  caretColor: '#8A6856',
  placeholderColor: 'rgba(138, 104, 86, 0.48)',
  contentCSSText: `
    font-size: 16px;
    line-height: 1.8;
    padding: 18px 20px 48px;
    color: #6F5144;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  `,
  cssText: `
    blockquote {
      margin: 10px 0;
      padding: 8px 12px;
      border-left: 3px solid #D9A6A0;
      background: rgba(255, 241, 235, 0.7);
      border-radius: 8px;
    }
    ul, ol { padding-left: 22px; }
    img {
      max-width: 100%;
      border-radius: 12px;
      margin: 8px 0;
    }
  `,
};

const styles = StyleSheet.create({
  container: {
    position: 'relative',
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(124, 91, 72, 0.18)',
    borderRadius: 16,
    backgroundColor: '#FFF8EE',
  },
  toolbar: {
    height: 56,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(124, 91, 72, 0.12)',
    backgroundColor: 'rgba(255, 250, 242, 0.96)',
  },
  webToolbar: {
    flexGrow: 0,
    height: 56,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(124, 91, 72, 0.12)',
    backgroundColor: 'rgba(255, 250, 242, 0.96)',
  },
  webToolbarContent: {
    minWidth: '100%',
    height: 56,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  tool: {
    width: 34,
    height: 34,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
  },
  toolSelected: {
    backgroundColor: 'rgba(216, 179, 132, 0.22)',
    borderWidth: 1,
    borderColor: 'rgba(138, 104, 86, 0.24)',
    borderRadius: 10,
  },
  toolDisabled: { opacity: 0.42 },
  toolText: {
    color: '#8A6856',
    fontSize: 18,
    fontWeight: '600',
  },
  toolTextSelected: { color: '#6F5144' },
  pellToolbarItem: {
    width: 34,
    height: 34,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
  },
  bold: { fontWeight: '900' },
  italic: { fontStyle: 'italic' },
  underline: { textDecorationLine: 'underline' },
  strike: { textDecorationLine: 'line-through' },
  divider: {
    width: 1,
    height: 22,
    marginHorizontal: 8,
    backgroundColor: 'rgba(124, 91, 72, 0.16)',
  },
  pellEditor: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  webEditorWrap: {
    flex: 1,
    position: 'relative',
  },
  placeholder: {
    position: 'absolute',
    left: 20,
    top: 18,
  },
  placeholderText: {
    color: 'rgba(138, 104, 86, 0.48)',
    fontSize: 16,
    lineHeight: 29,
  },
  count: {
    position: 'absolute',
    right: 18,
    bottom: 14,
    color: 'rgba(111, 81, 68, 0.58)',
    fontSize: 13,
  },
  countOverLimit: {
    color: '#B85C5C',
    fontWeight: '700',
  },
});

const toolbarItems = [
  { key: 'bold', label: 'B', textStyle: styles.bold },
  { key: 'italic', label: 'I', textStyle: styles.italic },
  { key: 'underline', label: 'U', textStyle: styles.underline },
  { key: 'strikeThrough', label: 'S', textStyle: styles.strike },
  { key: 'divider', divider: true },
  { key: 'insertOrderedList', label: '1.' },
  { key: 'insertUnorderedList', label: '-' },
  { key: 'formatBlock', label: '"', value: 'blockquote' },
];
