const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '..', 'api', 'photoApi.js'), 'utf8');

describe('photo private Storage URL guards', () => {
  test('identifies the exact failed write stage instead of reporting a generic permission error', () => {
    expect(source).toContain('function withOperationContext(result, operation)');
    expect(source).toContain("withOperationContext(result, '私有图片上传')");
    expect(source).toContain("'创建照片集'");
    expect(source).toContain("'写入照片记录'");
  });

  test('maps stored private paths to signed image URLs for authorized viewers', () => {
    expect(source).toContain('async function attachSignedPhotoUrls(collection, context)');
    expect(source).toContain("validateStoragePath('photos', storagePath, context, { requireOwner: false })");
    expect(source).toContain("context.supabase.storage.from('photos').createSignedUrl(storagePath, 3600)");
    expect(source).toContain('uri: signedUrl');
    expect(source).toContain("imageAccessError: signedUrl ? null : 'signed_url_unavailable'");
  });

  test('uses the same mapper for collection list, detail, and a newly uploaded collection', () => {
    expect(source).toContain('rows.map((collection) => attachSignedPhotoUrls(collection, context))');
    expect(source).toContain('await attachSignedPhotoUrls(data, context)');
    expect(source).toContain('await attachSignedPhotoUrls({ ...collection, photos }, context)');
  });
});
