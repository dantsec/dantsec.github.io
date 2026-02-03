---
title: Numeric Bases @ Crash Course
published: 2026-02-02
description: 'Main concepts of Numeric Bases that you need to know.'
image: ''
tags: [Crash-Course, Math]
category: Math
draft: false
lang: 'pt-br'
---

# Introducao

## Notacao Posicional

- Cada posicao de um digito tem um valor diferente dentro de um número;
- Em bases diferentes das de _10_ (decimais), le-se dizendo numero por numero;
- As bases mais comuns utilizadas na computacao sao **base 2 (binarios)**, **base 8 (octais)** e **base 16 (hexadecimais)**.
	- Sistema decimal: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9;
	- Sistema binario: 0, 1;
	- Sistema octal  : 0, 1, 2, 3, 4, 5, 6, 7;
	- Sistema hexadecimal : 0 ao 9 e A ao F.

## Sistema Decimal (Base 10)

- Usamos o sistema decimal, tambem chamado de sistema de _base 10_, denotamos da seguinte maneira:

```c
# Notation
S = 10^n + ... + 10^3 + 10^2 + 10^1 + 10^0

# Example
3785 (10) = 3 * 10^3 + 7 * 10^2 + 8 * 10^1 + 5 * 10^0
```

# Sistema Binario (Base 2)

- Contem `X` possibilidades, onde `X` pode ser definido como:

```c
// Num intervalo
// Assinadas: [-2^(8*x - 1) ... 2^(8*x - 1) - 1]
// Unsigneds: [0...2^(8*x) - 1]
x bytes = 2^(8 * x) bits

// Exemplo
1 byte = 2^(8 * 1) bits

[-2^(8*x - 1)...2^(8*x - 1) - 1]
[-2^(7)...2^(7) - 1] = [-128...127]
[0...2^(8*1)] = [0...255]
```

```c
# Notation
S = 2^n + ... + 2^3 + 2^2 + 2^1 + 2^0

# Combinar
0, 1, 10, 11, 100, 101,
110, 111, 1000, 1001, 1010,
1011, 1100, 1101, 1110, 1111,
...
```

## Conversao Binario (2) para Decimal (10)

```c
// Exemplo
1011 (2) = 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0 = 11 (10)
```

## Conversao Decimal (10) para Binario (2)

1. Divida o numero decimal por 2 ate que nao seja mais possivel dividi-lo;
2. 0's a esquerda sao facultativos.

```c
// EX1
13 =>
	13 / 2 = 6; 1 -> resto
	6  / 2 = 3; 0
	3  / 2 = 1; 1
	1  / 2 = 0; 1

Pegar a ordem inversa dos restos:
	13 (10) = 1101 (2)

// EX2
11,3 =>
	- Parte Inteira;
	P1) Pega a ordem inversa.
		11 / 2 = 5; 1
		5  / 2 = 2; 1
		2  / 2 = 1; 0
		1  / 2 = 0; 1

	- Parte Fracionaria;
	P2) Pega a ordem normal.
		0,3 * 2 = 0,6; 0
		0,6 * 2 = 1,2; 1
		0,2 * 2 = 0,4; 0
		0,4 * 2 = 0,8; 0
		0,8 * 2 = 1,6; 1
		0,6 * 2 = 1,2; 1
		...

11,3 (10) = 1011.010011... (2)
```

# Sistema Octal (Base 8)

## Conversao Octal (8) para Decimal (10)

```c
# Notation
S = 8^n + ... + 8^3 + 8^2 + 8^1 + 8^0

# Example
371 (8) = 3 * 8^2 + 7 * 8^1 + 1 * 8^0 = 249 (10)
```

## Conversao Decimal (10) para Octal (8)

1. Divida o numero decimal por 8 ate que nao seja mais possivel.

```c
// EX1
177 =>
	177 / 8 = 22; 1
	22  / 8 = 2;  6
	2   / 8 = 0;  2

Pegar a ordem inversa dos restos:
	177 (10) = 261 (8)

// EX2
0,634 =>
	0,634 * 8 = 5,072; 5
	0,072 * 8 = 0,576; 0
	0,576 * 8 = 4,608; 4
	0,608 * 8 = 4,864; 4
	...

Pegar os restos em ordem:
	0,634 (10) = 0,5044... (8)
```

# Sistema Hexadecimal (Base 16)

## Conversao Hexadecimal (16) para Decimal (10)

```c
# Notation
S = 16^n + ... + 16^3 + 16^2 + 16^1 + 16^0

# Example
1FA (16) = 1 * 16^2 + 15 * 16^1 + 10 * 16^0 = 506 (10)
```

## Conversao Decimal (10) para Hexadecimal (16)

1. Divida o numero decimal por 16 ate que nao seja mais possivel,

```c
// EX1
685 =>
	685 / 16 = 42; 13 = D
	42  / 16 = 2;  10 = A
	2   / 16 = 0;  2

1. Pegar a ordem inversa dos restos
2. Para os acima de 10, substitui-los por letras

// EX2
=> 685 (10) = 2AD (16)

178,6 =>
	1) 178 = B2
	2) 0,6 =>
		0,6 * 16 = 9,6; 9
		0,6 * 16 = 9,6; 9
		...

=> 178,6 (10) = B2,9 (16)
```

# Relacao entre Sistemas de Numeracao

- Na computacao nao usamos bases octais e hexadecimais a toa. Elas facilitam (e muito) quando vamos converter dados para binario;
- O processo eh simples, basta splitarmos / agruparmos o valor e fazer a conversao.

## Conversao Octal (8) para Binario (2)

1. Cada digito do octal corresponde a 3 digitos do binário (pois 8 = 2^3). Assim, temos que dividir cada digito do octal em 3 partes.

```c
27 (8):

2        7

0 1 0    1 1 1
_ _ _    _ _ _
4 2 1    4 2 1  => potencias da base 2 (..., 2^2, 2^1, 2^0)

Agora basta juntar tudo, dessa forma:

27 (8) = 010111 (2) ou 10111 (2)
```

## Conversao Binario (2) para Octal (8)

1. Dividir o numero binario em grupos de 3 de tras para frente.

```c
1000101 (2):

0 0 1 | 0 0 0 | 1 0 1
_ _ _   _ _ _   _ _ _
4 2 1   4 2 1   4 2 1

1       0       5

Agora basta juntar os digitos:

1000101 (2) = 105 (8)
```

## Conversao Hexadecimal (16) para Binario (2)

1. Dividimos cada digito do "numero" hexadecimal em 4 partes (pois 16 = 2^4).

```c
1B (16):

1          B = 11

0 0 0 1    1 0 1 1
_ _ _ _    _ _ _ _
8 4 2 1    8 4 2 1  => potencias da base 2 (..., 2^2, 2^1, 2^0)


Agora basta juntar tudo, dessa forma:

1B (16) = 11011 (2)
```

## Conversão Binario (2) para Hexadecimal (16)

1. Dividir o numero binario em agrupamentos de 4 de tras para frente.

```c
1011101 (2) =>

0 1 0 1 | 1 1 0 1
_ _ _ _   _ _ _ _
8 4 2 1   8 4 2 1

5          13 = D

=> 1011101 (2) = 5D (16)
```

## Conversao Octal (8) para Hexadecimal (16)

1. Transforme em binario em grupos de tres;
2. Depois divida-os em grupos de quatro.

```c
33 (8) =>

   3        3
 0 1 1    0 1 1
 _ _ _    _ _ _

0 0 0 1 | 1 0 1 1
|.|
 .-> 0's para fechar o grupo

Agora basta transformar em hexadecimal:

1 | B => 1B (16)
```

## Conversao Hexadecimal (16) para Octal (8)

1. Transforme em binario em grupos de quatro;
2. Divida-os em grupos de tres.

```c
1B (16) =>

  1        B

0 0 0 1  1 0 1 1
_ _ _ _  _ _ _ _

0 0 0 | 0 1 1 | 0 1 1
|
|-> 0 para fechar o grupo

Agora basta transformar em octal:

0 | 3 | 3 => 33 (8)
```

# Operacoes com Binarios

## Adição

- Regras:

```c
1. 0 + 0 = 0
2. 0 + 1 = 1
3. 1 + 0 = 1
4. 1 + 1 => 10 (== 2 (10))
5. 1 + 1 + 1 => 11 (2) (== 3 (10))
```

- Exemplo:

```c
1101 (2) + 1111 (2) = 11100 (2)

+1+1+1+1
  1101
+ 1111
-------
11100
```

## Subtracao

- Regras:

```c
1. 1 - 0 = 1
2. 1 - 1 = 0
3. 0 - 0 = 0
4. 0 - 1 = 1 ("e pegar 1 emprestado da casa do lado")
```

- Exemplo:

```c
1110 (2) - 1011 (2) = 11 (2)

-1               -1 +1
1110             110(10) => 2
- 1011      =>   - 1011
-------          -------
					0011
```

## Sinal Modulo / Magnitude

1. O 1° digito (esquerda) representa o sinal do numerom 0 para positivo e 1 para negativo;
2. Igualar o numero de digitos;
3. Representar todos os numeros em quantidades iguais (ex: 8, 16, 32 bits);
4. Primeiro se converte o numero para binario e depois igualamos ele ao numero de bits sendo que o 1° numero ira representar o sinal (positivo ou negativo).

```c
-> Representar o 21 (10) positivo e negativo

21 (10) = 10101 (2) = 00010101 (2)
	                  |----> complemento para ter 8 bits

21 (10) = 10101 (2) = 10010101 (2)
```

## Complemento de 1

- O complemento de 1 de um numero binario eh a inversao dos digitos (ou melhor dizendo, o complemento de um numero eh o quanto falta para que ele chegue no ultimo digito do sistema numerico).

```c
Complemento de 1 do número 10001110 (2)

10001110 -> 01110001 (2)
```

## Complemento de 2

- Consiste na utilizacao do complemento de 1, somando mais 1 a este complemento.

```c
Complemento de 2 do numero 10001110

1°) Complemento de 1

10001110
-> 01110001

2°) Complemento de 2

01110001
+      1
----------
01110010
```

## Realizando Subtração com Somas com o Complemento de 2

- Para isso, usamos o **complemento de 2**;
- Esse recurso eh muito utilizado em circuitos da ULA;
- Devemos igualar os numeros (ex.: usar o sinal-modulo de 8 bits);
- Somar o 1° numero com o complemento de 2 do 2°.

```c
Representar em sinal-modulo de 8 bits a operacao: 21 (10) - 14 (10)

1°) Transformar em Binario + Sinal Modulo de 8 bits

21 (10) = 10101 (2) -> 00010101 (2)
14 (10) =  1110 (2) -> 00001110 (2)

2°) Complemento no 2° numero

	2.1) Complemento de 1 do 2° numero [14 (10)]

	00001110
	-> 11110001

	2.2) Complemento de 2 do 2° numero [14 (10)]

	11110001
	+      1
	----------
	11110010

3°) Soma do 1° numero com o complemento de 2 do 2°

  00010101
+ 11110010
------------
 100000111

Agora basta retirar esse 1° "1" da frente (pois sao apenas 8 bits).
```
