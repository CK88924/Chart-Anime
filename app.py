from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from db import fetch_data_from_mysql, hash_data
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # 允許跨域

# 後台線程：檢測數據變更並推送到 WebSocket
def background_thread():
    last_hash = None
    while True:
        # 查詢數據庫
        query = "SELECT id, product_name, product_quantity, updated_at FROM products ORDER BY id ASC"
        current_data = fetch_data_from_mysql(query)
        current_hash = hash_data(current_data)

        # 如果數據發生變化，通過 WebSocket 推送
        if current_hash != last_hash:
            last_hash = current_hash
            print("Debug: Data changed, pushing update via WebSocket")
            socketio.emit('update_data', {'data': current_data}, namespace='/')

        time.sleep(2)  # 每2秒檢查一次數據變化

# 啟動後台線程
threading.Thread(target=background_thread, daemon=True).start()

# 路由：主頁
@app.route('/')
def index():
    query_all = "SELECT id, product_name, product_quantity, updated_at FROM products ORDER BY id ASC"
    table_data = fetch_data_from_mysql(query_all)

    query_chart = "SELECT product_name, product_quantity FROM products ORDER BY id ASC"
    chart_data = fetch_data_from_mysql(query_chart)

    return render_template('index.html', products=table_data, chart_data=chart_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
