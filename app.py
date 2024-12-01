from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from db import fetch_data_from_mysql, hash_data
from mq_utils import publish_message, consume_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # 允許跨域

# 後台線程：監聽消息隊列並推送更新到 WebSocket
def mq_listener():
    def handle_message(data):
        print(f"Debug: Pushing data to WebSocket: {data}")
        socketio.emit('update_data', {'data': data}, namespace='/')  # 推送數據到前端

    consume_messages(handle_message)

# 後台線程：檢測數據變更並發布到消息隊列
def background_thread():
    last_hash = None
    while True:
        query = "SELECT id, product_name, product_quantity, updated_at FROM products"
        current_data = fetch_data_from_mysql(query)
        current_hash = hash_data(current_data)

        if current_hash != last_hash:
            last_hash = current_hash
            print(f"Debug: Publishing message: {current_data}")
            publish_message(current_data)

# 啟動監聽線程
threading.Thread(target=mq_listener, daemon=True).start()
threading.Thread(target=background_thread, daemon=True).start()

# 路由：主頁
@app.route('/')
def index():
    query_all = "SELECT id, product_name, product_quantity, updated_at FROM products"
    table_data = fetch_data_from_mysql(query_all)

    query_chart = "SELECT product_name, product_quantity FROM products"
    chart_data = fetch_data_from_mysql(query_chart)

    return render_template('index.html', products=table_data, chart_data=chart_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
