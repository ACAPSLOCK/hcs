# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 12:04:31 2021

@author: RYZEN5
"""

import asyncio
import hcskr
async def main():
    res =await hcskr.asyncSelfCheck("김성룡","050220","대구","포산고","고","8456")
    print(res['message'])

asyncio.get_event_loop().run_until_complete(main())