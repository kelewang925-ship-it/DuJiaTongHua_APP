"""Convert current formal design PNGs into layered, editable HTML previews.

Usage: python design-html/build.py --source-root PATH
The source root contains the eight module directories under 新模块分布.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path

import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR


HERE = Path(__file__).resolve().parent
FONT = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "AnJingChenShouShuFangSong（Xin）-2.ttf"
ACTION_WORDS = ("登录", "注册", "保存", "确认", "继续", "开始", "查看", "添加", "上传", "编辑", "返回", "下一步", "完成", "发送", "创建", "进入", "阅读", "搜索", "取消", "分享", "选择", "确定")


def read_image(path: Path) -> np.ndarray:
    image = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def write_webp(path: Path, image: np.ndarray, quality: int = 94) -> None:
    ok, encoded = cv2.imencode(".webp", image, [cv2.IMWRITE_WEBP_QUALITY, quality])
    if not ok:
        raise ValueError(f"Cannot encode image: {path}")
    encoded.tofile(str(path))


def text_color(image: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> str:
    patch = image[max(0, y1):y2, max(0, x1):x2]
    if patch.size == 0:
        return "#674638"
    rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB).reshape(-1, 3)
    brightness = rgb.mean(axis=1)
    dark = rgb[brightness <= np.quantile(brightness, 0.16)]
    if len(dark) < 8:
        return "#674638"
    color = np.median(dark, axis=0).astype(int)
    return "#{:02x}{:02x}{:02x}".format(*color)


def build_layers(path: Path, ocr: RapidOCR):
    image = read_image(path)
    height, width = image.shape[:2]
    result, _ = ocr(str(path))
    result = result or []
    mask = np.zeros((height, width), dtype=np.uint8)
    layers = []
    for polygon, raw_text, confidence in result:
        text = str(raw_text).strip()
        if not text or confidence < 0.35:
            continue
        points = np.asarray(polygon, dtype=np.float32)
        x1 = max(0, int(np.floor(points[:, 0].min())))
        y1 = max(0, int(np.floor(points[:, 1].min())))
        x2 = min(width, int(np.ceil(points[:, 0].max())))
        y2 = min(height, int(np.ceil(points[:, 1].max())))
        if x2 - x1 < 4 or y2 - y1 < 5:
            continue
        color = text_color(image, x1, y1, x2, y2)
        cv2.fillPoly(mask, [points.astype(np.int32)], 255)
        role = "action" if any(word in text for word in ACTION_WORDS) and len(text) <= 16 else "text"
        layers.append({"text": text, "confidence": round(float(confidence), 3), "role": role, "x": x1, "y": y1, "w": x2-x1, "h": y2-y1, "color": color})
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    clean = cv2.inpaint(image, mask, 5, cv2.INPAINT_TELEA) if layers else image.copy()
    return image, clean, layers


def page_html(page: dict) -> str:
    width, height = page["width"], page["height"]
    spans = []
    for index, layer in enumerate(page["layers"]):
        style = f"left:{layer['x']/width*100:.4f}%;top:{layer['y']/height*100:.4f}%;min-width:{layer['w']/width*100:.4f}%;min-height:{layer['h']/height*100:.4f}%;font-size:{layer['h']/width*95:.4f}cqw;--ink:{layer['color']};background-size:100cqw {height/width*100:.4f}cqw;background-position:-{layer['x']/width*100:.4f}cqw -{layer['y']/width*100:.4f}cqw"
        label = html.escape(layer["text"], quote=True)
        spans.append(f'<span class="text-layer {layer["role"]}" contenteditable="true" spellcheck="false" data-id="{index}" data-confidence="{layer["confidence"]}" style="{style}">{label}</span>')
    title = html.escape(page["title"])
    module = html.escape(page["module"])
    layers_markup = "\n".join(spans)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 独家童话设计还原</title>
<style>
@font-face{{font-family:Fairy;src:url('../assets/font.ttf') format('truetype');font-display:swap}}
*{{box-sizing:border-box}}body{{margin:0;background:#eae2da;color:#674638;font-family:Fairy,'STFangsong','Songti SC',serif}}button{{font:inherit;cursor:pointer}}
.toolbar{{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 16px;background:#fff9f2;box-shadow:0 2px 10px #56382e20;font-size:14px}}.toolbar a{{color:#8e5d52}}.toolbar strong{{font-weight:500}}.toolbar button{{border:1px solid #d5b2a1;border-radius:20px;background:#f9e9e1;color:#764c42;padding:4px 12px}}.toolbar .hint{{margin-left:auto;color:#967b70;font-size:12px}}
.stage{{position:relative;isolation:isolate;width:min(100vw,{width}px);aspect-ratio:{width}/{height};margin:20px auto;container-type:inline-size;box-shadow:0 12px 35px #5b40332e;background:#fff9f3;overflow:hidden}}.art,.source{{position:absolute;inset:0;width:100%;height:100%;display:block}}.art{{display:none}}.text-layer{{position:absolute;display:block;width:max-content;max-width:98%;font-family:Fairy,'STFangsong','Songti SC',serif;font-weight:400;line-height:1;white-space:nowrap;color:transparent;caret-color:#9c6157;background-repeat:no-repeat;border:0;outline:0;z-index:2}}.text-layer.action{{cursor:text}}.stage.original .text-layer{{display:none}}.stage .text-layer:focus,.stage .text-layer.edited{{color:var(--ink);background-image:url('../assets/{page['id']}-art.webp')}}.stage .text-layer:focus{{outline:1px dashed #dd8e89}}.stage.layered .source{{display:none}}.stage.layered .art{{display:block}}.stage.layered .text-layer{{color:var(--ink);background-image:none}}.stage.show-boxes .text-layer{{outline:1px dashed #d9908b88}}@media(max-width:{width}px){{.stage{{margin:0 auto;box-shadow:none}}}}
</style></head><body>
<nav class="toolbar"><a href="../index.html">‹ 全部页面</a><strong>{module} / {title}</strong><button type="button" id="compare">编辑文字层</button><button type="button" id="layers">查看分层重建</button><button type="button" id="boxes">显示文字框</button><button type="button" id="reset">清除本页修改</button><span class="hint">编辑模式下点击文字；修改保存在当前浏览器</span></nav>
<main class="stage original" id="stage" aria-label="{title} HTML 还原"><img class="art" src="../assets/{page['id']}-art.webp" alt=""><img class="source" src="../assets/{page['id']}-source.webp" alt="原始设计稿">
{layers_markup}
</main>
<script>
const stage=document.querySelector('#stage');const key='fairy-design-html:{page['id']}';
let saved={{}};try{{saved=JSON.parse(localStorage.getItem(key)||'{{}}')}}catch{{}}
document.querySelectorAll('.text-layer').forEach(layer=>{{if(saved[layer.dataset.id]!==undefined){{layer.textContent=saved[layer.dataset.id];layer.classList.add('edited')}}layer.addEventListener('input',()=>{{layer.classList.add('edited');saved[layer.dataset.id]=layer.textContent;localStorage.setItem(key,JSON.stringify(saved))}})}});
document.querySelector('#compare').addEventListener('click',event=>{{stage.classList.toggle('original');if(stage.classList.contains('original'))stage.classList.remove('layered');event.currentTarget.textContent=stage.classList.contains('original')?'编辑文字层':'查看原稿';document.querySelector('#layers').textContent='查看分层重建'}});
document.querySelector('#layers').addEventListener('click',event=>{{stage.classList.remove('original');stage.classList.toggle('layered');document.querySelector('#compare').textContent='查看原稿';event.currentTarget.textContent=stage.classList.contains('layered')?'返回逐项编辑':'查看分层重建'}});
document.querySelector('#boxes').addEventListener('click',()=>stage.classList.toggle('show-boxes'));
document.querySelector('#reset').addEventListener('click',()=>{{localStorage.removeItem(key);location.reload()}});
</script></body></html>'''


def index_html(pages: list[dict]) -> str:
    cards = []
    for page in pages:
        title = html.escape(page["title"])
        module = html.escape(page["module"])
        cards.append(f'<a class="card" href="pages/{page["id"]}.html" data-search="{module} {title}"><img loading="lazy" src="assets/{page["id"]}-source.webp" alt="{title}"><span class="card-copy"><small>{module}</small><strong>{title}</strong><em>{len(page["layers"])} 个可编辑文字层</em></span></a>')
    cards_markup = "\n".join(cards)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>独家童话 · 设计稿 HTML 还原</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f7f1eb;color:#594039;font-family:system-ui,'Microsoft YaHei',sans-serif}}header{{padding:40px max(24px,calc((100vw - 1280px)/2));background:#fff8f1;border-bottom:1px solid #e7d5c5}}h1{{margin:0 0 10px;font-size:30px}}p{{line-height:1.6;max-width:750px}}input{{width:min(100%,420px);padding:12px 16px;border:1px solid #d5b7a9;border-radius:10px;font:inherit;background:white}}main{{max-width:1280px;margin:auto;padding:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:18px}}.card{{display:block;overflow:hidden;border:1px solid #e2cdbc;border-radius:14px;background:white;color:inherit;text-decoration:none;box-shadow:0 5px 14px #50332212}}.card:hover{{transform:translateY(-2px);box-shadow:0 9px 22px #50332224}}.card img{{display:block;width:100%;height:230px;object-fit:cover;object-position:top}}.card-copy{{display:flex;flex-direction:column;gap:5px;padding:12px}}small,em{{color:#967e70;font-size:12px;font-style:normal}}strong{{font-size:14px;line-height:1.4}}.card[hidden]{{display:none}}</style></head><body><header><h1>独家童话 · 设计稿 HTML 还原</h1><p>八个模块，共 {len(pages)} 张正式页面与状态稿。每页默认显示原稿，点击“编辑文字层”可进入 HTML 文字编辑模式。该模式使用去字图片保留插画、纹理和图形，自动识别结果仍需逐页校对。</p><input id="search" type="search" placeholder="搜索模块或页面" aria-label="搜索页面"></header><main>{cards_markup}</main><script>document.querySelector('#search').addEventListener('input',event=>{{const value=event.target.value.trim().toLowerCase();document.querySelectorAll('.card').forEach(card=>card.hidden=!card.dataset.search.toLowerCase().includes(value))}})</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--limit", type=int, default=0, help="Only build first N pages for a smoke test")
    parser.add_argument("--render-only", action="store_true", help="Rebuild HTML from the existing manifest without rerunning OCR")
    args = parser.parse_args()
    if args.render_only:
        pages = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        for page in pages:
            (HERE / "pages" / f"{page['id']}.html").write_text(page_html(page), encoding="utf-8")
        (HERE / "index.html").write_text(index_html(pages), encoding="utf-8")
        print(f"Rendered {len(pages)} pages from manifest", flush=True)
        return
    if args.source_root is None:
        parser.error("--source-root is required unless --render-only is specified")
    source = args.source_root.resolve()
    if not source.is_dir():
        raise SystemExit(f"Design root does not exist: {source}")
    modules = sorted(path for path in source.iterdir() if path.is_dir())
    files = [(module, image) for module in modules for image in sorted(module.glob("*.png")) if "提案" not in image.name]
    if len(files) != 114:
        raise SystemExit(f"Expected 114 formal PNGs, found {len(files)}. Check design scope before building.")
    if args.limit:
        files = files[:args.limit]
    assets = HERE / "assets"
    pages_dir = HERE / "pages"
    assets.mkdir(exist_ok=True)
    pages_dir.mkdir(exist_ok=True)
    shutil.copy2(FONT, assets / "font.ttf")
    ocr = RapidOCR()
    pages = []
    for count, (module, image_path) in enumerate(files, 1):
        module_number = int(re.match(r"\d+", module.name).group())
        module_position = sum(1 for item in pages if item["module_number"] == module_number) + 1
        page_id = f"m{module_number:02d}-p{module_position:02d}"
        original, clean, layers = build_layers(image_path, ocr)
        height, width = original.shape[:2]
        title = image_path.stem
        module_title = re.sub(r"^\d+[\s-]*", "", module.name)
        page = {"id": page_id, "module_number": module_number, "module": module_title, "title": title, "source": str(image_path.relative_to(source)), "width": width, "height": height, "layers": layers}
        write_webp(assets / f"{page_id}-source.webp", original)
        write_webp(assets / f"{page_id}-art.webp", clean)
        (pages_dir / f"{page_id}.html").write_text(page_html(page), encoding="utf-8")
        pages.append(page)
        print(f"[{count}/{len(files)}] {page_id}: {title} | {len(layers)} text layers", flush=True)
    (HERE / "manifest.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    (HERE / "index.html").write_text(index_html(pages), encoding="utf-8")
    print(f"Built {len(pages)} editable pages in {HERE}", flush=True)


if __name__ == "__main__":
    main()
