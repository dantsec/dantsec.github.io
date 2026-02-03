---
title: How Base 2^N works?
published: 2026-02-02
description: 'How the world of Base 2^N works.'
image: ''
tags: [Crypto]
category: Crypto
draft: false
lang: 'pt-br'
---

# What's Base2^N encoding?

- Assim como na Base 10 (decimal) usamos 10 simbolos para representar numeros, o _Encoding Base2^N_ nada mais eh do que mais uma maneira de representar os numeros (ou bytes), e **quanto mais digitos** tivermos, **mais compacto sera a representacao**;
- Observe esse exemplo, onde representamos um mesmo UUID de 128 bits:

```
3d89a119-b3f8-4107-8f29-3daf5b964e50   # standard UUID string
0x3d89a119b3f841078f293daf5b964e50     # hex
81797519916847327862337238645062651472 # decimal
1xh6ghkczr843rya9xnxdsckjg             # base32 (Crockford's variant)

# and binary:
111101100010011010000100011001101100111111100001000001000001111000111100101001001111011010111101011011100101100100111001010000
```

- O **numero disponivel de simbolos determina quantos bits podem ser representados por um unico caractere**, exemplos:
    - Com binarios (Base 2), podemos codificar 1 bit de dado em cada caractere (2^1, 2 combinacoes de caracteres de 1 bit);
    - Da mesma forma, com hexadecimais (Base 16), podemos codificar 4 bits de dado em 1 unico caractere (2^4, 16 combinacoes de caracteres de 4 bits).

# How to convert a number to Base2^N?

- O processo e simples e consiste de tres etapas principais (considere, para os exemplos a seguir, o inteiro Base 10 - decimal - 249);
    - Primeiro, _splitamos o binario em grupos_, e quem define a quantidade de bits em cada grupo eh o ˜N˜ de "2ˆN˜;
    - Depois disso devemos obter a mascara da base, que equivale a "2ˆN - 1";
    - Por fim, fazemos um **bitwise AND** e movemos ˜N˜ bits com **bitwise RIGHT SHIFT**.

```python
number = 249 # 11111001

"""
- Mask = 2ˆ3 - 1 = 7 (10) = 111 (2) = 0x7 (16)
- Shift = 3

    011 111 001
&   000 000 111
---------------
    000 000 001 (1 em Base 10), number >> 3

    000 011 111
&   000 000 111
---------------
    000 000 111 (7 em Base 10), number >> 3

    000 000 011
&   000 000 111
---------------
    000 000 011 (3 em Base 10), number >> 3
"""

MASK = 0x7
SHIFT = 3
converted_number_base8 = []

while number > 0:
    digit = number & MASK
    converted_number_base8.append(digit)
    number = number >> SHIFT

converted_number_base8.reverse()
print(''.join(map(str, converted_number_base8))) # 371
```

- O metodo descrito acima eh usado para encodar numeros, e estamos considerando o input um _chunk_ de tamanho fixo de dados, encodando do da **direita para a esquerda (LSB First)**;
- No entanto, os algoritmos padrao de Base32 e Base64 operam em dados de tamanhos arbitrarios, splitando eles em chunks menores, **comecando da esquerda para a direita (MSB First)**.

# Base32 Implementation (RFC 4648)

## Set of Characters

- Em Base 32 podemos encodar 5 bits de dados em um unico caractere (2ˆ5, 32 combinacoes de caracteres de 5 bits);
- A especificacao _RFC 4648_ (nao eh regra, mas eh o padrao) define o seguinte conjunto de caracteres:

```
Value Encoding  Value Encoding  Value Encoding  Value Encoding
    0 A             9 J            18 S            27 3
    1 B            10 K            19 T            28 4
    2 C            11 L            20 U            29 5
    3 D            12 M            21 V            30 6
    4 E            13 N            22 W            31 7
    5 F            14 O            23 X
    6 G            15 P            24 Y         (pad) =
    7 H            16 Q            25 Z
    8 I            17 R            26 2
```

## Encoding Flow

- Para encodar dados em base32, dividimos o conteudo em **chunks de 5 bytes (40 bits) cada**;
- Primeiramente, iremos converter a cadeira de caracteres em uma cadeia de bytes, posteriormente dividiremos o array em grupos de 5 bits ate que haja 8 grupos totalizando 40 bits, ou seja, um chunk completo;
    - Pode ser que, ao separar os grupos, haja um ultimo com bits remanescentes, dai precisamos preencher com zeros.
- Dai processamos cada conjunto e codificamos para a respectiva letra extraida pela sequencia de bits;
- Por fim, calculamos o **padding**, que sera responsavel por completar o ultimo chunk com os bits faltantes para 40;
    - Para isso, pegamos o total de bits, calculamos quantos bits existem no ultimo chunk e fazemos a diferenca para descobrir a quantidade de caracteres de padding.

```python
import math

CHARSET = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 2 3 4 5 6 7".split(" ")
MASK = 0x1f
CHUNK_SIZE = 5
CHARS_BY_CHUNK = 8

def encode_b32(content: str) -> str:
    encoded_str = ''

    if content == "":
        return encoded_str

    # Convert CONTENT to bits (with width 8) and join all bits together.
    bytes = [bin(ord(letter)) for letter in content]
    bits = int(''.join([byte[2:].zfill(8) for byte in bytes]), 2)

    # Fill in missing bits to make it a multiple of CHUNK_SIZE if chunk size is not a multiple of CHUNK_SIZE.
    if (len(content) * 8) % CHUNK_SIZE != 0:
        missing_bits = CHUNK_SIZE - (len(content) * 8) % CHUNK_SIZE # Represents remaining BITS.
        bits = bits << missing_bits

    # Extract each CHUNK_SIZE bits from BITS and convert to corresponding character.
    total_chunks = math.ceil((len(content) * 8) / CHUNK_SIZE)
    for i in range(total_chunks - 1, -1, -1): # 9 to 0, MSB to LSB.
        index = (bits >> (CHUNK_SIZE * i)) & MASK
        encoded_str += CHARSET[index]

    # Calculate padding and insert into encoded string if chunks are NOT COMPLETE.
    if total_chunks % CHARS_BY_CHUNK != 0:
        pads = CHARS_BY_CHUNK - (total_chunks % CHARS_BY_CHUNK) # Represents remaining CHARACTERS.
        encoded_str += '=' * pads

    return encoded_str
```

## Decoding Flow

- Com o texto encriptado primeiramente **retiramos os caracteres de padding** e **dividimos a string em sub-arrays com 8 caracteres cada** (que vale 5 bytes / 40 bits e representa um chunk);
- Nos sub-arrays de chunk completo, ou seja, 8 caracteres, transformamos eles de caracteres literais para inteiro e de inteiro para binario, e da esquerda para a direita reagrupamos em grupos de 8 bits (tamanho de um caractere ASCII);
- Depois de reagrupar, transformamos os caracteres nos seus valores correspondentes a tabela ASCII, e esse eh o fim da primeira parte;
- Para a segunda parte teremos que lidar com o **chunk que estava incompleto na hora do encoding**;
    - Nessa segunda parte, precisaremos calcular o **numero de bytes que o chunk atual incompleto representa na string original** e **numero de bits que foram adicionados como padding durante o encoding**.

```python
def decode_b32(content: str) -> str:
    decoded_str = ''

    # Remove padding characters.
    content = content.rstrip('=')

    # Convert each character to its corresponding value in CHARSET.
    chars = list(map(lambda char: CHARSET.index(char), content))

    bits = bit_count = 0
    for char in chars:
        bits = (bits << CHUNK_SIZE) | char
        bit_count += CHUNK_SIZE

        # Useful to extract bytes when we have 8 or more bits,
        # avoiding cases where encoding add extra bits.
        while bit_count >= BITS_PER_CHAR:
            bit_count -= BITS_PER_CHAR
            byte = (bits >> bit_count) & ASCII_MASK
            decoded_str += chr(byte)

    return decoded_str
```

# More Generic Approach

- Conseguimos esse feito de encodar e decodar dados em Base32, mas como isso ficaria em outras bases? Haveria uma mudanca drastica no codigo?
- E a resposta eh nao, nao haveria mudancas drasticas quanto ao processamento de dados, apenas em como tratamos certos valores, como o conjunto de caracteres, valores de chunks e etc, isso porque esse tipo de encode / decode eh **stream based**;
- No nosso codigo atual, basta alterar as constantes:

```python
MASK = 0x3f                 # 6 bits (2^6)
CHUNK_SIZE = 6              # bits per symbol
CHARS_BY_CHUNK = 4          # 4 chars per chunk in base64
CHARSET = list(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/"
)
BITS_PER_CHAR = 8
ASCII_MASK = 0xff           # 8 bits, 1 byte, ASCII char size

# code...

print(encode_b32("foobar"))
print(decode_b32("Zm9vYmFy"))
```

- E para mais, a diferenca conceitual eh:

| Propriedade        | Base32 | Base64          |
| ------------------ | ------ | --------------- |
| Bits por simbolo   | **5**  | **6**           |
| Mascara            | `0x1F` | `0x3F`          |
| Simbolos por bloco | **8**  | **4**           |
| Bits por bloco     | 40     | 24              |
| Bytes por bloco    | 5      | 3               |
| Padding            | `=`    | `=`             |
| Alfabeto           | A–Z2–7 | A–Z a–z 0–9 + / |

# Credits

- Special thanks to you, Piotr, for your amazing paper, it helped me a lot;
- Check him article [here](https://ptrchm.com/posts/base32-explained/#base32-implementation-rfc-4648)!
