import asyncio
from playwright.async_api import async_playwright
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on('console', lambda msg: print('LOG:', msg.text))
        page.on('pageerror', lambda err: print('ERROR:', err))
        await page.goto('http://127.0.0.1:5000/')
        await asyncio.sleep(2)
        await browser.close()
asyncio.run(run())