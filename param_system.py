from manim import *

# ── El sistema ───────────────────────────────────────────────────────────────
#   k x +   y +   z = 1
#     x + k y +   z = k
#     x +   y + k z = k²
#
# Escalonando (F1↔F3, F2−F1, F3−kF1, F3+F2) los pivotes son
#   1,  (k−1),  −(k−1)(k+2)
# de modo que los valores críticos son k = 1 y k = −2.
K_CRIT_A = 1
K_CRIT_B = -2

MATRIX_POS = DOWN * 0.55        # centro de la matriz en pantalla
MATRIX_MAX_WIDTH = 11.0         # se reescala si una etapa se hace muy ancha
STEP_POS = UP * 3.15 + RIGHT * 1.7   # banner "Paso N" (a la derecha de la tarjeta)
OP_POS = DOWN * 3.05            # anotación de la operación elemental


# ── Etapas de la matriz ampliada ─────────────────────────────────────────────
M0 = [                                   # sistema original
    ["k", "1", "1", "1"],
    ["1", "k", "1", "k"],
    ["1", "1", "k", "k^2"],
]

M1 = [                                   # tras F1 ↔ F3
    ["1", "1", "k", "k^2"],
    ["1", "k", "1", "k"],
    ["k", "1", "1", "1"],
]

M2 = [                                   # tras F2−F1 y F3−kF1
    ["1", "1", "k", "k^2"],
    ["0", "k-1", "-(k-1)", "-k(k-1)"],
    ["0", "-(k-1)", "-(k-1)(k+1)", "-(k-1)(k^2+k+1)"],
]

M3 = [                                   # escalonada: tras F3+F2
    ["1", "1", "k", "k^2"],
    ["0", "k-1", "-(k-1)", "-k(k-1)"],
    ["0", "0", "-(k-1)(k+2)", "-(k-1)(k+1)^2"],
]

M_K1 = [                                 # escalonada con k = 1
    ["1", "1", "1", "1"],
    ["0", "0", "0", "0"],
    ["0", "0", "0", "0"],
]

M_K2 = [                                 # escalonada con k = −2
    ["1", "1", "-2", "4"],
    ["0", "-3", "3", "-6"],
    ["0", "0", "0", "3"],
]


def augmented_matrix(rows, font_size=40, col_gap=0.55, row_gap=1.0, bar_gap=0.5):
    """Matriz ampliada con anchos de columna adaptados al contenido.

    `Matrix` usa un `h_buff` constante, así que las etapas con expresiones
    largas (−(k−1)(k²+k+1)) se solapan. Aquí cada columna se mide y se coloca
    según su entrada más ancha, y la barra de la ampliada cae siempre en el
    hueco anterior a la última columna.
    """
    nrows, ncols = len(rows), len(rows[0])
    cells = [[MathTex(s, font_size=font_size) for s in row] for row in rows]
    col_w = [max(cells[i][j].width for i in range(nrows)) for j in range(ncols)]

    xs, x = [], 0.0
    for j in range(ncols):
        if j == ncols - 1:
            x += bar_gap          # hueco extra para la barra vertical
        xs.append(x + col_w[j] / 2)
        x += col_w[j] + col_gap

    grid = VGroup()
    for i in range(nrows):
        for j in range(ncols):
            cells[i][j].move_to([xs[j], -i * row_gap, 0])
            grid.add(cells[i][j])

    top = grid.get_top()[1] + 0.3
    bot = grid.get_bottom()[1] - 0.3
    lx = grid.get_left()[0] - 0.38
    rx = grid.get_right()[0] + 0.38
    tick = 0.2

    left_b = VMobject(stroke_width=3.5, color=WHITE).set_points_as_corners(
        [[lx + tick, top, 0], [lx, top, 0], [lx, bot, 0], [lx + tick, bot, 0]]
    )
    right_b = VMobject(stroke_width=3.5, color=WHITE).set_points_as_corners(
        [[rx - tick, top, 0], [rx, top, 0], [rx, bot, 0], [rx - tick, bot, 0]]
    )

    x_bar = (
        xs[ncols - 2] + col_w[ncols - 2] / 2 + xs[ncols - 1] - col_w[ncols - 1] / 2
    ) / 2
    bar = DashedLine(
        [x_bar, top - 0.12, 0],
        [x_bar, bot + 0.12, 0],
        color=GRAY,
        dash_length=0.12,
        stroke_width=2.5,
    )

    group = VGroup(left_b, right_b, bar, grid)
    if group.width > MATRIX_MAX_WIDTH:
        group.scale(MATRIX_MAX_WIDTH / group.width)
    group.move_to(MATRIX_POS)

    group.cells = cells
    group.rows_ = [VGroup(*cells[i]) for i in range(nrows)]
    group.entries = VGroup(*[c for row in cells for c in row])
    group.brackets = VGroup(left_b, right_b)
    group.bar = bar
    return group


def step_banner(text):
    return Text(text, font_size=28, weight=BOLD, color=YELLOW).move_to(STEP_POS)


def card(header_text, lines, color=GRAY):
    """Tarjeta con marco en la esquina superior izquierda (patrón de maxmin.py)."""
    header = Text(header_text, font_size=24, weight=BOLD)
    content = VGroup(header, *lines).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    box = SurroundingRectangle(content, color=color, buff=0.3)
    return VGroup(box, content)


class ParametricSystemScene(MovingCameraScene):
    """
    Doce beats sobre la discusión de un sistema lineal 3×3 con parámetro:
    escalonar sin dividir por expresiones con k, localizar los valores que
    anulan un pivote, y estudiar los tres casos resultantes.
    """

    def construct(self):
        self._beat1_title()
        system = self._beat2_system_and_question()
        matrix = self._beat3_augmented_matrix(system)
        ops_card = self._beat4_elementary_operations(matrix)
        matrix = self._beat5_safe_pivot(matrix)
        matrix = self._beat6_zeros_below_pivot(matrix)
        matrix = self._beat7_last_row(matrix)
        self._beat8_pivots(matrix, ops_card)
        self._beat9_unique_solution()
        self._beat10_case_k_equals_one()
        self._beat11_case_k_equals_minus_two()
        self._beat12_summary()

    # ── Beat 1: Título ───────────────────────────────────────────────────────
    def _beat1_title(self):
        title = Text("Sistemas con parámetros", font_size=52, weight=BOLD)
        subtitle = Text(
            "Matrices y operaciones elementales",
            font_size=32,
            color=GRAY,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle)))

    # ── Beat 2: El sistema y la pregunta ─────────────────────────────────────
    def _beat2_system_and_question(self):
        eq1 = MathTex("k", "x", "+", "y", "+", "z", "=", "1", font_size=44)
        eq2 = MathTex("x", "+", "k", "y", "+", "z", "=", "k", font_size=44)
        eq3 = MathTex("x", "+", "y", "+", "k", "z", "=", "k^2", font_size=44)
        system = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        system.move_to(UP * 0.6)

        brace = Brace(system, LEFT, color=GRAY)

        self.play(Write(eq1), Write(eq2), Write(eq3), run_time=2.5)
        self.play(GrowFromCenter(brace))
        self.wait(1)

        # las k son el parámetro, no una incógnita
        ks = VGroup(eq1[0], eq2[2], eq3[4], eq2[7], eq3[7])
        self.play(ks.animate.set_color(YELLOW), run_time=1)
        self.play(Indicate(ks, color=YELLOW, scale_factor=1.4), run_time=1.5)
        self.wait(1)

        q = Text("¿Cuántas soluciones tiene?", font_size=34)
        q.next_to(system, DOWN, buff=0.9)
        self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(2)

        answer = Text("Depende de k.", font_size=38, weight=BOLD, color=YELLOW)
        answer.move_to(q)
        self.play(ReplacementTransform(q, answer))
        self.wait(2)
        self.play(FadeOut(answer), FadeOut(brace))

        return system

    # ── Beat 3: Del sistema a la matriz ampliada ─────────────────────────────
    def _beat3_augmented_matrix(self, system):
        self.play(
            system.animate.scale(0.62).to_edge(LEFT, buff=0.7).shift(UP * 0.3),
            run_time=1.5,
        )

        matrix = augmented_matrix(M0)
        matrix.scale(0.85).move_to(RIGHT * 2.4 + UP * 0.3)

        label = Text("Matriz ampliada", font_size=26, color=GRAY)
        label.next_to(matrix, UP, buff=0.45)

        self.play(FadeIn(label))
        self.play(Create(matrix.brackets), Create(matrix.bar))
        self.play(
            LaggedStart(
                *[FadeIn(e, scale=0.6) for e in matrix.entries],
                lag_ratio=0.12,
            ),
            run_time=2.5,
        )
        self.wait(2)


        # el sistema desaparece, la matriz pasa al centro
        target = augmented_matrix(M0)
        self.play(
            FadeOut(system),
            FadeOut(label),
            Transform(matrix, target),
            run_time=1.5,
        )
        self.wait(1)

        return matrix

    # ── Beat 4: Las tres operaciones elementales ─────────────────────────────
    def _beat4_elementary_operations(self, matrix):
        op1 = MathTex(r"1.\;\; F_i \leftrightarrow F_j", font_size=26)
        op2 = MathTex(
            r"2.\;\; F_i \to a\, F_i,\;\;",
            r"a \neq 0",
            font_size=26,
        )
        op2[1].set_color(RED)
        op3 = MathTex(r"3.\;\; F_i \to F_i + a\, F_j", font_size=26)

        ops = card("Operaciones elementales", [op1, op2, op3])
        ops.move_to(UP * 0.6).scale(1.5)

        # la matriz se aparta mientras se presenta la tarjeta
        self.play(FadeOut(matrix), run_time=0.8)

        self.play(FadeIn(ops[0]), Write(ops[1][0]))
        for line in ops[1][1:]:
            self.play(Write(line), run_time=0.9)
        self.wait(2)

        warning = Text(
            "Nunca dividas por el parámetro k",
            font_size=32,
            weight=BOLD,
            color=RED,
        )
        warning.next_to(ops, DOWN, buff=0.8)
        self.play(FadeIn(warning, shift=UP * 0.2))
        self.play(Circumscribe(warning, color=RED, buff=0.25), run_time=2)
        self.wait(2.5)

        # la tarjeta se retira a la esquina y se queda de referencia
        self.play(
            FadeOut(warning),
            ops.animate.scale(1 / 1.5).to_corner(UL, buff=0.35),
            run_time=1.5,
        )
        self.play(FadeIn(matrix), run_time=0.8)
        self.wait(0.5)

        return ops

    # ── Beat 5: Paso 1 — un pivote que no dependa de k ───────────────────────
    def _beat5_safe_pivot(self, matrix):
        banner = step_banner("Paso 1:  colocar un pivote totalmente seguro")
        self.play(FadeIn(banner, shift=DOWN * 0.2))

        # el pivote natural sería k... pero k puede ser 0
        pivot_k = matrix.cells[0][0]
        warn = MathTex(r"k \text{ puede ser } 0", font_size=32, color=RED)
        warn.move_to(OP_POS)
        self.play(Indicate(pivot_k, color=RED, scale_factor=1.8), FadeIn(warn))
        self.wait(2)

        op = MathTex(r"F_1 \leftrightarrow F_3", font_size=34, color=YELLOW)
        op.move_to(OP_POS)
        self.play(ReplacementTransform(warn, op))

        # intercambio físico de las filas 1 y 3
        r1, r3 = matrix.rows_[0], matrix.rows_[2]
        dy = r1.get_center()[1] - r3.get_center()[1]
        self.play(
            r1.animate.shift(DOWN * dy),
            r3.animate.shift(UP * dy),
            run_time=1.6,
            path_arc=PI / 2,
        )
        self.wait(1)

        # se reemplaza por una matriz reconstruida (filas ya en orden)
        swapped = augmented_matrix(M1)
        self.play(FadeTransform(matrix, swapped), run_time=0.8)

        pivot = swapped.cells[0][0]
        circle = Circle(radius=0.36, color=GREEN, stroke_width=4).move_to(pivot)
        self.play(Create(circle), pivot.animate.set_color(GREEN))
        self.wait(2)

        self.play(FadeOut(circle), FadeOut(op), FadeOut(banner))
        return swapped

    # ── Beat 6: Paso 2 — ceros bajo el pivote ────────────────────────────────
    def _beat6_zeros_below_pivot(self, matrix):
        banner = step_banner("Paso 2:  hacer ceros bajo el pivote")
        self.play(FadeIn(banner, shift=DOWN * 0.2))

        op = MathTex(r"F_2 \to F_2 - F_1", font_size=34, color=YELLOW)
        op.move_to(OP_POS)
        self.play(
            FadeIn(op),
            Indicate(matrix.rows_[1], color=YELLOW, scale_factor=1.1),
        )
        self.wait(1.5)

        op2 = MathTex(r"F_3 \to F_3 - k\,F_1", font_size=34, color=YELLOW)
        op2.move_to(OP_POS)
        self.play(
            ReplacementTransform(op, op2),
            Indicate(matrix.rows_[2], color=YELLOW, scale_factor=1.1),
        )
        self.wait(1.5)

        reduced = augmented_matrix(M2)
        self.play(FadeTransform(matrix, reduced), run_time=1.5)
        self.wait(2)

        note = Text(
            "todo lleva un factor (k − 1)",
            font_size=26,
            color=GRAY,
        )
        note.move_to(OP_POS)
        self.play(ReplacementTransform(op2, note))
        self.play(
            Indicate(reduced.rows_[1], color=YELLOW, scale_factor=1.06),
            Indicate(reduced.rows_[2], color=YELLOW, scale_factor=1.06),
            run_time=2,
        )
        self.wait(2)

        self.play(FadeOut(note), FadeOut(banner))
        return reduced

    # ── Beat 7: Paso 3 — la última fila ──────────────────────────────────────
    def _beat7_last_row(self, matrix):
        banner = step_banner("Paso 3:  la última fila")
        self.play(FadeIn(banner, shift=DOWN * 0.2))

        op = MathTex(r"F_3 \to F_3 + F_2", font_size=34, color=YELLOW)
        op.move_to(OP_POS)
        self.play(FadeIn(op))
        self.wait(1)

        echelon = augmented_matrix(M3)
        self.play(FadeTransform(matrix, echelon), run_time=1.8)
        self.wait(1.5)

        note = Text("sin dividir por nada", font_size=26, color=GREEN)
        note.move_to(OP_POS)
        self.play(ReplacementTransform(op, note))

        frame = SurroundingRectangle(echelon, color=GREEN, buff=0.28)
        title = Text("Matriz escalonada", font_size=26, color=GREEN)
        title.next_to(frame, UP, buff=0.3)
        self.play(Create(frame), FadeIn(title))
        self.wait(2.5)

        self.play(FadeOut(note), FadeOut(banner), FadeOut(frame), FadeOut(title))
        return echelon

    # ── Beat 8: Los pivotes deciden todo ─────────────────────────────────────
    def _beat8_pivots(self, matrix, ops_card):
        self.play(FadeOut(ops_card), run_time=0.8)

        pivot_cells = [matrix.cells[i][i] for i in range(3)]
        boxes = VGroup(*[
            SurroundingRectangle(c, color=YELLOW, buff=0.14) for c in pivot_cells
        ])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.35), run_time=2)
        self.wait(1)

        pivots = MathTex(
            r"1", r"\quad", r"(k-1)", r"\quad", r"-(k-1)(k+2)",
            font_size=40, color=YELLOW,
        )
        pivots.move_to(UP * 2.7)
        self.play(
            *[TransformFromCopy(c, p) for c, p in zip(pivot_cells, pivots[0::2])],
            run_time=2,
        )
        self.wait(1.5)

        key = Text(
            "Todo se decide donde un pivote se anula",
            font_size=34, weight=BOLD,
        )
        key.move_to(DOWN * 2.7)
        self.play(Write(key), run_time=2)
        self.wait(2.5)

        self.play(FadeOut(matrix), FadeOut(boxes), run_time=1)

        # la recta real partida en tres zonas por los valores críticos
        line = NumberLine(x_range=[-4, 3, 1], length=9, include_ticks=True)
        line.move_to(DOWN * 0.3)
        line.add_numbers([-4, -3, -2, -1, 0, 1, 2, 3], font_size=26)

        d1 = Dot(line.n2p(K_CRIT_B), color=RED, radius=0.11)
        d2 = Dot(line.n2p(K_CRIT_A), color=RED, radius=0.11)
        l1 = MathTex("k = -2", font_size=32, color=RED).next_to(d1, DOWN, buff=0.6)
        l2 = MathTex("k = 1", font_size=32, color=RED).next_to(d2, DOWN, buff=0.6)

        self.play(Create(line), run_time=1.5)
        self.play(
            GrowFromCenter(d1), GrowFromCenter(d2),
            FadeIn(l1, shift=UP * 0.2), FadeIn(l2, shift=UP * 0.2),
        )

        zones = VGroup(
            Text("zona 1", font_size=22, color=GRAY).next_to(line.n2p(-3), UP, buff=0.5),
            Text("zona 2", font_size=22, color=GRAY).next_to(line.n2p(-0.5), UP, buff=0.5),
            Text("zona 3", font_size=22, color=GRAY).next_to(line.n2p(2), UP, buff=0.5),
        )
        self.play(LaggedStart(*[FadeIn(z) for z in zones], lag_ratio=0.3))
        self.wait(3)

        self.play(
            FadeOut(VGroup(line, d1, d2, l1, l2, zones, key, pivots)),
            run_time=1.2,
        )

    # ── Beat 9: Caso 1 — solución única ──────────────────────────────────────
    def _beat9_unique_solution(self):
        head = MathTex(r"k \neq 1 \;\text{ y }\; k \neq -2", font_size=40, color=GREEN)
        head.to_edge(UP, buff=0.7)
        self.play(Write(head))

        echelon = augmented_matrix(M3).scale(0.68)
        echelon.next_to(head, DOWN, buff=0.6)
        self.play(FadeIn(echelon))
        self.wait(1)

        note = Text(
            "ahora sí se puede dividir: ningún pivote es cero",
            font_size=24, color=GREEN,
        )
        note.next_to(echelon, DOWN, buff=0.45)
        self.play(FadeIn(note))
        self.wait(2)

        z = MathTex(r"z = \frac{(k+1)^2}{k+2}", font_size=38)
        y = MathTex(r"y = \frac{1}{k+2}", font_size=38)
        x = MathTex(r"x = -\frac{k+1}{k+2}", font_size=38)
        sols = VGroup(z, y, x).arrange(RIGHT, buff=1.0)
        sols.next_to(note, DOWN, buff=0.6)

        for s in sols:
            self.play(Write(s), run_time=1.2)
            self.wait(0.6)
        self.wait(1.5)

        verdict = Text(
            "Sistema compatible determinado", font_size=32, weight=BOLD, color=GREEN
        )
        verdict.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(verdict, shift=UP * 0.2))
        self.wait(2.5)

        # comprobación numérica con k = 0
        self.play(
            FadeOut(VGroup(echelon, note, verdict, head)),
            sols.animate.scale(0.85).to_edge(UP, buff=0.9),
            run_time=1.2,
        )
        check_head = MathTex(
            r"k = 0 \;\Rightarrow\; \left(-\tfrac{1}{2},\, \tfrac{1}{2},\, \tfrac{1}{2}\right)",
            font_size=40, color=YELLOW,
        )
        check_head.next_to(sols, DOWN, buff=0.7)
        self.play(Write(check_head))
        self.wait(1)

        checks = VGroup(
            MathTex(r"y + z = \tfrac{1}{2} + \tfrac{1}{2} = 1", font_size=34),
            MathTex(r"x + z = -\tfrac{1}{2} + \tfrac{1}{2} = 0", font_size=34),
            MathTex(r"x + y = -\tfrac{1}{2} + \tfrac{1}{2} = 0", font_size=34),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        checks.next_to(check_head, DOWN, buff=0.6)

        for c in checks:
            tick = MathTex(r"\checkmark", font_size=38, color=GREEN)
            tick.next_to(c, RIGHT, buff=0.45)
            self.play(Write(c), run_time=0.9)
            self.play(FadeIn(tick, scale=0.5), run_time=0.4)
            c.add(tick)
        self.wait(2.5)

        self.play(FadeOut(VGroup(sols, check_head, checks)), run_time=1.2)

    # ── Beat 10: Caso 2 — k = 1 ──────────────────────────────────────────────
    def _beat10_case_k_equals_one(self):
        head = MathTex(r"k = 1", font_size=48, color=BLUE)
        head.to_edge(UP, buff=0.7)
        self.play(Write(head))

        general = augmented_matrix(M3).scale(0.75).move_to(UP * 0.7)
        self.play(FadeIn(general))
        self.wait(1)

        substituted = augmented_matrix(M_K1).scale(0.75).move_to(UP * 0.7)
        self.play(FadeTransform(general, substituted), run_time=1.8)
        self.wait(1)

        # las dos últimas filas no dicen nada
        r2, r3 = substituted.rows_[1], substituted.rows_[2]
        self.play(r2.animate.set_opacity(0.28), r3.animate.set_opacity(0.28))
        gone = Text("dos filas se anulan enteras", font_size=26, color=GRAY)
        gone.next_to(substituted, DOWN, buff=0.5)
        self.play(FadeIn(gone))
        self.wait(2)

        # zoom sobre la única fila con información
        r1 = substituted.rows_[0]
        self.play(self.camera.frame.animate.scale(0.5).move_to(r1), run_time=2)
        self.wait(1.5)
        self.play(self.camera.frame.animate.scale(1 / 0.5).move_to(ORIGIN), run_time=2)

        eq = MathTex(r"x + y + z = 1", font_size=44, color=BLUE)
        eq.move_to(gone)
        self.play(ReplacementTransform(gone, eq))
        self.wait(2)

        param = MathTex(
            r"x = 1 - s - t, \qquad y = s, \qquad z = t",
            font_size=36,
        )
        param.next_to(eq, DOWN, buff=0.6)
        self.play(Write(param), run_time=1.8)
        self.wait(2)

        verdict = Text(
            "Infinitas soluciones (2 parámetros)",
            font_size=32, weight=BOLD, color=BLUE,
        )
        verdict.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(verdict, shift=UP * 0.2))
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(head, substituted, eq, param, verdict)), run_time=1.2
        )

    # ── Beat 11: Caso 3 — k = −2 ─────────────────────────────────────────────
    def _beat11_case_k_equals_minus_two(self):
        head = MathTex(r"k = -2", font_size=48, color=RED)
        head.to_edge(UP, buff=0.7)
        self.play(Write(head))

        general = augmented_matrix(M3).scale(0.75).move_to(UP * 0.7)
        self.play(FadeIn(general))
        self.wait(1)

        substituted = augmented_matrix(M_K2).scale(0.75).move_to(UP * 0.7)
        self.play(FadeTransform(general, substituted), run_time=1.8)
        self.wait(1.5)

        r3 = substituted.rows_[2]
        box = SurroundingRectangle(r3, color=RED, buff=0.18)
        self.play(Create(box))

        # zoom sobre la fila imposible
        self.play(self.camera.frame.animate.scale(0.5).move_to(r3), run_time=2)
        self.wait(1.5)
        self.play(self.camera.frame.animate.scale(1 / 0.5).move_to(ORIGIN), run_time=2)

        absurd = MathTex(r"0 = 3", font_size=52, color=RED)
        absurd.next_to(substituted, DOWN, buff=0.8)
        self.play(TransformFromCopy(r3, absurd), run_time=1.5)
        self.play(Wiggle(absurd, scale_value=1.3), run_time=2)
        self.wait(1.5)

        verdict = Text(
            "Sistema incompatible: no tiene solución",
            font_size=32, weight=BOLD, color=RED,
        )
        verdict.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(verdict, shift=UP * 0.2))
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(head, substituted, box, absurd, verdict)), run_time=1.2
        )

    # ── Beat 12: Resumen y método ────────────────────────────────────────────
    def _beat12_summary(self):
        title = Text("Resumen", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title))

        specs = [
            (r"k \neq 1,\; k \neq -2", "Solución única", GREEN),
            (r"k = 1", "Infinitas soluciones", BLUE),
            (r"k = -2", "Sin solución", RED),
        ]

        cells = VGroup()
        rows = []
        for cond, result, color in specs:
            left = MathTex(cond, font_size=32, color=color)
            arrow = MathTex(r"\longrightarrow", font_size=32, color=GRAY)
            right = Text(result, font_size=28, color=color)
            cells.add(left, arrow, right)
            rows.append(VGroup(left, arrow, right))

        # columnas alineadas: condición a la derecha, resultado a la izquierda
        cells.arrange_in_grid(
            rows=3, cols=3,
            col_alignments="rcl",
            buff=(0.5, 0.5),
        )
        cells.move_to(UP * 1.4)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.5)
        self.wait(2)

        method = VGroup(
            Text("1.  Escalonar sin dividir por expresiones con k", font_size=26),
            Text("2.  Buscar los valores que anulan un pivote", font_size=26),
            Text("3.  Estudiar cada caso por separado", font_size=26),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        box = SurroundingRectangle(method, color=YELLOW, buff=0.35)
        method_card = VGroup(box, method)
        method_card.next_to(cells, DOWN, buff=0.8)

        self.play(Create(box))
        for line in method:
            self.play(Write(line), run_time=0.8)
        self.wait(3)

        self.play(FadeOut(VGroup(title, cells, method_card)), run_time=1.5)
        self.wait(0.5)
