from manim import *

# f(x) = x³ - 3x + 1  →  f'(x) = 3x² - 3  →  f''(x) = 6x
# Critical points: x = -1 (local max, f(-1)=3)  and  x = 1 (local min, f(1)=-1)
X_MAX = -1
X_MIN_PT = 1


def f(x):
    return x**3 - 3 * x + 1


def fp(x):
    return 3 * x**2 - 3


def fpp(x):
    return 6 * x


class MaxMinScene(MovingCameraScene):

    def construct(self):
        self._beat1_title()
        axes, graph, graph_label, ax_labels = self._beat2_axes_and_curve()
        markers = self._beat3_mark_critical_points(axes)
        deriv_group, card1 = self._beat4_paso1_derivar(axes)
        card2 = self._beat5_paso2_igualar_cero(card1, markers)
        card3 = self._beat6_paso3_segunda_derivada(card2, markers)
        self._beat7_conclusion(axes, graph, graph_label, ax_labels, deriv_group, markers, card3)

    # ── Beat 1: Title ────────────────────────────────────────────────────────
    def _beat1_title(self):
        title = Text("Máximos y Mínimos de Funciones", font_size=52, weight=BOLD)
        subtitle = Text(
            "Criterio de la segunda derivada",
            font_size=32,
            color=GRAY,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle)))

    # ── Beat 2: Axes and curve ───────────────────────────────────────────────
    def _beat2_axes_and_curve(self):
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2, 4, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": WHITE, "include_tip": True},
        )
        axes.shift(RIGHT * 2.0)

        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x"),
            y_label=MathTex("y"),
        )

        graph = axes.plot(f, color=BLUE, x_range=[-2.3, 2.3])
        graph_label = MathTex(r"f(x) = x^3 - 3x + 1", color=BLUE, font_size=26)
        graph_label.next_to(axes.c2p(1.8, f(1.8)), UP, buff=0.2)

        self.play(Create(axes), Write(ax_labels), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(Write(graph_label))
        self.wait(2)

        return axes, graph, graph_label, ax_labels

    # ── Beat 3: Mark critical points visually ───────────────────────────────
    def _beat3_mark_critical_points(self, axes):
        y_max = f(X_MAX)       # 3
        y_min_val = f(X_MIN_PT)  # -1

        v_line_max = DashedLine(
            axes.c2p(X_MAX, 0), axes.c2p(X_MAX, y_max),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )
        h_line_max = DashedLine(
            axes.c2p(0, y_max), axes.c2p(X_MAX, y_max),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )
        v_line_min = DashedLine(
            axes.c2p(X_MIN_PT, 0), axes.c2p(X_MIN_PT, y_min_val),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )
        h_line_min = DashedLine(
            axes.c2p(0, y_min_val), axes.c2p(X_MIN_PT, y_min_val),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )

        dot_max = Dot(axes.c2p(X_MAX, y_max), color=YELLOW, radius=0.1)
        dot_min = Dot(axes.c2p(X_MIN_PT, y_min_val), color=YELLOW, radius=0.1)

        x_max_label = MathTex("x = -1", color=YELLOW, font_size=26)
        x_max_label.next_to(axes.c2p(X_MAX, 0), DOWN, buff=0.25)
        x_min_label = MathTex("x = 1", color=YELLOW, font_size=26)
        x_min_label.next_to(axes.c2p(X_MIN_PT, 0), DOWN, buff=0.25)

        lbl_max = Text("máximo relativo", color=YELLOW, font_size=20)
        lbl_max.next_to(dot_max, UL, buff=0.2)
        lbl_min = Text("mínimo relativo", color=YELLOW, font_size=20)
        lbl_min.next_to(dot_min, DR, buff=0.2)

        self.play(Create(v_line_max), Create(h_line_max), Write(x_max_label))
        self.play(GrowFromCenter(dot_max), FadeIn(lbl_max))
        self.wait(1)
        self.play(Create(v_line_min), Create(h_line_min), Write(x_min_label))
        self.play(GrowFromCenter(dot_min), FadeIn(lbl_min))
        self.wait(2)

        return {
            "dot_max": dot_max,
            "dot_min": dot_min,
            "v_line_max": v_line_max,
            "h_line_max": h_line_max,
            "v_line_min": v_line_min,
            "h_line_min": h_line_min,
            "x_max_label": x_max_label,
            "x_min_label": x_min_label,
            "lbl_max": lbl_max,
            "lbl_min": lbl_min,
        }

    # ── Beat 4: PASO 1 — Derivar ─────────────────────────────────────────────
    def _beat4_paso1_derivar(self, axes):
        header = Text("Paso 1: Derivar", font_size=26, weight=BOLD)
        line1 = MathTex(r"f(x) = x^3 - 3x + 1", font_size=24)
        line2 = MathTex(r"f'(x) = 3x^2 - 3", font_size=28, color=ORANGE)

        content = VGroup(header, line1, line2).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        box = SurroundingRectangle(content, color=GRAY, buff=0.3)
        card = VGroup(box, content)
        card.to_corner(UL, buff=0.35)

        deriv_curve = axes.plot(fp, color=ORANGE, x_range=[-2.3, 2.3])
        deriv_label = MathTex(r"f'(x)", color=ORANGE, font_size=24)
        deriv_label.next_to(axes.c2p(-2.0, fp(-2.0)), UL, buff=0.15)
        deriv_group = VGroup(deriv_curve, deriv_label)

        self.play(FadeIn(box), Write(header))
        self.play(Write(line1))
        self.play(Write(line2))
        self.wait(1)
        self.play(Create(deriv_curve), Write(deriv_label), run_time=2)
        self.wait(1.5)

        return deriv_group, card

    # ── Beat 5: PASO 2 — Igualar a cero ──────────────────────────────────────
    def _beat5_paso2_igualar_cero(self, prev_card, markers):
        self.play(FadeOut(prev_card))

        header = Text("Paso 2:  f'(x) = 0", font_size=26, weight=BOLD)
        line1 = MathTex(r"3x^2 - 3 = 0", font_size=26)
        line2 = MathTex(r"x^2 = 1", font_size=26)
        line3 = MathTex(r"x = \pm\,1", font_size=32, color=YELLOW)

        content = VGroup(header, line1, line2, line3).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        box = SurroundingRectangle(content, color=GRAY, buff=0.3)
        card = VGroup(box, content)
        card.to_corner(UL, buff=0.35)

        self.play(FadeIn(box), Write(header))
        self.play(Write(line1))
        self.play(Write(line2))
        self.play(Write(line3))
        self.wait(0.5)
        self.play(
            Indicate(markers["dot_max"], color=YELLOW, scale_factor=1.8),
            Indicate(markers["dot_min"], color=YELLOW, scale_factor=1.8),
        )
        self.wait(2)

        return card

    # ── Beat 6: PASO 3 — Criterio de la segunda derivada ─────────────────────
    def _beat6_paso3_segunda_derivada(self, prev_card, markers):
        self.play(FadeOut(prev_card))

        header = Text("Paso 3: Segunda derivada", font_size=26, weight=BOLD)
        line1 = MathTex(r"f''(x) = 6x", font_size=26)
        line2 = MathTex(
            r"f''(-1) = -6 < 0 \;\Rightarrow\; \text{máximo}",
            font_size=24, color=GREEN,
        )
        line3 = MathTex(
            r"f''(1) = 6 > 0 \;\Rightarrow\; \text{mínimo}",
            font_size=24, color=RED,
        )

        content = VGroup(header, line1, line2, line3).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        box = SurroundingRectangle(content, color=GRAY, buff=0.3)
        card = VGroup(box, content)
        card.to_corner(UL, buff=0.35)

        self.play(FadeIn(box), Write(header))
        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.play(
            markers["dot_max"].animate.set_color(GREEN),
            markers["lbl_max"].animate.set_color(GREEN),
            markers["v_line_max"].animate.set_color(GREEN),
            markers["h_line_max"].animate.set_color(GREEN),
            markers["x_max_label"].animate.set_color(GREEN),
        )
        self.wait(1)
        self.play(Write(line3))
        self.play(
            markers["dot_min"].animate.set_color(RED),
            markers["lbl_min"].animate.set_color(RED),
            markers["v_line_min"].animate.set_color(RED),
            markers["h_line_min"].animate.set_color(RED),
            markers["x_min_label"].animate.set_color(RED),
        )
        self.wait(2)

        return card

    # ── Beat 7: Conclusion ───────────────────────────────────────────────────
    def _beat7_conclusion(self, axes, graph, graph_label, ax_labels, deriv_group, markers, card3):
        self.play(
            FadeOut(VGroup(
                axes, ax_labels, graph, graph_label,
                deriv_group,
                *markers.values(),
                card3,
            )),
            run_time=1.5,
        )

        line1 = MathTex(
            r"\text{Máximo relativo en } x = -1, \quad f(-1) = 3",
            font_size=38, color=GREEN,
        )
        line2 = MathTex(
            r"\text{Mínimo relativo en } x = 1, \quad f(1) = -1",
            font_size=38, color=RED,
        )
        line2.next_to(line1, DOWN, buff=0.5)

        self.play(Write(line1), run_time=1.5)
        self.play(FadeIn(line2, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(VGroup(line1, line2)))
