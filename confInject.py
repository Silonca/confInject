# _*_ coding:utf-8 _*_

import configparser
import sys


def inject(f1, f2):
    conf1 = configparser.RawConfigParser()
    conf2 = configparser.RawConfigParser()
    conf1.read(f1, encoding='utf-8')
    conf2.read(f2, encoding='utf-8')

    sections1 = conf1.sections()
    sections2 = conf2.sections()
    print('\tf1:' + str(sections1))
    print('\tf2:' + str(sections2))

    print('\t' + '-' * 60)

    # DEFAULT节需要单独处理
    if len(conf2.defaults()) != 0:
        print('\t[DEFAULT]')
        keys = [d for d in conf1.defaults()]

        for key, value in conf2['DEFAULT'].items():
            conf1.set('DEFAULT', key, value)
            if key not in keys:
                print('\t\tnew: %s = %s' % (key, value))
            else:
                print('\t\tupdate: %s = %s' % (key, value))

    print('\t' + '-' * 60)

    for s in sections2:
        # 没有对应的节，则添加新节
        print('\t[%s]' % s)
        if s not in sections1:
            conf1.add_section(s)
            print('\tnew section [%s]' % s)

        # 被注入的文件的键，用于区分插入还是更新
        keys = [item[0] for item in conf1[s].items() if item[0] not in conf1.defaults()]
        # 筛掉default中的内容（configparser可以在任意节中读到default节中的内容）
        items = [item for item in conf2[s].items() if item not in conf2['DEFAULT'].items()]
        # 将相应的内容设为f2中对应的值（覆盖）
        for key, value in items:
            conf1.set(s, key, value)
            if key not in keys:
                print('\t\tnew: %s = %s' % (key, value))
            else:
                print('\t\tupdate: %s = %s' % (key, value))
        print()
    print('\t' + '-' * 60)
    conf1.write(open(f1, "w+", encoding='utf-8'))


if __name__ == '__main__':
    filename = sys.argv[1]
    cnt = 0
    with open(filename, encoding='utf-8') as f:
        num = len(f.readlines())
        print('%d files will be injected.' % num)
        f.seek(0)
        for l in f.read().splitlines():
            cnt += 1
            (f1, f2) = l.split(' ')
            print('[%d/%d] "%s" injected by "%s"' % (cnt, num, f1, f2))
            inject(f1, f2)

    