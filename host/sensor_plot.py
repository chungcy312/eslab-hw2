import socket
import threading
import queue
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


PORT = 8002

data_queue = queue.Queue()

motion_queue = queue.Queue()
motion_times = deque(maxlen=100)
motion_lines = []

time_data = deque(maxlen=200)
x_data = deque(maxlen=200)
y_data = deque(maxlen=200)
z_data = deque(maxlen=200)


def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)

    print(f"TCP server is listening on port {PORT}...")
    connection, address = server.accept()
    print("STM32 connected from:", address)

    # 讓原本等待接收資料的 STM32 範例也能開始傳送
    connection.sendall(b"start\n")

    buffer = b""

    while True:
        received = connection.recv(1024)

        if not received:
            print("STM32 disconnected.")
            break

        buffer += received

        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)

            try:
                text = line.decode("utf-8").strip()
                values = text.split(",")

                if len(values) == 2 and values[0] == "MOTION":
                    motion_time = float(values[1]) / 1000.0
                    motion_queue.put(motion_time)

                    print("Significant motion detected at", values[1], "ms")
                    continue

                if len(values) != 4:
                    continue

                timestamp = float(values[0])
                x = float(values[1])
                y = float(values[2])
                z = float(values[3])

                data_queue.put((timestamp, x, y, z))

            except ValueError:
                print("Ignored:", line)

    connection.close()
    server.close()


def update_plot(frame):
    while not data_queue.empty():
        timestamp, x, y, z = data_queue.get()

        time_data.append(timestamp / 1000.0)
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

    while not motion_queue.empty():
        motion_times.append(motion_queue.get())

    if len(time_data) > 0:
        latest_time = time_data[-1]

        while time_data and time_data[0] < latest_time - 10:
            time_data.popleft()
            x_data.popleft()
            y_data.popleft()
            z_data.popleft()
        
        while motion_times and motion_times[0] < latest_time - 10:
            motion_times.popleft()

    line_x.set_data(time_data, x_data)
    line_y.set_data(time_data, y_data)
    line_z.set_data(time_data, z_data)

    if len(time_data) > 1:
        axis.set_xlim(
            max(0, time_data[-1] - 10),
            time_data[-1]
        )

        all_values = list(x_data) + list(y_data) + list(z_data)
        minimum = min(all_values) - 100
        maximum = max(all_values) + 100

        if minimum != maximum:
            axis.set_ylim(minimum, maximum)

        for marker in motion_lines:
            marker.remove()

    motion_lines.clear()

    for motion_time in motion_times:
        marker = axis.axvline(
            motion_time,
            color="red",
            linestyle="--",
            linewidth=1.5
        )

        motion_lines.append(marker)

    return line_x, line_y, line_z


threading.Thread(target=tcp_server, daemon=True).start()

figure, axis = plt.subplots()

line_x, = axis.plot([], [], label="X")
line_y, = axis.plot([], [], label="Y")
line_z, = axis.plot([], [], label="Z")

axis.set_title("STM32 LSM6DSL Accelerometer")
axis.set_xlabel("Time (seconds)")
axis.set_ylabel("Acceleration (mg)")
axis.legend()
axis.grid(True)

animation = FuncAnimation(
    figure,
    update_plot,
    interval=100,
    cache_frame_data=False
)

plt.show()
