# -*- coding: utf-8 -*-
"""作品集自检：资源引用是否都存在、总体积、大文件、未被页面引用的材料。

用法: python tools/check_site.py
退出码: 0 全部正常；1 有缺失引用
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, 'index.html')

# 平台限制提醒
WARN_SIZE_MB = 20      # GitHub 单文件软上限 50MB，Cloudflare Pages 25MB，这里留裕量
BLOCK_SIZE_MB = 95     # GitHub 硬拒绝 100MB


def human(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return '%.1f %s' % (n, unit) if unit != 'B' else '%d B' % n
        n /= 1024.0


def main():
    html = open(HTML, encoding='utf-8').read()
    refs = re.findall(r'(?:src|href)="([^"#]+?)"', html)
    local = [r for r in refs if not r.startswith(('http://', 'https://', 'mailto:', '#'))]

    print('=' * 66)
    print('作品集自检')
    print('=' * 66)
    missing = []
    for r in sorted(set(local)):
        p = os.path.join(BASE, r.replace('/', os.sep))
        if os.path.exists(p):
            print('  OK      %-62s %s' % (r, human(os.path.getsize(p))))
        else:
            print('  缺失 !! %s' % r)
            missing.append(r)

    # 全部文件与体积
    all_files = []
    for root, _dirs, files in os.walk(BASE):
        if '.git' in root.split(os.sep):
            continue
        for f in files:
            all_files.append(os.path.join(root, f))
    total = sum(os.path.getsize(f) for f in all_files)
    print('-' * 66)
    print('文件总数 %d，总体积 %s' % (len(all_files), human(total)))

    big = [f for f in all_files if os.path.getsize(f) > WARN_SIZE_MB * 1048576]
    if big:
        print('大文件提醒（> %d MB）：' % WARN_SIZE_MB)
        for f in big:
            size = os.path.getsize(f)
            flag = '会被 GitHub 拒绝' if size > BLOCK_SIZE_MB * 1048576 else '建议压缩'
            print('  %-58s %s (%s)' % (os.path.relpath(f, BASE), human(size), flag))
    else:
        print('无大文件（全部 < %d MB）' % WARN_SIZE_MB)

    # 未被页面引用的材料（持续补充材料的阶段属正常现象）
    used = set(r.replace('/', os.sep) for r in local)
    unused = []
    proj_root = os.path.join(BASE, 'projects')
    for root, _dirs, files in os.walk(proj_root):
        for f in files:
            if f.startswith('.'):
                continue
            rel = os.path.relpath(os.path.join(root, f), BASE)
            if rel not in used:
                unused.append(rel)
    print('-' * 66)
    if unused:
        print('尚未在页面中引用的材料（%d 个）——补充时可参考 tools/import_material.py 输出的 HTML 片段：' % len(unused))
        for u in sorted(unused):
            print('  %s' % u)
    else:
        print('所有材料都已在页面中引用')

    print('=' * 66)
    if missing:
        print('结论：有 %d 个引用缺失，必须修复' % len(missing))
        return 1
    print('结论：引用完整、体积正常')
    return 0


if __name__ == '__main__':
    sys.exit(main())
