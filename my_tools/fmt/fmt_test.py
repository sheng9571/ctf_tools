# -*- coding:utf-8 -*-

from fmt import fmt



t1 = [140334215500688, 6296112, 'w', 2]
t2 = ['0x7fa21b109390', '0x601230', 'r']
t = [t1, t2]

fmt = fmt(64, True)
fmt.c_payload([10, t])
