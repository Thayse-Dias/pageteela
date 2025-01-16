import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import sqlite3

class Application():
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.janela_login()
        self.janela.mainloop()
        
    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):    
        self.janela.geometry("700x400") 
        self.janela.title("Teela - Manutenção Hoteleira") 
        self.janela.resizable(False, False)
        
    def janela_login(self):
        lb_title = ctk.CTkLabel(master=self.janela, text="Bem Vindo(a) ao Teela\n Soluções em Manutenção Hoteleira", 
                                font=("Century Gothic bold", 18), text_color="#00B0F0").place(x=30, y=150)
        
        login_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        login_frame.pack(side="right")

        label_tt = ctk.CTkLabel(master=login_frame, text="Faça seu Login", font=("Century Gothic bold", 20)).place(x=100, y=10)

        self.username_entry = ctk.CTkEntry(master=login_frame, placeholder_text= "Nome do Usuário", width=300, 
                                      font=("Century Gothic bold", 14))
        self.username_entry.place(x=25, y=80)

        username_label = ctk.CTkLabel(master=login_frame, text="*O campo nome do usuário é de caráter obrigatório.", text_color="white", 
                                    font=("Century Gothic bold", 10)).place(x=25, y=110)

        self.password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Senha do Usuário", show="*", width=300, 
                                    font=("Century Gothic bold", 14))
        self.password_entry.place(x=25, y=160)

        password_label = ctk.CTkLabel(master=login_frame, text="*O campo senha de usuário é de caráter obrigatório.", text_color="white", 
                                    font=("Century Gothic bold", 10)).place(x=25, y=190)

        checkbox = ctk.CTkCheckBox(master=login_frame, text= "Mantenha-me conectado").place(x=25, y=230)

        login_Button = ctk.CTkButton(master=login_frame, text= "Entrar", width=300, command=self.login).place(x=25, y=280)

        register_label = ctk.CTkLabel(master=login_frame, text= "Não possue conta?").place(x=25, y=320)
        
        register_button = ctk.CTkButton(master=login_frame, text= "Cadastre-se", width=150, 
                                        fg_color="green", hover_color="#2D9334",command=self.tela_register).place(x=175, y=320)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conexao.close()

        if user:
            self.janela.withdraw()  # Oculta a janela de login
            os = OrdemDeServico(self.janela)  # Passa a referência
            os.run()  # Chama o método
          
    def tela_register(self):
        # Remover o frame de login
        login_frame = self.janela.children.get('!ctkframe')  # Obtem o frame de login
        login_frame.pack_forget()
        
        # Criando a tela de cadastro de usuários
        rg_frame = ctk.CTkFrame(master=janela, width=350, height=396)
        rg_frame.pack(side=RIGHT)
        
        label_tt = ctk.CTkLabel(master=rg_frame, text="Cadastro de Usuário", font=("Century Gothic bold", 20)).place(x=100, y=10)
        
        span = ctk.CTkLabel(master=rg_frame, text="*Preencha todos os campos com dados corretos", font=("Century Gothic bold", 11)).place(x=25, y=50)
        
        self.register_username_entry = ctk.CTkEntry(master=rg_frame, placeholder_text= "Nome do Usuário", width=300, 
                                      font=("Century Gothic bold", 14))
        self.register_username_entry.place(x=25, y=85)
        
        self.register_email_entry = ctk.CTkEntry(master=rg_frame, placeholder_text="E-mail do Usuário", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_email_entry.place(x=25, y=125)
        
        self.register_password_entry = ctk.CTkEntry(master=rg_frame, placeholder_text="Senha do Usuário", show="*", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_password_entry.place(x=25, y=165)
        
        self.register_confirme_entry = ctk.CTkEntry(master=rg_frame, placeholder_text="Confirme sua senha", show= "*", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_confirme_entry.place(x=25, y=205)

        back_Button = ctk.CTkButton(master=rg_frame, text= "Voltar", width=140, fg_color="gray", command=lambda: self.back(rg_frame, login_frame)).place(x=25, y=285)
       
        save_Button = ctk.CTkButton(master=rg_frame, text= "Salvar", width=140, command=self.save_user).place(x=185, y=285)
            
        checkbox = ctk.CTkCheckBox(master=rg_frame, text= "Aceito todos os Termos e Política", 
                                   font=("Century Gothic bold", 10)).place(x=25, y=350)

    def back(self, rg_frame, login_frame):
        # Remover o frame de Cadastro
        rg_frame.pack_forget()
        # Devolvendo o frame de login
        login_frame.pack(side=RIGHT)

    def save_user(self):
        username = self.register_username_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        conf_password = self.register_confirme_entry.get()

        if password != conf_password:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        
        # Conectar ao banco de dados e inserir os dados
        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()
        
        # Inserir dados na tabela
        cursor.execute("INSERT INTO users (Username, Email, Password, ConfPassword) VALUES (?, ?, ?, ?)", 
                       (username, email, password, conf_password))
        
        conexao.commit()  # Confirma as alterações
        conexao.close()   # Fecha a conexão
        
        messagebox.showinfo(title="Estado do Cadastro", message="Parabéns! Usuário cadastrado com sucesso.")       

class OrdemDeServico:
    def __init__(self, janela):  # Adicione o parâmetro 'janela'
        self.janela_os = ctk.CTk()  # Aqui você pode usar 'janela' se desejar
        self.janela_os.geometry("700x400")
        self.janela_os.title("Ordem de Serviço")

        # Label de boas-vindas
        label_os = ctk.CTkLabel(master=self.janela_os, text="Bem-vindo à Ordem de Serviço", font=("Century Gothic bold", 20))
        label_os.pack(pady=20)

        
    def run(self):
        self.janela_os.mainloop()

        # Campo de Data de Abertura
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.entry_data_atual = ctk.CTkEntry(master=self.janela_os,
                                                width=300,
                                                font=("Century Gothic bold", 12),
                                                state="readonly")
        self.entry_data_atual.place(x=25, y=70)
        self.entry_data_atual.insert(0, data_atual)

        # Campo de Local de Atendimento
        self.entry_local_atendimento = ctk.CTkEntry(master=self.janela_os, placeholder_text="Local de Atendimento", width=650,
                                                     font=("Century Gothic bold", 12))
        self.entry_local_atendimento.place(x=25, y=120)

        # Campo de Descrição do Serviço
        self.entry_descricao_servico = ctk.CTkEntry(master=self.janela_os, placeholder_text="Descrição do Serviço", width=650,
                                                     font=("Century Gothic bold", 12))
        self.entry_descricao_servico.place(x=25, y=170)

        # Campo de Status
        label_status = ctk.CTkLabel(master=self.janela_os, text="Status:")
        label_status.place(x=25, y=210)

        self.status_var = ctk.StringVar(value="Aberto")
        self.menu_status = ctk.CTkOptionMenu(master=self.janela_os, variable=self.status_var,
                                              command=self.update_status_color,
                                              values=["Aberto", "Concluído"])
        self.menu_status.place(x=25, y=240)
        self.update_status_color(self.status_var.get())

        # Campo de Setor
        label_setor = ctk.CTkLabel(master=self.janela_os, text="Setor:")
        label_setor.place(x=25, y=270)
        self.setor_var = ctk.StringVar(value="Ger.Operacional")
        self.menu_setor = ctk.CTkOptionMenu(master=self.janela_os, variable=self.setor_var,
                                             values=["Ger.Operacional", "Recepção", "Governança", "Manutenção", "A&B", "Eventos", "TI"])
        self.menu_setor.place(x=25, y=300)
        self.menu_setor.configure(fg_color="gray")

        label_observacoes = ctk.CTkLabel(master=self.janela_os, text="Observações:").place(x=210, y=210)

        self.entry_observacoes = ctk.CTkEntry(master=self.janela_os, width=465, height=90, font=("arial", 16),
                                               border_color="#aaa", border_width=2, fg_color="transparent")
        self.entry_observacoes.place(x=210, y=240)
    
        service_Button = ctk.CTkButton(master=self.janela_os, text= "Salvar", width=140).place(x=520, y=350)
   

    # Iniciar o loop principal
        self.janela_os.mainloop()
    
def update_status_color(self, value):
    if value == "Aberto":
        self.menu_status.configure(fg_color="red")
    elif value == "Concluído": 
        self.menu_status.configure(fg_color="green")
        
          
# Cria ou conecta ao banco de dados
conexao = sqlite3.connect("Sistema.db")
cursor = conexao.cursor()

# Cria a tabela de usuários caso não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    conf_password TEXT NOT NULL
)""")

# Cria a tabela de chamados caso não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data_atual TEXT NOT NULL,
    local_atendimento TEXT NOT NULL,
    descricao_servico TEXT NOT NULL,
    status TEXT NOT NULL,
    setor TEXT NOT NULL,
    observacoes TEXT NOT NULL  
)""")

conexao.commit()  
conexao.close()   # Fecha a conexão

# Função para inserir dados na tabela de chamados
def inserir_dados(data_atual, local_atendimento, descricao_servico, status, setor, observacoes):
    # Conectar ao banco de dados e inserir os dados
    conexao = sqlite3.connect("Sistema.db")
    cursor = conexao.cursor()
    
    # Inserir dados na tabela de chamados
    cursor.execute("INSERT INTO chamados (data_atual, local_atendimento, descricao_servico, status, setor, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (data_atual, local_atendimento, descricao_servico, status, setor, observacoes))
    
    conexao.commit()  # Confirma as alterações
    conexao.close()   # Fecha a conexão
    
    messagebox.showinfo(title="Estado do Cadastro", message="Parabéns! Ordem de serviço gerada com sucesso.")


Application()

