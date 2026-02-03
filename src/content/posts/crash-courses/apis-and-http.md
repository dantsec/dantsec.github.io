---
title: The world of APIs and HTTP
published: 2026-02-02
description: 'Main concepts of APIs and HTTP that you need to know.'
image: ''
tags: [Web, Software-Engineering]
category: Software-Engineering
draft: false
lang: 'pt-br'
---

# Protocolo HTTP

## Introducao

- Protocolo de aplicacao que serve para transferir informacoes entre cliente e servidor, chamado de HTTP ou _Hyper Text Transfer Protocol_;
- No modelo de camadas, o protocolo HTTP eh atribuido a **camada 7 (aplicacao)**, e usa o protocolo TCP para estabelecer suas comunicacoes;
- Funciona sem criptografia e envia todas as informacoes em texto nao criptografado (seu irmao, "HTTPS", faz o contrario e junta o poder do HTTP e do TLS/SSL) e eh **stateless**;
- **URI** (_Uniform Resource Identifier_) permite que o protocolo identifique qual recurso deve ser acessado (uma **URL** - _Uniform Resource Locator_ - eh um exemplo de como ele faz isso);
	- A construcao de um URL da-se pelo conjunto dos seguintes elementos:
		- **Scheme**: instrui sobre qual protocolo usar para acessar o recurso, como HTTP, HTTPS, FTP;
		- **User**: alguns servicos exigem autenticacao para efetuar login, voce pode inserir um nome de usuário e uma senha na URL para efetuar login;
		- **Host / Domain**: o nome de dominio ou endereco IP do servidor que voce deseja acessar;
		- **Port**: a porta a qual você se conectara;
		- **Path**: o nome do arquivo ou local do recurso que você está tentando acessar;
		- **Query String**: bits extras de informacao que podem ser enviados para o caminho solicitado (ex: `/blog?id=1`);
		- **Fragment**: referencia a um local na pagina solicitada. Isso é comumente usado para páginas com conteudo longo e pode ter uma determinada parte da pagina diretamente vinculada a ela, para que fique visivel ao usuario assim que ele acessa a pagina (ex: `#task1`).
- Recebe um pedido (**request**) e responde-o (**response**);
- Sua estrutura eh a seguinte:
	- Request:
		- **Metodo / Verbo**;
		- **Recurso**;
		- **Versao do Protocolo** + **Headers** + **Body**.
	- Response:
		- **Versao do Protocolo**;
		- **Status da Resposta**;
		- **Mensagem de Status** + **Headers** + **Body**.
	- Podemos ter alguns tipos de _headers_, sao eles:
		- _Gerais_: aparecem tanto em requests quanto em responses, e nao estao relacionados ao conteudo da mensagem;
			- ex: `Cache-Control`.
		- _De Requisicao_: contem mais informacoes sobre a requisicao, seu cliente ou sobre o recurso solicitado;
			- ex: `User-Agent`, `Accept`.
		- _De Resposta_: fornecem informacoes adicionais sobre a resposta, como o seu local ou o seu servidor;
			- ex: `Server`, `Set-Cookie`;
			- Eh ideal ter cautela com esses headers, pois eles podem apresentar risco a seguranca;
			- Quando for usar o `Set-Cookie`, sempre se atente em utilizar as flags `Secure` (serao enviados apenas sobre HTTPS) e `HttpOnly` (para nao serem acessadas pelo javascript).
		- _De Entidade_: contem informacoes sobre o corpo da entidade, como seu tamanho ou seu tipo;
			- ex: `Content-Type`, `Content-Length`;
			- Os tipos de `Content-type` mais comuns sao:
				- **URL Encoded** (`application/x-www-form-urlencoded`);
				- **Form Data** (`multipart/form-data`);
				- **JSON** (`application/json`);
				- **XML** (`application/xml`).
		- _De Seguranca_: ajudam a melhorar a seguranca geral do app web, fornecendo mitigacoes contra ataques;
			- **Content-Security-Policy (CSP)**:
				- Camada de segurança adicional que pode ajudar a mitigar contra ataques comuns, **controlando o que pode ser executado dentro da pagina**;
				- Fornece um caminho para administradores dizerem quais dominios ou recursos sao considerados seguros e prove uma camada de mitigacao para alguns ataques;
				- ex: `Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.tryhackme.com; style-src 'self'`
					- `default-src`: especifica a política padrão de si, o que significa apenas o site atual;
					- `script-src`: especificam a política de onde os scripts podem ser carregados;
					- `style-src`: especifica a política para as folhas de estilo CSS podem ser carregadas.
			- **Strict-Transport-Security (HSTS)**:
				- Garante que o web browser sempre se conectara via HTTPS;
				- ex: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`;
					- `max-age`: define o tempo de expiracao para essa configuracao;
					- `includeSubDomains`: configuracao opcional que instrui o browser para aplicar essa regra tambem nos subdominios;
					- `preload`: configuração opcional que permite que o site seja incluído nas listas de _preload_. Os navegadores podem usar listas de _preload_ para aplicar os HSTS antes mesmo de fazer sua primeira visita a um site.
			- **X-Content-Type-Options**:
				- Pode ser usado para instruir os navegadores a não adivinhar o tipo _MIME_ de um recurso, mas apenas usar o declarado no `Content-Type`;
				- ex: `X-Content-Type-Options: nosniff`;
					- `nosniff`: essa diretiva instrui o browser para nao _sniffar_ o tipo _MIME_.
			- **Referrer-Policy**:
				- Controla a quantidade de informacoes compartilhadas sobre a pagina de origem (referenciador) enviadas ao servidor da Web de destino quando um usuario eh redirecionado do servidor de origem, bem como quando clica em um hiperlink;
				- Resumidamente, controla a privacidade e seguranca dos dados da URL de origem enviados em requisicoes subsequentes;
				- ex:
					- `Referrer-Policy: no-referrer`: desabilita completamente qualquer informacao enviada sobre o referenciador;
					- `Referrer-Policy: origin`: envia apenas o dominio;
					- `Referrer-Policy: same-origin`: enviara apenas informacoes do referenciador quando o destino fizer parte da mesma origem (mesmo dominio);
					- `Referrer-Policy: strict-origin`:  envia apenas o referenciador como origem quando o protocolo permanece o mesmo (HTTPS para HTTPS);
					- `Referrer-Policy: strict-origin-when-cross-origin`: envia a URL completa em navegações internas seguras, domínio apenas em externas, nada se for HTTPS para HTTP.

```js
/** Request */
POST /uri HTTP/1.1

// @Headers
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: application/json // "O que eu quero receber"
Content-Type: application/json // "Como eu esto enviando"
Content-Length: 50
// EMPTY LINE: separa o header do body!
// @Body
{
    "name": "John Doe",
    "email": "john.doe@example.com"
}

/** Response */
HTTP/1.1 201 Created // Eh chamado de `status line`

// @Headers
Date: Sat, 27 Jul 2024 12:28:53 GMT
Content-Type: application/json
Content-Length: 92
Location: /api/users/1

// @Body
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "createdAt": "2024-07-27T12:28:53Z"
}
```

### CORS (Cross-Origin Resource Sharing)

- Mecanismo de seguranca (aplicado no servidor e no browser) que controla o acesso entre diferentes origens na web, controlando assim **quem pode acessar o recurso**;
- Por exemplo, quando um site hospedado em `siteA.com` tenta fazer uma requisição a uma API em `apiB.com`;
- Tem como **finalidade** impedir que páginas de outros domínios acessem recursos sem autorização, protegendo o usuário contra ataques como **Cross-Site Request Forgery (CSRF)**;
- Funciona assim:
	- O navegador envia uma requisição especial (preflight) perguntando ao servidor se a origem tem permissão;
	- O servidor responde com cabeçalhos HTTP específicos, como:
		- `Access-Control-Allow-Origin: https://siteA.com`;
		- `Access-Control-Allow-Methods: GET, POST`;
		- `Access-Control-Allow-Headers: Content-Type`.
	- Se o navegador receber autorização, ele permite a requisição; caso contrário, bloqueia.


## Metodos / Verbos HTTP

- Verbos / Metodos sao maneiras **semanticas** de dizer o que queremos fazer com a requisicao (no fundo todas funcionam da mesma maneira);
- Sao eles:
	- `GET`: solicitar conteudo;
	- `HEAD`: semelhante ao _get_, porem apenas os cabecalhos sao retornados;
	- `POST`: utilizado quando eh necessario enviar algo a ser processado;
	- `PUT` / `PATCH` / `MERGE`: utilizado para indicar alteracao de conteudo;
		- _Put_ seria para alteracoes em massa (e caso ainda nao exista alguma das alteracoes, ele gera);
		- _Patch_ para pequenas alteracoes.
	- `DELETE`: utilizado para indicar remocao de conteudo;
		- Nao aceita _body_ portanto se precisar de dados dinamicos use _queryStrings_;
		- Para **bulk delete** use arrays na query.
	- `OPTION`: utilizado para saber quais operacoes de um determinado recurso estao disponiveis;
	- `CONNECT`: estabelece um tunelamento _TCP / IP_ com o servidor, geralmente para facilicar a comunicacao SSL;
	- `TRACE`: envia um teste de loopback motrando o caminho que uma requisicao faz para chegar ate o recurso especificado no servidor destinado.

## Respostas (Responses) HTTP

- Existem 5 categorias, que estao localizadas nos _ranges_ `1~5`, onde de `1~3` sao informativos e de `4~5` sao erros.

### 1XX (Solicitacoes de Informacao)

- Nao representam erros e apenas indicam que a solicitacao foi recebida pelo servidor e esta pronta para dar sequencia ao processo;
- Algumas respostas:
	- `100`: _continue_;
		- indica que tudo ocorreu bem.

### 2XX (Operacao Bem Sucedida)

- Algumas respostas:
	- `200`: _ok_;
		- _GET_: recurso obtido e retornado no corpo da mensagem;
		- _PUT / POST_: recurso resultante da acao eh retornado no corpo da mensage.
	- `201`: _created_;
		- Nao deve ser usado sempre que algo for criado, mas quando atender a consideracao: "a requisicao foi feita com a intencao de criar algo?";
		- Recurso criado e **retornado no corpo** da resposta.
	- `202`: _accepted_;
		- Indica que a solicitacao foi recebida mas ainda nao foi atendida e nao ha uma forma de enviar posteriormente uma resposta assincrona indicando o resultado da solicitacao (tratamento assincrono).
	- `204`: _no-content_;
		- Indica que nao ha conteudo para enviar para esta solicitacao, mas os cabecalhos podem ser uteis e sao o suficiante.

### 3XX (Redirecionamento de Conteudo)

- Algumas respostas:
	- `301`: _moved permanently_;
		- A url do recurso requerido mudou.

### 4XX (Erros Cliente-Side)

- `400`: _bad request_;
	- Indica que o servidor nao pode ou nao ira processar a solicitacao devido a um problema com a sintaxe da request;
	- Esta relacionado a **estrutura dos dados**.
- `401`: _unauthorized_;
	- Semanticamente significa "unauthenticated", e o cliente deve autenticar-se ou renovar seu token para obter a resposta.
- `403`: _forbidden_;
	- Mesmo que autenticado, nao possui o nivel de acesso necessario, e sao **erros de permissao**.
- `404`: _not found_;
	- Indica que o recurso solicitado nao esta disposto a divulgar que existe ou nao pode ser solicitado.
- `422`: _unprocessable content_;
	- A solicitacao esta bem formatada, com a sintaxe correta e foi entendida, mas nao pode ser atendida devido a problemas com os dados fornecidos pelo cliente;
	- Exemplos:
		- Usuario tenta fazer o cadastro, mas tenta usar um e-mail que ja esta cadastrado;
		- Campo obrigatorio e eh esperado que tenha entre 4 a 255 caracteres e:
			- Usuario nao enviou o campo;
			- Usuario enviou 2 caracteres;
			- Usuario enviou 256 caracteres.

### 5XX (Erros Server-Side)

- `500`: _internal server error_;
	- Condicao inesperada e resposta automatica do servidor.
- `502`: _bad gateway_;
	- Enquanto atuando como servidor intermediario (gateway ou proxy), recebeu uma resposta invalida do servidor para o qual a request foi encaminhada.
- `503`: _service unavaiable_;
	- Indica que o servidor nao esta pronto para lidar com a request, podendo ser por conta de sobrecarregamento ou manutencao;
	- O cabecalho `HTTP Retry-After` deve sempre que possivel estar presente contendo o tempo estimado para restabelecimento do servico.
- `504`: _gateway timeout_;
	- Indica que o servidor atuando como gateway ou proxy nao conseguiu responder em tempo.

![status-codes-guide-image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*YjerWMVgAwQpf3qJLt7_8w.png)

# APIs

## Definicao

- Significado:
	- Interface de Programacao de Aplicacoes;
	- Application Programming Interface.
- Sao mecanismos que permitem que dois componentes de software se comuniquem usando um conjunto de definicoes e protocolos;
- Tambem pode ser vista como um contrato de servico entre duas aplicacoes.

## Funcionamento

- Funcionam com base nas comunicacoes **cliente e servidor**;
- Existem quatro maneiras diferentes pelas quais as APIs podem funcionar, dependendo de quando e por que elas foram criadas. Sao elas:
	- `SOAP`:
		- Usam o _Simple Object Access Protocol_;
		- O cliente e servidor trocam mensagens usando _XML_;
		- Esse design eh menos flexivel e era mais popular no passado.
	- `RPC`:
		- Conhecidas como _Remote Procedure Calls_;
		- O cliente conclui uma funcao / procedimento no servidor e o servidor envia a saida de volta ao cliente.
	- `WebSocket`:
		- Usa objetos _JSON_ para transmitir dados;
		- Oferece suporte a **comunicacao bidirecional** entre aplicativos cliente-servidor;
		- O servidor pode enviar mensagens de retorno de chamada a clientes conectados, tornando-o mais eficiante que o design _REST_.
	- `REST`:
		- Sao as mais populares e flexiveis atualmente;
		- O cliente envia solicitacoes ao servidor como dados e o servidor usa essa entrada do cliente para iniciar funcoes internas e retornar os dados de saida ao cliente.

## Autenticacao

### Basic Authentication

- Nome de usuario e senha dividido por `:` e codificados em _base64_;
- Exemplo: `Authorization: Basic YWRtaW46YWRtaW4=`.

### API Keys

- Servidor gera uma chave de acesso unica para o cliente e, para utilizar a API, o cliente envia essa chave unica em toda requisicao;
- Serve para autenticacao e nao autorizacao;
- Exemplo: `Api-key: thi123456`.

### SAML (Security Assertion Markup Language)

- Troca de autenticacao baseada em **XML** entre um _IdP_ (Identity Provider) e um _SP_ (Service Provider);
- Exemplo:
	- O _SP_ redireciona para o _IdP_;
	- _IdP_ autentica o usuário;
	- Retorna um SAML Assertion;
	- _SP_ valida e concede acesso.

### OAuth

- Protocolo completo com diversas especificacoes de seguranca;
- Util no processo de autenticacao e autorizacao.

#### Fluxo de Funcionamento

- **Resource Owner**: entidade dona do recurso, que eh capaz de controlar o cesso a um recurso. Normalmente eh o proprio usuario;
- **Resource Server**: servidor que possui os recursos, e por sua vez, recebe as requisicoes;
- **Authorization Server**: servidor que gera tokens de acesso para permitir que o client acesse os recursos autorizados pelo resource owner;
- **Client**: aplicacao que acessa os recursos do resource server.

![oauth-flow](https://i.imgur.com/NiQqASc.png)

#### Ferramentas Auxiliares

- **OpenID Connect**: extensao da funcionalidade de autenticacao do _OAuth_;
- **JWT**: formato de token seguro que utiliza _JSON_ como base.

# O que sao APIs REST / Restful?

- Significado:
	- **Transferencia Representacional de Estado**;
	- **Representational State Transfer**.
- Define um conjunto de **metodos / verbos**, e usa o **protocolo HTTP** para estabelecer comunicacoes;
- **Restful** eh o termo atribuido a uma API que possui a inteligencia de aplicao para o padrao _REST_;
- Dando uma breve passada em autenticacao, o principal servico _open-source_ utilizado atualmente eh o _OAuth2.0_ com _JWT_;
- Eh descrito em seis restricoes:
	- **Uniform Interface**: definido por mais 4 restricoes;
		- **URI**: identificador de recursos;
		- **Verbos HTTP**: manipulacao de recursos atraves de representacoes;
		- **Mensagens Auto-descritivas**: cada requisicao deve conter informacoes suficientes para o servidor processar a informacao;
		- **HATEOAS** (**Hypermedia as the Engine of Application State**) (opcional): diz que a resposta do servidor deve conter links de conteudos relacionados ao _resource_, dessa forma o controle de fluxo da aplicacao eh controlado atraves do servidor e nao do frontend.;
		- **Resource Based**:
			- _Resource_ eh qualquer coisa importante o suficiente para ser referenciada por um nome, nesse caso, _resource_ eh qualquer coisa que possa ter uma URI.
	- **Stateless**: servidores nao salvam dados dos clientes entre as solicitacoes;
	- **Cacheable**: a resposta de uma solicitacao deve implicitamente ou explicitamente informar se o dado pode ser mantido em cache ou nao, e o mesmo deve ser mantido e gerenciado pelo lado do cliente;
	- **Client-Server**: separa as responsabilidades do front / back end;
	- **Code on Demand** (opcional):  permite que as funcionalidades do cliente sejam extendidas baixando e executando applets ou scripts;
	- **Layered System**: o sistema deve ter uma arquitetura de camadas.

## Construindo uma API Rest

| Método HTTP | Rota            | Descrição                              | Corpo da Requisição                                                         | Corpo da Resposta                                                                                                         |
| ----------- | --------------- | -------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| GET         | /api/users      | Retorna uma lista de todos os usuários | N/A                                                                         | ```json [ { "id": 1, "name": "John Doe", "email": "john.doe@example.com" }, ... ] ```                                     |
| GET         | /api/users/{id} | Retorna um usuário específico          | N/A                                                                         | ```json { "id": 1, "name": "John Doe", "email": "john.doe@example.com" } ```                                              |
| POST        | /api/users      | Cria um novo usuário                   | ```json { "name": "John Doe", "email": "john.doe@example.com" } ```         | ```json { "id": 1, "name": "John Doe", "email": "john.doe@example.com", "createdAt": "2024-07-27T12:28:53Z" } ```         |
| PUT         | /api/users/{id} | Atualiza um usuário existente          | ```json { "name": "John Doe Updated", "email": "john.doe@example.com" } ``` | ```json { "id": 1, "name": "John Doe Updated", "email": "john.doe@example.com", "updatedAt": "2024-07-27T12:35:00Z" } ``` |
| DELETE      | /api/users/{id} | Deleta um usuário                      | N/A                                                                         | ```json { "message": "User deleted successfully" } ```                                                                    |

## Boas Praticas para Construcao de APIs

- Utilize o **mesmo padrao de URI** na identificacao dos recursos;
- Deixe facil o processo de **versionamento**;
- Para nomear, utilize substantivos no plural, **evite verbos** (ja que _URIs_ representam recursos e nao acoes) e **use hifens junto de letras minusculas**;
- Se atente ao contexto para usar o **verbo HTTP correto**;
- Evite adicionar na URI a **operacao a ser realizada** no recurso;
- Evite adicionar na URI o **formato desejado** da representacao do recurso;
	- Suporte diferentes representacaos (HTML, XML, JSON, etc).
- Evite manter **dados de autenticacao / autorizacao em sessao**, para isso use:
	- OAUTH, JWT, Keycloack, etc.
- Tente utilizar, **no maximo, 3 niveis de acoes**;
- Utilize acoes apenas apos definir uma URI para um resource, desde que a **acao nao sobrescreva o sentido do verbo** HTTP;
- Evite fazer com que o patch explique o da hierarquia anterior;
	- ex: `POST /usuarios/criar`;
		- Neste caso basta o verbo HTTP: `POST /usuarios`.
- Filtros sempre na _queryString_, e **nunca** deve ser colocado como **parametro / parte da rota**;
- Ordene endpoints por dependencia;
	- ex: `/courses/1/topics/1/class`;
		- _Courses_ depende de _topics_ que, por sua vez, depende de _class_.
- Para formatacao de data e hora use o padrao **ISO 8601** e **UTC**.

## Versionamento

- Temos dois tipos de versionamento, sao eles:
	- **URL**:
		- Por _Subdominio_ (ex: `http://api-v1.minhaapi.com/vinhos`);
		- Por _Path_ (ex: `http://minhaapi.com/v1/vinhos`);
		- Por _Querystring_ (ex: `http://minhaapi.com/vinhos?version=1.0`).
	- **Header**:
		- Via _Accept_ (ex: `Accept: application/vnd.gastronomia.v2+json`);
		- Via Header _Customizado_ (ex: `api-version: 2`);
			- Junto do _Path_ eh a melhor combinacao;
			- Podemos fornecer uma data, por exemplo, e a partir dela pegar a minor atualizada.

## Throttling, Rate Limiting e Outros Limitadores

- Sao estrategias complementares, mas nao tem as mesmas funcoes.

### Rate Limiting

- Protege sua API de um alto consumo de requisicoes;
- Configuracao do limite de requisicoes aceitas pela API em uma determinada janela de tempo, e que pode ser em segundos, horas, dias, etc (principalmente em minutos);
- Exemplo: 100 req/h.

### Throttling

- Prepara sua API para cenarios de picos de acesso;
- Configuracao da fila de requisicoes excedidas para processamento em uma janela de tempo posterior, ou seja, eh o tempo de delay do processamento da requisicao apos o client exceder os parametros de _rate limit_;
- Exemplo: 2 re-tentativas com delay de 1 min.

### API Quota

- Utilizado em cenarios comerciais com renovacao de consumo e modelos de cobranca (como uma conta de celular);
- Podem ser combinadas com _rate limit_;
- Exemplo: API Quota de cliente X eh 5 mil req/mes.

### API Burst

- Disponibiliza temporariamente infraestrutura ociosa para ganhar mais performance de processamento para requisicoes e clientes especificos;
- Exemplo: se o _rate limit_ de uma API X eh 10 req/min e um cliente envia 20 requisicoes de uma vez, o _API Burst_ vai verificar se existe capacidade no servidor que nao esta sendo usada, e ira processar as 20 requisicoes em alta performance, nao afetando outros clientes nem o resto da sua API.

### Exemplo Real (RL + TH)

![throttling-rate-limit](https://i.imgur.com/UbSqB3J.png)

## Filtragem, Paginacao e Ordenacao de Consultas

### Filtragem

- Permite restringir os resultados de uma API com base em criterios especificos.

```sql
-- GET /api/products?category=books&author=John

SELECT * FROM products WHERE category = 'books' AND author = 'John';
```

### Paginacao

- Divide os resultados em partes menores (**pages**), permitindo carregar apenas uma fracao dos dados, o que melhora o desempenho e reduz a carga da API;

```sql
-- Eq.: OFFSET = (current page - 1) * items per page

-- GET /api/products?per_page=10&page=1
SELECT * FROM products LIMIT 10 OFFSET 0;

-- GET /api/products?per_page=10&page=2
SELECT * FROM products LIMIT 10 OFFSET 10;

-- GET /api/products?per_page=10&page=3
SELECT * FROM products LIMIT 10 OFFSET 20;

-- ...
```

#### Subtipos

- **Cursor**: chave unica e sequencial que usa registro de dados para indicar.

```
GET /api/products?since_id=100&max_id=200

> Retorna todos os produtos de ID 100 ate 200.
```

- **Page** e **PageSize**: parametros de numero da pagina e seu tamanho.

```
GET /api/products?page=3&page_size=10

> Retorna 10 produtos da pagina 3.
```

- **Offset** e **Limit** (melhor em termos de performance): paginacao baseada em descolamento de registros.

```
GET /api/products?offset=10&limit=30

> Retorna 30 produtos a partir do decimo registro.
```

### Ordenacao

- Define a ordem de exibicao dos resultados.

```sql
-- GET /api/products?sort_by=author&order=desc

SELECT * FROM products ORDER BY author DESC;

-- GET /api/products?order=author:desc,price:asc,...

SELECT * FROM products
ORDER BY
	author DESC,
	price ASC,
	-- ...
```

### Juntanto as Pecas

```sql
/*
GET /api/products
	?category=books
	&start_date=2025-01-01
	&end_date=2025-01-28
	&min_price=1000
	&max_price=2000
	&sort_by=author
	&order=desc
	&per_page=10
	&page=1
*/

SELECT *
FROM products
WHERE
	category = 'books'
	AND created_at BETWEEN '2025-01-01' AND '2025-01-28'
	AND price BETWEEN 1000 AND 2000
ORDER BY author DESC
LIMIT 10 OFFSET 0;
```

## Cache

- Estrutura computacional de armazenamento focada em manter copias de dados que sao acessados com **frequencia**;
- Vantagens:
	- Reducao da latencia de rede;
	- Reducao de carga de processamento dos servidores;
	- Otimizacao de tempo de resposta do client.
- Tipos:
	- **Shared Cache**: armazena respostas de servidores para reutilizacao entre diversos usuarios;
	- **Private Cache**: armazena respostas de servidores para reutilizacao de apenas um usuario.

### Lado do Cliente

- Sao especificados no header da requisicao;
- Tipos:
	- `Cache-Control: no-store`:
		- Nao guarda nenhum cache;
		- A cada requisicao, o cliente fara downlod da respota do server normalmente.
	- `Cache-Control: no-cache`:
		- O browser ira enviar uma requisicao ao servidor para validacao desses dados;
		- Economiza banda, mas com a certeza que o cache esta atualizado.
	- `Cache-Control: public`:
		- Permite que os dados de reposta do servidor sejam armazenados em um cache compartilhado.
	- `Cache-Control: private`:
		- Permite que os dados de reposta do servidor sejam armazenados para utilizacao de apenas um usuario.
	- `Cache-Control: max-age=30`:
		- Limita o tempo maximo que o cache ficara disponivel (em segundos);
		- Indica ao browser que ele pode armazenar cache, mas que deve validar novamente quando a duracao for excedida.
	- `Cache-Control: must-revalidate`:
		- Obriga que o browser sempre revalide os dados.

### Lado do Servidor

- **Load Balancing**:
	- Distribui a capacidade de processamento das requisicoes e trafego de rede;
	- Sua API fica mais escalavel e segura, pois se um servidor falhar, voce tera outros funcionando.
- **Proxy Reverso**:
	- Interface publica da sua API, ou seja, funciona como intermediador de todas as requisicoes externas;
	- Vantagens:
		- Seguranca: protecao contra DDoS e configuracoes de certificados SSL;
		- Performance: funcionalidades nativas de _compressao de dados_ trafegados e _cache_. Como eh um intermediador, consegue tratar os dados de forma inteligente antes de retornar ao client.
- **API Gateway**:
	- Roteamento, monitoramento, autenticacao e autorizacao ("Proxy Reverso Plus");
	- Transformacao de dados, seguranca avancada por politicas, etc.
- **CDN** (Content Delivery Network - Rede de distribuicao de conteudo):
	- Mantem replicas de conteudos web em servidores geograficamente localizados para redirecionar requisicoes a fim de diminuir a latencia;
	- Principais players: _Akamai_ e _Cloudfront_.

### Compressao de Dados

- Reduz o tamanho da resposta para otimizar transferencia e desempenho;
- Aplicavel a JSON, HTML, CSS, JavaScript e outros dados, alem de arquivos;
- O cliente solicita compressão com `Accept-Encoding: gzip, compress`;
- O servidor, se suportar, responde com `Content-Encoding: gzip`.

# Tooling

- Saber mais sobre _Status Codes_: `https://http.cat/`;
- Linguagem de consulta para APIs: `https://graphql.org/`;
- Documentacao de APIs: `https://swagger.io/`.

# Referencias

- `https://medium.com/@jonatangall/um-breve-resumo-sobre-o-protocolo-http-1d32c333dd34`
- `https://www.hostgator.com.br/blog/o-que-e-protocolo-http/`
- `https://www.hostgator.com.br/guias/http-status-code-como-resolver/`
- `https://aws.amazon.com/pt/what-is/api/`
- `https://wssilva-willian.medium.com/design-de-api-rest-9807a5b16c9f`
- `https://www.brunobrito.net.br/padrao-rest/`
- `https://www.brunobrito.net.br/rest-nao-e-crud/`
- `https://www.alura.com.br/artigos/rest-principios-e-boas-praticas`
