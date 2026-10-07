# -*- coding: utf-8 -*-
"""把新材料归位到作品集：自动分类、规范命名、压缩、生成 HTML 片段。

用法
----
  # 归入 01 号项目（高温钢管检测平台）
  python tools/import_material.py 01 "C:/path/网格截图.png" "C:/path/收敛曲线.png"

  # 指定短描述（推荐，用于生成 URL 友好的文件名）
  python tools/import_material.py 01 截图.png --name mesh-overview
  python tools/import_material.py 01 动画.mp4 --name transient-preview

  # 一次导入一个目录里的所有图片
  python tools/import_material.py 02 "C:/path/电镀装备图片/" 

  # 查看各项目已有材料
  python tools/import_material.py --list

项目编号
--------
  01  高温钢管表面缺陷检测平台
  02  封闭式滚动电镀装备
  03  不锈钢板带力学性能预测（硕士学位论文）

命名规范
--------
  图片  figs/  →  figNN-<slug>.png|jpg      NN 为两位序号，决定页面展示顺序
  视频  videos/→  animNN-<slug>.mp4
  文档  docs/  →  docNN-<slug>.pdf
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

# Windows 控制台默认 GBK，中文与符号会 UnicodeEncodeError；统一按 UTF-8 输出
if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECTS = {
    '01': ('01-高温钢管检测平台', '高温钢管表面缺陷检测平台'),
    '02': ('02-电镀装备', '封闭式滚动电镀装备'),
    '03': ('03-力学性能预测', '不锈钢板带力学性能预测（硕士学位论文）'),
}

IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
VIDEO_EXT = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.m4v'}
DOC_EXT = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'}

MAX_IMAGE_WIDTH = 1600
VIDEO_CRF = '28'
VIDEO_HEIGHT = '720'


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\-]+', '-', text)
    text = re.sub(r'-{2,}', '-', text).strip('-')
    return text


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXT:
        return 'image'
    if ext in VIDEO_EXT:
        return 'video'
    if ext in DOC_EXT:
        return 'doc'
    return 'other'


def next_index(folder: str, prefix: str) -> int:
    n = 0
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            m = re.match(r'%s(\d{2})-.*' % prefix, f)
            if m:
                n = max(n, int(m.group(1)))
    return n + 1


def find_ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def optimize_image(src: str, dst: str) -> str:
    try:
        from PIL import Image
    except Exception:
        shutil.copyfile(src, dst)
        return 'PIL 不可用，直接复制'
    im = Image.open(src)
    w, h = im.size
    note = ''
    if w > MAX_IMAGE_WIDTH:
        ratio = MAX_IMAGE_WIDTH / float(w)
        im = im.resize((MAX_IMAGE_WIDTH, int(h * ratio)), Image.LANCZOS)
        note = '缩放 %dx%d -> %dx%d' % (w, h, im.width, im.height)
    ext = os.path.splitext(dst)[1].lower()
    if ext in ('.jpg', '.jpeg'):
        im.convert('RGB').save(dst, quality=85, optimize=True)
    else:
        im.save(dst, optimize=True)
    if not note:
        note = '尺寸 %dx%d 未变' % (w, h)
    return note


def compress_video(src: str, dst: str) -> str:
    ff = find_ffmpeg()
    if not ff:
        shutil.copyfile(src, dst)
        return '未找到 ffmpeg，原样复制（体积可能很大）'
    before = os.path.getsize(src)
    cmd = [ff, '-hide_banner', '-loglevel', 'error', '-y', '-i', src,
           '-vf', 'scale=-2:%s' % VIDEO_HEIGHT,
           '-c:v', 'libx264', '-crf', VIDEO_CRF, '-preset', 'veryfast',
           '-an', '-movflags', '+faststart', dst]
    subprocess.run(cmd, check=False)
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        return '压缩失败，原样复制'
    after = os.path.getsize(dst)
    return '压缩 %.1fMB -> %.1fMB (%sp)' % (before / 1048576, after / 1048576, VIDEO_HEIGHT)


def import_one(project_key: str, src: str, name: str = '') -> str:
    folder_slug, title = PROJECTS[project_key]
    kind = kind_of(src)
    sub = {'image': 'images', 'video': 'videos', 'doc': 'docs'}.get(kind, 'docs')
    prefix = {'image': 'fig', 'video': 'anim', 'doc': 'doc'}.get(kind, 'doc')
    out_dir = os.path.join(BASE, 'projects', folder_slug, sub)
    os.makedirs(out_dir, exist_ok=True)

    base = name if name else os.path.splitext(os.path.basename(src))[0]
    slug = slugify(base) or 'material'
    idx = next_index(out_dir, prefix)
    ext = os.path.splitext(src)[1].lower()
    if kind == 'image' and ext == '.jpeg':
        ext = '.jpg'
    dst_name = '%s%02d-%s%s' % (prefix, idx, slug, ext)
    dst = os.path.join(out_dir, dst_name)

    if kind == 'image':
        note = optimize_image(src, dst)
    elif kind == 'video':
        note = compress_video(src, dst)
    else:
        shutil.copyfile(src, dst)
        note = '原样复制'

    rel = 'projects/%s/%s/%s' % (folder_slug, sub, dst_name)
    print('  [%s] %s' % (title, note))
    print('  已保存: %s' % rel)
    print('  相对体积: %.0f KB' % (os.path.getsize(dst) / 1024))
    if kind == 'video':
        print('\n  HTML 片段（粘贴到 index.html 对应项目位置）:')
        print('''  <figure>
    <video controls muted playsinline preload="metadata">
      <source src="%s" type="video/mp4">
    </video>
    <figcaption><b>动画 N</b>　<!-- TODO: 一句话说明这动画展示什么 --></figcaption>
  </figure>''' % rel)
    elif kind == 'image':
        print('\n  HTML 片段（粘贴到 index.html 对应项目位置）:')
        print('''  <figure>
    <img src="%s" alt="<!-- TODO: 无障碍描述 -->">
    <figcaption><b>图 N</b>　<!-- TODO: 图注：显示对象、工况、色标范围、结论 --></figcaption>
  </figure>''' % rel)
    else:
        print('  建议在页面里用链接引用: <a href="%s">下载/查看</a>' % rel)
    print('  [脱敏提醒] 确认无企业名称/项目代号/图号/文件路径/CAD 界面残留后再发布\n')
    return dst


def list_materials():
    for key in sorted(PROJECTS):
        slug, title = PROJECTS[key]
        print('=' * 62)
        print('%s  %s   (projects/%s)' % (key, title, slug))
        print('=' * 62)
        for sub, prefix in (('images', 'fig'), ('videos', 'anim'), ('docs', 'doc')):
            d = os.path.join(BASE, 'projects', slug, sub)
            files = sorted(f for f in os.listdir(d) if not f.startswith('.')) if os.path.isdir(d) else []
            print('  %-7s %d 个%s' % (sub, len(files), '' if files else '（空）'))
            for f in files:
                print('      %-52s %6.0f KB' % (f, os.path.getsize(os.path.join(d, f)) / 1024))
        print('')


def main():
    ap = argparse.ArgumentParser(description='作品集材料归位工具', add_help=True)
    ap.add_argument('project', nargs='?', help='项目编号 01/02/03')
    ap.add_argument('files', nargs='*', help='要导入的文件或目录')
    ap.add_argument('--name', default='', help='短描述（英文小写连字符，用于文件名与 URL）')
    ap.add_argument('--list', action='store_true', help='列出各项目已有材料')
    args = ap.parse_args()

    if args.list or not args.project:
        list_materials()
        return

    if args.project not in PROJECTS:
        print('项目编号只能是: %s' % ', '.join(sorted(PROJECTS)))
        sys.exit(1)

    targets = []
    for f in args.files:
        if os.path.isdir(f):
            for n in sorted(os.listdir(f)):
                p = os.path.join(f, n)
                if os.path.isfile(p):
                    targets.append(p)
        elif os.path.isfile(f):
            targets.append(f)
        else:
            print('跳过（不存在）: %s' % f)
    if not targets:
        print('没有可导入的文件')
        sys.exit(1)

    print('导入到 %s（%s），共 %d 个文件\n' % (args.project, PROJECTS[args.project][1], len(targets)))
    for p in targets:
        import_one(args.project, p, args.name)


if __name__ == '__main__':
    main()
