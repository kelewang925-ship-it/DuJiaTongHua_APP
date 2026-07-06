import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Platform,
  Pressable,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { richTextToPlainText } from '../utils/richText';

export default function FairyRichTextEditor({
  value = '',
  placeholder = '写下今天的小故事...',
  maxLength = 2000,
  height = 360,
  editable = true,
  style,
  onChange,
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
}) {
  const editorRef = useRef(null);
  const lastHtmlRef = useRef(value || '');
  const savedSelectionRef = useRef(null);
  const [count, setCount] = useState(richTextToPlainText(value).length);
  const [focused, setFocused] = useState(false);
  const [activeFormats, setActiveFormats] = useState({});

  useEffect(() => {
    if (!editorRef.current || focused || value === lastHtmlRef.current) return;

    editorRef.current.innerHTML = value || '';
    lastHtmlRef.current = value || '';
    setCount(richTextToPlainText(value).length);
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

    const selection = window.getSelection();
    if (!selection) return false;

    editor.focus();
    selection.removeAllRanges();
    selection.addRange(range);
    return true;
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

    setActiveFormats({
      bold: isCommandActive('bold'),
      italic: isCommandActive('italic'),
      underline: isCommandActive('underline'),
      strikeThrough: isCommandActive('strikeThrough'),
      insertOrderedList: isCommandActive('insertOrderedList'),
      insertUnorderedList: isCommandActive('insertUnorderedList'),
      formatBlock: /blockquote/i.test(blockValue),
    });
  };

  useEffect(() => {
    if (typeof document === 'undefined') return undefined;

    const handleSelectionChange = () => {
      saveSelection();
      updateActiveFormats();
    };

    document.addEventListener('selectionchange', handleSelectionChange);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, []);

  const emitChange = () => {
    const editor = editorRef.current;
    if (!editor) return;

    const text = editor.innerText || '';
    if (text.length > maxLength) {
      editor.innerText = text.slice(0, maxLength);
      placeCaretAtEnd(editor);
    }

    const html = editor.innerHTML || '';
    const nextText = editor.innerText || '';

    lastHtmlRef.current = html;
    setCount(nextText.length);
    onChange?.({ html, text: nextText });
    saveSelection();
    updateActiveFormats();
  };

  const exec = (command, commandValue) => {
    if (!editable || typeof document === 'undefined') return;

    if (!restoreSelection()) {
      editorRef.current?.focus();
    }
    document.execCommand(command, false, commandValue || null);
    emitChange();
    saveSelection();
    updateActiveFormats();
  };

  return (
    <View style={[styles.container, { height }, style]}>
      <Toolbar activeFormats={activeFormats} onExec={exec} />
      <View style={styles.webEditorWrap}>
        {React.createElement('div', {
          ref: editorRef,
          contentEditable: editable,
          suppressContentEditableWarning: true,
          onInput: emitChange,
          onFocus: () => {
            setFocused(true);
            saveSelection();
            updateActiveFormats();
          },
          onBlur: () => {
            saveSelection();
            setFocused(false);
          },
          onKeyUp: () => {
            saveSelection();
            updateActiveFormats();
          },
          onMouseUp: () => {
            saveSelection();
            updateActiveFormats();
          },
          dangerouslySetInnerHTML: { __html: value || '' },
          style: {
            minHeight: height - 76,
            padding: '18px 20px 48px',
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
      <Text style={styles.count}>{count}/{maxLength}</Text>
    </View>
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
}) {
  const { RichEditor, RichToolbar, actions } = require('react-native-pell-rich-editor');
  const editorRef = useRef(null);
  const lastHtmlRef = useRef(value || '');
  const [count, setCount] = useState(richTextToPlainText(value).length);
  const toolbarActions = useMemo(
    () => [
      actions.setBold,
      actions.setItalic,
      actions.setUnderline,
      actions.setStrikethrough,
      actions.insertOrderedList,
      actions.insertBulletsList,
      actions.blockquote,
      actions.insertImage,
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
      [actions.insertImage]: ({ tintColor }) => <ToolbarIcon label="Img" color={tintColor} small />,
    }),
    [actions]
  );

  useEffect(() => {
    if (!editorRef.current || value === lastHtmlRef.current) return;

    editorRef.current.setContentHTML(value || '');
    lastHtmlRef.current = value || '';
    setCount(richTextToPlainText(value).length);
  }, [value]);

  const handleChange = (html) => {
    const text = richTextToPlainText(html);

    if (text.length > maxLength) {
      return;
    }

    lastHtmlRef.current = html;
    setCount(text.length);
    onChange?.({ html, text });
  };

  return (
    <View style={[styles.container, { height }, style]}>
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
        onPressAddImage={() => {}}
      />
      <RichEditor
        ref={editorRef}
        initialContentHTML={value || ''}
        placeholder={placeholder}
        disabled={!editable}
        initialHeight={height - 76}
        onChange={handleChange}
        useContainer={false}
        style={styles.pellEditor}
        editorStyle={pellEditorStyle}
        pasteAsPlainText={false}
      />
      <Text style={styles.count}>{count}/{maxLength}</Text>
    </View>
  );
}

function Toolbar({ activeFormats, onExec }) {
  return (
    <View style={styles.toolbar}>
      {toolbarItems.map((item) => {
        if (item.divider) {
          return <View key={item.key} style={styles.divider} />;
        }

        return (
          <Tool
            key={item.key}
            label={item.label}
            selected={activeFormats[item.key]}
            textStyle={item.textStyle}
            onPress={() => {
              if (item.key === 'insertImage') return;
              onExec(item.key, item.value);
            }}
          />
        );
      })}
    </View>
  );
}

function Tool({ label, selected, textStyle, onPress }) {
  return (
    <Pressable
      style={[styles.tool, selected && styles.toolSelected]}
      onMouseDown={(event) => event.preventDefault()}
      onPress={onPress}
    >
      <Text style={[styles.toolText, selected && styles.toolTextSelected, textStyle]}>{label}</Text>
    </Pressable>
  );
}

function ToolbarIcon({ label, color, textStyle, small }) {
  return (
    <Text style={[styles.toolText, { color, fontSize: small ? 13 : 18 }, textStyle]}>
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
    shadowColor: '#7C5B48',
    shadowOpacity: 0.08,
    shadowRadius: 14,
    shadowOffset: {
      width: 0,
      height: 6,
    },
    elevation: 2,
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
  { key: 'insertImage', label: 'Img' },
];
