import psutil
import time
import platform
import datetime

class SystemMonitor:

    def get_cpu(self):
        return psutil.cpu_percent(interval=1)

    def get_ram(self):
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent
        }

    def get_disk(self):
        disk = psutil.disk_usage("/")
        return {
            "total": disk.total,
            "used": disk.used,
            "percent": disk.percent
        }

    def get_network(self):
        net = psutil.net_io_counters()
        return {
            "sent": net.bytes_sent,
            "received": net.bytes_recv
        }

    def get_processes(self, limit=10):
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except:
                pass
        procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return procs[:limit]

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
            return f"Process {pid} terminated."
        except Exception as e:
            return f"Error: {e}"

    def get_uptime(self):
        boot = psutil.boot_time()
        uptime = time.time() - boot
        return str(datetime.timedelta(seconds=int(uptime)))
