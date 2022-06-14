import smtplib, ssl, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ARCHIVO = 'destinatarios.txt'
REMITENTE = ''
CONTRASENA = ''


def abrir_archivo(ARCHIVO:str):
    lista_destinatarios = list()

    with open(ARCHIVO, 'r') as archivo:
        lista_mails = csv.reader(archivo)
        for mail in lista_mails:
            lista_destinatarios.append(mail[0])

    return lista_destinatarios


def servidor(destinatario:str, mensaje, contexto):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as server:
        server.login(REMITENTE, CONTRASENA)
        server.sendmail(REMITENTE, destinatario, mensaje.as_string())
        server.quit()


def generar_html(texto_mensaje:str):
    html = f""" 
    <html>
    <body>
        <p>{texto_mensaje}</p>
    </body>
    </html>
    """
    return html


def generar_mensaje(lista_destinatarios:list, asunto:str):
    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = asunto
    mensaje['From'] = REMITENTE
    for destinatario in lista_destinatarios:
        mensaje['To'] = destinatario
    
    return mensaje


def enviar_correo(lista_destinatarios:list, asunto:str, texto_mensaje:str):
    
    mensaje = generar_mensaje(lista_destinatarios, asunto)
    html = generar_html(texto_mensaje)
    parte_html = MIMEText(html, 'html')
    mensaje.attach(parte_html)
    contexto = ssl.create_default_context()
    servidor(lista_destinatarios, mensaje, contexto)
    
    
def main():
    asunto = 'Mail desde Python'
    texto_mensaje = """ 
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus maiores, iure animi repellat sit in labore minima neque? Voluptate voluptatem quisquam dolores minima nisi porro perspiciatis temporibus nemo ipsam necessitatibus officiis distinctio omnis quod at dolorum fuga, numquam debitis magni optio in provident id nulla iure consequatur? Similique distinctio excepturi provident aliquam tenetur minus rerum magnam accusantium error nesciunt consequatur velit, cumque repellat maxime soluta, magni nam omnis reprehenderit incidunt! Voluptatum labore quas repudiandae dolor porro debitis, voluptate quasi totam obcaecati suscipit earum dolorum culpa officiis, sit dolorem ex dolore odio, vero iste ipsam ipsum asperiores. Maiores, repudiandae eaque. Eligendi aperiam, molestiae cupiditate enim fugiat incidunt, distinctio perspiciatis ipsum itaque saepe eveniet officiis in corrupti asperiores, excepturi eos quasi odio magnam reprehenderit iusto rem temporibus inventore aspernatur? Enim omnis iste atque odio dolore! Excepturi, deserunt quaerat veritatis ducimus voluptatum est tempora impedit cum voluptas. Corporis perferendis facere cum veritatis temporibus.
    """
    lista_destinatarios = abrir_archivo(ARCHIVO)
    enviar_correo(lista_destinatarios, asunto, texto_mensaje)

    print('Correos enviados')
    
main()