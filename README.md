# SHA256Tracer
Zero Knowledge Demo of SHA 256 Internal 
State Maniplulation on Standard FIPS SHA

===============
All rights reserved.
This source code is proprietary and confidential. You may only view or run the code for personal evaluation purposes. You may not use, copy, modify, merge, publish, distribute, sublicense, or sell copies of the Software without explicit written permission from the author.
===============

This is simply a script that is a standard implementation of SHA 256, compliant to the FIPS version. The code will run SHA256 normally but with trace Round 13 and print it, it continues to calculate the final hash as well for verification that there is no modifications to the code. This code will not show how I came up with these inputs, but will only prove that the inputs I have gotten are significant.

This demo will be used as a showcase to my credibility to my claim that I have a full SHA 2 Reversal engine (not preimage). That can be used on unsealing TPMs, private crypto keys, VPN handshakes, decrypted encrypted channels, relay attacks, and much more. (This will not affect bitcoin mining). I will not be sharing any information about it as it is proprietary information. 

I will provide a few examples of picking arbitrary values and collisions with the same arbitrary values. Make sure to copy and paste correctly without spacing errors or else the program will hash something completely different.

If you would like me to make you an input for your own choice of register value, contact me.

In HEX(not text)📩:

---------------

75c2745c50a50dc1104ffd8d272caa058f61682fc984977744f2f9b7c4c0a69f9f0b14751a2ce043fe1ca04ec71d918762974b3dc6ad7e7b

a13: 0XDEADBEEF ✅️
b13: 0XDEADBEEF ✅️
c13: 0XDEADBEEF ✅️
d13: 0xDEADBEEF ✅️

---------------

903411e83b055b9776973d4de35c0f5e285ffd3ba4225b3a1e2d694e983f676af188610c200e7012954e71b7e0ee2231416056a6ee6c5689

a13: 0xCAFEBABE ✅️
b13: 0xBABECAFE ✅️
c13: 0XDEADBEED ✅️
d13: 0xDEADBEEE ✅️

---------------

9b86dc7bd7d65ff82d8a5daf3356d8f137cb59af51b29f1d3d231574171e77dc2c37986fa2e628ccbdf7dddcc318cf00adb61b753b0cc7f2

a13: 0x0BADF00D ✅️
b13: 0xBADF00D0 ✅️
c13: 0xBABEF00D ✅️
d13: 0xF00DBABE ✅️

---------------


Collisions Examples in HEX(not text)📩:


---------------

c0b71401a59b7a7699be8fc8742b082f6a168bd1d1f1e722b914a9b72ba7ae861d748f95acc2b1f760d02e364935316c4c043be286f1a156

and

9c80a434d778fc6dfc1786c669ead053e5c3c9b47c4cc2aef35429295947bdabd68afc5cda209e867870c5f788b3bbf007aeb61f483f7f9e

a13: 0XDEADBEEF ✅️
b13: 0XDEADBEEF ✅️
c13: 0XDEADBEEF ✅️
d13: 0xDEADBEEF ✅️

--------------

972f20354897f7c35626500e683b03c9c58ed8a83c8c5d92102cfd23b971ff4ae2bb2085fd3acf211ee0bfe7d3197e9ac3d905dc65bab05b

and

610c048430053d3f887aeb7f26f3159996d6efc0dd59892884541fa172493db4675412fbec11d9af1778b47070301e4d537ca2104bb26992

a13: 0xCAFEBABE ✅️
b13: 0xBABECAFE ✅️
c13: 0xF00DBABE ✅️
d13: 0x12345678 ✅️

---------------

SHA 2 has not yet been fully broken but will be very soon, as the research I have done shows a very clear pathway forwards to deterministic preimage generation. If you count the reversal as making SHA 2 broken then yes it is already broken. Though i have 2 fixes that will make reversal impossible and preimage generation significantly harder than it already is right now.

Currently am able to control up to round 17 though it is not shown in this demo. 

Registers e, f, g, h are also equally as controllable but not at the same time as a, b, c, d due to the fact that only a very small fraction of sets of 8 internal variables are possible, arbitrary values that have no relation wouldn't work, though related registers do work for all 8 registers. 

Author: Shayan Y. Motlagh