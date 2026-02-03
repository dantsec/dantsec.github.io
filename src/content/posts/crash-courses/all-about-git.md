---
title: Git @ Crash Course
published: 2026-02-02
description: 'Main concepts of Git that you need to know.'
image: ''
tags: [Crash-Course, Tools]
category: Tools
draft: false
lang: 'pt-br'
---

# Introduction

## Git vs. Github

- Diferencas entre **GIT** e **GITHUB**:
	- _GIT_:
		- Sistema de controle de versao (SCV / VCS) distribuido (p2p);
		- Operacoes atomicas (sucesso ou falha);
		- Repositorio (inventario, colecao) para seus codigos;
		- Com ele voce pode consultar todas as modificacoes passadas atraves dos **commits**.
	- _GITHUB_:
		- Servico de repositorio em **nuvem**.

## Workflow

- **Working tree / Directory**: pasta / diretorio atual;
- **Index (Staging Area)**: sala de espera, lugar para onde os commits vao antes do push;
- **HEAD**: por padrao, aponta para o ultimo commit recebido dentro do repositorio;

![git-flow](https://i.imgur.com/mWlqNxG.png)

## Nomenclature

- Tipos de Comandos:
	- **PLUMBING**: comandos de baixo nivel usados internamente pelo GIT quando os usuarios digitam comandos de alto nivel;
	- **PORCELAIN**: comandos de alto nivel comumente usados pelos usuarios.
- **BRANCH**:
	- Referencias (mutaveis) que apontam para um commit especifico;
	- Forma de desenvolver funcionalidades de forma indepentente.
- **FORK**:
	- Copia de um repositorio para seu perfil, mas que mantem um apontamento para o repositorio no qual se originou.
- **TAG**:
	- Branches sao referencias mutaveis, porem, com a _tag_, podemos mudar essa historia;
	- Nao podem ter seus ponteiros alterados (a menos que haja a exclusao das branches e a re-criacao delas).
- **Merge** (_Fast-forward_, _Snapshot_ e _Three-way_):
	- `https://chat.openai.com/share/0e69690c-b1ea-4b57-b828-79dddf6ba5ae`

# Architecture

![git-structure](https://i.imgur.com/xCCZnTt.png)

## .git/objects

- No git, tudo eh persistido nessa estrutura atraves de funcoes hash e no **banco de dados de objetos do GIT**, sendo ele do tipo chave-valor (no-sql);
- Uma funcao hash mapeia dados de tamanho arbitrario e dinamico em valores de tamanho fixo, assim, o valor final sempre tera o mesmo tamanho;
- Uma ma implementacao dessas funcoes pode ocasionar colisoes (dados tem o mesmo hash);
- O git armazena dados e acompanha tudo apenas comparando hashes;
- Na pratica, podemos observar pelos seguintes comandos:
	- _Plumbing_ (**hash-object**):
		- `% echo "hello" | git hash-object --stdin`.
	- _Porcelain_:
		- `% echo -e "hello" | sha1sum`.
- Porem, o GIT adiciona uma palavra especifica seguida pelo tamanho do conteudo, o delimitador `\0` (_null byte_);
- Essa palavra eh o que o GIT chama de **tipo de objeto**;
	- Vamos ver o objeto __blob__:
		- O GIT adiciona o seguinte padrao:
			- `{tipo_objeto} {tamanho_conteudo}\0`;
				- `blob 6\0hello`;
				- `% echo -e "blob 6\0hello" | sha1sum`;
		- Mas, por padrao, o comando hash-object nao persiste no diretorio, portanto utilizamos a opcao `-w`:
			- `% echo "hello" | git hash-object --stdin -w`
	- Legal, mas como ler arquivos blob?
		- O GIT usa a hash como uma chave que aponta para um valor, compactando o conteudo e armazenando-o;
		- O comando plumbing `cat-file` faz com que, com uma chave, ele descomprime e obtem o conteudo original:
			- `git cat-file -p [hash]`.
		- Adicionando arquivos blob ao indice:
			- O comando plumbing `update-index` adiciona um blob ao _stage area_ e da um nome a ele:
				- `git update-index --add --cacheinfo 100644 [hash] [name_to_blob]`.
- **Object Tree**:
	- Usando o comando plumbing `write-tree`, o GIT agrupa todos os blobs que foram adicionados ao indice.
- **Objeto Commit**:
	- Apos a promocao do _objeto tree_, o comando plumbing `commit-tree` recebe a arvore, uma mensagem de commit e cria outro objeto na pasta,  onde guarda a arvore referenciada, autor / confirmador e a mensagem.
- **Log for the Rescue**
	- O comando porcelain `git log` percorre todos os commits, seus parents e arvores, nos dando uma perspectiva de uma timeline do nosso trabalho.

## .git/refs

- Usar `sha1` no comando `git log` pode ser trabalhoso. Como resolver?
	- Dando nomes aos hashes, e isso eh o que chamamos de referencias:
		- `echo [hash] > .git/refs/heads/[reference]`;
		- `git update-ref refs/heads/[reference] [hash]`;
	- E isso sao as famosas **branches**.

## .git/HEAD

- O comando `git log` percorre o **commit raiz**, que eh **referenciado pela branch atual (HEAD)**;
- Um unico arquivo que aponta para uma _referencia de cabeca_ (branch);
	- _Plumbing_: `% cat .git/HEAD`;
	- _Porcelain_: `git branch`.
- E para manipular qual branch a HEAD aponta, usamos o seguinte comando
	- `git symbolic-ref HEAD refs/head/[branch_name]`.

# Semantic / Conventional Commits, Commit Patterns

- Convencao simples para ser utilizada nas mensagens de commit;
- Define um conjunto de regras para criar um historico de commit explicito, facilitando na criacao de ferramentas automatizadas;
- Tambem auxiliam voce e a sua equipe a entenderem, de forma facilitada, quais alteracoes foram realizadas no trecho de codigo commitado;
- Essas identificacoes ocorrem por meio de uma palavra e / ou emoji que representa uma acao.

## Types and Descriptions

- `feat`: indicam que seu trecho de codigo esta **incluindo um novo recurso**;
- `fix` / `hotfix`: indicam que seu trecho de codigo esta **solucionando um problema (bugfix)**;
- `docs`: indicam que suas alteracoes implicaram em **mudancas na documentacao (nao inclui alteracoes em codigo)**;
- `test`: indicam que suas alteracoes **alteraram arquivos de testes (nao inclui alteracoes em codigo)**, seja criando / alterando / excluindo;
- `build`: indicam **modificacoes** em **arquivos de build e dependencias**;
- `perf`: indicam **alteracoes de codigo** que estejam relacionadas a **performance**;
- `style`: indicam que houveram alteracoes referentes a **formatacao de codigo (nao inclui alteracoes em codigo)**, seja elas semicolos, trailing spaces, etc e que nao alteram o funcionamento da aplicacao;
- `refactor`: indicam mudancas devido a **refatoracoes que nao alteraram a funcionalidade do codigo**;
- `chore`: indicam **atualizacoes de tarefas (nao inclui alteracoes em codigo)** de build, configuracoes de administrador, pacotes, e que **nao influenciam nosso sistema nem algum dos nossos testes**, um exemplo seria adicionar um pacote no _.gitignore_;
- `ci`: indicam mudancas relacionadas a **integracao continua (continuous integration)**;
- `raw`: indicam mudancas relacionadas a arquivos de **configuracao, dados, features e parametros**;
- `cleanup`: utilizados quando **removemos** codigo comentado, trechos desnecessarios ou qualquer outra forma de limpeza / legibilidade e manutenibilidade;
- `remove`: indicam a **exclusao de arquivos / diretorios / funcionalidades obsoletas ou nao utilizadas**;
- `revert`: implicam em **reverter commits**.

```sh
# :emoji: e (scope) sao opcionais!

:emoji: <type>(scope): description

[optional body]

[optional footer(s)]
```

## Tips

> "Spoken or written as if giving a command or instruction. Don't be ambiguous."

- A primeira linha deve ter, no maximo, 4 palavras;
- Seu commit deve responder a 3 perguntas:
    - **Porque** essa mudanca e necessaria?
    - **Como** ela resolve o problema?
    - **Quais os efeitos** essas mudancas tem?
- Use o imperativo junto do presente simples, pense que na hora de escrever voce vai respondar a pergunta **"O que esse commit faz?"**.

# Git Flow

## Happy Path

- No dia-a-dia, focamos principalmente em criar branches do tipo _feature_ saindo da development, mergeamos la novamente e depois um lider tecnico faz o _merge para a master_, sendo optativo a camada de release;
- Falando ainda sobre a camade de _release_, se for identificado algum bug durante o processo, deve-se tratar o bug na proprirra branch e enviar depois para a master e para a develop.

```sh
# @@ Criando a Develop @@
# > Verifica, sincroniza, cria local e depois remoto.
git branch -a
git fetch origin
git checkout -b develop && git push origin develop

# @@ Criando uma Feature @@
# > Considere-se dentro da branch develop.
# > Crira branch local, cria branch remota, volta para develop, mergeia e atualiza remoto.
git checkout -b feature/novo-componente
git push origin feature/novo-componente
git checkout develop
git merge feature/novo-componente && git push origin develop

# @@ Criando uma Release @@
# > Considere-se dentro da branch develop.
git checkout -b release/v1.0.1
git push origin release/v1.0.1
# > Criacao da Tag.
# > Opcional: `-a v1.0.1 -m "Release do novo componente"`.
git tag v1.0.1
# > Criar Tag remotamente (as duas maneiras estao corretas).
git show v1.0.1 && git push origin v1.0.1
git push --tags
# > Mergear nossa release na master.
git checkout master && git merge release/v1.0.1
```

![git-flow](https://media2.dev.to/dynamic/image/width=1600,height=900,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fsqxc7kepfadqqkg6sgdn.png)

## Cheatsheet

- https://training.github.com/downloads/pt_BR/github-git-cheat-sheet.pdf

```sh
1. Fazer um fork do projeto p/ seu github.
2. Clonar o repositorio forkado:
	> git clone [repo_link]
3. Criar uma branch onde ficara suas modificacoes:
	> git checkout -b [branch_name]
4. Fazer suas alteracoes.
5. Commitar mudancas:
	> git add [file_name]
	> git commit -m [comment]
6. Enviar alteracoes:
	> git push origin [branch_name]
7. Criar um pull request no github (compare & pull request).
```

# Commands

## Copiando / Clonando / Conectando um Repositorio

```sh
# REPOSITORIO VIA HTTP
git clone [project_link]

# REPOSITORIO REMOTO (VIA SSH)
git clone user.server@:/path/to/repo

# CONECTANDO / DESCONECTANDO REPO LOCAL A NUVEM
git remote add origin <project_link>
git remote remove origin <project_link>
```

## Obtendo Informacoes do Repositorio

```sh
# VER ESTADO DO GIT
git status

# VER ALTERACOES ENTRE ARQUIVOS / BRANCHES
git diff [origin_branch_name | commit-A] [target_branch_name | commit-B]

# VER TODAS AS ALTERACOES QUE FORAM FEITAS NO REPO LOCAL
git reflog
```

## Atualizando / Modificando Repositorio Local

```sh
# ATUALIZANDO REPOSITORIO LOCAL
git pull # git pull == git fetch + git merge

# CRIAR REPOSITORIO LOCAL
git init

# ADICIONANDO SEUS ARQUIVOS AO GIT
git add -i # (forma interativa)
git add <filename> # (1 por vez)
git add . # (todo o diretorio)

# CRIANDO COMMITS
git commit -m 'comments' # (arquivos nao comentados previamente)
git commit -am 'comments' # (arquivos comentados previamente - ammend)

# DESFAZENDO COMMITS
git log --pretty=oneline --color # (pegar a commit-key)
git revert <commit_key>
git reset HEAD~<number_of_commits>

# CRIANDO BRANCHES LOCAIS
git checkout -b <branch_name>

# EXCLUINDO BRANCHES LOCAIS
git branch -D <branch_name>

# RENOMEANDO BRANCHES
git branch -M <old_name> <new_name>

# NAVEGANDO ENTRE BRANCHES
git switch <branch_name>
git checkout <branch_name>

# REVERTENDO ALTERACOES LOCAIS
git checkout -- <file_name>

# MESCLANDO BRANCHES
git merge <branch_name>

# TAGGING
git tag <tag> <commit_key>
```

## Atualizando / Modificando Repositorio Remoto

```sh
# ENVIANDO SUAS ALTERACOES
# O `-u` define a "track upstream", usa-se apenas na primeira vez, depois nao ha necessidade.
git push -u origin <branch_name>
git push origin <branch_name>

# EXCLUINDO BRANCHES REMOTAS
git push origin --delete <remote_branch_name>
```

## Manipulacao de Commits

```sh
# REMOCAO DE TODAS AS ALTERACOES / COMMIT LOCAIS
git fetch origin && git reset --hard origin/master

# SOFT / HARD RESET
# Os commits posteriores continuam na staging area.
git reset <commit_key>
# Os commits posteriores e quaisquer alteracoes serao permanentemente deletadas.
git reset --hard

# MANIPULAR HISTORICO DE COMMITS
# Reordena / combina / edita / descarta commits.
git rebase <branch_rebase_from>

# APLICAR COMMIT ESPECIFICO DE UMA BRANCH PARA OUTRA
# Traz alteracao especifica de um branch p/ outro sem mesclar / rebasear a branch inteira.
git cherry-pick [commit_hash_incoming_branch]
```
