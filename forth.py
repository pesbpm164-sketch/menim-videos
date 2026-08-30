from manim import *
import numpy as np

class DetailedInclineSimulation(Scene):
    def construct(self):
        # --- Setup ---
        base_len = 5.5
        height = 2.2
        interior = np.arctan(height / base_len)
        
        origin = LEFT*3.5 + DOWN*1.8
        base_end = origin + RIGHT*base_len
        top = origin + UP*height

        base = Line(origin, base_end, color=WHITE, stroke_width=4)
        incline = Line(top, base_end, color=BLUE, stroke_width=10)
        left_wall = Line(origin, top, color=WHITE, stroke_width=2)
        left_wall.set_opacity(0.15)

        title = Text("Detailed: Object on Incline - All Forces", font_size=28).to_edge(UP, buff=0.3)

        # Small inside arc
        arc = Arc(radius=0.6, start_angle=PI - interior, angle=interior, color=YELLOW, stroke_width=5)
        arc.move_arc_center_to(base_end)
        theta_label = MathTex(r"\theta", color=YELLOW).scale(0.9).move_to(base_end + LEFT*1.2 + UP*0.25)

        # Block
        block_size = 0.6
        incline_angle = np.arctan2(-height, base_len)
        def point_on_incline(t):
            return top + (base_end - top) * t
        norm = np.array([height, base_len, 0])
        norm = norm / np.linalg.norm(norm)
        offset = norm * 0.32
        start_pos = point_on_incline(0.15) + offset

        block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(start_pos)

        # --- Equations panel on RIGHT side ---
        eq_panel = VGroup(
            MathTex(r"W = mg", color=WHITE).scale(0.6),
            MathTex(r"W_{\parallel} = mg\sin\theta", color=ORANGE).scale(0.55),
            MathTex(r"W_{\perp} = mg\cos\theta", color=GREEN).scale(0.55),
            MathTex(r"N = W_{\perp} = mg\cos\theta", color=BLUE).scale(0.55),
            MathTex(r"f_s \leq \mu_s N", color=YELLOW).scale(0.55),
            MathTex(r"f_k = \mu_k N", color=YELLOW).scale(0.55),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP*0.5)

        eq_panel_box = SurroundingRectangle(eq_panel, color=WHITE, buff=0.2, stroke_width=1, stroke_opacity=0.3)

        # Bottom equations
        bottom_eq = VGroup(
            MathTex(r"F_{net} = mg\sin\theta - f", color=WHITE).scale(0.65),
            MathTex(r"a = g(\sin\theta - \mu\cos\theta)", color=GREEN).scale(0.7),
            MathTex(r"\text{If } mg\sin\theta > \mu_s N \rightarrow \text{slides}", color=YELLOW).scale(0.5),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Create(left_wall), Create(arc), Write(theta_label), FadeIn(block), run_time=1.5)
        self.wait(0.5)

        # --- MG solid ---
        mg_vec = DOWN*1.4
        mg_arrow = Arrow(block.get_center(), block.get_center() + mg_vec, color=WHITE, buff=0, stroke_width=7)
        mg_label = MathTex(r"\vec{W}=mg", color=WHITE).scale(0.7).next_to(mg_arrow, RIGHT, buff=0.1)
        mg_label_box = SurroundingRectangle(mg_label, buff=0.05, color=WHITE, stroke_opacity=0.5)

        self.play(Create(mg_arrow), Write(mg_label), Create(eq_panel_box), Write(eq_panel[0]), run_time=1)
        self.wait(1)

        # --- Dotted components ---
        # Parallel component along incline (down)
        incline_unit = (base_end - top) / np.linalg.norm(base_end - top)  # down-right along incline
        perp_unit = -norm  # into incline (down-left)
        
        mg_parallel_len = 1.4 * np.sin(interior) * 1.5  # mg sinθ
        mg_perp_len = 1.4 * np.cos(interior) * 1.2

        # Dotted lines for components
        mg_parallel = DashedLine(block.get_center(), block.get_center() + incline_unit*1.1, color=ORANGE, stroke_width=5, dash_length=0.12)
        mg_parallel.add_tip(tip_length=0.15)
        mg_parallel_label = MathTex(r"mg\sin\theta", color=ORANGE).scale(0.6).next_to(mg_parallel, DOWN+RIGHT, buff=0.1)

        mg_perp = DashedLine(block.get_center(), block.get_center() + perp_unit*1.0, color=GREEN, stroke_width=5, dash_length=0.12)
        mg_perp.add_tip(tip_length=0.15)
        mg_perp_label = MathTex(r"mg\cos\theta", color=GREEN).scale(0.6).next_to(mg_perp, LEFT, buff=0.1)

        # Dotted rectangle showing decomposition
        dotted_h = DashedLine(block.get_center() + incline_unit*1.1, block.get_center() + incline_unit*1.1 + perp_unit*1.0, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.5)
        dotted_v = DashedLine(block.get_center() + perp_unit*1.0, block.get_center() + incline_unit*1.1 + perp_unit*1.0, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.5)

        self.play(Create(mg_parallel), Write(mg_parallel_label), Write(eq_panel[1]), run_time=1)
        self.play(Create(mg_perp), Write(mg_perp_label), Write(eq_panel[2]), Create(dotted_h), Create(dotted_v), run_time=1)
        self.wait(1.5)

        # --- Normal solid ---
        n_arrow = Arrow(block.get_center(), block.get_center() + norm*1.0, color=BLUE, buff=0, stroke_width=7)
        n_label = MathTex(r"\vec{N}=mg\cos\theta", color=BLUE).scale(0.6).next_to(n_arrow, UP, buff=0.1)
        
        self.play(Create(n_arrow), Write(n_label), Write(eq_panel[3]), run_time=1)
        self.wait(1)

        # --- Friction solid + dotted comparison ---
        friction_static = Arrow(block.get_center(), block.get_center() - incline_unit*0.8, color=YELLOW, buff=0, stroke_width=7)
        friction_label = MathTex(r"\vec{f}_s \leq \mu_s N", color=YELLOW).scale(0.6).next_to(friction_static, LEFT, buff=0.15)
        friction_kinetic = Arrow(block.get_center(), block.get_center() - incline_unit*0.6, color=YELLOW, buff=0, stroke_width=5, stroke_opacity=0.8)
        friction_kinetic_label = MathTex(r"\vec{f}_k = \mu_k N", color=YELLOW).scale(0.55).next_to(friction_kinetic, LEFT, buff=0.1)

        self.play(Create(friction_static), Write(friction_label), Write(eq_panel[4]), run_time=1)
        self.play(Transform(friction_static, friction_kinetic), Transform(friction_label, friction_kinetic_label), Write(eq_panel[5]), run_time=1)
        self.wait(1)

        # --- Bottom equations appear ---
        self.play(Write(bottom_eq[0]), run_time=0.8)
        self.play(Write(bottom_eq[1]), run_time=0.8)
        self.play(Write(bottom_eq[2]), run_time=0.8)
        self.wait(1.5)

        # --- Slide with all forces ---
        self.play(FadeOut(dotted_h), FadeOut(dotted_v))

        tracker = ValueTracker(0.15)
        # Keep all arrows during slide
        moving_block = always_redraw(lambda: Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(tracker.get_value()) + offset))
        moving_mg = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + DOWN*1.2, color=WHITE, buff=0, stroke_width=5, stroke_opacity=0.8))
        moving_n = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + norm*0.8, color=BLUE, buff=0, stroke_width=5, stroke_opacity=0.8))
        moving_f = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset - incline_unit*0.5, color=YELLOW, buff=0, stroke_width=5, stroke_opacity=0.8))

        self.add(moving_block, moving_mg, moving_n, moving_f)
        self.remove(block, mg_arrow, n_arrow, friction_static)

        self.play(tracker.animate.set_value(0.8), run_time=5, rate_func=rate_functions.ease_in_quad)
        self.remove(moving_block, moving_mg, moving_n, moving_f)

        final_block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(0.8) + offset)
        self.add(final_block)
        self.wait(2)

        self.play(FadeOut(base), FadeOut(incline), FadeOut(left_wall), FadeOut(arc), FadeOut(theta_label), FadeOut(final_block), FadeOut(mg_parallel), FadeOut(mg_perp), FadeOut(mg_parallel_label), FadeOut(mg_perp_label), FadeOut(mg_label), FadeOut(eq_panel), FadeOut(eq_panel_box), FadeOut(bottom_eq))

        quote = VGroup(
            Text("Detailed Analysis:", font_size=28, color=YELLOW),
            Text("Every component, every friction, every equation.", font_size=22),
        ).arrange(DOWN, buff=0.3)
        self.play(Write(quote), run_time=2)
        self.wait(2)
