import asyncio
import aiohttp
import os
from aiologger import Logger
from tqdm import tqdm
import aiofiles

MAIN_URL_FILE = 'main_url.txt'
ORIGINAL_TRACKERS_FILE = 'original_trackers.txt'
OUTPUT_TRACKERS_FILE = 'output_trackers.txt'

logger = Logger.with_default_handlers(name='my_async_logger')

async def download_main_url():
    main_url = "https://raw.githubusercontent.com/phishinqi/phishinqi.github.io/refs/heads/main/assets/txt/trackers_url.txt"
    
    if os.path.exists(MAIN_URL_FILE):
        logger.info(f"{MAIN_URL_FILE} 文件已存在，跳过下载。")
        return

    logger.info(f"正在下载 {MAIN_URL_FILE} 文件...")
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(main_url) as response:
                response.raise_for_status()
                content = await response.text()

        async with aiofiles.open(MAIN_URL_FILE, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        logger.info(f"{MAIN_URL_FILE} 文件下载完成。")
    except aiohttp.ClientError as e:
        logger.error(f"下载 {MAIN_URL_FILE} 时发生网络错误: {e}")
    except asyncio.TimeoutError:
        logger.error(f"下载 {MAIN_URL_FILE} 时超时。")

async def read_urls():
    if not os.path.exists(MAIN_URL_FILE):
        logger.error(f"{MAIN_URL_FILE} 文件不存在！")
        return []

    async with aiofiles.open(MAIN_URL_FILE, 'r', encoding='utf-8') as f:
        urls = await f.readlines()
    return [url.strip() for url in urls if url.strip()]

async def prepare_trackers_file(file_name):
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            logger.info(f"已删除旧的 {file_name} 文件。")
        except OSError as e:
            logger.error(f"删除 {file_name} 文件时发生错误: {e}")
    else:
        logger.info(f"{file_name} 文件不存在，无需删除。")
    async with aiofiles.open(file_name, 'w', encoding='utf-8') as f:
        await f.write("")

async def fetch_tracker(session, url, f_write, progress_bar):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            await f_write.write(content + '\n')
    except aiohttp.ClientError as e:
        logger.error(f"下载 {url} 时发生网络错误: {e}")
    except asyncio.TimeoutError:
        logger.error(f"下载 {url} 时超时。")
    except asyncio.CancelledError:
        logger.error(f"下载 {url} 时被取消。")
    except Exception as e:
        logger.error(f"下载 {url} 时发生未知错误: {e}")
    finally:
        progress_bar.update(1)

async def fetch_and_write_trackers(session, urls, output_file):
    logger.info("正在下载 trackers...")
    async with aiofiles.open(output_file, 'a', encoding='utf-8') as f_write:
        with tqdm(total=len(urls), desc="下载中", unit="个") as progress_bar:
            tasks = [fetch_tracker(session, url, f_write, progress_bar) for url in urls]
            await asyncio.gather(*tasks)

async def remove_duplicates(input_file, output_file):
    logger.info("正在去重...")
    seen = set()

    try:
        async with aiofiles.open(input_file, 'r', encoding='utf-8') as f_read:
            async with aiofiles.open(output_file, 'w', encoding='utf-8') as f_write:
                async for line in f_read:
                    stripped_line = line.strip()
                    if stripped_line and stripped_line not in seen:
                        seen.add(stripped_line)
                        await f_write.write(stripped_line + '\n\n')

        logger.info("去重完成。")
    except (OSError, IOError) as e:
        logger.error(f"去重过程中发生文件 I/O 错误: {e}")
    except Exception as e:
        logger.error(f"去重过程中发生其他错误: {e}")

async def main():
    await download_main_url()
    urls = await read_urls()
    
    if not urls:
        logger.error("没有可处理的 URL，请检查 main_url.txt 文件。")
        return
    
    await prepare_trackers_file(ORIGINAL_TRACKERS_FILE)

    async with aiohttp.ClientSession() as session:
        await fetch_and_write_trackers(session, urls, ORIGINAL_TRACKERS_FILE)

    await remove_duplicates(ORIGINAL_TRACKERS_FILE, OUTPUT_TRACKERS_FILE)
    await logger.shutdown()

    if os.path.exists(MAIN_URL_FILE):
        try:
            os.remove(MAIN_URL_FILE)
            logger.info(f"{MAIN_URL_FILE} 文件已删除。")
        except OSError as e:
            logger.error(f"删除 {MAIN_URL_FILE} 文件时发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
