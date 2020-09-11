from django.db import models
from datetime import date
from django.utils import timezone

class Customer(models.Model):
    CATEGORY = (
        ('Khách lẻ', 'Khách lẻ'),
        ('Khách tháng', 'Khách tháng'),
        ('IDT mới', 'IDT mới'),
        ('IDT cũ', 'IDT cũ'),
        ('Khác', 'Khác'),
    )
    CITY = (
        ('Miền Bắc','Miền Bắc'),
        ('Miền Nam','Miền Nam'),
        ('Miền Trung','Miền Trung'),
        ('Khác','Khác'),
    )
    DATEFILTER = (
        (str(date.today().month),'Tháng này'),
        (str(date.today().month-1),'Tháng trước'),
    )
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Ngày tạo')
    search_date = models.CharField(max_length=30,verbose_name='Ngày tìm kiếm',default=(str(timezone.datetime.now().day)+'.'+ str(timezone.datetime.today().month) +'.'+ str(timezone.datetime.today().year)))
    #Kinh doanh nhập vào
    name = models.CharField(max_length=60, null=True,verbose_name='Khách hàng',unique=True)
    popular_info = models.TextField(max_length=1000, null=False,verbose_name='Thông tin chung',default='')
    private_info = models.TextField(max_length=1000, null=False, verbose_name='Thông tin riêng',default='')
    customer_type = models.CharField(max_length=200, null=True, choices=CATEGORY, default='Khách lẻ',verbose_name='Loại KH')
    city = models.CharField(max_length=200, null=True, choices=CITY, default='Miền Nam',verbose_name='Thành phố')
    #Kinh doanh điều chỉnh
    status = models.BooleanField(default=False,verbose_name='Tình Trạng làm việc')
    
    def __str__(self):
        return  self.search_date + ' | ' + self.name
        
    def tongtien_receipt(self):
        return sum([pt.tongtien_order() for pt in self.receipt_set.all()])

    def tongtien_receipt_unpaid(self):
        return sum([pt.phaithu() for pt in self.receipt_set.filter(payment_status="False")])
    
class Receipt(models.Model):
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Ngày tạo')
    search_date = models.CharField(max_length=30,verbose_name='Ngày tìm kiếm',default=(str(timezone.datetime.now().day)+'.'+ str(timezone.datetime.today().month) +'.'+ str(timezone.datetime.today().year)))
    end_date = models.DateTimeField(blank=True,null=True,verbose_name='Ngày kết thúc')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    #Nhập vào
    name = models.CharField(max_length=60, null=True,verbose_name='Tên phiếu thu',default='Phiếu thu ')
    deposit = models.IntegerField(default=0,verbose_name="Đã thu")
    popular_info = models.TextField(max_length=1000, null=True,verbose_name='Lưu ý',default='- Tổng tiền chốt khách: \n- Deadline: ')
    #Điều chỉnh
    status = models.BooleanField(default=False,verbose_name='Xác nhận thực hiện')
    payment_status = models.BooleanField(default=False,verbose_name='Tình Trạng thanh toán')
    send_status = models.BooleanField(default=False,verbose_name='Trả đơn')
    approved_status = models.BooleanField(default=False,verbose_name='Duyệt thu')


    def __str__(self):
        return  self.search_date + ' | ' + self.customer.name + ' | ' + self.name 

    def tongtien_order(self):
        return sum([dh.tongtien() for dh in self.order_set.all()])

    def phaithu(self):
        return self.tongtien_order() - self.deposit

        
class Order(models.Model):
    CATEGORY = (
        ('Dịch thuật', 'Dịch thuật'),
        ('Dịch video', 'Dịch video'),
        ('Công chứng', 'Công chứng'),
        ('Sao y', 'Sao y'),
        ('HPHLS', 'HPHLS'),
        ('Ship', 'Ship'),
        ('VAT', 'VAT'),
        ('Khác', 'Khác'),
    )
    LANGUAGE = (
        ('Tiếng Anh', 'Tiếng Anh'),
        ('Tiếng Trung', 'Tiếng Trung'),
        ('Tiếng Nhật', 'Tiếng Nhật'),
        ('Tiếng Hàn', 'Tiếng Hàn'),
        ('Tiếng Pháp', 'Tiếng Pháp'),
        ('Tiếng Đức', 'Tiếng Đức'),
        ('Tiếng Nga', 'Tiếng Nga'),

    )
    UNIT = (
        ('Trang', 'Trang'),
        ('Bộ', 'Bộ'),
        ('Lần', 'Lần'),
        ('Phút', 'Phút'),
    )
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Ngày tạo')
    search_date = models.CharField(max_length=30,verbose_name='Ngày tìm kiếm',default=(str(timezone.datetime.now().day)+'.'+ str(timezone.datetime.today().month) +'.'+ str(timezone.datetime.today().year)))
    receipt = models.ForeignKey(Receipt, null=True, on_delete=models.CASCADE)
    #Tùy biến
    order_type = models.CharField(max_length=200, null=True, choices=CATEGORY, default='Dịch thuật',verbose_name="Loại Đơn hàng")
    language_type = models.CharField(max_length=200, blank=True, choices=LANGUAGE,verbose_name="Loại Ngôn ngữ")
    name = models.CharField(max_length=60, blank=True,verbose_name='Tên tài liệu/ Dịch vụ')
    quantity = models.IntegerField(default=0,verbose_name="Số lượng")
    unit = models.CharField(max_length=20,choices=UNIT, null=True,verbose_name="Đơn vị")
    price = models.IntegerField(default=0,verbose_name="Đơn giá")
    popular_info = models.TextField(max_length=1000, blank=True,null=True,verbose_name='Lưu ý',default='')

    def __str__(self):
        return  self.search_date + ' | ' + self.receipt.customer.name +  ' *** ' + self.order_type + ' ' + self.language_type + ' | ' + self.name + ' | ' + str(self.quantity * self.price)
    def tongtien(self):
        return self.quantity * self.price