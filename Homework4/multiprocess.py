import requests
import os
import time
import sys
import multiprocessing

urls = [
    'https://cdn.pixabay.com/photo/2023/08/11/04/51/fireworks-8182800_1280.jpg',
    'https://cdn.pixabay.com/photo/2023/09/30/17/13/coffee-beans-8286087_1280.jpg',
    'https://cdn.pixabay.com/photo/2024/02/13/19/02/poster-8571685_1280.jpg'
]

start_time = time.time()


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(
                f"Изображение {filename} скачано за "
                f"{time.time() - start_time:.5f} сек")
        else:
            print(f"Не удалось скачать изображение с URL: {url}")
    except Exception as e:
        print(f"Ошибка при загрузке изображения с URL: {url}: {e}")


def main_multiprocess():
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_image, args=(url,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"Время выполнения программы: {time.time() - start_time:.5f} сек")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        urls = sys.argv[1:]
    main_multiprocess()
