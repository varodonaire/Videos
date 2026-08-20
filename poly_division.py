from manim import *

# ── División de polinomios ───────────────────────────────────────────────────
#   El mismo algoritmo que la división larga de enteros:
#     ¿cuántas veces cabe el primer término? → multiplico → resto
#   Ejemplo 1 (resto 0):   (2x³ + 3x² − 11x − 6) : (x − 2)      = 2x² + 7x + 3
#   Ejemplo 2 (resto ≠ 0): (2x⁴ − 3x³ + 2x² + 5x − 7) : (x² − x + 2)
#                          = 2x² − x − 3, resto 4x − 1

FONT_ROW = 30

C_PROD = BLUE_C          # el producto, antes de cambiarle el signo
C_FLIP = ORANGE          # el producto con los signos ya cambiados
C_QUOT = YELLOW          # el cociente
C_LEAD = YELLOW          # los términos de mayor grado que se comparan
C_REST = GREEN

ANN_POS = np.array([5.3, 1.5, 0])      # anotación "cabe … veces" (bajo el cociente)
CARD_POS = np.array([-4.9, -2.85, 0])  # tarjeta con los tres pasos


# ── Filas de cada ejemplo ────────────────────────────────────────────────────
# Cada fila es una lista alineada por columnas de grado (None = hueco).

# División numérica de referencia: 852 : 4 = 213
N_DIVIDEND = ["8", "5", "2"]
N_STEPS = [
    (["8", None, None], ["0", "5", None], "2"),
    ([None, "4", None], [None, "1", "2"], "1"),
    ([None, "1", "2"], [None, None, "0"], "3"),
]

# Ejemplo 1: (2x³ + 3x² − 11x − 6) : (x − 2)
D1 = ["2x^3", "+3x^2", "-11x", "-6"]
S1 = [
    (
        ["2x^3", "-4x^2", None, None],
        ["-2x^3", "+4x^2", None, None],
        [None, "7x^2", "-11x", "-6"],
        "2x^2",
        r"\frac{2x^3}{x} = 2x^2",
    ),
    (
        [None, "7x^2", "-14x", None],
        [None, "-7x^2", "+14x", None],
        [None, None, "3x", "-6"],
        "+7x",
        r"\frac{7x^2}{x} = 7x",
    ),
    (
        [None, None, "3x", "-6"],
        [None, None, "-3x", "+6"],
        [None, None, None, "0"],
        "+3",
        r"\frac{3x}{x} = 3",
    ),
]

# Ejemplo 2: (2x⁴ − 3x³ + 2x² + 5x − 7) : (x² − x + 2)
D2 = ["2x^4", "-3x^3", "+2x^2", "+5x", "-7"]
S2 = [
    (
        ["2x^4", "-2x^3", "+4x^2", None, None],
        ["-2x^4", "+2x^3", "-4x^2", None, None],
        [None, "-x^3", "-2x^2", "+5x", "-7"],
        "2x^2",
        r"\frac{2x^4}{x^2} = 2x^2",
    ),
    (
        [None, "-x^3", "+x^2", "-2x", None],
        [None, "+x^3", "-x^2", "+2x", None],
        [None, None, "-3x^2", "+7x", "-7"],
        "-x",
        r"\frac{-x^3}{x^2} = -x",
    ),
    (
        [None, None, "-3x^2", "+3x", "-6"],
        [None, None, "+3x^2", "-3x", "+6"],
        [None, None, None, "4x", "-1"],
        "-3",
        r"\frac{-3x^2}{x^2} = -3",
    ),
]


class DivisionLayout:
    """La caja de la división larga, con columnas alineadas por grado.

    Cada fila es una lista de strings (None = hueco) del mismo largo: una
    columna por potencia de x, de mayor a menor. Las columnas se miden con
    todas las filas que van a aparecer, así que nada baila al avanzar el
    algoritmo y los signos quedan alineados en vertical.
    """

    def __init__(
        self,
        all_rows,
        divisor,
        origin,
        font_size=FONT_ROW,
        col_gap=0.3,
        row_gap=0.78,
        uniform=False,
    ):
        self.font_size = font_size
        self.row_gap = row_gap
        self.origin = np.array(origin, dtype=float)

        ncols = max(len(r) for r in all_rows)
        widths = []
        for j in range(ncols):
            w = 0.12
            for row in all_rows:
                if j < len(row) and row[j]:
                    w = max(w, MathTex(row[j], font_size=font_size).width)
            widths.append(w)
        if uniform:
            widths = [max(widths)] * ncols
        self.widths = widths

        xs, x = [], 0.0
        for j in range(ncols):
            xs.append(x)
            x += widths[j] + col_gap
        self.xs = xs                       # borde izquierdo de cada columna
        self.total_w = x - col_gap

        # línea de encabezado:   dividendo  :  divisor  =  cociente
        self.colon = MathTex(":", font_size=font_size)
        self.divisor = MathTex(divisor, font_size=font_size)
        self.equals = MathTex("=", font_size=font_size)
        y0 = self.y_of(0)
        x_end = self.origin[0] + self.total_w
        for mob, gap in ((self.colon, 0.36), (self.divisor, 0.28), (self.equals, 0.28)):
            mob.set_y(y0)
            mob.align_to(np.array([x_end + gap, 0, 0]), LEFT)
            x_end = mob.get_right()[0]
        self.quot_x = x_end + 0.3

    # ── coordenadas ──────────────────────────────────────────────────────────
    def _px(self, dx):
        return self.origin + RIGHT * dx

    def y_of(self, i):
        return self.origin[1] - i * self.row_gap

    def col_x(self, j):
        return self.origin[0] + self.xs[j]

    # ── piezas ───────────────────────────────────────────────────────────────
    def row(self, terms, i, color=WHITE, prefix=None):
        group = VGroup()
        cells = {}
        for j, t in enumerate(terms):
            if not t:
                continue
            cell = MathTex(t, font_size=self.font_size, color=color)
            cell.set_y(self.y_of(i))
            cell.align_to(np.array([self.col_x(j), 0, 0]), LEFT)
            cells[j] = cell
            group.add(cell)
        if prefix:
            first = min(cells)
            sign = MathTex(prefix, font_size=self.font_size, color=color)
            sign.next_to(cells[first], LEFT, buff=0.16)
            group.add(sign)
            group.sign = sign
        group.cells = cells
        return group

    def underline(self, i, terms, color=WHITE, pad=0.15):
        cols = [j for j, t in enumerate(terms) if t]
        y = self.y_of(i) - self.row_gap / 2 + 0.05
        x1 = self.col_x(cols[0]) - pad
        x2 = self.col_x(cols[-1]) + self.widths[cols[-1]] + 0.05
        return Line([x1, y, 0], [x2, y, 0], stroke_width=2.5, color=color)

    def header(self):
        """Los tres signos de la línea de arriba:  :  divisor  ="""
        return VGroup(self.colon, self.divisor, self.equals)

    def quotient(self, terms):
        group = VGroup(
            *[MathTex(t, font_size=self.font_size, color=C_QUOT) for t in terms]
        ).arrange(RIGHT, buff=0.14)
        group.set_y(self.y_of(0))
        group.align_to(np.array([self.quot_x, 0, 0]), LEFT)
        return group


def action_labels():
    return [
        Text("1.  ¿Cuántas veces cabe?", font_size=26, color=C_LEAD),
        Text("2.  Multiplico", font_size=26, color=C_PROD),
        Text("3.  Resto", font_size=26, color=C_FLIP),
    ]


class PolyDivisionScene(Scene):
    """
    Diez beats sobre el algoritmo de la división de polinomios: la misma
    división larga de los enteros, con una única regla nueva —se para cuando
    el resto tiene grado menor que el divisor.
    """

    def construct(self):
        self._beat1_title()
        card = self._beat2_numeric_division()
        lay1, quot1 = self._beat3_setup_first()
        self._beat4_5_first_example(lay1, quot1)
        self._beat6_exact(lay1, quot1)
        lay2, quot2 = self._beat7_setup_second()
        rest = self._beat8_second_example(lay2, quot2)
        self._beat9_when_to_stop(lay2, rest, card)
        self._beat10_identity()

    # ── Beat 1: Título ───────────────────────────────────────────────────────
    def _beat1_title(self):
        title = Text("División de polinomios", font_size=52, weight=BOLD)
        subtitle = Text("El mismo algoritmo de siempre", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.45)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle)))

    # ── Beat 2: La división de números, en la caja ───────────────────────────
    def _beat2_numeric_division(self):
        rows = [N_DIVIDEND] + [r for step in N_STEPS for r in step[:2]]
        lay = DivisionLayout(
            rows, "4", origin=[-4.4, 2.5, 0], font_size=36, col_gap=0.06,
            uniform=True,
        )

        dividend = lay.row(N_DIVIDEND, 0)
        header = lay.header()
        self.play(FadeIn(dividend), run_time=0.8)
        self.play(Write(header), run_time=1.0)
        self.wait(0.8)

        labels = action_labels()
        for lab in labels:
            lab.set_opacity(0)
        VGroup(*labels).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.4, -0.4, 0])

        quot = lay.quotient(["2", "1", "3"])
        drawn = VGroup(dividend, header)

        for n, (prod, res, digit) in enumerate(N_STEPS):
            i = 2 * n + 1
            p_row = lay.row(prod, i, color=C_PROD, prefix="-")
            r_row = lay.row(res, i + 1)
            line = lay.underline(i, prod, pad=0.45)

            if n == 0:
                self.play(labels[0].animate.set_opacity(1), run_time=0.6)
            self.play(
                Indicate(quot[n].copy().set_opacity(0), scale_factor=1),
                FadeIn(quot[n], shift=DOWN * 0.2),
                run_time=0.7,
            )
            if n == 0:
                self.wait(0.4)
                self.play(labels[1].animate.set_opacity(1), run_time=0.6)
            self.play(FadeIn(p_row), run_time=0.6)
            if n == 0:
                self.play(labels[2].animate.set_opacity(1), run_time=0.6)
            self.play(Create(line), run_time=0.4)
            self.play(FadeIn(r_row, shift=DOWN * 0.15), run_time=0.6)
            drawn.add(p_row, r_row, line)
            last = r_row
            self.wait(0.5 if n else 1.2)

        self.play(
            Circumscribe(last, color=C_REST, buff=0.15),
            last.animate.set_color(C_REST),
            run_time=1.6,
        )
        self.wait(1.5)

        # las tres etiquetas se agrupan en la tarjeta que acompaña el resto del vídeo
        card_lines = VGroup(*[lab.copy() for lab in labels])
        card_lines.arrange(DOWN, buff=0.28, aligned_edge=LEFT).scale(0.85)
        box = SurroundingRectangle(card_lines, color=GRAY, buff=0.3)
        card = VGroup(box, card_lines).move_to(CARD_POS)

        self.play(
            ReplacementTransform(VGroup(*labels), card_lines),
            Create(box),
            FadeOut(drawn, quot),
            run_time=1.6,
        )
        self.wait(1.5)
        return card

    # ── Beat 3: el mismo esquema, con letras ─────────────────────────────────
    def _beat3_setup_first(self):
        rows = [D1] + [r for step in S1 for r in step[:3]]
        lay = DivisionLayout(rows, "x - 2", origin=[-5.3, 2.7, 0])

        p = MathTex("2x^3", "+3x^2", "-11x", "-6", font_size=40)
        d = MathTex("x", "-2", font_size=40)
        VGroup(p, d).arrange(DOWN, buff=0.5).move_to(UP * 0.5)
        self.play(Write(p), Write(d), run_time=1.6)
        self.wait(1)

        dividend = lay.row(D1, 0)
        self.play(
            ReplacementTransform(p, dividend),
            ReplacementTransform(d, lay.divisor),
            run_time=1.4,
        )
        self.play(Write(VGroup(lay.colon, lay.equals)), run_time=0.9)

        lead_p = dividend.cells[0]
        lead_d = lay.divisor[0][0]
        self.play(
            lead_p.animate.set_color(C_LEAD),
            lead_d.animate.set_color(C_LEAD),
            run_time=0.8,
        )
        note = Text("los primeros términos", font_size=24, color=C_LEAD)
        note.move_to([0.0, 0.9, 0])
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(note))

        lay.box = VGroup(dividend, lay.header())
        return lay, lay.quotient(["2x^2", "+7x", "+3"])

    # ── Beats 4–5: el ejemplo con resto 0 ────────────────────────────────────
    def _beat4_5_first_example(self, lay, quot):
        prev = lay.box[0]
        for n, (prod, flip, res, _, lead) in enumerate(S1):
            prev = self._step(lay, quot, n, prod, flip, res, lead, prev, slow=(n == 0))

    def _step(self, lay, quot, n, prod, flip, res, lead, prev, slow):
        i = 2 * n + 1

        # 1 · ¿cuántas veces cabe?
        ann = MathTex(lead, font_size=34, color=C_LEAD).move_to(ANN_POS)
        if n > 0:
            self.play(
                prev.cells[min(prev.cells)].animate.set_color(C_LEAD), run_time=0.5
            )
        self.play(FadeIn(ann, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0 if slow else 0.6)
        self.play(TransformFromCopy(ann, quot[n]), run_time=1.0)
        self.wait(0.6)

        # 2 · multiplico
        p_row = lay.row(prod, i, color=C_PROD)
        self.play(FadeIn(p_row, shift=DOWN * 0.15), run_time=0.8)
        self.wait(1.0 if slow else 0.6)

        # 3 · resto (cambiando el signo de todos los términos)
        f_row = lay.row(flip, i, color=C_FLIP)
        if slow:
            warn = VGroup(
                Text("restar = cambiar", font_size=24, color=C_FLIP),
                Text("TODOS los signos", font_size=24, color=C_FLIP),
            ).arrange(DOWN, buff=0.16)
            warn.move_to(ANN_POS + DOWN * 1.15)
            self.play(FadeIn(warn, shift=UP * 0.15))
            self.play(ReplacementTransform(p_row, f_row), run_time=1.2)
            self.wait(1.5)
            self.play(FadeOut(warn))
        else:
            self.play(ReplacementTransform(p_row, f_row), run_time=0.8)
            self.wait(0.5)

        line = lay.underline(i, flip)
        r_row = lay.row(res, i + 1)
        self.play(Create(line), run_time=0.4)
        self.play(FadeIn(r_row, shift=DOWN * 0.15), run_time=0.8)
        self.play(
            FadeOut(ann),
            prev.animate.set_color(WHITE),
            run_time=0.6,
        )
        lay.box.add(f_row, line, r_row)
        self.wait(1.6 if slow else 1.1)
        return r_row

    # ── Beat 6: qué significa resto 0 ────────────────────────────────────────
    def _beat6_exact(self, lay, quot):
        zero = lay.box[-1]
        box = SurroundingRectangle(zero, color=C_REST, buff=0.18)
        label = Text("resto 0", font_size=26, color=C_REST).next_to(box, RIGHT, buff=0.4)
        self.play(Create(box), FadeIn(label), zero.animate.set_color(C_REST))
        self.wait(2)

        ident = MathTex(
            "2x^3 + 3x^2 - 11x - 6", "=", "(x - 2)", "(2x^2 + 7x + 3)", font_size=38
        )
        ident[2].set_color(C_LEAD)
        ident[3].set_color(C_QUOT)
        ident.to_edge(DOWN, buff=0.8)
        self.play(Write(ident), run_time=2)
        self.wait(3)

        self.play(FadeOut(VGroup(lay.box, quot, box, label, ident)), run_time=1.2)

    # ── Beat 7: planteamiento del segundo ejemplo ────────────────────────────
    def _beat7_setup_second(self):
        rows = [D2] + [r for step in S2 for r in step[:3]]
        lay = DivisionLayout(
            rows, "x^2 - x + 2", origin=[-6.4, 2.7, 0], font_size=28, col_gap=0.26
        )

        dividend = lay.row(D2, 0)
        self.play(FadeIn(dividend), run_time=1)
        self.play(Write(lay.header()), run_time=1.2)

        deg = VGroup(
            MathTex(r"\text{grado } 4", font_size=28, color=GRAY),
            MathTex(r"\text{grado } 2", font_size=28, color=GRAY),
        )
        deg[0].next_to(dividend, DOWN, buff=0.3).align_to(dividend, LEFT)
        deg[1].next_to(lay.divisor, UP, buff=0.28)
        self.play(FadeIn(deg[0]), FadeIn(deg[1]))
        self.wait(1.5)

        self.play(
            dividend.cells[0].animate.set_color(C_LEAD),
            lay.divisor[0][0:2].animate.set_color(C_LEAD),
            run_time=0.8,
        )
        self.wait(1.5)
        self.play(FadeOut(deg))

        lay.box = VGroup(dividend, lay.header())
        return lay, lay.quotient(["2x^2", "-x", "-3"])

    # ── Beat 8: los tres pasos del segundo ejemplo ───────────────────────────
    def _beat8_second_example(self, lay, quot):
        prev = lay.box[0]
        for n, (prod, flip, res, _, lead) in enumerate(S2):
            prev = self._step(lay, quot, n, prod, flip, res, lead, prev, slow=False)
        return prev

    # ── Beat 9: cuándo hay que parar ─────────────────────────────────────────
    def _beat9_when_to_stop(self, lay, rest, card):
        box = SurroundingRectangle(rest, color=C_REST, buff=0.18)
        self.play(Create(box))
        self.wait(0.8)

        q = MathTex(r"\frac{4x}{x^2} \; = \; ?", font_size=36).move_to(ANN_POS)
        self.play(FadeIn(q, shift=UP * 0.2))
        cross = Cross(q, color=RED, stroke_width=5)
        self.play(Create(cross), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(q, cross))

        self.play(FadeOut(card), run_time=0.8)
        cmp_ = VGroup(
            MathTex(r"\text{grado}(4x - 1) = 1", font_size=30, color=C_REST),
            MathTex("<", font_size=30),
            MathTex(r"\text{grado}(x^2 - x + 2) = 2", font_size=30),
        ).arrange(DOWN, buff=0.28)
        cmp_.arrange(RIGHT, buff=0.35)
        cmp_.move_to([2.6, -2.6, 0])
        for part in cmp_:
            self.play(FadeIn(part, shift=UP * 0.15), run_time=0.7)
        check = MathTex(r"\checkmark", font_size=44, color=C_REST)
        check.next_to(cmp_, DOWN, buff=0.4)
        self.play(FadeIn(check, scale=1.5))
        self.wait(2)

        rule = Text(
            "se para cuando el resto tiene grado menor que el divisor",
            font_size=28, weight=BOLD,
        )
        rule.to_edge(DOWN, buff=0.55)
        frame = SurroundingRectangle(rule, color=C_LEAD, buff=0.22)
        self.play(FadeIn(rule, shift=UP * 0.2), Create(frame))
        self.wait(3.5)
        self.play(FadeOut(VGroup(cmp_, check, rule, frame, box)), run_time=1)

    # ── Beat 10: la identidad de la división ─────────────────────────────────
    def _beat10_identity(self):
        self.play(FadeOut(*self.mobjects), run_time=1.2)

        ident = MathTex(
            "2x^4 - 3x^3 + 2x^2 + 5x - 7",
            "=",
            "(x^2 - x + 2)",
            r"\cdot",
            "(2x^2 - x - 3)",
            "+",
            "(4x - 1)",
            font_size=38,
        )
        ident[2].set_color(C_LEAD)
        ident[4].set_color(C_QUOT)
        ident[6].set_color(C_REST)
        ident.move_to(UP * 1.2)
        self.play(Write(ident), run_time=2.5)
        self.wait(2)

        general = MathTex("P", "=", "d", r"\cdot", "c", "+", "r", font_size=54)
        general[2].set_color(C_LEAD)
        general[4].set_color(C_QUOT)
        general[6].set_color(C_REST)
        general.next_to(ident, DOWN, buff=1.1)
        self.play(
            *[
                TransformFromCopy(ident[k], general[k])
                for k in (0, 1, 2, 3, 4, 5, 6)
            ],
            run_time=2,
        )
        box = SurroundingRectangle(general, color=WHITE, buff=0.35)
        self.play(Create(box))
        self.wait(1.5)

        cond = MathTex(r"\text{grado}(r) < \text{grado}(d)", font_size=34)
        cond[0][7].set_color(C_REST)
        cond.next_to(box, DOWN, buff=0.55)
        self.play(FadeIn(cond, shift=UP * 0.2))
        self.wait(4)
        self.play(FadeOut(VGroup(ident, general, box, cond)), run_time=1.5)
        self.wait(0.5)
