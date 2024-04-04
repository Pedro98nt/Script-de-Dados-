import platform
import psutil
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QTextEdit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SystemInfoWindow(QMainWindow):
    def _init_(self):
        super()._init_()

        self.setWindowTitle("System Information")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.cpu_mem_disk_widget = QWidget()
        self.os_network_widget = QWidget()

        self.tab_widget.addTab(self.cpu_mem_disk_widget, "CPU/Memória/Disco")
        self.tab_widget.addTab(self.os_network_widget, "Sistema Operacional/Rede")

        self.cpu_mem_disk_layout = QVBoxLayout()
        self.cpu_mem_disk_widget.setLayout(self.cpu_mem_disk_layout)

        self.os_network_layout = QVBoxLayout()
        self.os_network_widget.setLayout(self.os_network_layout)

        self.create_cpu_mem_disk_info()
        self.create_os_network_info()

        self.generate_report_button = QPushButton("Gerar Relatório PDF")
        self.layout.addWidget(self.generate_report_button)
        self.generate_report_button.clicked.connect(self.generate_report)

    def create_cpu_mem_disk_info(self):
        cpu_info = {
            "Nome do Processador": psutil.cpu_info().brand,
            "Arquitetura": psutil.cpu_info().arch,
            "Palavra (bits)": psutil.cpu_info().bits,
            "Núcleos Físicos": psutil.cpu_count(logical=False),
            "Núcleos Lógicos": psutil.cpu_count(logical=True)
        }

        mem_info = {
            "Total de Memória": round(psutil.virtual_memory().total / (1024 ** 3), 2),  # Em GB
            "Memória Disponível": round(psutil.virtual_memory().available / (1024 ** 3), 2),  # Em GB
            "Porcentagem de Memória Utilizada": psutil.virtual_memory().percent
        }

        disk_info = {
            "Total de Espaço em Disco": round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # Em GB
            "Espaço Disponível em Disco": round(psutil.disk_usage('/').free / (1024 ** 3), 2),  # Em GB
            "Porcentagem de Disco Utilizado": psutil.disk_usage('/').percent
        }

        self.add_info_to_layout(cpu_info, self.cpu_mem_disk_layout)
        self.add_info_to_layout(mem_info, self.cpu_mem_disk_layout)
        self.add_info_to_layout(disk_info, self.cpu_mem_disk_layout)

    def create_os_network_info(self):
        os_info = {
            "Sistema Operacional": platform.system(),
            "Versão": platform.version(),
            "Versão do Windows": platform.win32_ver()[1] if platform.system() == "Windows" else "N/A"
        }

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        network_info = {"Endereço IP": ip_address}

        self.add_info_to_layout(os_info, self.os_network_layout)
        self.add_info_to_layout(network_info, self.os_network_layout)

    def add_info_to_layout(self, info_dict, layout):
        for key, value in info_dict.items():
            label = f"{key}: {value}"
            text_edit = QTextEdit()
            text_edit.setPlainText(label)
            text_edit.setReadOnly(True)
            layout.addWidget(text_edit)

    def generate_report(self):
        cpu_info = {
            "Nome do Processador": psutil.cpu_info().brand,
            "Arquitetura": psutil.cpu_info().arch,
            "Palavra (bits)": psutil.cpu_info().bits,
            "Núcleos Físicos": psutil.cpu_count(logical=False),
            "Núcleos Lógicos": psutil.cpu_count(logical=True)
        }

        mem_info = {
            "Total de Memória": round(psutil.virtual_memory().total / (1024 ** 3), 2),  # Em GB
            "Memória Disponível": round(psutil.virtual_memory().available / (1024 ** 3), 2),  # Em GB
            "Porcentagem de Memória Utilizada": psutil.virtual_memory().percent
        }

        disk_info = {
            "Total de Espaço em Disco": round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # Em GB
            "Espaço Disponível em Disco": round(psutil.disk_usage('/').free / (1024 ** 3), 2),  # Em GB
            "Porcentagem de Disco Utilizado": psutil.disk_usage('/').percent
        }

        os_info = {
            "Sistema Operacional": platform.system(),
            "Versão": platform.version(),
            "Versão do Windows": platform.win32_ver()[1] if platform.system() == "Windows" else "N/A"
        }

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        network_info = {"Endereço IP": ip_address}

        pdf_filename = "system_info_report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 800, "Relatório de Informações do Sistema")

        y = 750
        for info_dict in [cpu_info, mem_info, disk_info, os_info, network_info]:
            for key, value in info_dict.items():
                text = f"{key}: {value}"
                c.drawString(100, y, text)
                y -= 20

        c.save()
        print(f"Relatório gerado com sucesso: {pdf_filename}")

if _name_ == "_main_":
    app = QApplication([])
    window = SystemInfoWindow()
    window.show()
    app.exec_()