import asyncio
import threading
import multiprocessing
import time
import os

# 1. Asyncio - Network I/O Simulation (Fetching Data)
async def fetch_data_from_api(item_id):
    print(f"Asyncio: Fetching data for item {item_id}...")
    await asyncio.sleep(1) # จำลองระยะเวลา Network Delay
    result = f"Data_{item_id}"
    print(f"Asyncio: Fetched data {result}")
    return result

async def run_async_tasks(num_items):
    print("--- Starting Asyncio (Network I/O) ---")
    start_time = time.time()
    # สร้าง Task การดึงข้อมูลพร้อมๆ กัน
    tasks = [fetch_data_from_api(i) for i in range(num_items)]
    results = await asyncio.gather(*tasks)
    print(f"Asyncio took {time.time() - start_time:.2f} seconds")
    return results


# 2. Threading - Disk I/O Simulation (Saving Data)
def save_data_to_file(data):
    thread_name = threading.current_thread().name
    print(f"Thread [{thread_name}]: Saving {data} to disk...")
    time.sleep(1) # จำลองระยะเวลาการเขียนไฟล์ (Disk I/O)
    print(f"Thread [{thread_name}]: Saved {data}")

def run_threading_tasks(data_list):
    print("\n--- Starting Threading (Disk I/O) ---")
    start_time = time.time()
    threads = []
    # เปิด Thread สำหรับแต่ละการบันทึกข้อมูล
    for data in data_list:
        t = threading.Thread(target=save_data_to_file, args=(data,))
        threads.append(t)
        t.start()
        
    # รอให้ทุก Thread ทำงานเสร็จ
    for t in threads:
        t.join()
    print(f"Threading took {time.time() - start_time:.2f} seconds")


# 3. Multiprocessing Pool - CPU Bound Task (Processing Data)
def calculate_prime_factors(n):
    # จำลองงานที่ใช้การประมวลผล CPU หนักๆ (CPU-bound)
    print(f"Process [{os.getpid()}]: Calculating prime factors for {n}...")
    i = 2
    factors = []
    num = n
    while i * i <= num:
        if num % i:
            i += 1
        else:
            num //= i
            factors.append(i)
    if num > 1:
        factors.append(num)
    print(f"Process [{os.getpid()}]: Done calculating for {n} -> Factors: {factors}")
    return factors

def run_process_pool_tasks(numbers):
    print("\n--- Starting Process Pool (CPU Bound) ---")
    start_time = time.time()
    # ใช้ Pool ในการจัดการ Process ตามจำนวน CPU Core ที่มี
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # map จะกระจายงานใน list ให้แต่ละ process ไปช่วยกันทำ
        results = pool.map(calculate_prime_factors, numbers)
    print(f"Process Pool took {time.time() - start_time:.2f} seconds")
    return results


if __name__ == "__main__":
    # ปรับใช้เพื่อป้องกันปัญหาการรันบน Windows (เฉพาะ Multiprocessing)
    multiprocessing.freeze_support()
    
    num_items = 5
    
    # รันส่วนที่ 1: Asyncio
    fetched_data = asyncio.run(run_async_tasks(num_items))
    
    # รันส่วนที่ 2: Threading
    run_threading_tasks(fetched_data)
    
    # รันส่วนที่ 3: Process Pool
    # ตัวเลขขนาดใหญ่เพื่อนำมาคำนวณแยกตัวประกอบ
    large_numbers = [600851475143, 89234892345, 999999990001, 1234567890123, 9876543210987]
    run_process_pool_tasks(large_numbers)
    
    print("\nAll tasks completed successfully!")
