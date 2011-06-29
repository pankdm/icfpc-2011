#!/sur/bin/python

from  micro_strategy import gen_num2 


tests=[(0,255),(1,255),(255,16384),(12,90),(63,255),(62,254),(1,2),(1,3),(1,4),(4,1),(255,128),(("I",),14),(255,10000),(0,10000),(8064,8192),(222,252),(232,252),(242,252)]

for test in tests:
    print test[0],test[1],gen_num2(test[0],test[1])
