import aiohttp
import asyncio
import os
import time
import sys
import aiofiles

urls = ['https://cdn.pixabay.com/photo/2023/08/11/04/51/'
        'fireworks-8182800_1280.jpg',
        'https://cdn.pixabay.com/photo/2023/09/30/17/13/'
        'coffee-beans-8286087_1280.jpg',
        'https://cdn.pixabay.com/photo/2024/02/13/19/02/'
        'poster-8571685_1280.jpg']

start_time = time.time()


async def download_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            # Получаем имя файла из URL
            filename = url.split('/')[-1]
            async with aiofiles.open(filename, 'wb') as f:
                # Сохраняем содержимое ответа в файл
                await f.write(await response.read())
            print(f"Изображение {filename} скачано за "
                  f"{time.time() - start_time:.5f} сек")
        else:
            print(f"Не удалось скачать изображение с URL: {url}")


async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(download_image(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Время выполнения программы: {end_time - start_time} сек")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        urls = sys.argv[1:]
    asyncio.run(main())
