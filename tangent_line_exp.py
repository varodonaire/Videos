from manim import *
import numpy as np

X0 = 0
ZOOM_SCALE = 0.18

def f(x):
    return (x + 1) * np.exp(x)

def fp(x):
    return (x + 2) * np.exp(x)

def L(x):
    return f(X0) + fp(X0) * (x - X0)  # 1 + 2x


class TangentLineExp(MovingCameraScene):
    """
    Pedagogical walkthrough of finding the tangent line to f(x)=(x+1)eˣ
    at x₀=0, then using it for linear approximation. Mirrors exam structure.
    """

    def construct(self):
        self._beat1_title()
        axes, graph, graph_label, ax_labels = self._beat2_axes_and_curve()
        v_line, h_line, dot, x0_label, y0_label = self._beat3_mark_point(axes)
        card = self._beat4_calculation_card()
        tangent, tan_label = self._beat5_draw_tangent(axes)
        approx_group = self._beat6_linear_approx(card)
        self._beat7_zoom_in(dot)
        self._beat8_zoom_out(
            axes, graph, graph_label, ax_labels,
            v_line, h_line, dot, x0_label, y0_label,
            card, tangent, tan_label, approx_group,
        )
        self._beat9_conclusion()

    # ── Beat 1: Title ────────────────────────────────────────────────────────
    def _beat1_title(self):
        title = Text("Recta tangente", font_size=60, weight=BOLD)
        subtitle = MathTex(
            r"f(x) = (x+1)e^x \quad \text{en} \quad x_0 = 0",
            font_size=34,
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
            x_range=[-2.5, 1.5, 1],
            y_range=[-0.5, 5.5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": WHITE, "include_tip": True},
        )
        axes.shift(RIGHT * 2.0)

        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x"),
            y_label=MathTex("y"),
        )

        graph = axes.plot(f, color=BLUE, x_range=[-2.3, 1.2])
        graph_label = MathTex(r"f(x)=(x+1)e^x", color=BLUE, font_size=28)
        graph_label.next_to(axes.c2p(0.6, f(0.6)), UR, buff=0.2)

        self.play(Create(axes), Write(ax_labels), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(Write(graph_label))
        self.wait(1)

        return axes, graph, graph_label, ax_labels

    # ── Beat 3: Mark x₀=0 and y₀=f(0)=1 ────────────────────────────────────
    def _beat3_mark_point(self, axes):
        y0 = f(X0)

        v_line = DashedLine(
            axes.c2p(X0, 0), axes.c2p(X0, y0),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )
        h_line = DashedLine(
            axes.c2p(0, y0), axes.c2p(X0, y0),
            color=YELLOW, dash_length=0.15, stroke_width=2.5,
        )
        dot = Dot(axes.c2p(X0, y0), color=YELLOW, radius=0.1)

        x0_label = MathTex("x_0=0", color=YELLOW, font_size=28)
        x0_label.next_to(axes.c2p(X0, 0), DOWN, buff=0.25)

        y0_label = MathTex("f(0)=1", color=YELLOW, font_size=28)
        y0_label.next_to(axes.c2p(0, y0), LEFT, buff=0.3)

        self.play(Create(v_line), Write(x0_label))
        self.play(Create(h_line), Write(y0_label))
        self.play(GrowFromCenter(dot))
        self.wait(1)

        return v_line, h_line, dot, x0_label, y0_label

    # ── Beat 4: Step-by-step calculation card ────────────────────────────────
    def _beat4_calculation_card(self):
        formula = MathTex(
            r"y = f(x_0) + f'(x_0)(x - x_0)",
            font_size=24,
            color=GRAY,
        )

        step1 = MathTex(
            r"f(0) = (0+1)e^0 = 1",
            font_size=26,
        )

        step2a = MathTex(
            r"f'(x) = e^x + (x+1)e^x",
            font_size=26,
        )
        step2b = MathTex(
            r"= (x+2)e^x",
            font_size=26,
        )
        step2c = MathTex(
            r"f'(0) = 2",
            font_size=26,
            color=GREEN,
        )

        result = MathTex(
            r"y = 1 + 2x",
            font_size=32,
            color=RED,
        )
        result_box = SurroundingRectangle(result, color=RED, buff=0.15)
        result_group = VGroup(result_box, result)

        content = VGroup(
            formula,
            step1,
            step2a, step2b, step2c,
            result_group,
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)

        box = SurroundingRectangle(content, color=GRAY, buff=0.3)
        card = VGroup(box, content)
        card.to_corner(UL, buff=0.35)

        self.play(FadeIn(box), Write(formula))
        self.wait(0.5)
        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2a))
        self.play(Write(step2b))
        self.play(Write(step2c))
        self.wait(0.5)
        self.play(Write(result), Create(result_box))
        self.wait(1.5)

        return card

    # ── Beat 5: Draw tangent line ────────────────────────────────────────────
    def _beat5_draw_tangent(self, axes):
        tangent = axes.plot(L, color=RED, x_range=[-2.3, 1.5])
        tan_label = MathTex(r"L(x)=1+2x", color=RED, font_size=26)
        tan_label.next_to(axes.c2p(1.2, L(1.2)), UR, buff=0.2)

        self.play(Create(tangent), run_time=2)
        self.play(Write(tan_label))
        self.wait(1.5)

        return tangent, tan_label

    # ── Beat 6: Linear approximation ────────────────────────────────────────
    def _beat6_linear_approx(self, card):
        approx = MathTex(
            r"f(0{,}1) \approx 1 + 2(0{,}1) = 1{,}2",
            font_size=26,
            color=YELLOW,
        )
        approx_box = SurroundingRectangle(approx, color=YELLOW, buff=0.15)
        approx_group = VGroup(approx_box, approx)
        approx_group.next_to(card, DOWN, buff=0.4)

        self.play(Write(approx), Create(approx_box))
        self.wait(2)

        return approx_group

    # ── Beat 7: Zoom in ──────────────────────────────────────────────────────
    def _beat7_zoom_in(self, dot):
        zoom_center = dot.get_center()

        TEXT_SCALE = ZOOM_SCALE * 2.0
        Y_OFFSET   = ZOOM_SCALE * 3.5

        zoom_label = MathTex(
            r"f(x) \approx 1 + 2x \quad \text{cerca de } x_0=0",
            color=YELLOW,
        )
        zoom_label.scale(TEXT_SCALE)
        zoom_label.move_to(zoom_center + UP * Y_OFFSET)

        self.play(
            self.camera.frame.animate
                .scale(ZOOM_SCALE)
                .move_to(zoom_center),
            run_time=3,
        )
        self.play(FadeIn(zoom_label), run_time=0.8)
        self.wait(3)
        self.play(FadeOut(zoom_label))

    # ── Beat 8: Zoom back out ────────────────────────────────────────────────
    def _beat8_zoom_out(
        self,
        axes, graph, graph_label, ax_labels,
        v_line, h_line, dot, x0_label, y0_label,
        card, tangent, tan_label, approx_group,
    ):
        self.play(
            self.camera.frame.animate
                .scale(1 / ZOOM_SCALE)
                .move_to(ORIGIN),
            run_time=3,
        )
        self.wait(1)
        self.play(
            FadeOut(VGroup(
                axes, ax_labels, graph, graph_label,
                v_line, h_line, dot, x0_label, y0_label,
                card, tangent, tan_label, approx_group,
            )),
            run_time=1.5,
        )

    # ── Beat 9: Conclusion ───────────────────────────────────────────────────
    def _beat9_conclusion(self):
        line1 = MathTex(
            r"y = 1 + 2x",
            font_size=52,
        )
        line2 = MathTex(
            r"f(0{,}1) \approx 1{,}2",
            font_size=38,
            color=GRAY,
        )
        line2.next_to(line1, DOWN, buff=0.5)

        self.play(Write(line1), run_time=2)
        self.play(FadeIn(line2, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(VGroup(line1, line2)))
