# Logic hoạt động
- Khi mới khởi động, hiển thị danh sách các loại rau với dấu > ở bên trái để trỏ tới
- Dùng phím lên trên, xuống dưới để lựa chọn
- Phím OK để chọn và vào chế độ đọc
- Phím RESET để bắt đầu lại

## Chế độ hoạt động
- Hiển thị LCD, dòng 1 là độ ẩm và nhiệt độ, dòng 2 là chỉ số NPK trong đất
- Các thiết bị như máy bơm, LED, chuông ở trạng thái tắt

## Chức năng bơm nước
- Điều kiện kích hoạt: độ ẩm dưới mức sinh trưởng tốt của cây + nhiệt độ thích hợp để tưới (10 - 30 độ C)
- Điều kiện thoát: khi đã đủ độ ẩm
Luồng hoạt động:
- Bật máy bơm, giả sử mỗi giây +1 % độ ẩm
- Trong khi đang bơm, để đảm bảo dữ liệu không bị lộn xộn, dừng đọc dữ liệu ngẫu nhiên từ giả lập độ ẩm và nhiệt độ
- Sau khi bơm xong, tiếp tục đọc dữ liệu từ giả lập

## Chức năng báo hiệu ngập úng
- Điều kiện kích hoạt: độ ẩm lớn hơn mức sinh trưởng tốt của cây
- Điều kiện thoát: độ ẩm nước ở mức sinh trưởng tốt cho cây hoặc đang báo mà ấn phím OK
Luồng hoạt động:
- Hiển thị ra màn hình thông báo "Độ ẩm cao, xin hãy rút nước" thay vì các thông số
- Bật chuông
- Mỗi giây giả sử -1% độ ẩm
- Trong khi đang bật chuông, dừng đọc data độ ẩm đất và nhiệt độ
- Sau khi xong đọc lại bth

## Chức năng báo hiệu NPK thấp
- Điều kiện kích hoạt: khi có 1 trong 3 thông số NPK dưới ngưỡng sinh trưởng tốt của cây
- Điều kiện thoát: cần bật máy bơm hoặc còi hoặc bấm OK
Luồng hoạt động:
- Dừng đọc data NPK
- Bật LED
- Hiển thị ra LCD số lượng NPK cần bón thêm cho cây
- Sau khi kết thúc đọc NPK và hiển thị thông số như bth
