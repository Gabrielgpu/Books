import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_email(isbn, numero):
    remetente = ''
    senha = ''
    destinatarios = ['']

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = ', '.join(destinatarios)
    mensagem['Subject'] = f'Baixa de produtos'

    corpo = f'Olá,\n\nProduto removido do sistema, possível erro, Não foi localizado na lista de pedidos. ISBN: {isbn} NUMERO: {numero}.'
    mensagem.attach(MIMEText(corpo, 'plain'))

    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente, senha)
    servidor_smtp.sendmail(remetente, destinatarios, mensagem.as_string())
    servidor_smtp.quit()
    print(f"E-mail enviado. Produto fora da lista de pedidos")

