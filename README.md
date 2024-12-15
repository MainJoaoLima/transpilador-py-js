# Transpilador de Python para JavaScript

## Introducao

O nosso projeto prototipo implementa um transpilador que converte códigos de Python para JavaScript. Como finalidade de possibilitar o reaproveitamento de um código em Python em aplicações voltadas para outras plataformas que necessitem de JavaScript, ajudando na portabilidade e integração.

---

### Linguagens

- **Linguagem de Origem:** Python
- **Linguagem de Destino:** JavaScript

---

## Justificativa

A conversão de Python para JavaScript faz se importante pois possibilita a portabilidade, em muitas aplicações web dependem exclusivamente de JavaScript no frontend. Sendo assim, pessoas que tem mais afinidade com Python poder reaproveitar os códigos e facilitar a transição entre backend e frontend.

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

- **Aritméticos:** `+`, `-`, `*`, `/`, `%`
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
comando ::= atribuicao
         | condicional
         | repeticao
         | chamada_funcao
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
    if x == 5 or y == 1:
        y = 3
    else:
        y = 4
    ```
   - JavaScript:
    ```javascript
    let x = 4;
    let y = 1;
    if (x) {
        let y = 3;
    } else {
        let y = 4;
    }
    ```

4. **Repetição (for):**

   - Python:
    ```python
    a = 2
    i = 1
    for i in range(5):
        i = i + 1
    ```
   - JavaScript:
    ```javascript
    for (let i = 0; i < 5; i += 1) {
        i = (i + 1);
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


1. Execute o transpilador:

   ```bash
   python3 main.py entrada.py saida.js
   ```

2. Verifique o arquivo `saida.js` para o código traduzido.

---

