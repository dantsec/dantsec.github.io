---
title: Assembly x86 @ Crash Course
published: 2026-02-02
description: 'Main concepts of ASMx86 that you need to know.'
image: ''
tags: [Programming, Crash-Course]
category: Programming
draft: false
lang: 'pt-br'
---

# Introduction

## Tools

- **Syscall Table**:
	- Voce pode usar `man syscalls` ou [este site](https://syscall.sh/).
- **Debugger**:
	- `sudo apt install strace`.
- **Compilador**:
	- O **NASM** (_The Netwide Assembly_) eh um compilador e linkeditor da linguagem assembly.

## Concepts

### Program vs. Source-Code

- Um programa geralmente se refere a uma **sequencia de instrucoes enviadas a um computador para que ele execute algo**;
- Um programa combinado com todos os outros recursos necessarios para sua execucao eh conhecido como **codigo objeto**;
- A palavra **codigo-fonte** eh reservada em geral para o codigo (de maquina ou de alto nivel) **usado para criar o programa**.

### Overflow vs. Underflow

- Calculos usando numeros em ponto flutuante podem gerar overflow e underflow se o algoritmo usado produzir um resultado que saida do intervalo aceitavel de valores;
- Por exemplo, se o resultado de um calculo eh um valor proximo de zero que nao pode ser expresso com precisao usando os bits disponiveis, ele gera o que chamamos de underflow.

### CPU Benchmark

- O **desempenho** da CPU eh determinado pela **velocidade de clock da CPU e sua velocidade de execucao de operacoes**;
- A velocidade do clock nos informa com que frequencia os circuitos logicos na ALU podem executar calculos, e a velocidade de execucao de operacoes nos informa o quao rapidamente a CPU pode executar calculos um apos o outro;
- Blocos de ALU de **CPUs mais antigas funcionavam apenas com aritmetica inteira**, por isso, o desempenho da CPU era medido em _quantas instrucoes ela podia trazer em um segundo_, o seu valor de **MIPS** (milhoes de instrucoes por segundo), em vez de quao rapidamente ela podia executar operacoes de calculo;
- Mas **CPUs modernas tem hardware integrado especializado apenas para a finalidade de calculos com ponto flutuante** e, por isso, recentemente a medida de desempenho preferia tornou-se a _quantidade de operacoes em ponto flutuante que a CPU pode executar em um segundo_, ou **MFLOPS** (milhoes de operacoes em ponto flutuante por segundo);
- Usa-se, para essa medicao, operacoes em ponto flutuante com 15 digitos significativos;
- As vezes usamos unidades diferentes de MFLOPS, como GFLOPS (gigaFlops) e TFLOPS (teraFLOPS).

### Big Endian vs Little Endian

- Define como bytes de um valor multibyte sao organizados na memoria, e faz referencia a primeira posicao desse valor, que pode receber o **MSB (Most Significant Bit)** ou o **LSB (Least Significat Bit)**;
- No caso do **MSB na primeira posicao**, temos o **Big Endian**, que seria a ordem "natural" para leitura humana, usado em protocolos de rede e alguns RISC antigos;
- Ja quando temos o **LSB na primeira posicao**, temos o **Little Endian**, que pode ser interpretado como a leitura contraria a "natural" humana, usada pela maioria das CPUs modernas e arquiteturas x86 / x86_64 / ARM.

```
> 0x12345678

BE:
	+0   +1   +2   +3
	12   34   56   78

LE:
	+0   +1   +2   +3
	78   56   34   12
```

### GOT Table and PLT Table

- A **GOT (Global Offset Table)**, eh uma tabela em memoria que guarda os enderecos reais das funcoes e variaveis dinamicas (majoritariamente simbolos definidos em _shared objects_) em **tempo de execucao**;
- A **PLT (Procedure Linkage Table)** eh um codigo _stub_ ("duble" de uma funcao real) usado para chamar funcoes de bibliotecas dinamicas;
- **A PLT consulta a GOT para saber onde saltar** (mas nao logicamente), o que ela faz eh **indirecionar o fluxo** via ponteiro armazenado na GOT;
- Funcionamento:

```
> Primeira Chamada:
- Resolve o addr real via "dynamic linker".

main
 │
 │ call puts@plt
 ▼
.plt[puts]
 │
 │ jmp *puts@got        ← ponteiro ainda NÃO resolvido
 ▼
.got[puts] ──────────────┐
                         │ (aponta inicialmente para)
                         ▼
                    .plt[0]  (resolver stub)
                         │
                         │ push reloc_index
                         │ push link_map
                         │ jmp ld.so
                         ▼
                dynamic linker (ld-linux.so)
                         │
                         │ resolve símbolo "puts"
                         │ encontra puts em libc.so
                         │ escreve addr real em puts@got
                         ▼
                     puts (libc.so)

> Proximas Chamadas (sem linker no meio)
- Vao direto para o addr resolvido.

main
 │
 │ call puts@plt
 ▼
.plt[puts]
 │
 │ jmp *puts@got  ─────────────► puts (libc.so)
```

#### ROP e JOP

- Sao tecnicas avancadas de exploracao de vulnerabilidades usadas para **executar codigo arbitrario** mesmo quando protecoes modernas estao ativas.

#### ROP (Return-Oriented Programming)

- Explora **falhas de buffer overflow para manipular a pilha**;
- Em vez de injetar codigo novo, o atacante reutiliza pequenos trechos de codigo legitimo ja existentes no programa, chamado **gadgets**;
- Cada gadget termina com uma instrucao `ret`, permitindo "encadear" execucoes;
- Contorna protecos como _DEP_ / _NX_ (memoria nao executavel);
- Basicamente usamos os `ret` do proprio programa para montar um "programa" malicioso.

#### JOP (Jump-Oriented Programming)

- Evolucao do _ROP_, criado para contornar defesas especificas contra _ROP_;
- Em vez de `ret`, utiliza instrucoes de salto indireto (`jmp`, `call`);
- Nao depende da pilha da mesma forma, usa registradores para controlar o fluxo;
- Basicamente controlamos saltos para encadear gadgets sem usar `ret`.

## Creating a Lib

- Nomeamos o arquivo com a extensao `.inc`;
- Para incluirmos no nosso programa, utilizamos `%include FILENAME.inc`;
- Alem disso, quando usamos bibliotecas nao usamos `sections`, mas sim `segments` (que sao organizacoes fisicas na memoria), que no final das contas recebem os mesmos nomes (`text`, `bss`, `data`, etc).

## Syntax

- Utiliza uma sintaxe simples e diferente do usual, mas simples: `label name operands ;comment`;
	- **Label**: nome pessoal opcional que damos a uma instrucao em nosso codigo;
	- **Name**: nome da operacao que iremos realizar;
	- **Operands**: lista opcional de parametros da funcao;
	- **Comment**: indicado por um `;`, funciona como um comentario.

## Registers

- O mnemonico _E_ nos registradores significa **extended**;
- Bootloaders sao feitos em _16 bits_, e posteriormente vao para _32 bits_;
- Na "caixa preta" da CPU (nao acessivel ao programador) temos o que chamamos de **temp register**, que armazena resultados intermediarios e auxiliam em instrucoes microcodificadas, tudo isso por "debaixo dos panos";
- Os principais sao:
    - Proposito _geral_:
        - **A** (accumulator):
	        - Armazena os resultados dos calculos da ALU;
	        - Projetado de tal modo que esta pronto para o proximo calculo assim que o anterior tiver terminado.
        - **B** (base):
	        - Frequentemente usado como registrador base para enderecamento indireto.
        - **C** (counter):
	        - Usado como contador de loops e instrucoes de repeticao.
        - **D** (data):
	        - Auxiliar de `AX` em operacoes de multiplicacao / divisao;
	        - Em BIOS, pode conter argumentos para interrupcoes;
	        - Tambem usado para acessar interface I / O.
    - Proposito _especifico_:
        - **SP** (stack pointer):
	        - Aponta para o topo da stack;
	        - Que, por sua vez, cresce "para baixo" na memoria;
	        - Usado automaticamente em instrucoes `push`, `pop`, `call` e `ret`.
        - **BP** (base pointer):
	        - Usado para acessar argumentos em funcoes;
	        - Permite acesso estavel a stack mesmo quando _SP_ muda.
        - **SI** (source index) (16 bits):
	        - Usado como ponteiro de origem em operacoes de string;
	        - Instrucoes como `movsb`, `cmpsb` e `lodsb` usam _SI_ implicitamente.
        - **DI** (destination index) (16 bits):
	        - Complemento do _SI_;
	        - Usado como destino em operacoes de string.
        - **IP** (instruction pointer):
            - Aponta para o endereco da proxima instrucao a ser executada;
            - Manipulado indiretamente por saltos, interrupcoes e retornos.

| 64 bits  | 32 bits    | Utilizacao                                                         |
| -------- | ---------- | ------------------------------------------------------------------ |
| rax      | eax        | Valores que sao retornados dos comandos em um registrador          |
| rbx      | ebx        | Registrador reservado, cuidado ao utiliza-lo                       |
| rcx      | ecx        | Uso livre, como por exemplo contador                               |
| rdx      | edx        | Uso livre em alguns comandos                                       |
| rsp      | esp        | Ponteiro de uma pilha                                              |
| rbp      | ebp        | Registrador preservado, algumas vezes armazena ponteiros de pilhas |
| rdi      | edi        | Na passagem de argumentos, contem a quantidade desses              |
| rsi      | esi        | Na passagem de argumentos, contem os argumentos em si              |
| r8 ~ r15 | r8d ~ r15d | Utilizados nas movimentacoes correntes durante o nossa programa    |

### Schema

```
+--------------------------------------+
|          General-purpose Registers   |
+--------------------------------------+
| EAX (32 bits)                        |
|  +----------------+                  |
|  | AX (16 bits)   |                  |
|  |  +----+----+   |                  |
|  |  | AH | AL |   | <- AH: 8 bits    |
|  |  +----+----+   |    AL: 8 bits    |
+--------------------+-----------------+
| EBX (32 bits)                        |
|  +----------------+                  |
|  | BX (16 bits)   |                  |
|  |  +----+----+   |                  |
|  |  | BH | BL |   | <- BH: 8 bits    |
|  |  +----+----+   |    BL: 8 bits    |
+--------------------+-----------------+
| ECX (32 bits)                        |
|  +----------------+                  |
|  | CX (16 bits)   |                  |
|  |  +----+----+   |                  |
|  |  | CH | CL |   | <- CH: 8 bits    |
|  |  +----+----+   |    CL: 8 bits    |
+--------------------+-----------------+
| EDX (32 bits)                        |
|  +----------------+                  |
|  | DX (16 bits)   |                  |
|  |  +----+----+   |                  |
|  |  | DH | DL |   | <- DH: 8 bits    |
|  |  +----+----+   |    DL: 8 bits    |
+--------------------------------------+

+--------------------------------------+
|         Special-purpose Registers    |
+--------------------------------------+
| ESP (Stack Pointer)  (32 bits)       |
+--------------------------------------+
| EBP (Base Pointer)   (32 bits)       |
+--------------------------------------+
| ESI (32 bits)                        |
+--------------------------------------+
| EDI (32 bits)                        |
+--------------------------------------+
```

### 8 bits Segments

- Sempre que tratamos de um unico caractere temos um **byte isolado (8 bits)** e podemos usar os operadores desse segmento para realizar transformacoes;
- Essas transformacoes ocorrem nos segmentos de 8 bits dos registradores, como por exemplo, o `al`.

### Flags (Flags Register)

- Tambem chamado de **FLAGS** (16 bits), **EFLAGS** (32 bits) ou **RFLAGS** (64 bits);
- Guarda informacoes sobre o resultado da ultima operacao da CPU e controla certos comportamentos do processador;
- Nao armazena dados, e sim **estados e condicoes**, util para desvios;
- As principais flags sao:
	- **ZF / Zero Flag / Flag-Z**:
		- Indica se o acumulador eh zero;
		- Se a CPU nao tiver um modulo dedicado par afazer comparacoes, essa flag tambem pode ser o flag que reporta o resultado de um teste de comparacao (a **Flag-EQ** - outras flags podem ser implementadas na ULA, como **Flag-GT** e **Flag-LT**).
	- **SF / Sinal Flag / Flag-S / Negative Flag / Flag-N**:
		- Se o acumulador contem um numero, esse flag diz se o numero eh negativo ou positivo.
	- **CF / Carry Flag / Flag-C**:
		- Indica se houve carry / borrow em uma operacao **sem sinal (unsigned)**;
		- Se preocupa com limites binarios, nao com valores positivos / negativos;
		- Pode-se chamar de **unsigned overflow**, pois esta ligada a "estourou os bits disponiveis?", e nao sabe nada sobre numero negativo.
	- **OF / Overflow Flag / Flag-OV**:
		- Indica erro de magnitude em **operacoes com sinal (signed)**, ou seja, se o resultado ultrapassou o intervalo designado;
		- Na soma, a flag eh ativada se, ao somar dois numeros do mesmo sinal, o resultado apresenta um sinal diferente, isso porque o **bit MSB designa o sinal em operacoes signed**;
		- Basicamente, mede o **signed overflow**, e esta ligado a mudanca inesperada de sinal e nao tem relacao com carry / borrow.
	- **PF / Parity Flag**:
		- Indica se o numero de bits 1 no resultado da ultima operacao eh par;
		- Usado principalmente em operacoes antigas de verificacao de erro (pense como se fosse um _checksum_ a nivel de hardware) e no comportamento de algumas instrucoes especificas.
	- **DF / Direction Flag**:
		- Determina a direcao (frente ou tras) de avanco dos registradores _SI_ e _DI_ nas instrucoes de string.
	- **IF / Interrupt Flag**:
		- Controla se a CPU **aceita interrupcoes mascaraveis** (interrupcoes externas normais), que determina que tipos de interrupcoes ocorrerao;
		- Essa flag eh manipulada com instrucoes como _CLI_ (Clear Interrupt Flag) e _STI_ (Set Interrupt Flag).

### Command Categories

- Existem 3 categorias, sao elas:
    - **Movimentacao de Dados**:
        - `mov`;
        - `movzx` (_move with zero-extended_):
	        - Os bits superiores do operador de destino sao preenchidos com zero.
        - `push`;
        - `pop`;
        - `lea`.
    - **Logica Aritmetica**:
        - `add`, `inc`;
        - `sub`, `dec`;
        - `imul`;
        - `idiv`;
        - `div`:
            - Divide pelo valor presente em _eax_;
            - Quociente vai para _eax_;
            - Resto vai para _edx_.
        - `and`, `or`, `xor`, `not`;
        - `neg`;
        - `shl`, `shr`;
            - `sh` eh o mesmo que _shift_;
            - E _l_ eh _left_ e _r_ eh _right_.
    - **Controle de Fluxo**:
        - `jmp` (e suas variacoes);
        - `cmp`;
        - `call`, `ret`.

## Sections

- Serve para a organizacao logica do codigo;
- Possuimos 4 _sections_, sao elas:
    - Texto executavel (`.text`);
    - Dados `READ-ONLY` (`.rodata`);
    - Dados `READ-WRITE` inicializados (`.data`);
    - Dados `READ-WRITE` nao inicializados (`.bss` - _Block Starting Symbol_).

## Data Types

- Diretivas de alocacao de memoria para armazenar diferentes tamanhos;
- Tipos usados para **variaveis inicializadas**, na _section_ `.data`:

| Sigla | Tipo               | Significado                          | Bytes    | Operador          |
| ----- | ------------------ | ------------------------------------ | -------- | ----------------- |
| db    | Define Byte        | Alocacao de 8 bits                   | 1 byte   | `BYTE[]`          |
| dw    | Define Word        | Alocacao de 16 bits                  | 2 bytes  | `WORD[]`          |
| dd    | Define Doubleword  | Alocacao de 32 bits                  | 4 bytes  | `DWORD[]`         |
| dq    | Define Quadword    | Alocacao de 64 bits                  | 8 bytes  | `QWORD[]`         |
| ddq   | Define Double Quad | Alocacao de 128 bits - para inteiros | 10 bytes | **Nao Aplicavel** |
| dt    | Define Ten Bytes   | Alocacao de 128 bits - para decimais | 10 bytes | **Nao Aplicavel** |

- Tipos usados para **variaveis nao inicializadas** (nesse caso arrays de elementos), na _section_ `.bss`:

| Sigla | Tipo        | Significado          |
| ----- | ----------- | -------------------- |
| resb  | byte        | variavel de 8 bits   |
| resw  | word        | variavel de 16 bits  |
| resd  | double      | variavel de 32 bits  |
| resq  | quad        | variavel de 64 bits  |
| resdq | double quad | variavel de 128 bits |

## Addressing Modes

### Absolute Addressing

-  Quando o valor do operando eh usado como o **endereco efetivo** (endereco no qual esta localizado o dado de destino da operacao);
- As vezes ele tambem eh chamado de _direct addressing_.

### Relative Addressing

- Enderecamento relativo eh quando o endereco efetivo resulta da soma do valor do operando e o contador do programa;
- Mais comumente usado para instrucoes do tipo **jump**;
- Uma vez que a distancia ate o endereco que desejamos apontar eh limitada pelo intervalo expresso pelo complemento de dois do numero de bits disponiveis no operando, o enderecamento relativo eh melhor usado para instrucoes de desvio condicional no programa e nao eh recomendado para saltos maiores no espaco de enderecos;
- Alem de usar o contador do programa como valor base para o endereco relativo, podemos usar o endereco em um registrador; chamamos enderecos desse tipo de enderecos _relativos de registrador-xx_.

### Indirect Addressing

- Usado quando o operando contem o endereco para algum registrador e esse registrador, por sua vez contem o endereco efetivo para nosso dado de destino;
- Podemos pensar nele como ponteiros da linguagem C, que trabalham com referencia e deferencia.

### Address Modification

- Processo de usar o valor armazenado em um registrador de modificacao para alterar um numero ou endereco;
- Obtemos o endereco efetivo adicionando o valor no registrador de modificacao a um valor base que pode ser armazenado em outro registrador ou no contador do programa, ou mesmo em um valor imediato;
- Um dos registradores de modificacao mais usados eh o _registrador de indice_;
- Geralmente chamamos o registrador contendo o valor base de _registrador base_;
	- Nesse caso, a maioria das CPUs cria o endereco efetivo simplesmente adicionando o valor no registrador base e o valor no registrador de modificacao.
- Ao usar a modificacao de endereco dessa forma eh possivel obter efeitos muito praticos, como, por exemplo, extrair algum dado particular de um conjunto especificando o deslocamento no registrador de indice e o inicio dos dados definido em um registrador base.

# Deeping in Commands

## Jumpings

### Inconditional

- Usamos a instrucoa `JMP`, e nao depende que nada ocorra;
- Simplificadamente, apenas pula para pontos "etiquetados" (marcadores / _labels_) do programa.

### Conditional

- Usamos, para expressar e representar saltos condicionais, as letras `jcc`;
- http://unixwiz.net/techtips/x86-jumps.html

| Mnemonico | Significado                  | Contrario | Significado                     |
| --------- | ---------------------------- | --------- | ------------------------------- |
| JE        | (==) Salta se igual          | JNE       | (!=) Salta se nao igual         |
| JG        | (>) Salta se maior           | JNG       | (<=) Salta se nao maior         |
| JL        | (<) Salta se menor           | JNL       | (>=) Salta se nao menor         |
| JGE       | (>=) Salta se maior ou igual | JNGE      | (<) Salta se nao maior ou igual |
| JLE       | (<=) Salta se menor ou igual | JNLE      | (>) Salta se nao menor ou igual |

## Functions

### How Call / Ret Works?

- O funcionamento das instrucoes `CALL` e `RET` esta diretamente ligado a **pilha de execucao (stack)**, que eh usada para armazenar o endereco de retorno quando uma sub-rotina (funcao) eh chamada.

#### Call

- A instrucao `CALL` eh usada para desviar a execucao para uma sub-rotina (funcao);
- Quando `CALL` eh executado:
    - O endereco da proxima instrucao (aquela que vem apos o `CALL`) eh **empilhado** na **stack**;
    - O fluxo de execução **salta** para o endereco da sub-rotina.

#### Ret

- A instrucao `RET` eh usada para retornar da sub-rotina;
- Quando `RET` eh executado:
    - O processador **desempilha** o endereco salvo na pilha;
    - Esse endereco eh carregado no **contador de instrucoes** (`EIP` em _x86_, `RIP` em _x86-64_);
    - A execucao continua de onde parou antes do `CALL`.

#### How Memory Works?

- A pilha funciona como uma **estrutura LIFO (Last In, First Out)**;
- Quando `CALL` é executado:
    - O processador **empilha** o endereco de retorno na pilha;
    - Quando `RET` eh chamado, o processador **desempilha** esse endereco e retorna a execucao normal.

```
> Suponha que o `EIP` esteja em `0x1000` e chamamos `CALL` para `0x2000`.

| Endereco | Conteudo (antes do CALL) |
|----------|--------------------------|
| ...      | ...                      |
| 0xFFFC   | ???                      |

> Apos `CALL 0x2000`:

| Endereco | Conteudo (depois do CALL) |
|----------|---------------------------|
| ...      | ...                       |
| 0xFFFC   | 0x1003 (endereco de ret)  |

> Agora, quando `RET` for chamado dentro da funcao em `0x2000`:
    1. O endereco `0x1003` sera retirado da pilha;
    2. A execucao continuara a partir de `0x1003`.
```

### Load Effective Address (lea)

- Instrucao utilizada para **calcular enderecos**, ou seja, obter endereco de memoria de uma variavel ou expressa o **sem acessar o conteudo** da memoria naquele endereco;
- Simplificadamente, calcula um endereco e o coloca em um registrador, nao acessando diretamente a memoria;
- Quando usar:
    - Calcular enderecos (como ao obter o endereco de uma variavel ou de um elemento em um array);
    - Quando se precisa de um valor em um registrador, mas nao quer acessar diretamente o valor armazenado na memoria.

## Loops

- Usam a instrucao `loop`;
- Esta, por sua vez, tem como delimitador o registrador `ecx`, e sempre **decrementa-o**, caso seja **igual a zero**, vai para a **proxima instrucao**.

```asm
; Global Label
_start:
    mov ecx, 0x1

    ; Local Label
    .next_digit:
	    ; Here, ecx was dec by 1
        loop .next_digit

	.finish:
		ret
```

## Arrays

- Sao dados que estao **sequencialmente na memoria**;

> Para acessa-los, basta usar a equacao: (label_name) + (label_data_size) * position.

```asm
; Neste exemplo como os dados sao inteiros (4 bytes) devemos utilizar esse valor como offset;
; E eh por isso que o index dos arrays comecam por 0.

section .data
    array: DD 10, 22, 13, 14, 55

; ...

_start:
    print_output:
	    ; (array) + (4) * 3
        mov eax, [array + 4 * 3] ; 14

; ...
```

# File Handling

## Introduction

- Primeiro, vamos conhecer alguns valores:

```
; Operacoes Basicas

EAX:
    0x3: Op. Leitura do Arquivo
    0x4: Op. Escrita do Arquivo
    0x5: Op. Abertura do Arquivo
    0x6: Op. Fechamento do Arquivo
    0x8: Op. Criacao do Arquivo
ECX:
    0x0: Arquivo aberto para Leitura
    0x1: Arquivo aberto para Escrita
    0x2: Arquivo aberto para Leitura e Escrita
    0x40: Criar arquivo caso nao exista
    0x400: Preparado para novas adicoes de valores

; Localizacoes no Arquivo

EAX:
    0x13: Op. de localizacao no arquivo

EDX:
    0x0: A partir do Inicio do Arquivo (SEEK_SET)
    0x1: Na Posicao que Estiver o Cursor (SEEK_CUR)
    0x2: Final do Arquivo (SEEK_END)
```

- Outro ponto importante eh o **file descriptor** (`fd`), que vai ser responsavel por **salvar o local do arquivo na memoria**, e qualquer operacao vai ter esse ponteiro como referencia;
- Quando lemos ou gravamos um arquivo o conteudo eh lido (ou gravado) por partes e nao de modo instantaneo;
    - O SO envia a informacao para um buffer e o descarrega fisicamente na trilha de informacao;
    - Sendo assim, quanto maior esse buffer mais rapido sera feito os processos com o arquivo, porem mais memoria sera utilizada.
- Por fim, eh importante sempre que definir um `file_path` coloque um terminador `0`, exemplo:

```
file_path db "grades.txt", 0
```

## Writing in a File

- Para setarmos as permissoes devemos ter em mente valores octais respectivos para `read` (4), `write` (2) e `execute` (1);
- E, semelhante aos sistemas Unix, a soma das permissoes resulta na permissao final que deve ser manejada em 3 octais, sendo eles:
    - Permissoes de usuario como **dono**;
    - Permissoes de **grupo de usuario** do dono;
    - Permissoes de **terceiros**.

## Walking Through a File

- Para andarmos sobre um arquivo primeiro devemos indicar a operacao em `eax` no valor de SEEK_FILE (_0x13_);
- Depois, definir o _file descriptor_ em `ebx`;
- Depois, dizer a quantidade de caracteres para saltar (parte complicada) em `ecx`;
- E por fim, definir a maneira de salto a partir do inicio (**SEEK_SET**), cursor (**SEEK_CUR**) ou no final (**SEEK_END**).

# Union with C / Cpp

- O que realmente nos importa eh o `extern`, que indica o **nome de um marcador global** que devemos definir no assembly;
- A ordem de argumentos que vem para os registradores sao:
    - **RDI** (primeiro argumento), **RSI** (segundo argumento), **RDX** (terceiro argumento), **RCX** (quarto argumento), **R8** (quinto argumento), **R9** (sexto argumento).
- Eh preciso ficar atento ao registrador `EBX`, pois ele eh reservado do sistema e caso seja utilizado eh necessario garantir que o valor original seja restaurado.

```cpp
// main.cpp
#include <iostream>

using namespace std;

extern "C" int GetValorASM(int a);

int main() {
    cout << "ASM me deu " << GetValorASM(32) << endl;
    return 0;
}

// main.asm
section .text

global GetValorASM

GetValorASM:
    mov eax, edi
    add eax, 1
    ret

// makefile
NAME = main

all: $(NAME).cpp $(NAME).o
	g++ $(NAME).o $(NAME).cpp -o $(NAME)

	rm -rf $(NAME).o

%.o: %.asm
	nasm -f elf64 $<
```

# Tips

## Calculating String Size

- Comecando com `mov edx, ecx`, ficamos com ambos os registradores apontando para o mesmo endereco;
- Verificamos se chegamos no _NULL Byte_, caso nao incrementamos `edx`, ate que o mesmo chega ao final da string (demarcado por `\0`);
- Por fim, devemos fazer a subtracao de `edx` por `ecx`, ja que um aponta para o endereco final e o outro para o endereco inicial, assim descobrimos o tamanho da string.

```asm
// main.asm
; Example:
;
; 0x1000: 'H'
; 0x1001: 'e'
; 0x1002: 'l'
; 0x1003: 'l'
; 0x1004: 'o'
; 0x1005: '\0'
;
; 0x1005 - 0x1000 = 5 (len)

string_size:
    mov edx, ecx

    .next_char:
        ; edx* = '\0'
        cmp byte[edx], NULL

        ; if true, goto .end
        je .end

        ; edx++
        inc edx

        ; goto .next_char
        jmp .next_char

    .end:
        ; str_len = end_addr - start_addr
        sub edx, ecx

        ret

// makefile
NAME = main

all: $(NAME).o
	ld -s $(NAME).o -o $(NAME)
	rm -rf *.o;

%.o: %.asm
	nasm -f elf64 $<

clean:
	rm -rf *.o $(NAME)
```

# Brief ASMx64 Introduction

- Agora, com um recurso muito poderoso: as **Pilhas**;
- Seguem uma estrutura **LIFO** (_Last In, First Out_);
- Possui dois comandos principais sao eles:
    - **PUSH**: usado para **empilhar** um elemento no topo;
        - `push [data]`: empilha o dado na pilha.
    - **POP**: usado para **remover** o elemento do topo;
        - `pop [reg]`: coloca o elemento removido no registrador.
