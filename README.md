# Chart Anime

## 問題描述

在開發過程中，我們發現以下問題可能導致應用程式運行異常：

1. **Flask 無法即時檢測錯誤狀態**  
   Flask 作為靜態資源，當連線中斷或資料庫相關問題發生時（例如資料庫或資料表不存在），它不會主動報錯。此情況會導致頁面維持上一筆資料的表格與圖表樣式，而無法更新至最新狀態。

2. **RabbitMQ 與 Flask 中斷**  
   若上述錯誤未解決，RabbitMQ 與 Flask 的連線可能中斷，導致即使資料庫或資料表修復後，依然無法進行資料推播與頁面渲染。

---

## 解決方案

為了解決這些問題，我們設計了一個簡單的解決方案：  
在發生錯誤時，透過執行以下指令手動重啟伺服器，進行資料初始化，確保應用程式恢復正常運行。

```bash
python app.py
