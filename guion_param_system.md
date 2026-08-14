# Guión — Sistemas de ecuaciones lineales con parámetros

Vídeo: `param_system.py` → `ParametricSystemScene`

Discusión y resolución de un sistema lineal 3×3 que depende de un parámetro `k`, usando la matriz
ampliada y operaciones elementales (Gauss). Sin determinantes, sin Rouché-Frobenius explícito y sin
interpretación geométrica en 3D.

Idea pedagógica central: **un sistema con parámetro se rompe exactamente donde se anula un pivote.**
Los tres casos son consecuencia de eso.

---

## El ejemplo

Sistema clásico, elegido porque produce los tres casos con aritmética limpia:

```
k·x +  y  +  z  = 1
 x  + k·y +  z  = k
 x  +  y  + k·z = k²
```

Matriz ampliada:

```
[ k  1  1 | 1  ]
[ 1  k  1 | k  ]
[ 1  1  k | k² ]
```

### Escalonamiento

**F1 ↔ F3** (para tener un pivote `1` que no dependa de `k`):

```
[ 1  1  k | k² ]
[ 1  k  1 | k  ]
[ k  1  1 | 1  ]
```

**F2 → F2 − F1** y **F3 → F3 − k·F1**:

```
[ 1    1        k        | k²             ]
[ 0   k−1     −(k−1)     | −k(k−1)        ]
[ 0  −(k−1)  −(k−1)(k+1) | −(k−1)(k²+k+1) ]
```

(en F3 se usa `1−k² = (1−k)(1+k)` y `1−k³ = (1−k)(1+k+k²)`)

**F3 → F3 + F2** — nunca se divide por `k−1`, el factor sale solo:

```
[ 1   1       k        | k²             ]
[ 0  k−1   −(k−1)      | −k(k−1)        ]
[ 0   0   −(k−1)(k+2)  | −(k−1)(k+1)²   ]
```

**Pivotes:** `1`, `(k−1)`, `−(k−1)(k+2)` → **valores críticos: k = 1 y k = −2.**

### Los tres casos

| Caso | Última fila | Resultado |
|---|---|---|
| `k ≠ 1` y `k ≠ −2` | pivote ≠ 0 | **Solución única** |
| `k = 1` | F2 y F3 se anulan enteras | **Infinitas soluciones** (2 parámetros) |
| `k = −2` | `[0 0 0 \| 3]` | **Sin solución** |

**Solución única** (sustitución hacia atrás, dividiendo por `k−1` ya legítimamente):

```
z = (k+1)²/(k+2)     y = 1/(k+2)     x = −(k+1)/(k+2)
```

Comprobación en pantalla con `k = 0`: `x = −1/2, y = 1/2, z = 1/2` satisface `y+z=1`, `x+z=0`,
`x+y=0`.

**k = 1:** el sistema colapsa a `x + y + z = 1` → `x = 1 − s − t`, `y = s`, `z = t`.

**k = −2:** la escalonada queda

```
[ 1   1  −2 |  4 ]
[ 0  −3   3 | −6 ]
[ 0   0   0 |  3 ]
```

y la última fila dice `0 = 3`, absurdo.

---

## Guión por beats

Duración estimada: 6–7 min (el render final quedó en 3:24; los tiempos de `wait` marcan el ritmo).

### Beat 1 — Título (~10 s)
Título "Sistemas con parámetros" y subtítulo gris "Matrices y operaciones elementales".

> Cuando un sistema depende de un parámetro, no tiene *una* respuesta: tiene tres.

### Beat 2 — El sistema y la pregunta (~30 s)
Aparecen las tres ecuaciones centradas. Las `k` se colorean en amarillo. Debajo, la pregunta motriz
«¿Cuántas soluciones tiene?» se transforma en «Depende de k.»

> Aquí `k` no es una incógnita: es un número que todavía no sabemos cuál es. Y según lo que valga, el
> sistema puede tener una solución, infinitas, o ninguna.

### Beat 3 — Del sistema a la matriz ampliada (~25 s)
El sistema se desplaza a la izquierda y encoge; a la derecha se construye `(A | b)` entrada a
entrada, con barra vertical separando `b`.

> Las letras `x`, `y`, `z` no aportan información: solo los coeficientes. Los guardamos en la matriz
> ampliada.

### Beat 4 — Las tres operaciones elementales (~35 s)
Tarjeta con las tres operaciones: `F_i ↔ F_j`; `F_i → λ·F_i` con `λ ≠ 0` en rojo; `F_i → F_i + λ·F_j`.
Debajo, el aviso destacado: **«Nunca dividas por una expresión con `k`.»**

> Estas operaciones no cambian las soluciones. Pero con un parámetro hay una trampa: si divido por
> `k−1` estoy suponiendo, sin decirlo, que `k` no vale 1. Y ese caso es justamente el interesante.
> Regla de oro: no dividir por nada que contenga `k`.

### Beat 5 — Paso 1: colocar un pivote seguro (~25 s)
`F1 ↔ F3` con las filas intercambiándose físicamente. El pivote `1` se rodea con un círculo verde.

> El pivote natural sería `k`… pero `k` puede ser cero. Intercambiamos filas para tener arriba un `1`
> limpio, que no depende del parámetro.

### Beat 6 — Paso 2: hacer ceros bajo el pivote (~50 s)
`F2 → F2 − F1`, pausa, luego `F3 → F3 − k·F1`. Se resalta el factor `k−1` que aparece por todas
partes.

> Restamos F1 de F2, y `k` veces F1 de F3. Fíjate en lo que aparece: casi todo lo de abajo lleva un
> factor `k−1`.

### Beat 7 — Paso 3: la última fila (~50 s)
`F3 → F3 + F2`. La matriz escalonada final queda enmarcada.

> Sumamos F2 a F3 —sin dividir por nada— y la matriz queda escalonada.

### Beat 8 — El corazón del vídeo: los pivotes (~45 s)
Los tres pivotes se extraen de la diagonal y suben a una línea. Aparece la frase clave: **«Todo se
decide donde un pivote se anula.»** Cierra con una recta real donde `−2` y `1` marcan tres zonas.

> Mientras los tres pivotes sean distintos de cero, el sistema se resuelve sin más. Los únicos
> valores problemáticos son los que anulan alguno: `k = 1` y `k = −2`. Estos dos números parten la
> recta real en tres zonas, y hay que estudiarlas una a una.

### Beat 9 — Caso A: k ≠ 1 y k ≠ −2 (~55 s)
Sustitución hacia atrás en tres líneas: `z`, luego `y`, luego `x`. Comprobación con `k = 0`
sustituida en el sistema original, con tres ✓ verdes.

> Ahora sí puedo dividir por `k−1` y por `k+2`, porque ya he declarado que no son cero. Sistema
> compatible determinado: una única solución, que depende de `k`.

### Beat 10 — Caso B: k = 1 (~50 s)
La escalonada se transforma sustituyendo `k = 1`: F2 y F3 se desvanecen. Queda `x + y + z = 1` y la
solución paramétrica con dos grados de libertad.

> Con `k = 1` las tres ecuaciones originales eran la misma ecuación disfrazada. Queda un solo plano
> de información y dos grados de libertad: infinitas soluciones.

### Beat 11 — Caso C: k = −2 (~50 s)
La última fila queda `[0 0 0 | 3]`, que se traduce a `0 = 3` en rojo.

> Con `k = −2` el coeficiente se anula pero el término independiente no. La última fila dice
> literalmente cero igual a tres. Eso es imposible: el sistema no tiene solución.

### Beat 12 — Resumen y método (~40 s)
Tabla con los tres casos (verde / azul / rojo) y el método en tres pasos:

1. Escalonar **sin dividir por expresiones con `k`**
2. Buscar los valores que **anulan un pivote**
3. Estudiar cada caso por separado

> Tres pasos. Escalona con cuidado, localiza dónde muere un pivote, y estudia esos valores uno por
> uno. Lo demás es aritmética.
