import random
import numpy as np

class BankQueue:
    def __init__(self):
        self.queue = []  # 等待队列
        self.current_time = 0
        self.total_wait_time = 0
        self.served_customers = 0

    def simulate(self, simulation_time):
        # 模拟参数
        arrival_rate = 0.1  # 平均每分钟到达的顾客数
        service_rate = 0.12  # 平均每分钟服务的顾客数
        
        while self.current_time < simulation_time:
            # 生成顾客到达
            if random.random() < arrival_rate:
                service_time = np.random.exponential(1/service_rate)
                self.queue.append(service_time)
            
            # 处理队列中的顾客
            if self.queue:
                self.queue[0] -= 1
                if self.queue[0] <= 0:
                    self.queue.pop(0)
                    self.served_customers += 1
                    
            self.total_wait_time += len(self.queue)
            self.current_time += 1
    
    def get_average_wait_time(self):
        return self.total_wait_time / self.served_customers if self.served_customers > 0 else 0

# 运行模拟
bank = BankQueue()
bank.simulate(1000)  # 模拟1000分钟
print(f"平均等待时间: {bank.get_average_wait_time():.2f} 分钟")
print(f"服务的顾客数: {bank.served_customers}")