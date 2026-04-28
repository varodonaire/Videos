from manim import *

# ── Parameters ──────────────────────────────────────────────────────────────
X0 = 1.2           # base point (not a critical point of f)
ZOOM_SCALE = 0.12  # fraction of the original frame shown during zoom-in

# ── Function definitions ─────────────────────────────────────────────────────
def f(x):
    return 0.2 * x**4 +0.1*x**3 - 0.6 * x**2 + 0.3 * x + 1


def fp(x):
    return 0.8 * x**3 + 0.3 * x**2 - 1.2 * x + 0.3


def L(x):
    return f(X0) + fp(X0) * (x - X0)


# ── Scene ────────────────────────────────────────────────────────────────────
class LinearApproximation(MovingCameraScene):
    """
    Eight-beat animation that introduces linear approximation through
    a zoom-in revelation: locally, every differentiable function is a line.
    """

    def construct(self):
        self._beat1_title()
        axes, graph, graph_label, ax_labels = self._beat2_axes_and_curve()
        v_line, h_line, dot, x0_label, y0_label = self._beat3_mark_point(axes)
        card = self._beat4_formula_card()
        tangent, tan_label = self._beat5_tangent_line(axes)
        self._beat6_zoom_in(dot)
        self._beat7_zoom_out(
            axes, graph, graph_label, ax_labels,
            v_line, h_line, dot, x0_label, y0_label,
            card, tangent, tan_label,
        )
        self._beat8_conclusion()

    # ── Beat 1: Title ────────────────────────────────────────────────────────
    def _beat1_title(self):
        title = Text("Aproximación lineal", font_size=60, weight=BOLD)
        subtitle = Text(
            "Linealidad local de funciones diferenciables",
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
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.5, 3.0, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "include_tip": True},
        )
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x"),
            y_label=MathTex("y"),
        )
        # f(x) = 0.2x⁴ − 0.6x² + 0.3x + 1  (W-shaped degree-4 polynomial)
        graph = axes.plot(f, color=BLUE, x_range=[-2.2, 2.2])

        graph_label = MathTex("f(x)", color=BLUE, font_size=36)
        graph_label.next_to(axes.c2p(1.8, f(1.8)), UP, buff=0.15)

        self.play(Create(axes), Write(ax_labels), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(Write(graph_label))
        self.wait(1)

        return axes, graph, graph_label, ax_labels

    # ── Beat 3: Mark x₀ and y₀ ──────────────────────────────────────────────
    def _beat3_mark_point(self, axes):
        y0 = f(X0)

        v_line = DashedLine(
            axes.c2p(X0, 0),
            axes.c2p(X0, y0),
            color=YELLOW,
            dash_length=0.15,
            stroke_width=2.5,
        )
        h_line = DashedLine(
            axes.c2p(0, y0),
            axes.c2p(X0, y0),
            color=YELLOW,
            dash_length=0.15,
            stroke_width=2.5,
        )
        dot = Dot(axes.c2p(X0, y0), color=YELLOW, radius=0.1)

        x0_label = MathTex("x_0", color=YELLOW, font_size=32)
        x0_label.next_to(axes.c2p(X0, 0), DOWN, buff=0.25)

        y0_label = MathTex("y_0 = f(x_0)", color=YELLOW, font_size=28)
        y0_label.next_to(axes.c2p(0, y0), LEFT, buff=0.25)

        self.play(Create(v_line), Write(x0_label))
        self.play(Create(h_line), Write(y0_label))
        self.play(GrowFromCenter(dot))
        self.wait(1)

        return v_line, h_line, dot, x0_label, y0_label

    # ── Beat 4: Formula card ─────────────────────────────────────────────────
    def _beat4_formula_card(self):
        header = MathTex(
            r"\text{Aproximación lineal en }x_0\text{:}",
            font_size=28,
        )
        formula = MathTex(
            r"L(x) = f(x_0) + f'(x_0)\,(x - x_0)",
            font_size=34,
        )
        content = VGroup(header, formula).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        box = SurroundingRectangle(content, color=GRAY, buff=0.25)
        card = VGroup(box, content)
        card.to_corner(UL, buff=0.4)

        self.play(FadeIn(box), Write(header))
        self.play(Write(formula))
        self.wait(2)

        return card

    # ── Beat 5: Tangent line ─────────────────────────────────────────────────
    def _beat5_tangent_line(self, axes):
        tangent = axes.plot(L, color=RED, x_range=[-2.2, 2.2])

        tan_label = MathTex("L(x)", color=RED, font_size=34)
        # Position label where curve and tangent are well-separated
        tan_label.next_to(axes.c2p(-2.0, L(-2.0)), DL, buff=0.2)

        self.play(Create(tangent), run_time=2)
        self.play(Write(tan_label))
        self.wait(1.5)

        return tangent, tan_label

    # ── Beat 6: Zoom in ──────────────────────────────────────────────────────
    def _beat6_zoom_in(self, dot):
        zoom_center = dot.get_center()

        # Text must be tiny in scene coordinates to appear at a readable
        # size once the camera is zoomed in by ZOOM_SCALE.
        TEXT_SCALE = ZOOM_SCALE * 2.0   # rendered height ≈ 12 % of zoomed frame
        Y_OFFSET   = ZOOM_SCALE * 3.0   # ≈ 37 % of zoomed frame height above center

        zoom_label = MathTex(
            r"\text{Cerca de }x_0\text{: }f(x) \approx L(x)",
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

    # ── Beat 7: Zoom back out ────────────────────────────────────────────────
    def _beat7_zoom_out(
        self,
        axes, graph, graph_label, ax_labels,
        v_line, h_line, dot, x0_label, y0_label,
        card, tangent, tan_label,
    ):
        self.play(
            self.camera.frame.animate
                .scale(1 / ZOOM_SCALE)
                .move_to(ORIGIN),
            run_time=3,
        )
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(
                axes, ax_labels, graph, graph_label,
                v_line, h_line, dot, x0_label, y0_label,
                card, tangent, tan_label,
            )),
            run_time=1.5,
        )

    # ── Beat 8: Conclusion ───────────────────────────────────────────────────
    def _beat8_conclusion(self):
        conclusion = MathTex(
            r"f(x) \approx f(x_0) + f'(x_0)\,(x - x_0)",
            font_size=48,
        )
        tagline = MathTex(
            r"\text{para }x \approx x_0",
            font_size=36,
            color=GRAY,
        )
        tagline.next_to(conclusion, DOWN, buff=0.5)

        self.play(Write(conclusion), run_time=2)
        self.play(FadeIn(tagline, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(VGroup(conclusion, tagline)))
