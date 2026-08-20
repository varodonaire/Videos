# Guión — División de polinomios

Vídeo: `poly_division.py` → `PolyDivisionScene`

El algoritmo de la división de polinomios, presentado como la misma división de enteros que ya se
sabe hacer. Nada más: sin Ruffini, sin teorema del resto, sin factorización.

Idea pedagógica central: **es la división larga de siempre. El gesto es
“¿cuántas veces cabe? · multiplico · resto”, y lo único nuevo es cuándo parar.**

Notación: la chilena, en línea — `dividendo : divisor = cociente` en la primera fila, y debajo
los productos (con el signo ya cambiado) y los restos sucesivos.

---

## Los ejemplos

### Ejemplo 0 — la división numérica de referencia

```
852 : 4 = 213     resto 0
```

Se hace en pantalla, en voz alta, para nombrar el gesto antes de usarlo con letras.

### Ejemplo 1 — resto 0

```
P(x) = 2x³ + 3x² − 11x − 6        d(x) = x − 2
```

| Paso | ¿Cuántas veces cabe? | Al cociente | Multiplico | Resto y queda |
|---|---|---|---|---|
| 1 | `2x³ : x` | `2x²` | `2x³ − 4x²` | `7x² − 11x − 6` |
| 2 | `7x² : x` | `7x` | `7x² − 14x` | `3x − 6` |
| 3 | `3x : x` | `3` | `3x − 6` | `0` ← **división exacta** |

```
c(x) = 2x² + 7x + 3        r = 0
2x³ + 3x² − 11x − 6 = (x − 2)(2x² + 7x + 3)
```

### Ejemplo 2 — resto no nulo

```
P(x) = 2x⁴ − 3x³ + 2x² + 5x − 7        d(x) = x² − x + 2
```

| Paso | ¿Cuántas veces cabe? | Al cociente | Multiplico | Resto y queda |
|---|---|---|---|---|
| 1 | `2x⁴ : x²` | `2x²` | `2x⁴ − 2x³ + 4x²` | `−x³ − 2x² + 5x` |
| 2 | `−x³ : x²` | `−x` | `−x³ + x² − 2x` | `−3x² + 7x − 7` |
| 3 | `−3x² : x²` | `−3` | `−3x² + 3x − 6` | `4x − 1` ← **grado 1 < grado 2: parar** |

```
c(x) = 2x² − x − 3        r(x) = 4x − 1
2x⁴ − 3x³ + 2x² + 5x − 7 = (x² − x + 2)(2x² − x − 3) + (4x − 1)
```

---

## Guión por beats

Duración estimada: 5 min.

### Beat 1 — Título (~8 s)
Título "División de polinomios" y subtítulo gris "El mismo algoritmo de siempre".

> Dividir polinomios no es una técnica nueva. Es la división larga que ya sabes hacer, con letras.

### Beat 2 — La división de números (~45 s)
Se resuelve `852 : 4` en la notación de siempre, paso a paso y con las tres acciones etiquetadas al lado
según ocurren: **¿cuántas veces cabe? → multiplico → resto**. Al terminar, esas tres etiquetas se
agrupan en una tarjeta que se queda en una esquina el resto del vídeo.

> Ochocientos cincuenta y dos entre cuatro. ¿Cuántas veces cabe el cuatro en el ocho? Dos.
> Multiplico dos por cuatro, y lo resto. Bajo el siguiente. Y otra vez: cabe, multiplico, resto.
> Fíjate en el gesto, porque es el único que vamos a usar en todo el vídeo.

### Beat 3 — El mismo esquema, con letras (~30 s)
La división numérica se desvanece y en su sitio aparece la línea
`2x³ + 3x² − 11x − 6 : x − 2 =`, con el polinomio y el divisor colocados igual. Los dos primeros términos,
`2x³` y `x`, se resaltan en amarillo.

> Misma disposición, mismas posiciones. La única diferencia: en vez de mirar la primera cifra, miro el
> **primer término** de cada uno. Aquí, `2x³` arriba y `x` abajo.

### Beat 4 — Ejemplo 1, paso 1 (~50 s)
`2x³ : x = 2x²`, con la división de términos escrita aparte para que se vea. `2x²` sube al
cociente. Se escribe `2x²·(x − 2) = 2x³ − 4x²` debajo, en otro color, y se resta con los signos
cambiados explícitamente. `2x³` se cancela con una tachadura. Queda `7x² − 11x − 6`.

> ¿Cuántas veces cabe `x` en `2x³`? `2x²` veces. Ese es el primer trozo del cociente. Ahora
> multiplico `2x²` por todo el divisor y lo resto. Cuidado aquí: restar significa cambiar el signo
> de **todos** los términos. El `2x³` se va — que era justo lo que buscábamos.

### Beat 5 — Ejemplo 1, pasos 2 y 3 (~50 s)
Los dos pasos restantes, con el mismo montaje pero más rápido: `7x² : x = 7x`, resta;
`3x : x = 3`, resta. El `0` final se enmarca en verde.

> Otra vez lo mismo. Cabe `7x` veces: multiplico, resto. Y `3`: multiplico, resto… y no queda nada.
> Resto cero.

### Beat 6 — Qué significa resto 0 (~30 s)
Aparece `2x³ + 3x² − 11x − 6 = (x − 2)(2x² + 7x + 3)`, con colores que enlazan cada pieza con su
sitio en la división.

> Igual que `852` entre `4` daba exacto, aquí la división es exacta: el dividendo es el divisor por
> el cociente. Ni más ni menos.

### Beat 7 — Ejemplo 2, planteamiento (~25 s)
Línea nueva con `P(x) = 2x⁴ − 3x³ + 2x² + 5x − 7` y `d(x) = x² − x + 2`. Se resaltan `2x⁴` y `x²`.

> Segundo ejemplo, un poco más grande: grado 4 entre grado 2. Cambia el tamaño, no el
> procedimiento. Sigo mirando solo los primeros términos: `2x⁴` y `x²`.

### Beat 8 — Ejemplo 2, los tres pasos (~70 s)
Los tres pasos encadenados con el mismo montaje del ejemplo 1, a ritmo constante:
`2x⁴ : x² = 2x²` · `−x³ : x² = −x` · `−3x² : x² = −3`. Queda `4x − 1`.

> Cabe `2x²` veces: multiplico el divisor entero, resto. Cabe `−x` veces: multiplico, resto —
> atento al signo. Cabe `−3` veces: multiplico, resto. Y me queda `4x − 1`.

### Beat 9 — Cuándo hay que parar (~45 s)
`4x − 1` se enmarca. Debajo, la pregunta «¿cuántas veces cabe `x²` en `4x`?» con una cruz roja.
Aparece la condición de parada, destacada: **se para cuando el resto tiene grado menor que el
divisor**, con `grado(4x − 1) = 1 < 2 = grado(x² − x + 2)` y un ✓ verde.

> ¿Puedo seguir? ¿Cuántas veces cabe `x²` en `4x`? Ninguna: `4x` es más pequeño, tiene grado menor.
> Y esa es la regla de parada, la única cosa nueva del vídeo: se para cuando lo que queda tiene
> **grado menor que el divisor**. Igual que con números parabas cuando lo que sobraba era menor que
> el divisor.

### Beat 10 — Cierre: la identidad (~35 s)
Se monta en pantalla, con los colores de la división:
`2x⁴ − 3x³ + 2x² + 5x − 7 = (x² − x + 2)(2x² − x − 3) + (4x − 1)`.
Debajo, en genérico y enmarcado: `P = d · c + r`, con `grado(r) < grado(d)`.

> Y así queda escrito: dividendo igual a divisor por cociente, más el resto. Es la misma frase que
> con los números, y sirve además para comprobar cualquier división sin volver a hacerla.
