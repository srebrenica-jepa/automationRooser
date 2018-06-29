FLEX_RULE_DEF1 = 'udp and ( (udp[8:4]=0x41206361 and udp[12:4]=0x74206973 and udp[16:4]=0x2066696e and ' \
                 'udp[20:4]=0x6520746f) or (udp[8:4]=0x7a784646 and udp[12:4]=0xffffff55 and udp[16:4]=0x4ba1d522) ' \
                 'or (udp[8:4]=0x666c6f6f and udp[12:4]=0x64000000) or (udp[8:4]=0x7a7a7a7a and (udp[12:4]=0x7a7a7a7a' \
                 ' or len<61)) or ( (udp[8:4]=0x7a000000 or udp[8:4]=0x7a7a0000 or udp[8:4]=0x7a7a7a00 or ' \
                 'udp[8:4]=0x7a7a7a7a or udp[8:4]=0xffff0000) and udp[12:4]=0x00000000 ) or ((src port 53 or src ' \
                 'port 3074 or src portrange 27015-27024) and dst port 25200) or (udp[8:4]=0x6675636b and ' \
                 'udp[12:4]=0x206c696c))'


FLEX_RULE_DEF2 = 'udp and ( (udp[8:4]=0x41206361 and udp[12:4]=0x74206973 and udp[16:4]=0x2066696e and ' \
                 'udp[20:4]=0x6520746f) or (udp[8:4]=0x7a784646 and udp[12:4]=0xffffff55 and udp[16:4]=0x4ba1d522) ' \
                 'or (udp[8:4]=0x666c6f6f and udp[12:4]=0x64000000) or (udp[8:4]=0x7a7a7a7a and (udp[12:4]=0x7a7a7a7a ' \
                 'or len<61)) or ( (udp[8:4]=0x7a000000 or udp[8:4]=0x7a7a0000 or udp[8:4]=0x7a7a7a00 or ' \
                 'udp[8:4]=0x7a7a7a7a or udp[8:4]=0xffff0000) and udp[12:4]=0x00000000 ) or ((src port 53 or src ' \
                 'port 3074 or src portrange 27015-27024) and dst port 25200) or (udp[8:4]=0x6675636b and udp[12:4]=0x206c696c))'