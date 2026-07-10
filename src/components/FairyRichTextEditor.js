import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
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

export default function FairyRichTextEditor({
  value = '',
  placeholder = '写下今天的小故事...',
  maxLength = 2000,
  height = 360,
  editable = true,
  style,
  onChange,
  onFocus,
  onBlur,
}) {
  if (Platform.OS === 'web') {
    return (
      <WebContentEditableEditor
        value={value}
        placeholder={placeholder}
        maxLength={maxLength}
        height={height}
        editable={editable}
        style={style}
        onChange={onChange}
        onFocus={onFocus}
        onBlur={onBlur}
      />
    );
  }

  return (
    <NativePellRichEditor
      value={value}
      placeholder={placeholder}
      maxLength={maxLength}
      height={height}
      editable={editable}
      style={style}
      onChange={onChange}
      onFocus={onFocus}
      onBlur={onBlur}
    />
  );
}

function WebContentEditableEditor({
  value,
  placeholder,
  maxLength,
  height,
  editable,
  style,
  onChange,
  onFocus,
  onBlur,
}) {
  const editorRef = useRef(null);
  const lastHtmlRef = useRef(value || '');
  const lastTextRef = useRef(richTextToPlainText(value, { trim: false }));
  const initialHtmlRef = useRef({ __html: value || '' });
  const savedSelectionRef = useRef(null);
  const composingRef = useRef(false);
  const formatFrameRef = useRef(null);
  const [count, setCount] = useState(getTextLength(lastTextRef.current));
  const [focused, setFocused] = useState(false);
  const [activeFormats, setActiveFormats] = useState({});

  useEffect(() => {
    if (!editorRef.current || focused || value === lastHtmlRef.current) return;

    editorRef.current.innerHTML = value || '';
    lastHtmlRef.current = value || '';
    lastTextRef.current = richTextToPlainText(value, { trim: false });
    savedSelectionRef.current = null;
    setCount(getTextLength(lastTextRef.current));
  }, [focused, value]);

  const saveSelection = () => {
    if (typeof window === 'undefined') return;

    const editor = editorRef.current;
    const selection = window.getSelection();
    if (!editor || !selection || selection.rangeCount === 0) return;

    const anchorNode = selection.anchorNode;
    const focusNode = selection.focusNode;
    if (!isNodeInside(editor, anchorNode) || !isNodeInside(editor, focusNode)) return;

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

    if (formatFrameRef.current !== null) {
      window.cancelAnimationFrame(formatFrameRef.current);
    }

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
      if (formatFrameRef.current !== null) {
        window.cancelAnimationFrame(formatFrameRef.current);
      }
    };
  }, [queueSelectionUpdate]);

  const emitChange = ({ force = false } = {}) => {
    const editor = editorRef.current;
    if (!editor || (composingRef.current && !force)) return;

    const text = editor.innerText || '';
    const nextCount = getTextLength(text);
    if (nextCount > maxLength) {
      editor.innerHTML = lastHtmlRef.current;
      setCount(getTextLength(lastTextRef.current));
      placeCaretAtEnd(editor);
      return;
    }

    const html = editor.innerHTML || '';

    lastHtmlRef.current = html;
    lastTextRef.current = text;
    setCount(nextCount);
    onChange?.({ html, text });
    saveSelection();
    queueSelectionUpdate();
  };

  const handleBeforeInput = (event) => {
    const nativeEvent = event.nativeEvent || event;
    const inputType = nativeEvent.inputType || '';
    if (nativeEvent.isComposing || inputType.startsWith('delete') || inputType.startsWith('history')) return;

    let insertedText = nativeEvent.data;
    if (insertedText == null && inputType === 'insertParagraph') insertedText = '\n';
    if (insertedText == null && nativeEvent.dataTransfer) {
      insertedText = nativeEvent.dataTransfer.getData('text/plain');
    }
    if (insertedText == null) return;

    const editor = editorRef.current;
    const selectedText = getSelectedTextInside(editor);
    const nextLength =
      getTextLength(editor?.innerText || '') - getTextLength(selectedText) + getTextLength(insertedText);

    if (nextLength > maxLength) {
      event.preventDefault();
    }
  };

  const exec = (command, commandValue) => {
    if (!editable || typeof document === 'undefined') return;

    if (!restoreSelection()) {
      editorRef.current?.focus();
    }
    document.execCommand(command, false, commandValue || null);
    emitChange();
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
          onBeforeInput: handleBeforeInput,
          onInput: emitChange,
          onCompositionStart: () => {
            composingRef.current = true;
          },
          onCompositionEnd: () => {
            composingRef.current = false;
            emitChange({ force: true });
          },
          onFocus: () => {
            setFocused(true);
            saveSelection();
            queueSelectionUpdate();
            onFocus?.();
          },
          onBlur: () => {
            if (!composingRef.current) emitChange();
            saveSelection();
            setFocused(false);
            onBlur?.();
          },
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
      <Text pointerEvents="none" style={styles.count}>{count}/{maxLength}</Text>
    </FairyCard>
  );
}

function NativePellRichEditor({
  value,
  placeholder,
  maxLength,
  height,
  editable,
  style,
  onChange,
  onFocus,
  onBlur,
}) {
  const { RichEditor, RichToolbar, actions } = require('react-native-pell-rich-editor');
  const editorRef = useRef(null);
  const lastHtmlRef = useRef(value || '');
  const lastTextRef = useRef(richTextToPlainText(value, { trim: false }));
  const restoringRef = useRef(false);
  const [count, setCount] = useState(getTextLength(lastTextRef.current));
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

  useEffect(() => {
    if (!editorRef.current || value === lastHtmlRef.current) return;

    editorRef.current.setContentHTML(value || '');
    lastHtmlRef.current = value || '';
    lastTextRef.current = richTextToPlainText(value, { trim: false });
    setCount(getTextLength(lastTextRef.current));
  }, [value]);

  const handleChange = (html) => {
    if (restoringRef.current) {
      restoringRef.current = false;
      return;
    }

    const text = richTextToPlainText(html, { trim: false });
    const nextCount = getTextLength(text);

    if (nextCount > maxLength) {
      restoringRef.current = true;
      editorRef.current?.setContentHTML(lastHtmlRef.current);
      setCount(getTextLength(lastTextRef.current));
      requestAnimationFrame(() => {
        editorRef.current?.focusContentEditor();
        editorRef.current?.commandDOM(PELL_PLACE_CARET_AT_END_COMMAND);
        restoringRef.current = false;
      });
      return;
    }

    lastHtmlRef.current = html;
    lastTextRef.current = text;
    setCount(nextCount);
    onChange?.({ html, text });
  };

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
        initialContentHTML={value || ''}
        placeholder={placeholder}
        disabled={!editable}
        initialHeight={height - 76}
        onChange={handleChange}
        onFocus={onFocus}
        onBlur={onBlur}
        useContainer={false}
        style={styles.pellEditor}
        editorStyle={pellEditorStyle}
        pasteAsPlainText
        autoCorrect
      />
      <Text pointerEvents="none" style={styles.count}>{count}/{maxLength}</Text>
    </FairyCard>
  );
}

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
        if (item.divider) {
          return <View key={item.key} style={styles.divider} />;
        }

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
  return (
    <Text style={[styles.toolText, { color }, textStyle]}>
      {label}
    </Text>
  );
}

function placeCaretAtEnd(element) {
  if (typeof window === 'undefined') return;

  element.focus();
  const range = document.createRange();
  range.selectNodeContents(element);
  range.collapse(false);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}

function isNodeInside(parent, node) {
  if (!parent || !node) return false;

  return node === parent || parent.contains(node);
}

function getSelectedTextInside(editor) {
  if (!editor || typeof window === 'undefined') return '';

  const selection = window.getSelection();
  if (!selection?.rangeCount || !isNodeInside(editor, selection.anchorNode) || !isNodeInside(editor, selection.focusNode)) {
    return '';
  }

  return selection.toString();
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

const PELL_PLACE_CARET_AT_END_COMMAND = `
  var element = $('#content');
  if (element) {
    var range = element.ownerDocument.createRange();
    range.selectNodeContents(element);
    range.collapse(false);
    var selection = element.ownerDocument.defaultView.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }
`;

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
    ul, ol {
      padding-left: 22px;
    }
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
  toolDisabled: {
    opacity: 0.42,
  },
  toolText: {
    color: '#8A6856',
    fontSize: 18,
    fontWeight: '600',
  },
  toolTextSelected: {
    color: '#6F5144',
  },
  pellToolbarItem: {
    width: 34,
    height: 34,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
  },
  bold: {
    fontWeight: '900',
  },
  italic: {
    fontStyle: 'italic',
  },
  underline: {
    textDecorationLine: 'underline',
  },
  strike: {
    textDecorationLine: 'line-through',
  },
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
