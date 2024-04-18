#!/usr/bin/env python3

# Target.ndx
# 首先是根目录
#
# {
#   short total
#   entry e[total]
# }
#
# struct entry {
#   short name_len
#   char name[name_len]
#   int dir_offset
# }
#
# idx: 保存着每个文件在bin的位置

def file_name_hash(name):
  name = name.lower()[1:]
  ret = 0
  for s in name:
    ret = 37 * ret + ord(s)
  return ret

def file_name_idx_offset(name):
  return (file_name_hash(name) & 0x7FF) * 7 + 8

print(file_name_idx_offset('HomeNixSign_Targa.bmp'))
