import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/photo/album.js'), 'utf8');

describe('photo album real-data guards', () => {
  test('does not fabricate three photos when count is missing', () => {
    expect(source).not.toContain('item.photoCount || 3');
    expect(source).not.toContain('(item.photoCount || 3)');
    expect(source).toContain("const getPhotoCount = (item)");
    expect(source).toContain('数量未记录');
  });

  test('does not fabricate a photo tag for empty real records', () => {
    expect(source).not.toContain("item.tags || ['照片']");
    expect(source).toContain('item.tags?.length');
  });

  test('uses the real delete action in real mode', () => {
    expect(source).toContain('deletePhotoReal');
    expect(source).toContain('isReal ? await deletePhotoReal(pendingDelete.id)');
    expect(source).toContain('照片记录删除失败，请重试');
  });

  test('does not use decorative covers as missing real photos', () => {
    expect(source).toContain('if (!isReal) return <FairyImage');
    expect(source).toContain('照片暂时无法加载');
    expect(source).toContain('这组记录没有可用封面');
  });
});
