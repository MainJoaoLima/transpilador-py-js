# Transpilador de Python para JavaScript

## Introducao

O nosso projeto protótipo implementa um transpilador que converte códigos de Python para JavaScript. Com finalidade de possibilitar o reaproveitamento de um código em Python em aplicações voltadas para outras plataformas que necessitem de JavaScript, ajudando na portabilidade e integração.

---

### Linguagens

- **Linguagem de Origem:** Python
- **Linguagem de Destino:** JavaScript

---

## Justificativa

A conversão de Python para JavaScript faz se importante pois possibilita a portabilidade, porque muitas aplicações web dependem exclusivamente de JavaScript no frontend. Sendo assim, pessoas que têm mais afinidade com Python podem reaproveitar os códigos e facilitar a transição entre backend e frontend.

---

## Tokens Suportados

### Literais de Dados

- **Números inteiros** 
- **Strings**

### Palavras Reservadas

- **Declaração:** `let`, `var`, `const` 
- **Controle de fluxo:** `if`, `else`, `for`)
- **Funções:** `def`, `return`
- **Lógica:** `and`, `or`

### Operadores

- **Aritméticos:** `+`, `-`, `*`, `/`
- **Lógicos:** `and`, `or`

---

## Gramática Utilizada

### Produções

#### Programa

```
programa ::= declaracao* | funcao*
```

#### Declarações

```
declaracao ::= atribuicao
atribuicao ::= IDENTIFICADOR '=' expressao
```

#### Funções

```
funcao ::= 'def' IDENTIFICADOR '(' parametros? ')' ':' bloco
parametros ::= IDENTIFICADOR (',' IDENTIFICADOR)*
bloco ::= comando+
```

#### Comandos

```
comando ::= atribuicao | condicional | repeticao | chamada_funcao
```

#### Condicional

```
condicional ::= 'if' expressao ':' bloco ('else' ':' bloco)?
```

#### Repetição

```
repeticao ::= 'for' IDENTIFICADOR 'in' expressao ':' bloco

```

#### Expressões

```
expressao ::= expressao_logica | expressao_aritmetica
expressao_logica ::= expressao 'and' expressao
                   | expressao 'or' expressao

expressao_aritmetica ::= termo (( '+' | '-' ) termo)*
termo ::= fator (( '*' | '/' ) fator)*
fator ::= IDENTIFICADOR | LITERAL | '(' expressao ')'
```

#### Chamada de Função

```
chamada_funcao ::= IDENTIFICADOR '(' argumentos? ')'
argumentos ::= expressao (',' expressao)*
```

---

## Comandos Suportados

1. **Declaração/Atribuição de Valores a Variáveis:**

   - Python: `x = 5`
   - JavaScript: `let x = 5;`

2. **Expressões Aritméticas:**

   - Python: `x = a + b * c`
   - JavaScript: `let x = a + b * c;`

3. **Condicional (if/else) e Expressões Lógicas (E/OU):**

   - Python:
    ```python
    x = 4
    y = 1
    if (x == 5 or y == 1):
      y = 3
    else:
      y = 4

    ```
   - JavaScript:
    ```javascript
    let x = 4;
    let y = 1;
    if (x == 5 || y == 1) {
      y = 3;
    }
    else {
      y = 4;
    }

    ```

4. **Repetição (for):**

   - Python:
    ```python
    x = 2
    g = [1, 2, 3, 4]
    y = 2

   for n in g:
     y += 1

    ```
   - JavaScript:
    ```javascript
    let x = 2;
    let g = [1, 2, 3, 4];
    let y = 2;


    for (let n of g) {
      y += 1;
    }

    ```

5. **Funções:**

   - Python:
     ```python
     def soma(a, b):
         return a + b
     ```
   - JavaScript:
     ```javascript
     function soma(a, b) {
         return a + b;
     }
     ```

---

## Instruções de Execução

1. Adicione o codigo em Python desejado em `entrada.py`
   
2. Execute o transpilador:

   ```bash
   python3 main.py entrada.py saida.js
   ```

3. Verifique o arquivo `saida.js` para o código traduzido.

---

