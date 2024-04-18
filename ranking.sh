#!/bin/bash

echo """===== Gitea 仓库贡献者排名 =====
排名的依据是删除的行数。
这是因为翻译中往往都是+1-1的，删除的行数才代表真正的工作量。
避免导入文本的人在排名中占上风。
"""

Contributers=$(git log --format="%aN" | sort -u)
for p in $Contributers; do
  echo -en $p": "
  delta=$(git log --author="$p" --pretty=tformat: --numstat | \
    awk '{ add += $1; subs += $2 } END { printf "%s,%s", add, subs }' -)

  add=$(echo $delta | cut -f 1 -d ',')
  sub=$(echo $delta | cut -f 2 -d ',')
  echo "+${add}, -${sub}"
done | sort -rk 3
