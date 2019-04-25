import tkinter as tk
import sys,urllib.request,time,os,zipfile,hashlib,unrar,rarfile
import base64 as b64
from tkinter import filedialog,messagebox,ttk
from urllib.request import urlopen
from threading import Thread
from pathlib import Path

root = tk.Tk()
root.title("Subdl")
root.withdraw()

DOWNLOAD_DELAY_S = 2 # segundos de espera antes de baixar a proxima legenda

def GetBaixada(jaBaixadas,NomeArq):
    for jbi in jaBaixadas:
        if NomeArq == jbi[0]:
            return jbi


def ChecarBaixadas():
    bfLista = []
    bfDir = os.path.join(o_dir.parents[0],"baixadas.txt")
    if not os.path.exists(bfDir):
        return

    try:
        with open(bfDir,"r") as bf:
            bfLinhas = bf.readlines()
        for bfLinha in bfLinhas:
            bfLista.append(bfLinha.split(";"))
        return bfLista

    except Exception as e:
        return

def LimparResiduos(zipLista):

    print("[  *  ] Iniciando procedimento de limpeza dos residuos...")

    statuslbl.set("Removendo resíduos..." )

    for zip_item in zipLista:
        if zip_item[0][-4:] == ".srt": continue;
        zip_dir = os.path.join(o_dir,zip_item[0])
        if os.path.exists(zip_dir):
            os.remove(zip_dir)
            sys.stdout.write("\r[ ... ] Removendo {0}...".format(zip_item[0]))
            sys.stdout.flush()
        print("OK")
    statuslbl.set("Resíduos removidos !" )
    print("[  *  ] Residuos removidos.")
    time.sleep(3)
    print("\nFim.")
    statuslbl.set("Fim." )

def Extrair(zipLista):
    print("[  *  ] Iniciando procedimento de extração...")
    for zip_item in zipLista: #zip nome



        if zip_item[0][-4:] == ".srt": continue;

        if zip_item[0][-4:] == ".rar": # extrai RAR

            with rarfile.RarFile(os.path.join(o_dir,zip_item[0]),"r") as rar_arq:


                for srt in rar_arq.infolist():



                    if srt.filename[-4:] != ".srt": continue;

                    if(len(srt.filename) > 36):
                        arqNomelbl.set(srt.filename[:26]+"..."+srt.filename[-10:])
                    else:
                        arqNomelbl.set(srt.filename)

                    progress["value"] = 0
                    progress["maximum"] = srt.file_size
                    arqAlbl.set(" 0 / %s" %(srt.file_size))

                    SRT_PARTE = 200 * 1024
                    with rar_arq.open(srt) as srt_dados:



                        #encurta diretorio se n for o suficiente
                        MAX_LEN_SRT_NOME = (247-len(os.path.dirname(os.path.join(o_dir, srt.filename))))
                        SRT_FILENAME_LEN = len(os.path.split(srt.filename)[1])
                        srt_filename_dir, srt_filename = os.path.split(srt.filename)
                        if SRT_FILENAME_LEN > MAX_LEN_SRT_NOME:

                            srt_filename = srt_filename[:(int(MAX_LEN_SRT_NOME / 2) - 4) + int(MAX_LEN_SRT_NOME % 2)] +"..."+ srt_filename[SRT_FILENAME_LEN - int(MAX_LEN_SRT_NOME / 2) :]
                            srt.filename = os.path.join(srt_filename_dir,srt_filename)




                        if not os.path.exists(os.path.dirname(os.path.join(o_dir, srt.filename))):

                            try:
                                os.makedirs(os.path.dirname(os.path.join(o_dir, srt.filename)))

                            except OSError as e:

                                if e.errno != errno.EEXIST:
                                    raise



                        with open(os.path.join(o_dir,srt.filename),"wb") as o_file:
                            while True:
                                srt_parte = srt_dados.read(SRT_PARTE)

                                if not srt_parte:
                                    break

                                o_file.write(srt_parte)

                                progress["value"] += len(srt_parte)
                                arqAlbl.set(" %s / %s" %( progress["value"],srt.file_size))
                                statuslbl.set("[ {0:.0%} ] Extraindo...".format((progress["value"] / srt.file_size) ) )
                                sys.stdout.write("\r[ {0:.0%} ] Extraindo {1}...".format((progress["value"] / srt.file_size),srt.filename))
                                sys.stdout.flush()
                            print("OK")
        else:

            with zipfile.ZipFile(os.path.join(o_dir,zip_item[0]),"r") as zip_arq:


                for srt in zip_arq.infolist():
                    if srt.filename[-4:] != ".srt": continue;

                    if(len(srt.filename) > 36):
                        arqNomelbl.set(srt.filename[:26]+"..."+srt.filename[-10:])
                    else:
                        arqNomelbl.set(srt.filename)

                    progress["value"] = 0
                    progress["maximum"] = srt.file_size
                    arqAlbl.set(" 0 / %s" %(srt.file_size))

                    SRT_PARTE = 200 * 1024
                    with zip_arq.open(srt) as srt_dados:


                        #encurta diretorio se n for o suficiente
                        MAX_LEN_SRT_NOME = (247-len(os.path.dirname(os.path.join(o_dir, srt.filename))))
                        SRT_FILENAME_LEN = len(os.path.split(srt.filename)[1])
                        srt_filename_dir, srt_filename = os.path.split(srt.filename)
                        if SRT_FILENAME_LEN > MAX_LEN_SRT_NOME:
                            srt_filename = srt_filename[:(int(MAX_LEN_SRT_NOME / 2) - 4) + int(MAX_LEN_SRT_NOME % 2)] +"..."+ srt_filename[SRT_FILENAME_LEN - int(MAX_LEN_SRT_NOME / 2) :]
                            srt.filename = os.path.join(srt_filename_dir,srt_filename)


                        if not os.path.exists(os.path.dirname(os.path.join(o_dir, srt.filename))):

                            try:
                                os.makedirs(os.path.dirname(os.path.join(o_dir, srt.filename)))

                            except OSError as e:
                                if e.errno != errno.EEXIST:
                                    raise

                        with open(os.path.join(o_dir,srt.filename),"wb") as o_file:
                            while True:
                                srt_parte = srt_dados.read(SRT_PARTE)

                                if not srt_parte:
                                    break

                                o_file.write(srt_parte)

                                progress["value"] += len(srt_parte)
                                arqAlbl.set(" %s / %s" %( progress["value"],srt.file_size))
                                statuslbl.set("[ {0:.0%} ] Extraindo...".format((progress["value"] / srt.file_size) ) )
                                sys.stdout.write("\r[ {0:.0%} ] Extraindo {1}...".format((progress["value"] / srt.file_size),srt.filename))
                                sys.stdout.flush()
                            print("OK")

    statuslbl.set("Legendas extraidas com sucesso !" )


def Baixar():
    print("[  *  ] Iniciando procedimento de download...")
    PARTE = 5 * 1024 # 100KB ;1MB = 1024KB
    baixadas = len(conteudo) #total baixadas
    n_BaixadasL = []
    BaixadasL = []
    jaBaixadas = ChecarBaixadas()

    userAgent,cookies = conteudo[0].split(";")

    #headers
    hUserAgent = b64.b64decode(userAgent)
    hCookies = b64.b64decode(cookies)


    for item in conteudo[1:]: #cada linha;1 = reservado



        flagTipo,NomeArq,UrlArq,Referencia = item.split(";")
        flagTipo = int(flagTipo)

        #NomeArq += ".zip"


        #verifica se já Baixado

        if(jaBaixadas):
            ljb = GetBaixada(jaBaixadas,NomeArq)

            if ljb:
                print("[ ... ] {0}({1}) Já foi baixada e extraida...".format(NomeArq,ljb[1]))
                continue;



        if(len(NomeArq) > 36):
            arqNomelbl.set(NomeArq[:26]+"..."+NomeArq[-10:])
        else:
            arqNomelbl.set(NomeArq)



        if flagTipo == 1:
            urlReq = "https://dl.opensubtitles.org/en/download/sub/"+UrlArq[51:]
            req = urllib.request.Request(urlReq)


            req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            req.add_header("Accept-Encoding","gzip, deflate, br")
            req.add_header("Accept-Language","pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3")
            #req.add_header("Cookie","__cfduid=d823390389c6735a2df2212acc0e2de2e1545971347; searchform=formname%3Dsearchform%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C1%7C%7C%7C1%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C; pref_mk=%7B%22tv%22%3A20%2C%22m%22%3A0%7D; _ga=GA1.2.1914789230.1547362938; weblang=en; user=13105; user=13105; remember_sid=N0asYapgr9NTakubcvQ%2Ch0QP8P4; cto_lwid=54b33099-2cac-4004-8498-55f7a249ee01; cto_idcpy=ff081563-7715-46b7-86d6-751c6164a762; __qca=P0-1494849547-1551148695522; PHPSESSID=N0asYapgr9NTakubcvQ%2Ch0QP8P4; _gid=GA1.2.39195340.1551588559; adblockmsg=1000; logged=1")

        else:
            req = urllib.request.Request(UrlArq)

        req.add_header("User-Agent",hUserAgent)
        req.add_header("Referer",Referencia)
        #req.add_header("Cookie",hCookies)
        try:


            #time.sleep(DOWNLOAD_DELAY_S)
            resposta = urlopen(req)

            if(resposta.getcode() == 429):

                time.sleep(int(resposta.getheader("Retry-After")))
                resposta = urlopen(req)



            tamanhoTotal = int(resposta.getheader("Content-Length"))
            extensao = resposta.getheader("Content-Disposition").split(";")[1].partition("=")[::2][1].replace("\"","")[-4:]

            NomeArq += extensao



            sha1 = hashlib.sha1()


            progress["maximum"] = tamanhoTotal
            progress["value"] = 0


            with open(os.path.join(o_dir,NomeArq),"wb") as f:
                while True:

                    parte = resposta.read(PARTE)

                    if not parte:
                        break


                    f.write(parte)
                    sha1.update(parte)


                    progress["value"] += len(parte)
                    arqAlbl.set(" %s / %s" %( progress["value"],tamanhoTotal))
                    statuslbl.set("[ {0:.0%} ] Baixando...".format((progress["value"] / tamanhoTotal) ) )
                    sys.stdout.write("\r[ {0:.0%} ] Baixando {1}...".format((progress["value"] / tamanhoTotal),NomeArq ))
                    sys.stdout.flush()
            BaixadasL.append([NomeArq,str(tamanhoTotal),sha1.hexdigest()])
            print("OK")
            print("| SHA1:\t{0}\n| Tamanho (Bytes):\t\t{1} B\n| Tamanho (Kilo Bytes):\t\t{2} KBs\n| Tamanho (Mega Bytes):\t\t{3} MBs\n|__________________________________________\n".format(sha1.hexdigest(),tamanhoTotal,round(tamanhoTotal / 1024),round(tamanhoTotal / 1024 / 1024,2)))


        except Exception as e:

            statuslbl.set(e)
            progress["value"] = 0
            arqAlbl.set(" 0 / 0")
            print("\r[  !  ] Error: {0} : {1}.".format(NomeArq,str(e) ))
            n_BaixadasL.append(item)
            baixadas-=1


            pass





    if(baixadas < len(conteudo)):
        statuslbl.set("Registrando %s legenda(s) não baixada(s)..."%(len(conteudo)-baixadas))

        with open(os.path.join(o_dir.parents[0],"Legendas não baixadas.txt"),"w") as nbf: #nao baixadas file
            for inb in n_BaixadasL: #item não baixado
                nbf.write(inb+"\n")
        statuslbl.set("Legendas não baixadas registradas !")

    else:
        statuslbl.set("%s / %s Legendas baixadas !"%(baixadas,len(conteudo)))





    if(len(BaixadasL) > 0):

        #salva log de baixadas para não precisar baixar dnv
        with open(os.path.join(o_dir.parents[0],"baixadas.txt"),"a") as bf: #baixadas file
            for baixada in BaixadasL:

                bf.write(baixada[0][0:-4]+";"+baixada[1]+";"+baixada[2]+"\n")

        statuslbl.set("Iniciando procedimento de extração...")
        Extrair(BaixadasL)
        LimparResiduos(BaixadasL)

    else:
        statuslbl.set("Nenhuma legenda foi baixada.")

def iniciarProc():
    Thread(target=Baixar).start()



if len(sys.argv) < 2:
    messagebox.showerror("Subdl","Arquivo contendo a lista de links não especificado.")
    sys.exit()
try:
    with open(sys.argv[1]) as f:
        conteudo = f.readlines()


    pass

except FileNotFoundError as e:
    messagebox.showerror("Subdl","Arquivo contendo a lista de links não encontrado.")
    sys.exit()

conteudo = [x.strip() for x in conteudo]

if len(conteudo) < 1:
    messagebox.showerror("Subdl","Nenhuma url de legenda foi especificada na lista.")
    sys.exit()

# index 0 = reservado para nome da serie
o_dir = filedialog.askdirectory() #output dir; diretorio de saida

if len(o_dir) <= 0:
    messagebox.showerror("Subdl","Diretorio para salvar legendas não especificado.")
    sys.exit()

if not os.path.exists(Path(o_dir+"/Legendas")):

    os.mkdir(Path(o_dir+"/Legendas"))
    o_dir = Path(o_dir+"/Legendas")
else:
    o_dir = Path(o_dir+"/Legendas")



if not os.path.isdir(str(o_dir)):
    messagebox.showerror("Subdl","Diretorio especificado invalido.")
    sys.exit()

root.iconbitmap(os.path.join(os.getcwd(),"icon/subdl.ico"))
root.geometry("370x100")
root.resizable(width=False,height=False)
root.deiconify()



progress = ttk.Progressbar(orient=tk.HORIZONTAL, mode="determinate",length=350)


progress.pack()

arqAlbl = tk.StringVar()
tk.Label(root,textvariable=arqAlbl,font=("Arial",9)).pack()
arqAlbl.set("-")

arqNomelbl = tk.StringVar()
tk.Label(root,textvariable=arqNomelbl,font=("Helvetica",10)).pack()

statuslbl = tk.StringVar()
tk.Label(root,textvariable=statuslbl,font=("Arial",8)).pack()

iniciarProc()

root.mainloop()
sys.exit()
